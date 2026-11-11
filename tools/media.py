# Video's en geluiden per hoofdstuk. Alleen officiële bronnen (museum, omroep, orkest, rechthebbende) of publiek domein.
# Elk item: (anker-id van de kop waaronder het komt, type, id, titel, bron, uitleg)
# type: "youtube" (via youtube-nocookie), "vimeo", "archive" (Internet Archive)
MEDIA = {
 "muziek": [
  ("4-2-1-jaws-1975", "youtube", "BePfzCOMRZQ", "John Williams, Main Title (Jaws, 1975)", "YouTube, kanaal van John Williams", "Luister naar de twee lage noten die een halve toon van elkaar liggen."),
  ("4-3-2-le-sacre-du-printemps-1913", "youtube", "EkwqPJZe8ms", "Igor Stravinsky, Le Sacre du printemps (1913)", "London Symphony Orchestra, dirigent Sir Simon Rattle", "Volledige uitvoering. Begin bij de fagot in de inleiding."),
  ("4-4-1-prelude-in-des-groot-op-28-nr-15-1838-1839", "youtube", "R2d2spnXyLA", "Frédéric Chopin, Prelude op. 28 nr. 15 (1838-1839)", "Steinway & Sons, gespeeld door Lang Lang", ""),
  ("oefening-1-bernard-herrmann-psycho-1960", "youtube", "BYnPGS9Ev8w", "Alfred Hitchcock, Psycho (1960): de douchescène", "Universal Pictures", "Luister eerst zonder naar het beeld te kijken, en bekijk het daarna opnieuw met beeld."),
 ],
 "modernisme": [
  ("5-2-1-le-dejeuner-sur-l-herbe-1863", "youtube", "MpXxz2MuGcA", "Édouard Manet, Le Déjeuner sur l'herbe (1863)", "Musée d'Orsay, documentairefragment (Frans)", ""),
 ],
 "iconografie": [
  ("3-7-de-genres-en-de-verborgen-laag", "youtube", "wM6d9BOj4Ww", "Jan van Eyck, Het Arnolfini-portret (1434)", "The National Gallery, Londen (Engels)", "Een conservator bekijkt de symbolen in het schilderij van dichtbij."),
 ],
 "sjklovski": [
  ("3-2-hans-holbein-de-jonge-de-ambassadeurs", "youtube", "paA8hqqQ-_w", "Hans Holbein de Jonge, De ambassadeurs (1533)", "The National Gallery, Londen (Engels)", "Let op hoe de schedel pas leesbaar wordt als je van opzij kijkt."),
 ],
 "caravaggio": [
  ("caravaggio", "youtube", "cTDKgk66k_k", "Caravaggio, Het avondmaal in Emmaüs (1601)", "The National Gallery, Londen (Engels)", ""),
 ],
 "architectuur-en-design": [
  ("3-3-1-kerk-van-het-licht-1989", "youtube", "ucHo12HrQuQ", "Tadao Ando, Kerk van het Licht, Osaka", "Goethe-Institut (Engels)", ""),
 ],
 "ron-mueck": [
  ("1-3-werkwijze-van-klei-tot-huid", "youtube", "g2iPpa4azRc", "Still Life: Ron Mueck at Work (2013)", "Fondation Cartier pour l'art contemporain, film van Gautier Deblonde", "Mueck aan het werk in zijn atelier, zonder commentaar."),
 ],
 "duchamp": [
  ("1-de-lezing", "youtube", "xkmnozjaQEk", "Marcel Duchamp in gesprek (1966)", "RTBF Archives (Frans)", "Een zeldzaam televisie-interview met Duchamp."),
 ],
 "popart": [
  ("4-2-de-factory", "youtube", "nAxuvImOpvw", "13 Most Beautiful: Songs for Andy Warhol's Screen Tests", "The Andy Warhol Museum", "Warhols Screen Tests met nieuwe muziek, voorgesteld door het museum."),
 ],
 "performance": [
  ("inleiding-marina-abramovi-ulay-en-de-performance", "vimeo", "224530065", "The Story of Marina Abramović & Ulay (2017)", "Louisiana Channel, Louisiana Museum of Modern Art (Engels)", "Abramović en Ulay vertellen zelf over hun twaalf jaar samenwerking."),
 ],
 "dada": [
  ("a-hugo-ball", "archive", "karawane_1012_librivox", "Hugo Ball, Karawane (1916), voorgelezen", "LibriVox, publiek domein", "Zeventien verschillende stemmen lezen hetzelfde klankgedicht. Kies er een in de lijst."),
 ],
}

DIJKSTRA = [
 ("youtube", "fAaTYH3Ggjk", "Rineke Dijkstra en Hans den Hartog Jager: The Dutch Tradition of Portraiture (2013)", "The Frick Collection, New York (Engels)", "Dijkstra in gesprek over haar werk en de Hollandse portrettraditie."),
 ("youtube", "ntuExp7sWts", "Conversation Piece VI: Rineke Dijkstra", "Frans Hals Museum, Haarlem", "Dijkstra's portretten naast de schutters en regenten van Frans Hals."),
]

CSS = """
figure.media{margin:1.6rem 0;padding:.6rem;background:var(--kader);border:1px solid var(--lijn)}
.media-scherm{position:relative;aspect-ratio:16/9;background:#0d0a07;overflow:hidden}
.media-scherm.audio{aspect-ratio:auto;height:9rem}
.media-scherm iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
.media-start{position:absolute;inset:0;width:100%;height:100%;border:0;background:radial-gradient(circle at 50% 45%,#3a2a16 0%,#0d0a07 70%);color:#f3e6cc;font:inherit;cursor:pointer;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:.6rem;padding:1rem;text-align:center}
.media-start:hover .knop,.media-start:focus-visible .knop{background:#e0a248;color:#0d0a07}
.media-start .knop{display:inline-flex;align-items:center;gap:.5rem;border:1px solid #e0a248;color:#e0a248;padding:.45rem 1rem;font-family:var(--data);font-size:.75rem;letter-spacing:.05em;text-transform:uppercase}
.media-start .knop::before{content:"";width:0;height:0;border-left:.6rem solid currentColor;border-top:.38rem solid transparent;border-bottom:.38rem solid transparent}
.media-start .m-titel{font-size:1.05rem;max-width:30rem;line-height:1.3}
.media-start .m-noot{font-size:.78rem;opacity:.7;max-width:30rem}
figure.media figcaption{font-size:1rem;line-height:1.4;padding:.6rem .2rem 0;text-align:center}
figure.media .m-bron{display:block;font-size:.9rem;color:var(--zacht)}
"""

JS = """
document.querySelectorAll(".media-start").forEach(function(b){b.addEventListener("click",function(){
  var s=b.parentNode,t=b.dataset.type,id=b.dataset.id,src;
  if(t==="youtube")src="https://www.youtube-nocookie.com/embed/"+id+"?autoplay=1&rel=0";
  else if(t==="vimeo")src="https://player.vimeo.com/video/"+id+"?autoplay=1&dnt=1";
  else src="https://archive.org/embed/"+id+"?playlist=1";
  var f=document.createElement("iframe");f.src=src;f.title=b.dataset.titel;f.allow="autoplay; fullscreen; picture-in-picture; encrypted-media";f.allowFullscreen=true;
  s.replaceChildren(f);});});
"""

def blok(tp, mid, titel, bron, uitleg):
    import html
    E = lambda x: html.escape(x, quote=True)
    dienst = {"youtube": "YouTube", "vimeo": "Vimeo", "archive": "Internet Archive"}[tp]
    url = {"youtube": f"https://www.youtube.com/watch?v={mid}", "vimeo": f"https://vimeo.com/{mid}", "archive": f"https://archive.org/details/{mid}"}[tp]
    knop = "Afspelen" if tp != "archive" else "Beluisteren"
    audio = " audio" if tp == "archive" else ""
    return (f'<figure class="media"><div class="media-scherm{audio}"><button type="button" class="media-start" data-type="{tp}" data-id="{E(mid)}" data-titel="{E(titel)}">'
            f'<span class="knop">{knop}</span><span class="m-titel">{E(titel)}</span>'
            f'<span class="m-noot">Wordt geladen van {dienst} wanneer je klikt.</span></button></div>'
            f'<figcaption>{E(titel)}<span class="m-bron">{E(bron)}. <a href="{url}">Bekijk bij {dienst}</a></span>'
            + (f'<span class="m-bron">{E(uitleg)}</span>' if uitleg else "") + '</figcaption></figure>')
