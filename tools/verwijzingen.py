# Kruisverwijzingen: een kunstwerk, een naam of een begrip dat elders op de site besproken wordt,
# krijgt een link naar die plaats. De link opent in een nieuw venster.
# - Kunstwerken: elke titel die cursief staat en elders een eigen kop of beeld heeft (wordt automatisch gevonden).
# - Namen en begrippen: de lijsten NAMEN en BEGRIPPEN hieronder. Nieuwe term? Voeg een regel toe.
# Per deel van een pagina (per kop 2) wordt elke bestemming één keer gelinkt. Kan altijd opnieuw draaien.
import re, html, pathlib, sys, unicodedata
HIER = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HIER))
from onderwerpen import ONDERWERPEN

SITE = HIER.parent
INFO = {o[0]: o for o in ONDERWERPEN}
SLUGS = [o[0] for o in ONDERWERPEN if o[7] == "online"]

# (wat in de tekst staat, pagina, stukje van het anker op die pagina of "", eventueel: pagina's waar de term iets anders betekent)
# Een = voor een begrip: alleen in kleine letters (aura, niet de nimf Aura).
NAMEN = [
 ("Immanuel Kant|Kant", "kant", ""), ("Marcel Duchamp|Duchamp", "duchamp", ""), ("Viktor Sjklovski|Sjklovski", "sjklovski", ""),
 ("Walter Benjamin", "walter-benjamin", ""), ("Susan Sontag|Sontag", "susan-sontag", ""), ("Roland Barthes|Barthes", "roland-barthes", ""),
 ("Arthur Danto|Danto", "arthur-danto", ""), ("Gilles Deleuze|Deleuze", "gilles-deleuze", ""), ("Junichiro Tanizaki|Tanizaki", "tanizaki", ""),
 ("Erwin Panofsky|Panofsky", "iconografie", "stappenplan-van-panofsky"), ("Edmund Husserl|Husserl", "epoche", "3-husserl"),
 ("Caravaggio", "caravaggio", "caravaggio"), ("Marina Abramović|Abramović", "performance", "marina-abramovi-en-het-lichaam"),
 ("Ron Mueck|Mueck", "ron-mueck", ""), ("Rineke Dijkstra|Dijkstra", "rineke-dijkstra", ""), ("Anouk De Clercq|De Clercq", "anouk-de-clercq", ""),
 ("Andy Warhol|Warhol", "popart", "4-andy-warhol"), ("Richard Hamilton", "popart", "3-1-richard-hamilton"), ("Roy Lichtenstein|Lichtenstein", "popart", "3-2-roy-lichtenstein"),
 ("Gustave Courbet|Courbet", "modernisme", "gustave-courbet"), ("Jean-François Millet|Millet", "modernisme", "jean-francois-millet"),
 ("Édouard Manet|Manet", "modernisme", "5-2-edouard-manet"), ("Claude Monet|Monet", "modernisme", "claude-monet"),
 ("Pierre-Auguste Renoir|Renoir", "modernisme", "pierre-auguste-renoir"), ("Paul Cézanne|Cézanne", "modernisme", "paul-cezanne"),
 ("Vincent van Gogh|Van Gogh", "modernisme", "vincent-van-gogh"), ("Piet Mondriaan|Mondriaan", "modernisme", "piet-mondriaan"),
 ("Wassily Kandinsky|Kandinsky", "modernisme", "wassily-kandinsky"),
 ("Antoine Watteau|Watteau", "rococo", "antoine-watteau"), ("Jean-Honoré Fragonard|Jean Honoré Fragonard|Fragonard", "rococo", "jean-honore-fragonard"),
 ("Jacques-Louis David", "neoclassicisme", "jacques-louis-david"), ("Jean-Auguste-Dominique Ingres|Ingres", "neoclassicisme", "jean-auguste-dominique-ingres"),
 ("Caspar David Friedrich", "romantiek", "caspar-david-friedrich"), ("Théodore Géricault|Géricault", "romantiek", "theodore-gericault"),
 ("Sesshu Toyo|Sesshu", "japanse-meesters", "2-1-sesshu"), ("Hasegawa Tohaku|Hasegawa Tōhaku|Tohaku|Tōhaku", "japanse-meesters", "2-2-hasegawa"),
 ("Katsushika Hokusai|Hokusai", "japanse-meesters", "3-1-katsushika"), ("Utagawa Hiroshige|Hiroshige", "japanse-meesters", "3-2-utagawa"),
 ("Jeff Wall", "japanse-meesters", "5-2-jeff-wall"),
 ("Le Corbusier", "architectuur-en-design", "3-2-le-corbusier"), ("Tadao Ando", "architectuur-en-design", "3-3-tadao-ando"),
 ("Hugo Ball", "dada", "a-hugo-ball"), ("Hans Arp", "dada", "b-hans-arp"), ("Man Ray", "dada", "b-man-ray"), ("Hannah Höch", "dada", "b-hannah-hoch"),
 ("Raoul Hausmann", "dada", "c-raoul-hausmann"), ("George Grosz", "dada", "d-george-grosz"), ("John Heartfield", "dada", "e-john-heartfield"),
 ("Max Ernst", "dada", "a-max-ernst"), ("Kurt Schwitters|Schwitters", "dada", "b-kurt-schwitters"),
 ("Allan Kaprow|Kaprow", "performance", "allan-kaprow"), ("Joseph Beuys|Beuys", "performance", "joseph-beuys"),
 ("Joseph Kosuth|Kosuth", "conceptuele-kunst", "3-1-joseph-kosuth"), ("Marcel Broodthaers|Broodthaers", "conceptuele-kunst", "3-2-marcel-broodthaers"),
 ("Alfred Hitchcock|Hitchcock", "film", "4-3-2-alfred-hitchcock"), ("Arthur Lipsett|Lipsett", "film", "4-3-1-arthur-lipsett"),
 ("Henri Bergson|Bergson", "film", "4-4-1-henri-bergson"), ("Lynne Ramsay", "film", "4-1-2-lynne-ramsay"),
 ("John Williams", "muziek", "4-2-john-williams"), ("Richard Wagner|Wagner", "muziek", "b-wagner"), ("Eduard Hanslick|Hanslick", "muziek", "b-hanslick"),
]
BEGRIPPEN = [
 ("barok", "caravaggio", "de-barok"), ("rococo", "rococo", ""), ("neoclassicisme", "neoclassicisme", ""), ("romantiek", "romantiek", ""),
 ("modernisme", "modernisme", ""), ("impressionisme|impressionisten", "modernisme", "5-3-impressionisme"),
 ("postimpressionisme", "modernisme", "5-4-postimpressionisme"), ("abstracte kunst", "modernisme", "5-5-abstracte-kunst"),
 ("Salon des Refusés", "modernisme", "cabanel-en-manet"),
 ("dadaïsme|dada", "dada", ""), ("Cabaret Voltaire", "dada", "1-2-zurich"), ("Entartete Kunst", "dada", "1-8-entartete-kunst"),
 ("popart|pop-art", "popart", ""), ("de Factory", "popart", "4-2-de-factory"), ("The Velvet Underground", "popart", "4-3-the-velvet-underground"),
 ("conceptuele kunst", "conceptuele-kunst", ""), ("readymades|readymade", "duchamp", ""),
 ("performancekunst|performance", "performance", "2-1-wat-is-performancekunst"), ("happenings|happening", "performance", "allan-kaprow"),
 ("tijdskunst|time based art", "performance", "2-5-tijdskunst"),
 ("Bauhaus", "architectuur-en-design", "3-1-het-bauhaus"),
 ("mimesis", "ron-mueck", "1-1-mimesis"), ("hyperrealisme", "ron-mueck", "c-hyperrealisme"),
 ("iconografie|iconologie", "iconografie", "3-3-iconografie-en-iconologie"), ("personificatie", "iconografie", "a-personificatie"),
 ("allegorie", "iconografie", "b-allegorie"), ("attribuut|attributen", "iconografie", "d-attribuut"),
 ("epoché", "epoche", ""), ("ekphrasis", "epoche", "6-ekphrasis"), ("suprematisme", "epoche", "4-2-kazimir-malevich"),
 ("=aura", "walter-benjamin", "2-de-kerngedachte"), ("punctum|studium", "roland-barthes", "2-de-kerngedachte"),
 ("vreemdmaken|vreemd maken", "sjklovski", "2-de-kerngedachte"),
 ("het sublieme", "kant", "2-5-het-sublieme"), ("belangeloos welgevallen", "kant", "a-belangeloos-welgevallen"),
 ("leitmotiv", "muziek", "b-het-leitmotiv"), ("luisterwijzer", "muziek", "b-een-luisterwijzer"), ("montage", "film", "4-3-montage-en-filmtaal", ["dada"]),
 ("japonisme", "japanse-meesters", "4-japan-in-parijs"), ("vier elementen", "de-vier-elementen", ""), ("kijkwijzer", "kijkwijzer", ""),
]

# Cursieve woorden die geen titel van één werk zijn, of die al als begrip een bestemming hebben.
NIET_ALS_WERK = {"allegorie", "boeddha", "entartete kunst", "ibid", "time based art"}

CSS = """/*kruis*/
a.kruis{text-decoration:underline dotted var(--rood);text-decoration-thickness:1.5px;text-underline-offset:3px}
a.kruis:hover{text-decoration-style:solid}
a.kruis::after{content:"\\2197";font-family:var(--data);font-size:.62em;font-style:normal;color:var(--rood);margin-left:.12em;vertical-align:.35em}
@media print{a.kruis{text-decoration:none}a.kruis::after{content:""}}
/*/kruis*/"""

# De link opent als apart venster bovenop de pagina. Blokkeert de browser dat, dan opent hij gewoon in een nieuw tabblad.
JS = """<script>/*kruis*/
document.addEventListener("click",function(e){var a=e.target.closest&&e.target.closest("a.kruis");if(!a||e.ctrlKey||e.metaKey||e.shiftKey||e.button)return;
var b=Math.min(1100,screen.availWidth-60),h=Math.min(860,screen.availHeight-80),x=Math.max(0,Math.round((screen.availWidth-b)/2)),y=Math.max(0,Math.round((screen.availHeight-h)/2));
var w=null;try{w=window.open(a.href,"kijknu-verwijzing","popup=yes,width="+b+",height="+h+",left="+x+",top="+y+",scrollbars=yes,resizable=yes");}catch(f){}
if(w){e.preventDefault();try{w.focus();}catch(f){}}});
/*/kruis*/</script>"""

def plat(t):
    return html.unescape(re.sub(r"<[^>]+>", "", t)).replace("’", "'").replace("‘", "'").strip()

def kaal(t):
    """Vergelijkingsvorm: kleine letters, geen accenten, geen leestekens."""
    t = unicodedata.normalize("NFKD", plat(t)).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", t).strip()

def slugify(t):
    return re.sub(r"[^a-z0-9]+", "-", kaal(t)).strip("-")[:60]

def patroon(term):
    """Regex voor een term in de html-tekst: aanhalingstekens en spaties in al hun vormen."""
    p = re.escape(term)
    p = p.replace("'", "(?:'|’|&\\#x27;|&\\#39;)").replace("’", "(?:'|’|&\\#x27;|&\\#39;)")
    p = p.replace("\\&", "(?:&amp;|&)").replace("\\ ", "(?:\\s|&nbsp;)+")
    return p

def schoon(s):
    s = re.sub(r'<a class="kruis"[^>]*>(.*?)</a>', r"\1", s, flags=re.S)
    s = re.sub(r'(<figure class="beeld") id="beeld-[^"]*"', r"\1", s)
    s = re.sub(r"\n?<script>/\*kruis\*/.*?/\*/kruis\*/</script>", "", s, flags=re.S)
    return re.sub(r"\n?/\*kruis\*/.*?/\*/kruis\*/", "", s, flags=re.S)

# ------------------------------------------------------------------ register opbouwen
def lees():
    return {s: schoon((SITE / s / "index.html").read_text(encoding="utf-8")) for s in SLUGS if (SITE / s / "index.html").exists()}

def koppen(s):
    return [(m.start(), m.group(2), plat(m.group(3))) for m in re.finditer(r'<(h[234])[^>]*\bid="([^"]+)"[^>]*>(.*?)</\1>', s, flags=re.S)]

def werken_register(paginas):
    """titel -> (slug, anker, score). Een kop met de titel wint van een los beeld."""
    cursief = set()
    for s in paginas.values():
        for m in re.finditer(r"<i>(.*?)</i>", s, flags=re.S):
            cursief.add(kaal(m.group(1)))
    reg, fig_ids = {}, {}
    def meld(titel, slug, anker, score):
        k = kaal(titel)
        if len(k) < 3 or k in NIET_ALS_WERK: return
        if k not in reg or score > reg[k][2]: reg[k] = (slug, anker, score, plat(titel))
    for slug, s in paginas.items():
        ks = koppen(s)
        # koppen die een werk benoemen
        for pos, kid, tx in ks:
            t = re.sub(r"^(?:Oefening \d+:\s*|\d+(?:\.\d+)*\s+|[a-z]\.\s+|Kunsthistorische verwijzing:\s*)", "", tx)
            t = re.sub(r"\s*\((?:ca\. |circa )?[\d][^)]*\)\s*$", "", t)
            kandidaten = [t] + ([t.split(", ", 1)[1]] if ", " in t else []) + ([t.split(": ", 1)[0]] if ": " in t else [])
            for c in kandidaten:
                if kaal(c) in cursief: meld(c, slug, kid, 3 if c == t else 2)
        # beelden met een titel in het bijschrift
        for n, m in enumerate(re.finditer(r'<figure class="beeld">(.*?)</figure>', s, flags=re.S)):
            cap = re.search(r"<figcaption>(.*?)(?:<br|</figcaption)", m.group(1), flags=re.S)
            if not cap: continue
            ti = re.search(r"<i>(.*?)</i>", cap.group(1), flags=re.S)
            if not ti: continue
            titel = plat(ti.group(1))
            vorige = [k for k in ks if k[0] < m.start()]
            if vorige and kaal(titel) in kaal(vorige[-1][2]):
                meld(titel, slug, vorige[-1][1], 2); continue
            fid = "beeld-" + slugify(titel)
            fig_ids.setdefault(slug, {}).setdefault(m.start(), fid)
            meld(titel, slug, fid, 1)
    return reg, fig_ids

def anker(paginas, slug, stuk):
    if not stuk: return ""
    ids = [k[1] for k in koppen(paginas[slug])]
    goed = [i for i in ids if i == stuk] or [i for i in ids if i.startswith(stuk)] or [i for i in ids if stuk in i]
    if not goed: print("  ANKER NIET GEVONDEN:", slug, stuk); return ""
    return goed[0]

# ------------------------------------------------------------------ links zetten
OVERSLAAN = ("a", "h1", "h2", "h3", "h4", "h5", "h6", "script", "style", "nav", "button", "label", "textarea", "header", "footer", "dt")
GRENS_V, GRENS_N = r"(?<![\w\-À-ÿ])", r"(?![\wÀ-ÿ])"

def bouw_zoekers(paginas, reg):
    werken = []
    for k, (slug, ank, score, titel) in reg.items():
        werken.append((re.compile(r"\s*" + patroon(titel) + r"[\s.,;:]*"), slug, ank, len(titel), ()))
    tekst = []
    for termen, slug, stuk, *niet in NAMEN:
        if slug not in paginas: continue
        a = anker(paginas, slug, stuk)
        for t in termen.split("|"):
            tekst.append((re.compile(GRENS_V + patroon(t) + r"(?:(?:'|’|&\#x27;)?s)?" + GRENS_N), slug, a, len(t), tuple(niet[0]) if niet else ()))
    for termen, slug, stuk, *niet in BEGRIPPEN:
        if slug not in paginas: continue
        a = anker(paginas, slug, stuk)
        for t in termen.split("|"):
            vast = t.startswith("="); t = t.lstrip("=")
            vlag = 0 if (vast or t[0].isupper()) else re.I
            tekst.append((re.compile(GRENS_V + patroon(t) + GRENS_N, vlag), slug, a, len(t), tuple(niet[0]) if niet else ()))
    return werken, tekst

def link(doel_slug, ank, binnen):
    titel = html.escape(INFO[doel_slug][1], quote=True)
    href = f"../{doel_slug}/" + (f"#{ank}" if ank else "")
    return f'<a class="kruis" href="{href}" target="_blank" rel="noopener" title="Opent in een nieuw venster: {titel}">{binnen}</a>'

def verwerk(slug, s, werken, tekst, fig_ids):
    # ankers op losse beelden
    for pos, fid in sorted(fig_ids.get(slug, {}).items(), reverse=True):
        s = s[:pos] + f'<figure class="beeld" id="{fid}">' + s[pos + len('<figure class="beeld">'):]
    a = s.find("<main"); b = s.rfind("</main>")
    if a < 0: return s, 0
    kop, midden, staart = s[:a], s[a:b], s[b:]
    uit, diep, in_i, gezien, n, in_kader = [], 0, 0, set(), 0, False
    for stuk in re.split(r"(<[^>]+>)", midden):
        if stuk.startswith("<"):
            m = re.match(r"<(/?)([a-zA-Z0-9]+)", stuk)
            if m:
                naam, sluit = m.group(2).lower(), bool(m.group(1))
                if naam in OVERSLAAN and not stuk.endswith("/>"): diep += -1 if sluit else 1
                if 'class="sit-kader"' in stuk: in_kader = True; diep += 1
                elif in_kader and naam == "ol" and sluit: in_kader = False; diep -= 1
                if naam == "i": in_i += -1 if sluit else 1
                if naam == "h2" and not sluit: gezien = set()
            uit.append(stuk); continue
        if diep > 0 or not stuk.strip():
            uit.append(stuk); continue
        treffers = []
        # Cursief = een titel: alleen linken als de hele cursieve tekst de titel of de term is.
        for rx, dslug, ank, lengte, niet in (werken + tekst if in_i > 0 else tekst):
            if dslug == slug or slug in niet or (dslug, ank) in gezien: continue
            if in_i > 0:
                m = rx.fullmatch(stuk) or re.fullmatch(r"\s*(?:" + rx.pattern + r")[\s.,;:]*", stuk, rx.flags)
                if m: treffers.append((0, -lengte, len(stuk), dslug, ank))
                continue
            m = rx.search(stuk)
            if m: treffers.append((m.start(), -lengte, m.end(), dslug, ank))
        treffers.sort()
        gekozen, einde, doelen = [], 0, set()
        for start, _, stop, dslug, ank in treffers:
            if start < einde or (dslug, ank) in doelen: continue
            gekozen.append((start, stop, dslug, ank)); einde = stop; doelen.add((dslug, ank))
        for start, stop, dslug, ank in reversed(gekozen):
            stuk = stuk[:start] + link(dslug, ank, stuk[start:stop]) + stuk[stop:]
            gezien.add((dslug, ank)); n += 1
        uit.append(stuk)
    s = kop + "".join(uit) + staart
    if n:
        s = s.replace("</style>", "\n" + CSS + "</style>", 1)
        k = s.rfind("</body>"); s = s[:k] + JS + "\n" + s[k:]
    return s, n

def alles(toon=False):
    paginas = lees()
    reg, fig_ids = werken_register(paginas)
    werken, tekst = bouw_zoekers(paginas, reg)
    totaal, per = 0, {}
    for slug, s in paginas.items():
        nieuw, n = verwerk(slug, s, werken, tekst, fig_ids)
        (SITE / slug / "index.html").write_text(nieuw, encoding="utf-8")
        totaal += n; per[slug] = n
    print(f"kruisverwijzingen: {totaal} links op {sum(1 for v in per.values() if v)} pagina's; {len(reg)} kunstwerken, {len(NAMEN)} namen, {len(BEGRIPPEN)} begrippen in het register")
    if toon:
        for k, v in sorted(reg.items()): print("  ", v[3], "->", v[0] + "#" + v[1])
    return per

if __name__ == "__main__":
    alles("-v" in sys.argv)
