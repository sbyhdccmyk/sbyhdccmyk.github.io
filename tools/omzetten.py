# Zet Sammy's cursushoofdstukken (Google Docs-structuur als JSON) om naar webpagina's.
# Gebruik: zie maak_alles.py. Blokken -> HTML met dezelfde opmaak als het hoofdstuk Rineke Dijkstra.
import json, re, html, pathlib

E = html.escape
HIER = pathlib.Path(__file__).resolve().parent
CSS = (HIER / "hoofdstuk.css").read_text(encoding="utf-8")

EXTRA_CSS = """
.uitbreiding{color:var(--zacht)}
p.uitbreiding,div.uitbreiding{border-left:2px solid var(--lijn);padding-left:.8rem}
.legende{font-size:.95rem;color:var(--zacht);border:1px solid var(--lijn);padding:.6rem .9rem;margin:0 0 1.5rem}
.legende span{border-left:2px solid var(--lijn);padding-left:.5rem}
.tabel{overflow-x:auto;margin:1.2rem 0 1.6rem}
.tabel table{border-collapse:collapse;width:100%;font-size:1rem;line-height:1.4}
.tabel th,.tabel td{border:1px solid var(--lijn);padding:.45rem .6rem;text-align:left;vertical-align:top}
.tabel th{background:#e7e6e6}
main ul.lijst,main ol.lijst{margin:0 0 1rem;padding-left:1.4rem}
main ul.lijst li,main ol.lijst li{margin-bottom:.3rem}
sup.bron a{font-family:var(--data);font-size:.7rem;color:var(--rood);text-decoration:none}
.hoofdstuk-nav{display:flex;flex-wrap:wrap;justify-content:space-between;gap:1rem;margin-top:4rem;padding-top:1rem;border-top:1px solid var(--inkt)}
.hoofdstuk-nav a{text-decoration:none;font-weight:700}
.hoofdstuk-nav span{display:block;font-family:var(--data);font-size:.7rem;letter-spacing:.05em;text-transform:uppercase;color:var(--zacht);font-weight:400}
"""

# ---------------------------------------------------------------- Google Docs JSON -> blokken
def laad_doc(pad):
    d = json.load(open(pad, encoding="utf-8"))
    d = d.get("content", d)
    tab = d["tabs"][0]["documentTab"]
    fns = {}
    for k, v in tab.get("footnotes", {}).items():
        links = []
        for x in v["content"]:
            for el in x.get("paragraph", {}).get("elements", []):
                tr = el.get("textRun")
                if tr and tr.get("textStyle", {}).get("link", {}).get("url"):
                    links.append((tr["content"].strip(), tr["textStyle"]["link"]["url"]))
        fns[k] = links
    return tab["body"]["content"], fns

def is_grijs(st):
    c = st.get("foregroundColor", {}).get("color", {}).get("rgbColor")
    if not c:
        return False
    r, g, b = c.get("red", 0), c.get("green", 0), c.get("blue", 0)
    return abs(r - g) < .08 and abs(g - b) < .08 and .25 < r < .85

def runs_html(p, fns, bronnen):
    """Tekst van een paragraaf met cursief, vet en links. Voetnoten met link worden een kleine bronverwijzing."""
    uit, platte = [], []
    for el in p["elements"]:
        if "textRun" in el:
            t = el["textRun"]["content"].replace("\n", "").replace("\u000b", " ")
            if not t:
                continue
            st = el["textRun"].get("textStyle", {})
            h = E(t)
            if st.get("italic") and t.strip():
                h = f"<i>{h}</i>"
            url = st.get("link", {}).get("url")
            if url and url.startswith("http"):
                h = f'<a href="{E(url)}">{h}</a>'
            uit.append(h); platte.append(t)
        elif "footnoteReference" in el:
            fid = el["footnoteReference"]["footnoteId"]
            for naam, url in fns.get(fid, []):
                bronnen.append((naam, url))
                uit.append(f'<sup class="bron"><a href="{E(url)}" title="Bron: {E(naam)}">bron</a></sup>')
    h = "".join(uit).strip()
    h = re.sub(r"</i>(\s*)<i>", r"\1", h)
    return h, "".join(platte).strip()

def para_info(p):
    els = [e for e in p["elements"] if "textRun" in e and e["textRun"]["content"].strip()]
    st = p.get("paragraphStyle", {})
    return {
        "stijl": st.get("namedStyleType", "NORMAL_TEXT"),
        "img": any("inlineObjectElement" in e for e in p["elements"]),
        "shading": bool(st.get("shading", {}).get("backgroundColor", {}).get("color")),
        "vet": bool(els) and all(e["textRun"].get("textStyle", {}).get("bold") for e in els),
        "grijs": bool(els) and all(is_grijs(e["textRun"].get("textStyle", {})) for e in els),
        "bullet": "bullet" in p,
    }

def figuur(caption_paras, fns):
    regels, links = [], []
    for p in caption_paras:
        h, t = runs_html(p, fns, links)
        h = re.sub(r'<sup class="bron">.*?</sup>', "", h).strip()
        if not t or "afbeelding invoegen" in t.lower():
            h = re.sub(r"\[?\s*Afbeelding invoegen\s*\]?", "", h, flags=re.I).strip()
            if not h:
                continue
        regels.append(h)
    if not regels and not links:
        return None
    return {"type": "fig", "regels": regels, "links": links}

def cel_paras(cel):
    return [x["paragraph"] for x in cel["content"] if "paragraph" in x]

def doc_naar_blokken(body, fns):
    blokken, i, n = [], 0, len(body)
    while i < n:
        el = body[i]
        if "tableOfContents" in el or "sectionBreak" in el:
            i += 1; continue
        if "table" in el:
            t = el["table"]; rijen = t["tableRows"]
            if t["rows"] == 1 and t["columns"] == 1:
                ps = cel_paras(rijen[0]["tableCells"][0])
                if any(para_info(p)["img"] for p in ps):
                    f = figuur([p for p in ps if not para_info(p)["img"]], fns)
                    if f: blokken.append(f)
                else:
                    inhoud = []
                    for p in ps:
                        h, tx = runs_html(p, fns, [])
                        if tx: inhoud.append((h, tx, para_info(p)))
                    if inhoud:
                        if inhoud[0][1].lower().startswith("colofon"):
                            blokken.append({"type": "colofon"})
                        else:
                            blokken.append({"type": "kader", "regels": inhoud})
            else:
                cellen = [[" ".join(runs_html(p, fns, [])[0] for p in cel_paras(c)).strip() for c in r["tableCells"]] for r in rijen]
                kop = [re.sub("<.*?>", "", c).strip().lower() for c in cellen[0]]
                if kop[:2] == ["woord", "definitie"] or kop[:2] == ["begrip", "betekenis"]:
                    blokken.append({"type": "woorden", "items": [(c[0], c[1]) for c in cellen[1:] if len(c) > 1 and c[0]]})
                elif t["columns"] == 2 and not any(k in ("", ) for k in kop) and len(cellen) <= 8 and all(len(re.sub("<.*?>","",c[0])) < 30 for c in cellen):
                    blokken.append({"type": "fiche", "items": [(c[0], c[1]) for c in cellen if c[0]]})
                else:
                    blokken.append({"type": "tabel", "rijen": cellen})
            i += 1; continue
        if "paragraph" not in el:
            i += 1; continue
        p = el["paragraph"]; info = para_info(p)
        # figuur als gearceerde paragrafen: beeld, dan bijschriftregels
        if info["img"] and info["shading"]:
            j = i + 1; caps = []
            while j < n and "paragraph" in body[j]:
                pi = para_info(body[j]["paragraph"])
                if not pi["shading"] or pi["img"]: break
                caps.append(body[j]["paragraph"]); j += 1
            f = figuur(caps, fns)
            if f: blokken.append(f)
            i = j; continue
        if info["img"]:
            i += 1; continue
        h, tx = runs_html(p, fns, [])
        if not tx:
            i += 1; continue
        st = info["stijl"]
        if st in ("HEADING_1", "TITLE"):
            blokken.append({"type": "h1", "html": h, "tekst": tx})
        elif st == "HEADING_2":
            blokken.append({"type": "h2", "html": h, "tekst": tx})
        elif st in ("HEADING_3", "HEADING_4"):
            blokken.append({"type": "h3", "html": h, "tekst": tx})
        elif st == "SUBTITLE":
            blokken.append({"type": "subtitel", "html": h, "tekst": tx})
        elif info["bullet"]:
            blokken.append({"type": "li", "html": h, "tekst": tx, "grijs": info["grijs"]})
        elif info["vet"] and len(tx) < 90 and not tx.endswith("."):
            blokken.append({"type": "h4", "html": h, "tekst": tx})
        else:
            blokken.append({"type": "p", "html": h, "tekst": tx, "grijs": info["grijs"]})
        i += 1
    return blokken

# ---------------------------------------------------------------- Markdown (tekstexport) -> blokken
def md_inline(t):
    t = E(t)
    t = re.sub(r"\\\*", "*", t)
    t = re.sub(r"\*\*(.+?)\*\*", r"\1", t)
    t = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", t)
    t = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r'<a href="\2">\1</a>', t)
    t = t.replace("\\!", "!").replace("\\-", "-").replace("\\.", ".").replace("\\[", "[").replace("\\]", "]")
    return t.strip()

def platte(h):
    return html.unescape(re.sub("<.*?>", "", h)).strip()

def md_naar_blokken(tekst):
    """Tekstexport zonder opmaakdetails: koppen, alinea's, tabellen. Beeldbijschriften zijn hier niet herkenbaar en vallen weg."""
    blokken = []
    regels = tekst.split("\n"); i = 0
    while i < len(regels):
        r = regels[i].rstrip()
        if not r.strip():
            i += 1; continue
        m = re.match(r"^(#{1,4}) (.*)$", r)
        if m:
            niv = len(m.group(1)); h = md_inline(m.group(2))
            blokken.append({"type": {1: "h1", 2: "h2", 3: "h3", 4: "h3"}[niv], "html": h, "tekst": platte(h)})
            i += 1; continue
        if r.startswith("|"):
            rij = []
            while i < len(regels) and regels[i].startswith("|"):
                cel = [c.strip() for c in regels[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-+:?", c) or c == "" for c in cel):
                    rij.append([md_inline(c) for c in cel])
                i += 1
            rij = [x for x in rij if any(c for c in x)]
            if not rij: continue
            if len(rij[0]) == 1:
                tx = rij[0][0]
                if "colofon" in tx.lower(): blokken.append({"type": "colofon"}); continue
                blokken.append({"type": "kader", "regels": [(tx, platte(tx), {"vet": False, "grijs": False})]})
            else:
                kop = [platte(c).lower() for c in rij[0]]
                if kop[:2] in (["woord", "definitie"], ["begrip", "betekenis"]):
                    blokken.append({"type": "woorden", "items": [(c[0], c[1]) for c in rij[1:] if c[0]]})
                elif len(rij[0]) == 2 and len(rij) <= 8 and all(len(platte(c[0])) < 30 for c in rij):
                    blokken.append({"type": "fiche", "items": [(c[0], c[1]) for c in rij]})
                else:
                    blokken.append({"type": "tabel", "rijen": rij})
            continue
        if r.startswith("[") and "docs.google.com" in r:
            i += 1; continue
        m = re.match(r"^\s*(?:[-*]|\d+\\?\.)\s+(.*)$", r)
        h = md_inline(m.group(1) if m else r)
        tx = platte(h)
        if m:
            blokken.append({"type": "li", "html": h, "tekst": tx, "grijs": False})
        elif re.fullmatch(r"\*\*[^*]{2,85}\*\*", r.strip()) and not tx.endswith("."):
            blokken.append({"type": "h4", "html": h, "tekst": tx})
        else:
            blokken.append({"type": "p", "html": h, "tekst": tx, "grijs": False})
        i += 1
    return blokken

# ---------------------------------------------------------------- blokken opsplitsen
def voorkant(blokken):
    """Alles voor de eerste kop 1 die geen inhoudstafel is."""
    for k, b in enumerate(blokken):
        if b["type"] == "h1" and "inhoudstafel" not in b["tekst"].lower() and not re.match(r"^(Hoofdstuk \d+|Jaarcursus)", b["tekst"]):
            return blokken[:k], blokken[k:]
    return [], blokken

def splits_h1(blokken):
    delen, huidig = [], None
    for b in blokken:
        if b["type"] == "h1":
            huidig = {"titel": b["tekst"], "blokken": []}; delen.append(huidig)
        elif huidig is not None:
            huidig["blokken"].append(b)
    return delen

def splits_h2(blokken):
    delen, huidig = [], None
    for b in blokken:
        if b["type"] == "h2":
            huidig = {"titel": b["tekst"], "blokken": []}; delen.append(huidig)
        elif huidig is not None:
            huidig["blokken"].append(b)
    return delen

# ---------------------------------------------------------------- blokken -> HTML
def slugify(t):
    t = html.unescape(re.sub("<.*?>", "", t)).lower()
    t = re.sub(r"[àáâä]", "a", t); t = re.sub(r"[èéêë]", "e", t); t = re.sub(r"[ìíîï]", "i", t)
    t = re.sub(r"[òóôö]", "o", t); t = re.sub(r"[ùúûü]", "u", t); t = t.replace("ç", "c")
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")[:60] or "deel"

ELEMENTEN = ("Lichaam", "Ruimte", "Object", "Tijd")

def blokken_html(blokken, nav, ids):
    out, lijst, lijsttype = [], [], "ul"
    def sluit():
        nonlocal lijst
        if lijst:
            out.append(f'<{lijsttype} class="lijst">' + "".join(f"<li>{x}</li>" for x in lijst) + f"</{lijsttype}>")
            lijst = []
    for b in blokken:
        t = b["type"]
        if t != "li": sluit()
        if t in ("h2", "h3"):
            sid = slugify(b["tekst"])
            while sid in ids: sid += "-2"
            ids.add(sid)
            klasse = ' class="verwijzing"' if b["tekst"].lower().startswith("kunsthistorische verwijzing") else (' class="sub"' if t == "h3" else "")
            out.append(f'<{t} id="{sid}"{klasse}>{b["html"]}</{t}>')
            nav.append((t, sid, b["tekst"]))
        elif t == "h4":
            out.append(f'<h4>{b["html"]}</h4>')
        elif t == "p":
            m = re.match(r"^(Lichaam|Ruimte|Object|Tijd)\.\s+(.*)$", b["html"])
            if m:
                out.append(f'<div class="el {m.group(1).lower()}"><h5>{m.group(1)}</h5><p>{m.group(2)}</p></div>')
            else:
                out.append(f'<p class="uitbreiding">{b["html"]}</p>' if b.get("grijs") else f'<p>{b["html"]}</p>')
        elif t == "li":
            lijst.append(b["html"])
        elif t == "fig":
            cap = "<br>".join(b["regels"])
            links = ""
            gezien = set()
            for naam, url in b["links"]:
                if url in gezien: continue
                gezien.add(url)
                links += f'<a class="werk-link" href="{E(url)}">Bekijk bij {E(naam)}</a>'
            out.append(f'<figure class="beeld"><figcaption>{cap}</figcaption>' + (f'<div class="werk-links">{links}</div>' if links else "") + "</figure>")
        elif t == "kader":
            r = b["regels"]
            kop = ""
            if len(r) > 1 and len(r[0][1]) < 80 and not r[0][1].endswith("."):
                kop = f"<h4>{r[0][0]}</h4>"; r = r[1:]
            out.append('<aside class="kader">' + kop + "".join(f"<p>{h}</p>" for h, _, _ in r) + "</aside>")
        elif t == "fiche":
            out.append('<dl class="fiche">' + "".join(f"<dt>{a}</dt><dd>{v}</dd>" for a, v in b["items"]) + "</dl>")
        elif t == "tabel":
            rijen = b["rijen"]
            kop = "<tr>" + "".join(f"<th>{c}</th>" for c in rijen[0]) + "</tr>"
            rest = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rijen[1:])
            out.append(f'<div class="tabel"><table>{kop}{rest}</table></div>')
        elif t == "woorden":
            out.append("<!--WOORDEN-->")
    sluit()
    return "\n".join(out)

def vragen_uit(blokken):
    """Splitst voorbeeldvragen in groepen (A. ..., B. ...)."""
    groepen, huidig = [], None
    for b in blokken:
        tx = b.get("tekst", "")
        if b["type"] in ("h2", "h3", "h4") or (b["type"] == "p" and re.match(r"^[A-D]\. ", tx) and len(tx) < 60):
            huidig = {"titel": tx, "vragen": []}; groepen.append(huidig); continue
        if b["type"] in ("p", "li") and tx:
            if huidig is None:
                huidig = {"titel": "", "vragen": []}; groepen.append(huidig)
            huidig["vragen"].append(re.sub(r"^\d+\\?\.\s*", "", b["html"]))
    return [g for g in groepen if g["vragen"]]

def maak_pagina(meta, inhoud, woorden, vragen, extra=None, vorige=None, volgende=None, heeft_grijs=False):
    """meta: slug, titel, ondertitel, eyebrow. inhoud: lijst blokken zonder titelpagina."""
    nav, ids = [], set()
    body = blokken_html(inhoud, nav, ids)
    heeft_el = body.count('<div class="el ') >= 4
    if heeft_el:
        filt = ('<div class="kijkfilter" role="group" aria-label="Volg één element"><span>Volg één element</span>'
                '<button type="button" data-focus="" aria-pressed="true">Alles</button>'
                + "".join(f'<button type="button" data-focus="{x.lower()}" aria-pressed="false">{x}</button>' for x in ELEMENTEN) + "</div>")
        body = filt + '<div id="werken">' + body + "</div>"
    extra_html = ""
    for titel, blok in (extra or []):
        sid = slugify(titel); nav.append(("h2", sid, titel))
        extra_html += f'<section id="{sid}"><h2>{E(titel)}</h2>' + blokken_html(blok, [], ids) + "</section>"
    woord_html = ""
    if woorden:
        nav.append(("h2", "woordenschat", "Woordenschat"))
        data = json.dumps([[platte(a), platte(b)] for a, b in woorden], ensure_ascii=False)
        woord_html = ('<section id="woordenschat"><h2>Woordenschat</h2><div class="hulp">'
                      '<label for="zoekwoord" style="position:absolute;left:-999rem">Zoek een woord</label>'
                      '<input type="search" id="zoekwoord" placeholder="Zoek een woord">'
                      '<button type="button" id="oefenknop" aria-pressed="false">Definities verbergen om te oefenen</button></div>'
                      '<dl class="woorden" id="woordenlijst"></dl><p class="leeg" id="geenwoord" hidden>Geen woord gevonden. Probeer een ander zoekwoord.</p>'
                      f'<script type="application/json" id="woorddata">{data.replace("</", "<\\/")}</script></section>')
    vraag_html = ""
    if vragen:
        nav.append(("h2", "vragen", "Oefenvragen"))
        vraag_html = '<section id="vragen"><h2>Oefenvragen</h2><p class="teller" id="teller"></p>'
        for k, g in enumerate(vragen):
            if g["titel"]: vraag_html += f'<h3 class="sub">{E(g["titel"])}</h3>'
            vraag_html += '<ol class="vragen">' + "".join(
                f'<li><input type="checkbox" id="v{k}-{j}" data-vraag="{k}-{j}"><label for="v{k}-{j}">{v}</label></li>' for j, v in enumerate(g["vragen"])) + "</ol>"
        vraag_html += "</section>"
    navitems = []
    for niv, sid, tx in nav:
        if niv == "h2": navitems.append([sid, tx, []])
        elif navitems: navitems[-1][2].append((sid, tx))
        else: navitems.append([sid, tx, []])
    nav_html = "".join(
        f'<li><a href="#{sid}">{E(tx)}</a>' + (("<ol>" + "".join(f'<li><a href="#{s}">{E(t)}</a></li>' for s, t in sub) + "</ol>") if 0 < len(sub) <= 14 else "") + "</li>"
        for sid, tx, sub in navitems)
    legende = '<p class="legende"><span>Tekst met een grijze lijn ervoor is uitbreiding of achtergrond.</span></p>' if (heeft_grijs or 'class="uitbreiding"' in body) else ""
    buren = ""
    if vorige or volgende:
        buren = '<nav class="hoofdstuk-nav" aria-label="Vorig en volgend onderwerp">'
        buren += f'<a href="../{vorige[0]}/"><span>Vorig onderwerp</span>&larr; {E(vorige[1])}</a>' if vorige else "<span></span>"
        buren += f'<a href="../{volgende[0]}/" style="text-align:right"><span>Volgend onderwerp</span>{E(volgende[1])} &rarr;</a>' if volgende else ""
        buren += "</nav>"
    pagina = f'''<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(meta["titel"])}</title>
<meta name="description" content="{E(meta.get("ondertitel",""))}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Carlito:ital,wght@0,400;0,700;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>{CSS}{EXTRA_CSS}</style>
</head>
<body>
<div class="pagina">
<nav class="inhoud" aria-label="Inhoud">
  <p class="vak"><a href="../" style="text-decoration:none;color:inherit">&larr; Kunst bekijken</a></p>
  <p class="vak">Inhoud</p>
  <ol>{nav_html}</ol>
</nav>
<main>
<header class="titel">
  <p class="vak"><a href="../" style="color:inherit">Kunst bekijken</a> / {E(meta.get("eyebrow",""))}</p>
  <h1>{E(meta["titel"])}</h1>
  <p class="onder">{E(meta.get("ondertitel",""))}</p>
</header>
{legende}
{body}
{extra_html}
{woord_html}
{vraag_html}
{buren}
<footer><p>Samengesteld door Sammy Ben Yakoub. Titels van kunstwerken staan cursief. De kunstwerken bekijk je via de links naar de musea en archieven die ze bewaren. <a href="../">Terug naar alle onderwerpen</a>.</p></footer>
</main>
</div>
<script>
var werken=document.getElementById("werken");
document.querySelectorAll(".kijkfilter button").forEach(function(k){{k.addEventListener("click",function(){{var f=k.getAttribute("data-focus");if(f){{werken.setAttribute("data-focus",f);}}else{{werken.removeAttribute("data-focus");}}document.querySelectorAll(".kijkfilter button").forEach(function(b){{b.setAttribute("aria-pressed",b===k?"true":"false");}});}});}});
var wd=document.getElementById("woorddata");
if(wd){{var W=JSON.parse(wd.textContent),lijst=document.getElementById("woordenlijst");
W.forEach(function(w){{var r=document.createElement("div"),dt=document.createElement("dt"),dd=document.createElement("dd");dt.textContent=w[0];dd.textContent=w[1];r.appendChild(dt);r.appendChild(dd);r.addEventListener("click",function(){{if(lijst.classList.contains("verborgen"))r.classList.toggle("toon");}});lijst.appendChild(r);}});
document.getElementById("zoekwoord").addEventListener("input",function(e){{var q=e.target.value.trim().toLowerCase(),n=0;lijst.querySelectorAll("div").forEach(function(r){{var p=!q||r.textContent.toLowerCase().indexOf(q)>-1;r.hidden=!p;if(p)n++;}});document.getElementById("geenwoord").hidden=n>0;}});
var ok=document.getElementById("oefenknop");ok.addEventListener("click",function(){{var a=lijst.classList.toggle("verborgen");lijst.querySelectorAll("div").forEach(function(r){{r.classList.remove("toon");}});ok.setAttribute("aria-pressed",a?"true":"false");ok.textContent=a?"Definities weer tonen":"Definities verbergen om te oefenen";}});}}
var S="vragen-{meta["slug"]}",G={{}};try{{G=JSON.parse(localStorage.getItem(S)||"{{}}")||{{}};}}catch(e){{G={{}};}}
var cb=document.querySelectorAll("ol.vragen input");
function tel(){{var t=document.getElementById("teller");if(!t)return;var n=0;cb.forEach(function(c){{if(c.checked)n++;}});t.textContent=n+" van "+cb.length+" vragen geoefend. Vink een vraag af als je ze hebt beantwoord.";}}
cb.forEach(function(c){{c.checked=!!G[c.dataset.vraag];c.addEventListener("change",function(){{G[c.dataset.vraag]=c.checked;try{{localStorage.setItem(S,JSON.stringify(G));}}catch(e){{}}tel();}});}});tel();
if("IntersectionObserver" in window){{var L={{}};document.querySelectorAll("nav.inhoud a[href^='#']").forEach(function(a){{L[a.getAttribute("href").slice(1)]=a;}});
var io=new IntersectionObserver(function(it){{it.forEach(function(x){{if(x.isIntersecting&&L[x.target.id]){{Object.keys(L).forEach(function(k){{L[k].classList.remove("actief");}});L[x.target.id].classList.add("actief");}}}});}},{{rootMargin:"-10% 0px -80% 0px"}});
Object.keys(L).forEach(function(id){{var el=document.getElementById(id);if(el)io.observe(el);}});}}
</script>
</body>
</html>
'''
    return pagina
