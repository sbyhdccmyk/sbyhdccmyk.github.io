# Zet bij elk hoofdstuk een blok "Waar en wanneer": het referentiekader als strook, de mijlpalen in de kunst
# en in de wereld, en links naar hoofdstukken uit dezelfde tijd. Kan altijd opnieuw draaien: het oude blok wordt vervangen.
import re, html, pathlib, sys
HIER = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HIER))
from onderwerpen import ONDERWERPEN
from tijdlijnen import BANDEN, T

SITE = HIER.parent
E = html.escape
INFO = {o[0]: o for o in ONDERWERPEN}

CSS = """/*situering*/
.situering{margin:0 0 2.5rem;padding:1rem 1.1rem 1.1rem;background:var(--kader);border:1px solid var(--lijn)}
.sit-kop{font-family:var(--data);font-size:.72rem;letter-spacing:.06em;text-transform:uppercase;color:var(--rood);margin:0 0 .7rem}
.sit-feiten{display:grid;grid-template-columns:repeat(auto-fit,minmax(13rem,1fr));gap:.4rem 1.5rem;margin:0 0 1rem}
.sit-feiten dt{font-family:var(--data);font-size:.68rem;letter-spacing:.05em;text-transform:uppercase;color:var(--zacht)}
.sit-feiten dd{margin:0;font-weight:700;line-height:1.3}
.sit-scroll{margin:0 0 .8rem}
ol.sit-kader{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(5.6rem,1fr));gap:2px}
ol.sit-kader li{background:var(--wand);border-top:4px solid var(--lijn);padding:.3rem .35rem .4rem;font-size:.72rem;line-height:1.15;color:var(--zacht);display:flex;flex-direction:column;gap:.2rem;hyphens:auto}
ol.sit-kader li span{font-family:var(--data);font-size:.6rem}
ol.sit-kader li.ook{border-top-color:#e0a248;color:var(--inkt)}
ol.sit-kader li.hier{border-top-color:var(--rood);color:var(--inkt);font-weight:700}
ol.sit-kader li.hier span{font-weight:400}
ol.sit-lijn{list-style:none;margin:0 0 .8rem 0;padding:0;border-left:2px solid var(--inkt);margin-left:.35rem}
ol.sit-lijn li{position:relative;display:grid;grid-template-columns:8.2rem minmax(0,1fr);gap:.8rem;padding:.16rem 0 .16rem 1rem;font-size:1rem;line-height:1.35}
ol.sit-lijn li::before{content:"";position:absolute;left:-.4rem;top:.52rem;width:.55rem;height:.55rem;border-radius:50%;background:var(--inkt);border:1px solid var(--inkt)}
ol.sit-lijn li.w::before{border-radius:0;background:var(--kader);border:2px solid var(--zacht);transform:rotate(45deg);width:.5rem;height:.5rem}
ol.sit-lijn li.w{color:var(--zacht)}
ol.sit-lijn .j{font-family:var(--data);font-size:.8rem;padding-top:.1rem;font-variant-numeric:tabular-nums}
.sit-uitleg{font-size:.88rem;color:var(--zacht);margin:0 0 .5rem}
.sit-uitleg b{display:inline-block;width:.55rem;height:.55rem;border-radius:50%;background:var(--inkt);margin-right:.3rem}
.sit-uitleg b.w{border-radius:0;background:var(--kader);border:2px solid var(--zacht);transform:rotate(45deg);margin-left:1rem}
.sit-uitleg i.h,.sit-uitleg i.o{display:inline-block;width:1.1rem;height:4px;vertical-align:middle;margin:0 .3rem 0 0;background:var(--rood)}
.sit-uitleg i.o{background:#e0a248;margin-left:1rem}
.sit-buren,.sit-noot{font-size:.95rem;margin:.5rem 0 0}
.sit-noot{color:var(--zacht)}
@media (max-width:34rem){ol.sit-lijn li{grid-template-columns:minmax(0,1fr);gap:0}}
/*/situering*/"""

def cursief(tekst):
    """Titels van werken staan cursief: alles na 'Naam, ' tot een dubbele punt of het einde, als het zo in de gegevens staat."""
    return re.sub(r"\*(.+?)\*", r"<i>\1</i>", E(tekst))

def buren(slug):
    t = T[slug]
    mijn = set(t["hoofd"])
    if not mijn: return ""
    uit = []
    for o in ONDERWERPEN:
        s = o[0]
        if s == slug or s not in T or o[7] != "online": continue
        if mijn & set(T[s]["hoofd"]): uit.append(f'<a href="../{s}/">{E(o[1])}</a>')
    return ('<p class="sit-buren">Uit dezelfde tijd: ' + ", ".join(uit) + ".</p>") if uit else ""

def blok(slug):
    t = T[slug]
    kader = "".join(
        f'<li class="{"hier" if i in t["hoofd"] else "ook" if i in t["ook"] else ""}">{E(n)}<span>{E(j)}</span></li>'
        for i, (n, j) in enumerate(BANDEN))
    lijn = "".join(f'<li class="{s}"><span class="j">{E(j)}</span><span>{cursief(tx)}</span></li>' for j, tx, s in t["lijn"])
    heeft_w = any(s == "w" for _, _, s in t["lijn"])
    uitleg = ""
    if t["hoofd"]:
        uitleg = '<p class="sit-uitleg"><i class="h"></i>hier hoort dit hoofdstuk thuis' + ('<i class="o"></i>hier verwijst het naar' if t["ook"] else "") + "</p>"
    legende = ""
    if lijn:
        legende = '<p class="sit-uitleg"><b></b>kunstwerken en teksten uit dit hoofdstuk' + ('<b class="w"></b>wat er in de wereld gebeurde' if heeft_w else "") + "</p>"
    noot = f'<p class="sit-noot">{E(t["noot"])}</p>' if t.get("noot") else ""
    return ('<!--situering--><section class="situering" aria-label="Situering in tijd en plaats">'
            '<p class="sit-kop">Waar en wanneer</p>'
            f'<dl class="sit-feiten"><div><dt>Wanneer</dt><dd>{E(t["wanneer"])}</dd></div><div><dt>Waar</dt><dd>{E(t["waar"])}</dd></div></dl>'
            f'<div class="sit-scroll" role="group" aria-label="Het referentiekader, van prehistorie tot vandaag"><ol class="sit-kader">{kader}</ol></div>{uitleg}'
            + (f'<ol class="sit-lijn">{lijn}</ol>{legende}' if lijn else "")
            + buren(slug) + noot + '</section><!--/situering-->')

def zet(slug):
    p = SITE / slug / "index.html"
    if slug not in T or not p.exists(): return False
    s = p.read_text(encoding="utf-8")
    s = re.sub(r"\n?<!--situering-->.*?<!--/situering-->", "", s, flags=re.S)
    s = re.sub(r"\n?/\*situering\*/.*?/\*/situering\*/", "", s, flags=re.S)
    k = s.find('<header class="titel">'); e = s.find("</header>", k)
    if k < 0 or e < 0: print("  geen titel gevonden:", slug); return False
    e += len("</header>")
    s = s[:e] + "\n" + blok(slug) + s[e:]
    s = s.replace("</style>", "\n" + CSS + "</style>", 1)
    p.write_text(s, encoding="utf-8")
    return True

def volgorde():
    kijken = [o[0] for o in ONDERWERPEN if "kijken" in o[3]]
    tijd = [o[0] for o in sorted([o for o in ONDERWERPEN if "tijd" in o[3]], key=lambda o: o[4])]
    rest = [o[0] for o in ONDERWERPEN if not o[3]]
    denken = [o[0] for o in ONDERWERPEN if "denken" in o[3]]
    seq = []
    for s in kijken + tijd + rest + denken:
        if s not in seq and INFO[s][7] == "online": seq.append(s)
    return seq

def onderaan():
    """Vorig en volgend onderwerp onderaan elke pagina in lijn brengen met de volgorde."""
    from omzetten import buren_html
    import kijkwijzer
    seq = volgorde()
    k = seq.index("kijkwijzer")
    kijkwijzer.bouw((seq[k + 1], INFO[seq[k + 1]][1]) if k + 1 < len(seq) else None)
    for k, slug in enumerate(seq):
        p = SITE / slug / "index.html"
        if slug == "kijkwijzer" or not p.exists(): continue
        s = p.read_text(encoding="utf-8")
        vorige = (seq[k - 1], INFO[seq[k - 1]][1]) if k > 0 else None
        volgende = (seq[k + 1], INFO[seq[k + 1]][1]) if k + 1 < len(seq) else None
        nieuw = re.sub(r'<nav class="hoofdstuk-nav".*?</nav>', lambda m: buren_html(vorige, volgende), s, count=1, flags=re.S)
        if nieuw != s: p.write_text(nieuw, encoding="utf-8"); print("  buren bijgewerkt:", slug)

def alles():
    onderaan()
    n = sum(zet(o[0]) for o in ONDERWERPEN)
    zonder = [o[0] for o in ONDERWERPEN if o[0] not in T and o[7] == "online" and o[0] != "kijkwijzer"]
    print("situering geplaatst bij", n, "hoofdstukken;", "zonder:", zonder or "geen")
    import verwijzingen
    verwijzingen.alles()  # kruisverwijzingen opnieuw leggen, ook in het nieuwe blok

if __name__ == "__main__":
    alles()
