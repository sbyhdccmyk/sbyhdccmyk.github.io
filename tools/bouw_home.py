# Bouwt index.html uit de lijst ONDERWERPEN. Zet status op "online" zodra een hoofdstuk op de site staat.
import html, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from onderwerpen import ONDERWERPEN, KUNSTVORMEN
from tijdlijnen import BANDEN, REGIOS, T

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

# Het referentiekader: elke periode een rij, met de hoofdstukken en de teksten die erin thuishoren.
def vak(o):
    t = T.get(o[0], {})
    return t.get("vak", t["hoofd"][0] if t.get("hoofd") else None)

def band_html(i, naam, jaren):
    hfd = [o for o in tijd if vak(o) == i]
    tekst = [(T[o[0]]["tekstjaar"][0], o) for o in ONDERWERPEN if o[0] in T and T[o[0]].get("tekstjaar", (None, None))[1] == i]
    binnen = ""
    if hfd: binnen += '<ul class="kaarten">' + "".join(kaart(o, True) for o in hfd) + "</ul>"
    if tekst:
        binnen += '<p class="b-tekst">Geschreven in deze tijd: ' + ", ".join(
            f'<a href="{o[0]}/">{e(o[1])}</a> ({e(j)})' for j, o in sorted(tekst, key=lambda x: x[0])) + "</p>"
    if not binnen: binnen = '<p class="b-leeg">Hier staat nog geen hoofdstuk.</p>'
    return (f'<li class="band{"" if (hfd or tekst) else " leeg"}"><div class="b-kop"><span class="b-naam">{e(naam)}</span>'
            f'<span class="b-jaar">{e(jaren)}</span></div><div class="b-inhoud">{binnen}</div></li>')

kader_html = "".join(band_html(i, n, j) for i, (n, j) in enumerate(BANDEN))

# Over de wereld: dezelfde hoofdstukken, gesorteerd volgens de plaats waar de kunst ontstond.
wereld_html = "".join(
  f'<div class="vorm"><h3>{e(naam)}</h3><ul>{"".join(lijn(o) for o in ONDERWERPEN if o[0] in T and code in T[o[0]]["regio"])}</ul></div>'
  for code, naam in REGIOS if any(o[0] in T and code in T[o[0]]["regio"] for o in ONDERWERPEN))

vormen_html = "".join(
  f'<div class="vorm"><h3>{e(naam)}</h3><ul>{"".join(lijn(o) for o in ONDERWERPEN if code in o[6])}</ul></div>'
  for code,naam in KUNSTVORMEN)

pagina = f'''<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>KIJK NU!</title>
<meta name="description" content="Leren kijken en luisteren naar kunst: een kijkwijzer, een tijdlijn van de Oudheid tot vandaag, kunst uit verschillende samenlevingen, kunstvormen en kunstfilosofie.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Carlito:ital,wght@0,400;0,700;1,400&family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{{
  /* Atelier: een donkere aanhef rond Courbet, daarna de witte zaal van de hoofdstukken. Eén warm accent. */
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

/* Aanhef: titel links in het donker, Courbet rechts, zijn blik vrij. */
.aanhef{{position:relative;background:var(--nacht);color:var(--was);display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.25fr);min-height:min(40rem,84vh);overflow:hidden}}
.aanhef-beeld{{position:relative;grid-column:2;grid-row:1;min-height:100%}}
.aanhef-beeld img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 42%}}
.aanhef-beeld::before{{content:"";position:absolute;inset:0;z-index:1;background:linear-gradient(90deg,var(--nacht) 0%,rgba(13,10,7,.55) 14%,rgba(13,10,7,0) 34%),linear-gradient(0deg,rgba(13,10,7,.55) 0%,rgba(13,10,7,0) 22%)}}
.aanhef-tekst{{grid-column:1;grid-row:1;align-self:end;position:relative;z-index:2;padding:6rem 1.5rem 3rem max(1.5rem,calc((100vw - 72rem)/2 + 1.5rem))}}
.aanhef .eyebrow{{font-family:var(--data);font-size:.75rem;letter-spacing:.08em;text-transform:uppercase;color:var(--vlam);margin:0 0 1rem}}
.aanhef h1{{font-family:var(--display);font-weight:600;font-size:clamp(3.2rem,8vw,6.2rem);line-height:.95;margin:0 0 1.2rem;max-width:10ch;text-wrap:balance}}
.aanhef .intro{{max-width:30rem;font-size:1.2rem;color:var(--was);margin:0 0 2rem}}
.aanhef .bijschrift{{font-size:.85rem;color:rgba(243,230,204,.72);margin:0;max-width:30rem}}
.aanhef .bijschrift i{{color:var(--was)}}

/* Vier deuren */
.deuren{{width:calc(100% - 3rem);max-width:69rem;margin:0 auto;display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:1px;background:var(--lijn);border:1px solid var(--lijn);transform:translateY(-1.5rem);position:relative;z-index:2}}
.deur{{background:var(--wand);padding:1.3rem 1.2rem 1.4rem;text-decoration:none;display:flex;flex-direction:column;gap:.35rem}}
.deur:hover{{background:#fbf6ec}}
.deur .nr{{font-family:var(--data);font-size:.72rem;color:var(--rood)}}
.deur .d-titel{{font-family:var(--display);font-weight:600;font-size:1.5rem;line-height:1.05}}
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

/* Referentiekader */
ol.kader{{list-style:none;margin:0;padding:0}}
.band{{display:grid;grid-template-columns:minmax(0,13rem) minmax(0,1fr);gap:1.5rem;padding:1rem 0 1.2rem;border-top:1px solid var(--lijn)}}
.band:last-child{{border-bottom:1px solid var(--lijn)}}
.b-kop{{display:flex;flex-direction:column;gap:.15rem;border-left:4px solid var(--vlam);padding-left:.8rem;align-self:start}}
.band.leeg .b-kop{{border-left-color:var(--lijn)}}
.b-naam{{font-family:var(--display);font-weight:600;font-size:1.45rem;line-height:1.05}}
.b-jaar{{font-family:var(--data);font-size:.75rem;color:var(--rood);font-variant-numeric:tabular-nums}}
.band.leeg{{padding:.6rem 0 .7rem}}
.band.leeg .b-naam{{color:var(--zacht);font-size:1.2rem}}
.band.leeg .b-jaar{{color:var(--zacht)}}
.b-leeg{{margin:0;color:var(--zacht);font-size:.95rem;align-self:center}}
.b-tekst{{margin:.7rem 0 0;font-size:1rem;color:var(--zacht)}}
.b-inhoud > .b-tekst:first-child{{margin-top:.2rem}}
.b-tekst a{{color:var(--inkt);font-weight:700;text-decoration-color:var(--vlam);text-underline-offset:3px}}

/* Kunstvormen */
.vormen{{display:grid;grid-template-columns:repeat(auto-fill,minmax(14rem,1fr));gap:1.5rem 2rem}}
.vorm h3{{font-size:1.05rem;margin:0 0 .4rem;padding-bottom:.3rem;border-bottom:1px solid var(--lijn)}}
.vorm ul{{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:.25rem;font-size:1rem}}
.vorm a{{font-weight:700;text-decoration-color:var(--vlam);text-underline-offset:3px}}
.later-tekst{{color:var(--zacht)}}

footer{{border-top:1px solid var(--inkt);margin-top:5rem;padding-top:1rem;font-size:.9rem;color:var(--zacht);display:flex;flex-wrap:wrap;gap:.5rem 2rem;justify-content:space-between}}

@media (max-width:56rem){{
  .aanhef{{grid-template-columns:minmax(0,1fr);min-height:0}}
  .aanhef-beeld{{grid-column:1;grid-row:1;aspect-ratio:1500/1228;min-height:0}}
  .aanhef-beeld::before{{background:linear-gradient(0deg,var(--nacht) 0%,rgba(13,10,7,0) 30%)}}
  .aanhef-tekst{{grid-row:2;padding:1rem 1.5rem 3rem}}
  .deuren{{grid-template-columns:repeat(2,minmax(0,1fr))}}
  .band{{grid-template-columns:minmax(0,1fr);gap:.7rem}}
  .kop{{grid-template-columns:minmax(0,1fr);gap:.6rem}}
}}
@media (max-width:34rem){{
  .deuren{{grid-template-columns:minmax(0,1fr);transform:none;margin-top:1rem}}
}}
</style>
</head>
<body>

<header class="aanhef">
  <div class="aanhef-beeld">
    <img src="https://upload.wikimedia.org/wikipedia/commons/8/8f/Gustave_Courbet_-_Le_D%C3%A9sesp%C3%A9r%C3%A9_%281843%29.jpg"
         srcset="https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Gustave_Courbet_-_Le_D%C3%A9sesp%C3%A9r%C3%A9_%281843%29.jpg/960px-Gustave_Courbet_-_Le_D%C3%A9sesp%C3%A9r%C3%A9_%281843%29.jpg 960w, https://upload.wikimedia.org/wikipedia/commons/8/8f/Gustave_Courbet_-_Le_D%C3%A9sesp%C3%A9r%C3%A9_%281843%29.jpg 1500w"
         sizes="(max-width: 56rem) 100vw, 56vw" alt="Een jonge man met wilde, donkere haren kijkt met wijd open ogen recht naar de kijker. Hij grijpt met beide handen in zijn haar.">
  </div>
  <div class="aanhef-tekst">
    <p class="eyebrow">Leren kijken naar kunst</p>
    <h1>KIJK NU!</h1>
    <p class="intro">Eerst kijk en luister je, lang genoeg om iets te ervaren. Dan leer je benoemen wat je ziet: hoe een werk gemaakt is, waarover het gaat, waarvoor het diende, in welke tijd en welke samenleving het ontstond. Zo merk je dat één werk meer dan één betekenis draagt, en vind je de woorden voor wat het voor jou betekent.</p>
    <p class="bijschrift">Gustave Courbet, <i>Le Désespéré</i> (1843-1845). Privécollectie. Publiek domein, afbeelding via <a href="https://commons.wikimedia.org/wiki/File:Gustave_Courbet_-_Le_D%C3%A9sesp%C3%A9r%C3%A9_(1843).jpg">Wikimedia Commons</a>.</p>
  </div>
</header>

<nav class="deuren" aria-label="Vijf ingangen">
  <a class="deur" href="#kijken"><span class="nr">01</span><span class="d-titel">Leren kijken</span><span class="d-tekst">Vorm, inhoud, functie en context van elk kunstwerk</span></a>
  <a class="deur" href="#tijd"><span class="nr">02</span><span class="d-titel">Door de tijd</span><span class="d-tekst">Elk onderwerp op zijn plaats in de tijdlijn</span></a>
  <a class="deur" href="#wereld"><span class="nr">03</span><span class="d-titel">Over de wereld</span><span class="d-tekst">Kunst uit verschillende samenlevingen</span></a>
  <a class="deur" href="#vormen"><span class="nr">04</span><span class="d-titel">Kunstvormen</span><span class="d-tekst">Beeld, gebouw, foto, film, performance en muziek</span></a>
  <a class="deur" href="#denken"><span class="nr">05</span><span class="d-titel">Denken over kunst</span><span class="d-tekst">Meer dan één blik, en je eigen oordeel</span></a>
</nav>

<main>
<section id="kijken">
  <div class="kop"><div><span class="nr">01</span><h2>Leren kijken</h2></div>
  <p>Begin hier. De kijkwijzer en deze hoofdstukken geven je de woorden om te zeggen hoe een werk gemaakt is, waarover het gaat en waarvoor het diende, bij elk kunstwerk, oud of nieuw.</p></div>
  <ul class="kaarten">{"".join(kaart(o) for o in kijken)}</ul>
</section>

<section id="tijd">
  <div class="kop"><div><span class="nr">02</span><h2>Door de tijd</h2></div>
  <p>Elk hoofdstuk heeft zijn vak in de tijd. De periodes zijn die van de westerse kunstgeschiedenis; wat van elders komt, staat erbij op het moment waarop het ontstond. In elk hoofdstuk vind je bovenaan een tijdlijn met de werken en met wat er toen in de wereld gebeurde.</p></div>
  <ol class="kader">{kader_html}</ol>
</section>

<section id="wereld">
  <div class="kop"><div><span class="nr">03</span><h2>Over de wereld</h2></div>
  <p>Kunst hangt vast aan de plaats en de samenleving waar ze ontstaat. Hier staan de onderwerpen volgens die plaats. De meeste vertrekken nog vanuit Europa; een hoofdstuk dat tussen twee plaatsen reist, staat bij allebei.</p></div>
  <div class="vormen">{wereld_html}</div>
</section>

<section id="vormen">
  <div class="kop"><div><span class="nr">04</span><h2>Kunstvormen</h2></div>
  <p>Dezelfde onderwerpen, gesorteerd volgens het medium. Elke kunstvorm heeft eigen bouwstenen, materialen en technieken: een foto lees je anders dan een gebouw of een muziekstuk.</p></div>
  <div class="vormen">{vormen_html}</div>
</section>

<section id="denken">
  <div class="kop"><div><span class="nr">05</span><h2>Denken over kunst</h2></div>
  <p>Eén werk, meer dan één lezing. Elke denker geeft je een ander standpunt om naar hetzelfde te kijken, telkens toegepast op twee kunstwerken. Zo leer je ook je eigen oordeel onderbouwen.</p></div>
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
