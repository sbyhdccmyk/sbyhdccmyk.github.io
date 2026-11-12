# Bouwt de pagina Kijkwijzer: acht stappen om een kunstwerk te analyseren, te interpreteren en te beoordelen.
import html, pathlib, sys
HIER = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HIER))
E = html.escape
CSS = (HIER / "hoofdstuk.css").read_text(encoding="utf-8")

STAPPEN = [
 ("ervaren", "Ervaren", "Neem de tijd. Kijk of luister minstens een minuut voor je iets opschrijft.",
  ["Wat valt je het eerst op?", "Wat doet het werk met je: trekt het je aan, stoot het je af, laat het je koud?",
   "Schrijf je eerste indruk op in één zin. In stap 8 kom je erop terug."],
  [("../epoche/", "De epoché: je eerste oordeel uitstellen")]),
 ("vormgeving", "Vormgeving", "Hoe is het gemaakt?",
  ["Welke kunstvorm is het, met welk materiaal en welke techniek?", "Hoe groot is het, of hoe lang duurt het?",
   "Welke bouwstenen gebruikt de maker? Bij beeld: lijn, kleur, licht, vorm, ruimte, compositie. Bij muziek: ritme, melodie, klankkleur, dynamiek. Bij film: kader, montage, geluid.",
   "Wat is opvallend fijn of opvallend ruw gemaakt?"],
  [("../de-vier-elementen/", "De vier elementen: tijd, ruimte, lichaam en object"), ("../film/", "Filmtaal"), ("../muziek/", "Luisteren naar muziek")]),
 ("inhoud", "Inhoud", "Waarover gaat het?",
  ["Wat is er te zien of te horen: figuren, voorwerpen, een handeling?", "Is er een verhaal, een thema of een idee?",
   "Uit welke bron komt het: de Bijbel, een mythe, de geschiedenis, het dagelijks leven?", "Welke tekens of symbolen herken je?"],
  [("../iconografie/", "Iconografie en iconologie: betekenis lezen")]),
 ("functie", "Functie", "Waarvoor diende het?",
  ["Voor wie en voor welke plek is het gemaakt?", "Wil het behagen, versieren, vertellen, herinneren, overtuigen, verkopen, aanklagen, schokken of doen nadenken?",
   "Speelt het vandaag nog dezelfde rol als toen?"], []),
 ("context", "Context", "Waar en wanneer?",
  ["In welke periode of stroming hoort het thuis? Aan welke kenmerken zie je dat?", "In welke samenleving ontstond het, en wat gebeurde daar toen?",
   "Wie was de maker? Wie bestelde of betaalde het werk?", "Welke techniek of uitvinding maakte het mogelijk?"],
  [("../#tijd", "Het referentiekader: door de tijd"), ("../#wereld", "Over de wereld")]),
 ("samenhang", "Samenhang", "Leg de vorige stappen naast elkaar.",
  ["Hoe helpt de vormgeving de inhoud?", "Hoe verklaart de context de vorm of de functie?",
   "Welk kenmerk is zo belangrijk dat het werk zonder dat kenmerk een ander werk zou zijn?"], []),
 ("blikken", "Andere blikken", "Jij bent niet de enige die kijkt.",
  ["Hoe keek iemand uit de tijd van de maker naar dit werk?", "Hoe kijkt de opdrachtgever, een gelovige, een criticus, iemand uit een andere cultuur of van een andere generatie?",
   "Welke lezing van het werk botst met de jouwe?"],
  [("../#denken", "Denken over kunst")]),
 ("oordeel", "Jouw oordeel", "Een oordeel heeft drie lagen: gevoel, kennis en waarde.",
  ["Gevoel: wat deed het werk met jou?", "Kennis: wat weet je nu dat je bij stap 1 nog niet wist?",
   "Waarde: is je eerste indruk veranderd? Wat vind je er nu van, en met welke argumenten uit stap 2 tot 7 onderbouw je dat?"],
  [("../kant/", "Immanuel Kant: het schone en het aangename")]),
]
ONDERZOEK = [
 "Kies een werk en verken het met de kijkwijzer.",
 "Schrijf één vraag op die je na de acht stappen nog niet kan beantwoorden.",
 "Beslis hoe je het antwoord zoekt: in het werk zelf, op de pagina van het museum, in een boek, in een interview met de maker.",
 "Verzamel wat je vindt en noteer telkens je bron.",
 "Vergelijk wat de bronnen zeggen met wat je zelf zag of hoorde.",
 "Formuleer je antwoord, en zeg ook wat je niet te weten kwam.",
 "Toon het resultaat: een tekst, een presentatie, een poster of een playlist.",
]

def bouw(volgende=None):
    nav = "".join(f'<li><a href="#{s}">{i} {E(t)}</a></li>' for i, (s, t, *_ ) in enumerate(STAPPEN, 1)) + '<li><a href="#onderzoek">Zelf op onderzoek</a></li>'
    stappen = ""
    for i, (sid, titel, lead, vragen, links) in enumerate(STAPPEN, 1):
        meer = ""
        if links:
            meer = '<p class="meer">Lees verder: ' + ", ".join(f'<a href="{u}">{E(t)}</a>' for u, t in links) + ".</p>"
        stappen += (f'<section id="{sid}" class="stap"><h2><span class="nr">{i}</span>{E(titel)}</h2><p class="lead">{E(lead)}</p>'
                    '<ul class="vraaglijst">' + "".join(f"<li>{E(v)}</li>" for v in vragen) + "</ul>"
                    f'<label for="n-{sid}">Jouw notities bij stap {i}</label><textarea id="n-{sid}" data-veld="{sid}" rows="4"></textarea>{meer}</section>')
    buren = ""
    if volgende:
        buren = (f'<nav class="hoofdstuk-nav" aria-label="Vorig en volgend onderwerp"><span></span>'
                 f'<a href="../{volgende[0]}/" style="text-align:right"><span>Volgend onderwerp</span>{E(volgende[1])} &rarr;</a></nav>')
    pagina = f'''<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Kijkwijzer</title>
<meta name="description" content="Acht stappen die je bij elk kunstwerk kan zetten, van de eerste indruk tot je eigen oordeel.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Carlito:ital,wght@0,400;0,700;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>{CSS}
.hoofdstuk-nav{{display:flex;flex-wrap:wrap;justify-content:space-between;gap:1rem;margin-top:4rem;padding-top:1rem;border-top:1px solid var(--inkt)}}
.hoofdstuk-nav a{{text-decoration:none;font-weight:700}}
.hoofdstuk-nav span{{display:block;font-family:var(--data);font-size:.7rem;letter-spacing:.05em;text-transform:uppercase;color:var(--zacht);font-weight:400}}
.stap h2{{display:flex;gap:.8rem;align-items:baseline;margin-top:3.2rem}}
.stap h2 .nr{{font-family:var(--data);font-size:1rem;font-weight:500;color:var(--rood)}}
.lead{{font-style:italic;color:var(--zacht);font-size:1.2rem}}
ul.vraaglijst{{margin:0 0 1.1rem;padding-left:1.2rem}}
ul.vraaglijst li{{margin-bottom:.35rem}}
.werkveld{{display:grid;grid-template-columns:repeat(auto-fit,minmax(12rem,1fr));gap:.8rem;margin:1.5rem 0 0;padding:1rem 1.1rem;background:var(--kader);border:1px solid var(--lijn)}}
label{{display:block;font-family:var(--data);font-size:.7rem;letter-spacing:.05em;text-transform:uppercase;color:var(--zacht);margin-bottom:.25rem}}
input[type="text"],textarea{{font:inherit;font-size:1rem;width:100%;padding:.45rem .6rem;border:1px solid var(--inkt);background:var(--wand);color:var(--inkt);border-radius:0}}
textarea{{resize:vertical;line-height:1.4}}
textarea:focus-visible{{outline:2px solid var(--rood);outline-offset:2px}}
.meer{{font-size:.95rem;color:var(--zacht);margin:.6rem 0 0}}
.knoppen{{display:flex;flex-wrap:wrap;gap:.6rem;margin:2.5rem 0 0}}
.knoppen button{{font:inherit;font-size:.95rem;padding:.45rem 1rem;border:1px solid var(--inkt);background:var(--wand);color:var(--inkt);cursor:pointer}}
.knoppen button:hover{{background:var(--inkt);color:var(--wand)}}
.status{{font-family:var(--data);font-size:.75rem;color:var(--zacht);margin:.6rem 0 0;min-height:1.2em}}
ol.onderzoek{{padding-left:1.3rem}}
ol.onderzoek li{{margin-bottom:.4rem}}
@media print{{nav.inhoud,.knoppen,.status,.meer,.hoofdstuk-nav,footer{{display:none}}.pagina{{display:block}}main{{max-width:none;padding:0}}.stap{{break-inside:avoid}}h2{{margin-top:1.5rem}}textarea{{border-color:var(--lijn)}}}}
</style>
</head>
<body>
<div class="pagina">
<nav class="inhoud" aria-label="Inhoud">
  <p class="vak"><a href="../" style="text-decoration:none;color:inherit">&larr; KIJK NU!</a></p>
  <p class="vak">De acht stappen</p>
  <ol>{nav}</ol>
</nav>
<main>
<header class="titel">
  <p class="vak"><a href="../" style="color:inherit">KIJK NU!</a> / Leren kijken</p>
  <h1>Kijkwijzer</h1>
  <p class="onder">Acht stappen die je bij elk kunstwerk kan zetten, van de eerste indruk tot je eigen oordeel</p>
</header>
<p>Deze kijkwijzer werkt bij een schilderij, een beeld, een gebouw, een film, een dansvoorstelling of een muziekstuk. Bij muziek lees je luisteren waar kijken staat.</p>
<p>Je hoeft niet elke vraag te beantwoorden. Kies per stap de vragen waar het werk om vraagt. Wat je invult, blijft bewaard op dit toestel en wordt nergens heen gestuurd. Onderaan kan je je blad afdrukken of leegmaken voor een volgend werk.</p>
<div class="werkveld">
  <div><label for="w-maker">Maker</label><input type="text" id="w-maker" data-veld="maker"></div>
  <div><label for="w-titel">Titel en jaar</label><input type="text" id="w-titel" data-veld="titel"></div>
  <div><label for="w-plek">Waar zag of hoorde je het?</label><input type="text" id="w-plek" data-veld="plek"></div>
</div>
{stappen}
<div class="knoppen"><button type="button" id="druk">Druk je blad af</button><button type="button" id="leeg">Maak leeg voor een nieuw werk</button></div>
<p class="status" id="status" aria-live="polite"></p>

<section id="onderzoek"><h2>Zelf op onderzoek</h2>
<p>Blijft er na de acht stappen een vraag hangen? Dan heb je een onderzoeksvraag. Zo werk je ze uit.</p>
<ol class="onderzoek">{"".join(f"<li>{E(x)}</li>" for x in ONDERZOEK)}</ol></section>
{buren}
<footer><p>Samengesteld door Sammy Ben Yakoub. <a href="../">Terug naar alle onderwerpen</a>.</p></footer>
</main>
</div>
<script>
var S="kijkwijzer",G={{}},kan=true;try{{G=JSON.parse(localStorage.getItem(S)||"{{}}")||{{}};}}catch(e){{G={{}};kan=false;}}
var velden=document.querySelectorAll("[data-veld]"),st=document.getElementById("status"),t;
function bewaar(){{try{{localStorage.setItem(S,JSON.stringify(G));st.textContent="Bewaard op dit toestel.";}}catch(e){{st.textContent="Bewaren lukt niet in deze browser. Druk je blad af voor je de pagina sluit.";}}}}
velden.forEach(function(v){{v.value=G[v.dataset.veld]||"";v.addEventListener("input",function(){{G[v.dataset.veld]=v.value;clearTimeout(t);t=setTimeout(bewaar,400);}});}});
if(!kan)st.textContent="Bewaren lukt niet in deze browser. Druk je blad af voor je de pagina sluit.";
document.getElementById("druk").addEventListener("click",function(){{window.print();}});
var leeg=document.getElementById("leeg"),zeker=false;
leeg.addEventListener("click",function(){{if(!zeker){{zeker=true;leeg.textContent="Zeker? Klik nog eens om alles te wissen";setTimeout(function(){{zeker=false;leeg.textContent="Maak leeg voor een nieuw werk";}},4000);return;}}G={{}};velden.forEach(function(v){{v.value="";}});bewaar();st.textContent="Leeggemaakt.";zeker=false;leeg.textContent="Maak leeg voor een nieuw werk";}});
if("IntersectionObserver" in window){{var L={{}};document.querySelectorAll("nav.inhoud a[href^='#']").forEach(function(a){{L[a.getAttribute("href").slice(1)]=a;}});
var io=new IntersectionObserver(function(it){{it.forEach(function(x){{if(x.isIntersecting&&L[x.target.id]){{Object.keys(L).forEach(function(k){{L[k].classList.remove("actief");}});L[x.target.id].classList.add("actief");}}}});}},{{rootMargin:"-10% 0px -80% 0px"}});
Object.keys(L).forEach(function(id){{var el=document.getElementById(id);if(el)io.observe(el);}});}}
</script>
</body>
</html>
'''
    (HIER.parent / "kijkwijzer").mkdir(exist_ok=True)
    (HIER.parent / "kijkwijzer" / "index.html").write_text(pagina, encoding="utf-8")
    print("kijkwijzer gebouwd")

if __name__ == "__main__":
    from onderwerpen import ONDERWERPEN
    bouw()
