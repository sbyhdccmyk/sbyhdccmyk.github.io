# Bouwt index.html uit de lijst ONDERWERPEN. Zet status op "online" zodra een hoofdstuk op de site staat.
import html, pathlib

ONDERWERPEN = [
 # slug, titel, ondertitel, deuren, jaar (voor de tijdlijn), periode-tekst, kunstvormen, status
 ("de-vier-elementen","De vier elementen","Tijd, ruimte, lichaam en object: een manier van kijken die bij elk kunstwerk werkt",["kijken"],None,"",[],"later"),
 ("epoche","De epoché en de ekphrasis","Je eerste oordeel uitstellen en in woorden vatten wat je ziet",["kijken"],None,"",["schilderkunst"],"later"),
 ("iconografie","Iconografie en iconologie","Betekenis lezen in een kunstwerk met het stappenplan van Panofsky",["kijken"],None,"",["schilderkunst"],"later"),

 ("caravaggio","Caravaggio en de barok","Licht, donker en de rauwe werkelijkheid",["tijd"],1600,"ca. 1600",["schilderkunst"],"later"),
 ("rococo","Rococo","Watteau en Fragonard: spel, verleiding en melancholie",["tijd"],1715,"1715-1780",["schilderkunst"],"later"),
 ("neoclassicisme","Neoclassicisme","David en Ingres: terug naar de Oudheid",["tijd"],1780,"1780-1830",["schilderkunst"],"later"),
 ("romantiek","Romantiek","Friedrich en Géricault: gevoel, natuur en drama",["tijd"],1800,"1800-1840",["schilderkunst"],"later"),
 ("modernisme","Modernisme","Van het realisme en Manet over het impressionisme tot de abstracte kunst",["tijd"],1850,"1850-1915",["schilderkunst"],"later"),
 ("duchamp","Marcel Duchamp","De readymade: een voorwerp wordt kunst",["tijd","denken"],1913,"vanaf 1913",["beeldhouwkunst"],"later"),
 ("dada","Dada","Een houding, geen stijl: van Zürich tot Parijs",["tijd"],1916,"1916-1924",["schilderkunst","performance"],"later"),
 ("architectuur-en-design","Architectuur en design","Het Bauhaus, Le Corbusier en Tadao Ando",["tijd"],1919,"vanaf 1919",["architectuur"],"later"),
 ("popart","Popart","Andy Warhol, de Factory en The Velvet Underground",["tijd"],1955,"1955-1970",["schilderkunst","muziek"],"later"),
 ("conceptuele-kunst","Conceptuele kunst","Het idee als kunstwerk: Joseph Kosuth en Marcel Broodthaers",["tijd"],1965,"vanaf 1965",["beeldhouwkunst"],"later"),
 ("performance","Performance als tijdskunst","Marina Abramović en Ulay",["tijd"],1970,"vanaf 1970",["performance"],"later"),
 ("rineke-dijkstra","Rineke Dijkstra, het portret","Fotografie, lichaam, blik en het tussenmoment",["tijd"],1991,"1991-2006",["fotografie","film"],"online"),
 ("ron-mueck","Ron Mueck en mimesis","Mensfiguren van huid en haar, op de verkeerde schaal",["tijd"],1996,"vanaf 1996",["beeldhouwkunst"],"later"),
 ("film","Film als tijdskunst","Montage en filmtaal, aan de hand van de kortfilm Swimmer",["tijd"],2012,"2012",["film"],"later"),
 ("anouk-de-clercq","Anouk De Clercq","Love that Moves the Sun: een video-installatie om in te wandelen",["tijd"],2026,"2026",["film"],"later"),
 ("muziek","Muziek: luisteren naar tijd","Hoe je naar muziek luistert, van de voorouders van de filmmuziek tot John Williams",[],None,"",["muziek"],"later"),

 ("kant","Immanuel Kant","Het schone, het aangename en het sublieme",["denken"],None,"",[],"later"),
 ("sjklovski","Viktor Sjklovski","De kunst van het vreemdmaken",["denken","kijken"],None,"",["schilderkunst"],"later"),
 ("walter-benjamin","Walter Benjamin","Het aura en de kopie: kunst in het tijdperk van de reproductie",["denken"],None,"",["fotografie"],"later"),
 ("susan-sontag","Susan Sontag","Tegen de interpretatie: kijken naar wat er is",["denken"],None,"",["schilderkunst"],"later"),
 ("roland-barthes","Roland Barthes","Studium en punctum: wat een foto met je doet",["denken"],None,"",["fotografie"],"later"),
 ("arthur-danto","Arthur Danto","De kunstwereld: wat maakt een voorwerp tot kunst?",["denken"],None,"",[],"later"),
 ("gilles-deleuze","Gilles Deleuze","De scheppende daad als verzet",["denken"],None,"",["schilderkunst"],"later"),
 ("tanizaki","Junichiro Tanizaki","Lof der schaduw: schoonheid in het halfdonker",["denken"],None,"",["schilderkunst"],"later"),
]

KUNSTVORMEN = [("schilderkunst","Schilderkunst"),("beeldhouwkunst","Beeldhouwkunst en objecten"),("fotografie","Fotografie"),
               ("performance","Performance"),("film","Film en video"),("architectuur","Architectuur en design"),("muziek","Muziek")]

e = html.escape
def kaart(o, met_periode=False):
    slug,titel,onder,_,_,periode,_,status = o
    meta = f'<span class="periode">{e(periode)}</span>' if (met_periode and periode) else ''
    if status == "online":
        return f'<li><a class="kaart" href="{slug}/">{meta}<span class="k-titel">{e(titel)}</span><span class="k-onder">{e(onder)}</span><span class="k-ga">Lees het hoofdstuk</span></a></li>'
    return f'<li><div class="kaart later" aria-disabled="true">{meta}<span class="k-titel">{e(titel)}</span><span class="k-onder">{e(onder)}</span><span class="k-ga">Binnenkort online</span></div></li>'

def lijn(o):
    slug,titel,_,_,_,_,_,status = o
    return f'<li><a href="{slug}/">{e(titel)}</a></li>' if status=="online" else f'<li><span class="later-tekst">{e(titel)}</span></li>'

kijken = [o for o in ONDERWERPEN if "kijken" in o[3]]
tijd = sorted([o for o in ONDERWERPEN if "tijd" in o[3]], key=lambda o:o[4])
denken = [o for o in ONDERWERPEN if "denken" in o[3]]
n_online = sum(o[7]=="online" for o in ONDERWERPEN)

vormen_html = "".join(
  f'<div class="vorm"><h3>{e(naam)}</h3><ul>{"".join(lijn(o) for o in ONDERWERPEN if code in o[6])}</ul></div>'
  for code,naam in KUNSTVORMEN)

pagina = f'''<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Kunst bekijken</title>
<meta name="description" content="Leren kijken naar kunst: methodes, kunstgeschiedenis van Caravaggio tot nu, kunstvormen en kunstfilosofie.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Carlito:ital,wght@0,400;0,700;1,400&family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{{
  /* Kaarslicht: een donkere aanhef rond De La Tour, daarna de witte zaal van de hoofdstukken. Eén warm accent. */
  --nacht:#0d0a07;
  --was:#f3e6cc;
  --vlam:#e0a248;
  --wand:#ffffff;
  --inkt:#141414;
  --zacht:#5f5f5f;
  --kader:#f2f2f2;
  --lijn:#bfbfbf;
  --rood:#c8102e;
  --display:"Cormorant Garamond","Georgia",serif;
  --tekst:"Carlito","Calibri","Segoe UI",Arial,sans-serif;
  --data:"IBM Plex Mono","Consolas","Courier New",monospace;
  color-scheme:light;
}}
*{{box-sizing:border-box}}
html{{scroll-behavior:smooth}}
@media (prefers-reduced-motion:reduce){{html{{scroll-behavior:auto}}}}
body{{margin:0;background:var(--wand);color:var(--inkt);font-family:var(--tekst);font-size:1.125rem;line-height:1.55}}
a{{color:inherit}}
a:focus-visible{{outline:2px solid var(--vlam);outline-offset:3px}}

/* Aanhef */
.aanhef{{position:relative;background:var(--nacht);color:var(--was);overflow:hidden;min-height:min(46rem,88vh);display:grid;align-items:end}}
.aanhef img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:68% 38%}}
.aanhef::after{{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(13,10,7,.94) 0%,rgba(13,10,7,.78) 34%,rgba(13,10,7,.15) 68%,rgba(13,10,7,0) 100%),linear-gradient(0deg,rgba(13,10,7,.85) 0%,rgba(13,10,7,0) 40%)}}
.aanhef-tekst{{position:relative;z-index:1;max-width:72rem;width:100%;margin:0 auto;padding:6rem 1.5rem 2.5rem}}
.aanhef .eyebrow{{font-family:var(--data);font-size:.75rem;letter-spacing:.08em;text-transform:uppercase;color:var(--vlam);margin:0 0 1rem}}
.aanhef h1{{font-family:var(--display);font-weight:600;font-size:clamp(3.2rem,9vw,6.5rem);line-height:.95;margin:0 0 1.2rem;max-width:12ch;text-wrap:balance}}
.aanhef .intro{{max-width:34rem;font-size:1.2rem;color:var(--was);margin:0 0 2rem}}
.aanhef .bijschrift{{font-size:.85rem;color:rgba(243,230,204,.72);margin:0;max-width:34rem}}
.aanhef .bijschrift i{{color:var(--was)}}

/* Vier deuren */
.deuren{{width:calc(100% - 3rem);max-width:69rem;margin:0 auto;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:1px;background:var(--lijn);border:1px solid var(--lijn);transform:translateY(-1.5rem);position:relative;z-index:2}}
.deur{{background:var(--wand);padding:1.3rem 1.2rem 1.4rem;text-decoration:none;display:flex;flex-direction:column;gap:.35rem}}
.deur:hover{{background:#fbf6ec}}
.deur .nr{{font-family:var(--data);font-size:.72rem;color:var(--rood)}}
.deur .d-titel{{font-family:var(--display);font-weight:600;font-size:1.65rem;line-height:1.05}}
.deur .d-tekst{{font-size:.98rem;color:var(--zacht);line-height:1.4}}

main{{max-width:72rem;margin:0 auto;padding:1.5rem 1.5rem 5rem}}
section{{margin-top:4.5rem;scroll-margin-top:1.5rem}}
.kop{{display:grid;grid-template-columns:minmax(0,18rem) minmax(0,1fr);gap:2rem;border-top:1px solid var(--inkt);padding-top:1rem;margin-bottom:1.6rem}}
.kop .nr{{font-family:var(--data);font-size:.75rem;color:var(--rood);display:block;margin-bottom:.3rem}}
h2{{font-family:var(--display);font-weight:600;font-size:2.4rem;line-height:1;margin:0;text-wrap:balance}}
.kop p{{margin:.2rem 0 0;color:var(--zacht);max-width:40rem}}

ul.kaarten{{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(16rem,1fr));gap:.9rem}}
.kaart{{display:flex;flex-direction:column;gap:.3rem;height:100%;padding:1rem 1.1rem 1.1rem;border:1px solid var(--lijn);background:var(--wand);text-decoration:none}}
a.kaart{{border-color:var(--inkt);border-left:4px solid var(--vlam)}}
a.kaart:hover{{background:#fbf6ec}}
.kaart.later{{background:var(--kader);color:var(--zacht)}}
.k-titel{{font-weight:700;font-size:1.15rem;line-height:1.25;color:var(--inkt)}}
.later .k-titel{{color:#3a3a3a}}
.k-onder{{font-size:.98rem;line-height:1.4}}
.k-ga{{margin-top:auto;padding-top:.6rem;font-family:var(--data);font-size:.7rem;letter-spacing:.05em;text-transform:uppercase}}
a.kaart .k-ga{{color:var(--rood)}}
a.kaart .k-ga::after{{content:" \\2192"}}
.periode{{font-family:var(--data);font-size:.72rem;color:var(--rood)}}

/* Tijdlijn */
ol.tijdlijn{{list-style:none;margin:0;padding:0;border-left:2px solid var(--inkt);margin-left:6.5rem}}
ol.tijdlijn li{{position:relative;padding:0 0 .9rem 1.4rem}}
ol.tijdlijn li::before{{content:"";position:absolute;left:-.42rem;top:1.15rem;width:.7rem;height:.7rem;border-radius:50%;background:var(--wand);border:2px solid var(--inkt)}}
ol.tijdlijn li.on::before{{background:var(--vlam);border-color:var(--vlam)}}
ol.tijdlijn .jaar{{position:absolute;left:-6.5rem;top:.9rem;width:5.6rem;text-align:right;font-family:var(--data);font-size:.8rem;font-variant-numeric:tabular-nums}}
ol.tijdlijn .kaart{{max-width:40rem}}

/* Kunstvormen */
.vormen{{display:grid;grid-template-columns:repeat(auto-fill,minmax(14rem,1fr));gap:1.5rem 2rem}}
.vorm h3{{font-size:1.05rem;margin:0 0 .4rem;padding-bottom:.3rem;border-bottom:1px solid var(--lijn)}}
.vorm ul{{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:.25rem;font-size:1rem}}
.vorm a{{font-weight:700;text-decoration-color:var(--vlam);text-underline-offset:3px}}
.later-tekst{{color:var(--zacht)}}

footer{{border-top:1px solid var(--inkt);margin-top:5rem;padding-top:1rem;font-size:.9rem;color:var(--zacht);display:flex;flex-wrap:wrap;gap:.5rem 2rem;justify-content:space-between}}

@media (max-width:56rem){{
  .deuren{{grid-template-columns:repeat(2,minmax(0,1fr))}}
  .kop{{grid-template-columns:minmax(0,1fr);gap:.6rem}}
}}
@media (max-width:34rem){{
  .aanhef img{{object-position:72% 30%}}
  .aanhef::after{{background:linear-gradient(0deg,rgba(13,10,7,.96) 0%,rgba(13,10,7,.8) 45%,rgba(13,10,7,.2) 80%)}}
  .deuren{{grid-template-columns:minmax(0,1fr);transform:none;margin-top:1rem}}
  ol.tijdlijn{{margin-left:.4rem}}
  ol.tijdlijn .jaar{{position:static;display:block;width:auto;text-align:left;margin-bottom:.2rem}}
  ol.tijdlijn li::before{{top:.35rem}}
}}
</style>
</head>
<body>

<header class="aanhef">
  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/The_Penitent_Magdalen_MET_DT7252.jpg/1920px-The_Penitent_Magdalen_MET_DT7252.jpg"
       srcset="https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/The_Penitent_Magdalen_MET_DT7252.jpg/960px-The_Penitent_Magdalen_MET_DT7252.jpg 960w, https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/The_Penitent_Magdalen_MET_DT7252.jpg/1920px-The_Penitent_Magdalen_MET_DT7252.jpg 1920w"
       sizes="100vw" alt="Een vrouw zit in het donker, het hoofd in de hand, en kijkt naar een kaars die weerspiegelt in een spiegel. Op haar schoot ligt een schedel.">
  <div class="aanhef-tekst">
    <p class="eyebrow">Leren kijken naar kunst</p>
    <h1>Kunst bekijken</h1>
    <p class="intro">Van Caravaggio tot nu: hoe je naar een kunstwerk kijkt, wat er in de kunstgeschiedenis gebeurde, en wat filosofen over kunst dachten. Voor iedereen die meer wil zien.</p>
    <p class="bijschrift">Georges de La Tour, <i>De boetvaardige Magdalena</i> (ca. 1640). The Metropolitan Museum of Art, New York. Publiek domein. <a href="https://www.metmuseum.org/art/collection/search/436839">Bekijk het werk bij het museum</a>.</p>
  </div>
</header>

<nav class="deuren" aria-label="Vier ingangen">
  <a class="deur" href="#kijken"><span class="nr">01</span><span class="d-titel">Leren kijken</span><span class="d-tekst">Methodes om elk kunstwerk te benaderen</span></a>
  <a class="deur" href="#tijd"><span class="nr">02</span><span class="d-titel">Door de tijd</span><span class="d-tekst">Van de barok tot de kunst van vandaag</span></a>
  <a class="deur" href="#vormen"><span class="nr">03</span><span class="d-titel">Kunstvormen</span><span class="d-tekst">Schilderkunst, foto, film, performance en meer</span></a>
  <a class="deur" href="#denken"><span class="nr">04</span><span class="d-titel">Denken over kunst</span><span class="d-tekst">Wat filosofen en schrijvers over kunst zeiden</span></a>
</nav>

<main>
<section id="kijken">
  <div class="kop"><div><span class="nr">01</span><h2>Leren kijken</h2></div>
  <p>Begin hier. Deze hoofdstukken geven je een manier van kijken die je bij elk kunstwerk kan gebruiken, oud of nieuw.</p></div>
  <ul class="kaarten">{"".join(kaart(o) for o in kijken)}</ul>
</section>

<section id="tijd">
  <div class="kop"><div><span class="nr">02</span><h2>Door de tijd</h2></div>
  <p>Stromingen en kunstenaars in de volgorde waarin ze verschenen, van de schilders van het licht rond 1600 tot een video-installatie van vandaag.</p></div>
  <ol class="tijdlijn">{"".join(f'<li class="{"on" if o[7]=="online" else ""}"><span class="jaar">{e(o[5])}</span>{kaart(o).removeprefix("<li>").removesuffix("</li>")}</li>' for o in tijd)}</ol>
</section>

<section id="vormen">
  <div class="kop"><div><span class="nr">03</span><h2>Kunstvormen</h2></div>
  <p>Dezelfde onderwerpen, gesorteerd volgens het medium. Handig als je wil weten hoe fotografie, film of performance werkt.</p></div>
  <div class="vormen">{vormen_html}</div>
</section>

<section id="denken">
  <div class="kop"><div><span class="nr">04</span><h2>Denken over kunst</h2></div>
  <p>Korte inleidingen op een denker of een tekst, telkens toegepast op twee kunstwerken.</p></div>
  <ul class="kaarten">{"".join(kaart(o) for o in denken)}</ul>
</section>

<footer>
  <p>Samengesteld door Sammy Ben Yakoub. {n_online} van {len(ONDERWERPEN)} hoofdstukken staan online, de rest volgt.</p>
  <p>De kunstwerken bekijk je via links naar de musea die ze bewaren.</p>
</footer>
</main>
</body>
</html>
'''
pathlib.Path(__file__).resolve().parent.parent.joinpath("index.html").write_text(pagina, encoding="utf-8")
print("index.html gebouwd:", n_online, "online van", len(ONDERWERPEN))
