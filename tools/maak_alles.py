# Bouwt alle hoofdstukpagina's uit de opgehaalde Google Docs (in /tmp/docs) en werkt de startpagina bij.
import sys, re, json, pathlib
HIER = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HIER))
from omzetten import *
from onderwerpen import ONDERWERPEN
from herschrijvingen import HERSCHRIJF
import media

DOCS = pathlib.Path("/tmp/docs")
SITE = HIER.parent

LOS = {  # slug -> doc met één hoofdstuk
 "epoche": "KBS5_EPOCHE_CLASS_2627", "iconografie": "KBS5_ICONOGRAFIE_CLASS_2627", "performance": "KBS5_PERFORMANCE_CLASS_2627",
 "sjklovski": "KBS4_SJKLOVSKI_CLASS_2627", "walter-benjamin": "KBS5_BENJAMIN_CLASS_2627", "susan-sontag": "KBS5_SONTAG_CLASS_2627",
 "roland-barthes": "EST5_BARTHES_CLASS_2627", "arthur-danto": "KBS6_DANTO_CLASS_2627", "gilles-deleuze": "KBS6_DELEUZE_CLASS_2627",
 "tanizaki": "EST6_TANIZAKI_CLASS_2627", "conceptuele-kunst": "KBS6_CONCEPTUEEL_CLASS_2627", "popart": "KBS6_POPART_CLASS_2627",
 "duchamp": "KBS6_DUCHAMP_CLASS_2627", "anouk-de-clercq": "CULT_DECLERCQ_CLASS_2627",
}
KBS6 = {"dada": "1", "kant": "2", "architectuur-en-design": "3", "muziek": "4"}
KBS5 = {"de-vier-elementen": "Inleiding", "ron-mueck": "1", "film": "4", "modernisme": "5"}
KBS4 = {"caravaggio": "Barok", "rococo": "Rococo", "neoclassicisme": "Neoclassicisme", "romantiek": "Romantiek"}

INFO = {o[0]: o for o in ONDERWERPEN}

def eyebrow(o):
    slug, titel, onder, deuren, jaar, periode, vormen, status = o
    if "tijd" in deuren: return f"Door de tijd, {periode}" if periode else "Door de tijd"
    if "kijken" in deuren: return "Leren kijken"
    if "denken" in deuren: return "Denken over kunst"
    return "Kunstvormen"

def opschonen(blokken):
    uit, skip = [], False
    for b in blokken:
        t = b["type"]
        if t == "colofon": continue
        if t == "fig" and b["regels"] and re.sub("<.*?>", "", b["regels"][0]).lower().startswith("tijdlijn"): continue
        if t in ("h2", "h3", "h1"): skip = False
        if t == "h4" and b["tekst"].lower().startswith(("samengevat", "samenvatting", "besluit")): skip = True
        if skip: continue
        if t in ("p", "li") and re.match(r"^\[\s*afbeelding", b.get("tekst", ""), re.I): continue
        if t in ("p", "h4", "h2") and b["tekst"].lower().strip(" :") in ("inhoudstafel",): continue
        uit.append(b)
    # alinea's die midden in een zin zijn afgebroken weer samenvoegen
    samen = []
    for b in uit:
        if (b["type"] == "h4" and samen and samen[-1]["type"] == "p" and not re.search(r"[.!?:;)\"’”]$", samen[-1]["tekst"])):
            samen[-1] = dict(samen[-1], html=samen[-1]["html"] + " " + b["html"].rstrip(":") + ":", tekst=samen[-1]["tekst"] + " " + b["tekst"]); continue
        if (b["type"] == "p" and samen and samen[-1]["type"] == "p" and not samen[-1].get("grijs")
                and not re.search(r"[.!?:;)\"’”]$", samen[-1]["tekst"]) and re.match(r"^[a-zàéèëï(]", b["tekst"])):
            samen[-1] = dict(samen[-1], html=samen[-1]["html"] + " " + b["html"], tekst=samen[-1]["tekst"] + " " + b["tekst"])
        else:
            samen.append(b)
    return samen

def strepen(blokken):
    """Geen gedachtestreepjes: ' – ' wordt een komma, 1509–1511 wordt 1509-1511."""
    def fix(h):
        h = re.sub(r"(\d)\s*[–—]\s*(\d)", r"\1-\2", h)
        return re.sub(r"\s+[–—]\s+", ", ", h)
    uit = []
    for b in blokken:
        b = dict(b)
        for k in ("html", "tekst"):
            if k in b: b[k] = fix(b[k])
        if "regels" in b and b["type"] == "fig": b["regels"] = [fix(r) for r in b["regels"]]
        if "items" in b: b["items"] = [(fix(a), fix(v)) for a, v in b["items"]]
        uit.append(b)
    return uit

def bijschriften_uit_tekst(blokken):
    """Tekstexport: een korte regel met een jaartal tussen haakjes, gevolgd door een korte regel, is een bijschrift."""
    uit, i = [], 0
    while i < len(blokken):
        b = blokken[i]
        if (b["type"] == "p" and len(b["tekst"]) < 170 and not b["tekst"].endswith(".")
                and (b["tekst"].endswith(")") or re.search(r"°\d{4}|\(\d{4}", b["tekst"]))
                and i + 1 < len(blokken) and blokken[i + 1]["type"] == "p" and len(blokken[i + 1]["tekst"]) < 260):
            uit.append({"type": "fig", "regels": [b["html"], blokken[i + 1]["html"]], "links": []}); i += 2; continue
        uit.append(b); i += 1
    return uit

def addenda(delen):
    """Haalt woordenschat, vragen en overige addenda uit een lijst H1-delen."""
    woorden, vragen, extra, inhoud = [], [], [], []
    for d in delen:
        titel = d["titel"]
        if titel.lower().startswith("addendum"):
            naam = titel.split(":", 1)[-1].strip()
            if "woordenschat" in naam.lower():
                for b in d["blokken"]:
                    if b["type"] == "woorden": woorden += b["items"]
            elif "vragen" in naam.lower():
                vragen += vragen_uit(d["blokken"])
            else:
                extra.append((naam, opschonen(d["blokken"])))
        else:
            inhoud.append(d)
    return woorden, vragen, extra, inhoud

def addendum_per_hoofdstuk(delen, sleutel):
    """Jaarcursus: addenda hebben per hoofdstuk een kop 2 'Hoofdstuk N: ...' of 'Inleiding: ...'."""
    woorden, vragen, extra = [], [], []
    for d in delen:
        if not d["titel"].lower().startswith("addendum"): continue
        naam = d["titel"].split(":", 1)[-1].strip()
        for sub in splits_h2(d["blokken"]):
            t = sub["titel"]
            if not (t.startswith(f"Hoofdstuk {sleutel}:") or (sleutel == "Inleiding" and t.startswith("Inleiding"))): continue
            if "woordenschat" in naam.lower():
                for b in sub["blokken"]:
                    if b["type"] == "woorden": woorden += b["items"]
            elif "vragen" in naam.lower():
                vragen += vragen_uit(sub["blokken"])
            else:
                extra.append((naam, opschonen(sub["blokken"])))
    return woorden, vragen, extra

def zonder_woorden(blokken):
    return [b for b in blokken if b["type"] != "woorden"]

def volgorde():
    kijken = [o[0] for o in ONDERWERPEN if "kijken" in o[3]]
    tijd = [o[0] for o in sorted([o for o in ONDERWERPEN if "tijd" in o[3]], key=lambda o: o[4])]
    rest = [o[0] for o in ONDERWERPEN if not o[3]]
    denken = [o[0] for o in ONDERWERPEN if "denken" in o[3]]
    seq = []
    for s in kijken + tijd + rest + denken:
        if s not in seq: seq.append(s)
    return seq

GEBOUWD = {}

def schrijf(slug, inhoud, woorden, vragen, extra):
    GEBOUWD[slug] = (strepen(inhoud), strepen([{"type":"x","items":woorden}])[0]["items"], vragen, [(t, strepen(b)) for t, b in extra])

def voeg_media_toe(slug, html_):
    items = media.MEDIA.get(slug, [])
    if not items: return html_
    for anker, tp, mid, titel, bron, uitleg in items:
        pos = html_.find(f'id="{anker}"')
        if pos < 0: print("  ANKER NIET GEVONDEN", slug, anker); continue
        nxt = [i for i in (html_.find(t, pos + 10) for t in ('<h2 id=', '<h3 id=', '<section', '<nav class="hoofdstuk-nav"')) if i > 0]
        at = min(nxt)
        html_ = html_[:at] + media.blok(tp, mid, titel, bron, uitleg) + "\n" + html_[at:]
    html_ = html_.replace("</style>", media.CSS + "</style>", 1)
    html_ = html_.replace("</script>\n</body>", media.JS + "</script>\n</body>")
    return html_

def dijkstra_media():
    p = SITE / "rineke-dijkstra" / "index.html"
    s = p.read_text(encoding="utf-8")
    if 'class="media"' in s: return
    blokken = "".join(media.blok(*x) for x in media.DIJKSTRA)
    s = s.replace('<ul class="links">', blokken + '\n<ul class="links">', 1)
    s = s.replace('<h2>Verder kijken en lezen</h2>', '<h2>Verder kijken en luisteren</h2>', 1)
    s = s.replace("</style>", media.CSS + "</style>", 1)
    s = s.replace("</script>\n</body>", media.JS + "</script>\n</body>")
    p.write_text(s, encoding="utf-8")

def render_alles():
    seq = [s for s in volgorde() if s in GEBOUWD or s == "rineke-dijkstra"]
    for slug, (inhoud, woorden, vragen, extra) in GEBOUWD.items():
        o = INFO[slug]; k = seq.index(slug)
        vorige = (seq[k - 1], INFO[seq[k - 1]][1]) if k > 0 else None
        volgende = (seq[k + 1], INFO[seq[k + 1]][1]) if k + 1 < len(seq) else None
        meta = {"slug": slug, "titel": o[1], "ondertitel": o[2], "eyebrow": eyebrow(o)}
        html_ = maak_pagina(meta, inhoud, woorden, vragen, extra, vorige, volgende)
        for oud, nieuw in HERSCHRIJF.get(slug, []):
            oud_e, nieuw_e = html.escape(oud, quote=False), html.escape(nieuw, quote=False)
            if oud_e not in html_: print("  NIET GEVONDEN", slug, oud[:60]); continue
            html_ = html_.replace(oud_e, nieuw_e)
        html_ = re.sub(r"<p>\s*</p>", "", html_)
        html_ = voeg_media_toe(slug, html_)
        (SITE / slug).mkdir(exist_ok=True)
        (SITE / slug / "index.html").write_text(html_, encoding="utf-8")
        print(f"{slug:24} {len(html_)//1024:4} kB  {len(woorden):3} woorden  {sum(len(g['vragen']) for g in vragen):3} vragen  {html_.count('class=\"beeld\"'):3} beelden  {html_.count('werk-link'):3} links")

# ---- losse docs
for slug, naam in LOS.items():
    body, fns = laad_doc(DOCS / f"{naam}.json")
    bl = doc_naar_blokken(body, fns)
    _, rest = voorkant(bl)
    delen = splits_h1(rest)
    w, v, x, inh = addenda(delen)
    inhoud = []
    for d in inh:
        if "inhoudstafel" in d["titel"].lower(): continue
        inhoud += d["blokken"]
    schrijf(slug, zonder_woorden(opschonen(inhoud)), w, v, x)

# ---- jaarcursus 6
body, fns = laad_doc(DOCS / "KBS6_JAARCURSUS_CLASS_2627.json")
delen = splits_h1(voorkant(doc_naar_blokken(body, fns))[1])
for slug, nr in KBS6.items():
    d = next(d for d in delen if d["titel"].startswith(nr + " "))
    w, v, x = addendum_per_hoofdstuk(delen, nr)
    schrijf(slug, zonder_woorden(opschonen(d["blokken"])), w, v, x)

# ---- jaarcursus 5 (tekstexport)
tekst = (DOCS.parent / "drive" / "KBS5.md").read_text(encoding="utf-8")
delen = splits_h1(md_naar_blokken(tekst))
for slug, nr in KBS5.items():
    d = next(d for d in delen if d["titel"].startswith(nr + " ") or (nr == "Inleiding" and d["titel"].startswith("Inleiding")))
    w, v, x = addendum_per_hoofdstuk(delen, nr)
    schrijf(slug, zonder_woorden(bijschriften_uit_tekst(opschonen(d["blokken"]))), w, v, x)

# ---- jaarcursus 4 (oudere opmaak)
body, fns = laad_doc(DOCS / "cursus_KBS_4_totaal_jaar_2 (2).json")
delen = splits_h1(doc_naar_blokken(body, fns))
for slug, begin in KBS4.items():
    d = next(d for d in delen if d["titel"].startswith(begin))
    schrijf(slug, zonder_woorden(opschonen(d["blokken"])), [], [], [])

render_alles()
dijkstra_media()
