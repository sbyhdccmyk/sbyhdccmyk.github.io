"""Publiek-domeinbeelden (Wikimedia Commons) in de hoofdstukken invoegen.

beelden.json
  bestaand: [slug, n, bestand]  -> afbeelding in de n-de <figure class="beeld"> van die pagina
  nieuw:    [slug, h|t, anker, bestand, regel1, regel2] -> nieuwe figuur na kop (h) of alinea (t)
  lokaal:   [slug, n, bestand, breedte, hoogte, credit] -> eigen bestand in de map <slug>/beelden/, in de n-de figuur;
            credit is de html van de bronregel (maker en licentie)
maten.json: [bestand, breedte, hoogte] (opgevraagd via de Commons-API)
"""
import hashlib, html, json, re, urllib.parse
from pathlib import Path

HIER = Path(__file__).parent
DATA = json.loads((HIER / "beelden.json").read_text(encoding="utf-8"))
MATEN = {b: (w, h) for b, w, h in json.loads((HIER / "maten.json").read_text(encoding="utf-8"))}
BREED = 960

CSS = (".beeld .pd{display:block;margin:0 auto .7rem}"
       ".beeld .pd img{display:block;max-width:100%;max-height:78vh;width:auto;height:auto;margin:0 auto;"
       "box-shadow:0 1px 6px rgba(0,0,0,.18);background:#ddd}"
       ".beeld .credit{font-size:.8rem;opacity:.75;margin:.35rem 0 0}"
       ".beeld .credit a{color:inherit}")


def _naam(b):
    return b.replace(" ", "_")


def url(b):
    n = _naam(b)
    h = hashlib.md5(n.encode("utf-8")).hexdigest()
    q = urllib.parse.quote(n, safe="")
    w, _ = MATEN[b]
    if w <= BREED:
        return f"https://upload.wikimedia.org/wikipedia/commons/{h[0]}/{h[:2]}/{q}", w
    if n.lower().endswith((".tif", ".tiff")):
        q2 = f"lossy-page1-{BREED}px-{q}.jpg"
    else:
        q2 = f"{BREED}px-{q}"
    return f"https://upload.wikimedia.org/wikipedia/commons/thumb/{h[0]}/{h[:2]}/{q}/{q2}", BREED


def pagina(b):
    return "https://commons.wikimedia.org/wiki/File:" + urllib.parse.quote(_naam(b), safe="(),'")


def img(b, alt):
    src, w = url(b)
    W, H = MATEN[b]
    h = round(H * w / W)
    alt = html.escape(re.sub(r"<[^>]+>", "", html.unescape(alt)).strip(), quote=True)
    return (f'<a class="pd" href="{pagina(b)}" title="Grotere versie op Wikimedia Commons">'
            f'<img src="{src}" width="{w}" height="{h}" loading="lazy" decoding="async" alt="{alt}"></a>')


def credit(b):
    return (f'<p class="credit">Publiek domein. Afbeelding via '
            f'<a href="{pagina(b)}">Wikimedia Commons</a></p>')


def _zonder_tags(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s))


def voeg_toe(slug, s):
    """Zet beelden in de pagina-HTML s. Geeft (nieuwe html, aantal)."""
    n = 0
    regels = {k: b for sl, k, b in DATA["bestaand"] if sl == slug}
    if regels:
        delen = s.split('<figure class="beeld">')
        for k, b in regels.items():
            d = delen[k + 1]
            if 'class="pd"' in d:
                continue
            m = re.match(r"<figcaption>(.*?)</figcaption>", d, re.S)
            alt = m.group(1).split("<br>")[0] if m else ""
            d = img(b, alt) + d
            d = d.replace("</figcaption>", "</figcaption>" + credit(b), 1)
            delen[k + 1] = d
            n += 1
        s = '<figure class="beeld">'.join(delen)
    lokaal = [x for x in DATA.get("lokaal", []) if x[0] == slug]
    if lokaal:
        delen = s.split('<figure class="beeld">')
        for _, k, b, w, h, cr in lokaal:
            d = delen[k + 1]
            if 'class="pd"' in d:
                continue
            m = re.match(r"<figcaption>(.*?)</figcaption>", d, re.S)
            alt = _zonder_tags(m.group(1).split("<br>")[0]).strip() if m else ""
            d = (f'<a class="pd" href="beelden/{b}" title="Grotere versie"><img src="beelden/{b}" width="{w}" height="{h}" '
                 f'loading="lazy" decoding="async" alt="{html.escape(alt, quote=True)}"></a>') + d
            d = d.replace("</figcaption>", f'</figcaption><p class="credit">{cr}</p>', 1)
            delen[k + 1] = d
            n += 1
        s = '<figure class="beeld">'.join(delen)
    for sl, tp, anker, b, r1, r2 in DATA["nieuw"]:
        if sl != slug:
            continue
        fig = (f'<figure class="beeld">{img(b, r1)}<figcaption>{r1}<br>{r2}</figcaption>'
               f'{credit(b)}</figure>\n')
        if tp == "h":
            pat = r"<h[34][^>]*>.*?</h[34]>"
        else:
            pat = r"<p>.*?</p>"
        for m in re.finditer(pat, s, re.S):
            if anker.lower() in _zonder_tags(m.group(0)).lower():
                s = s[:m.end()] + "\n" + fig + s[m.end():]
                n += 1
                break
        else:
            print("  BEELDANKER NIET GEVONDEN", slug, anker)
    if n and CSS not in s:
        s = s.replace("</style>", CSS + "</style>", 1)
    return s, n
