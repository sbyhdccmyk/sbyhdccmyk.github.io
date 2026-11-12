# Situering van elk onderwerp in tijd en plaats: het referentiekader van de site.
# BANDEN = de periodes van het westerse referentiekader, in volgorde. Elk onderwerp krijgt:
#   wanneer, waar : korte tekst
#   hoofd         : banden waarin het onderwerp thuishoort (rood in de strook)
#   ook           : banden waarnaar het hoofdstuk verwijst (geel in de strook)
#   regio         : sleutels uit REGIOS, voor "Over de wereld" op de startpagina
#   lijn          : mijlpalen (jaar, tekst, soort). soort "k" = kunstwerk of tekst uit het hoofdstuk, "w" = wat er in de wereld gebeurde
#   noot          : optionele zin onder de tijdlijn
#   tekstjaar     : (jaar, band) voor denkers: waar hun tekst op de startpagina in het kader komt

BANDEN = [
 ("Prehistorie", "tot 3000 v.C."),
 ("Oudheid", "3000 v.C.-500"),
 ("Middeleeuwen", "500-1400"),
 ("Renaissance", "1400-1600"),
 ("Barok", "1600-1715"),
 ("Rococo", "1715-1780"),
 ("Neoclassicisme en romantiek", "1780-1850"),
 ("Modernisme", "1850-1915"),
 ("Avant-gardes", "1915-1945"),
 ("Na de oorlog", "1945-1980"),
 ("Hedendaags", "1980-nu"),
]
PRE, OUD, MID, REN, BAR, ROC, NEO, MOD, AVA, NAO, HED = range(11)

REGIOS = [
 ("azie", "Zuid- en Centraal-Azië"),
 ("japan", "Japan"),
 ("italie", "Italië"),
 ("frankrijk", "Frankrijk"),
 ("duits", "Duitsland, Zwitserland en Oostenrijk"),
 ("laag", "België en Nederland"),
 ("brits", "Groot-Brittannië"),
 ("oost", "Rusland en Oost-Europa"),
 ("vs", "Verenigde Staten"),
]

T = {}

T["de-vier-elementen"] = dict(
 wanneer="Van alle tijden", waar="Overal", hoofd=[], ook=[], regio=[], lijn=[],
 noot="Tijd, ruimte, lichaam en object zijn geen kenmerken van één periode. Je kan ze meenemen naar elk vak van dit kader, van een grotschildering tot een video-installatie.")

T["epoche"] = dict(
 wanneer="Een woord uit de Oudheid, een methode uit 1913", waar="Griekenland, Duitsland, Frankrijk, Rusland",
 hoofd=[MOD, AVA], ook=[OUD], regio=["duits"],
 lijn=[("8ste eeuw v.C.", "Homeros beschrijft in de *Ilias* het schild van Achilles: het oudste voorbeeld van ekphrasis", "k"),
       ("ca. 360-270 v.C.", "Pyrrho en de sceptici schorten hun oordeel op: epoché", "k"),
       ("1902-1904", "Paul Cézanne, *Mont Sainte-Victoire*", "k"),
       ("1913", "Edmund Husserl maakt in *Ideen* van de epoché een methode", "k"),
       ("1914-1918", "Eerste Wereldoorlog", "w"),
       ("1918", "Kazimir Malevich, *Wit op wit*", "k"),
       ("1945", "Maurice Merleau-Ponty schrijft *Le doute de Cézanne*", "k")])

T["iconografie"] = dict(
 wanneer="Kunstwerken van 1434 tot ca. 1664, gelezen met een methode uit 1939", waar="Vlaanderen, Duitsland, Italië, Frankrijk, Holland",
 hoofd=[REN, BAR], ook=[AVA], regio=["laag", "italie"],
 lijn=[("1434", "Jan van Eyck, *Het Arnolfini-portret*", "k"),
       ("1514", "Albrecht Dürer, *De heilige Hiëronymus in zijn studeervertrek*", "k"),
       ("1517", "Luther hangt zijn stellingen uit: begin van de Reformatie", "w"),
       ("1533", "Hans Holbein de Jongere, *De gezanten*", "k"),
       ("ca. 1545", "Agnolo Bronzino, *Allegorie met Venus en Cupido*", "k"),
       ("1593", "Cesare Ripa, *Iconologia*: een handboek vol zinnebeelden voor kunstenaars", "k"),
       ("1637-1638", "Nicolas Poussin, *Les Bergers d'Arcadie*", "k"),
       ("ca. 1664", "Johannes Vermeer, *Vrouw met weegschaal*", "k"),
       ("1939", "Erwin Panofsky, *Studies in Iconology*: het stappenplan", "k")])

T["boeddhabeeld"] = dict(
 wanneer="Van de 1ste eeuw tot vandaag", waar="India, Pakistan, Afghanistan, Japan",
 hoofd=[OUD], ook=[MID, HED], regio=["azie", "japan"],
 lijn=[("5de eeuw v.C.", "Leven van Siddhartha Gautama, de Boeddha", "w"),
       ("ca. 327 v.C.", "Alexander de Grote bereikt het noordwesten van India; de Griekse beeldtaal blijft er eeuwen aanwezig", "w"),
       ("tot de 2de eeuw", "De Boeddha wordt alleen met tekens getoond: een lege troon, een boom, voetafdrukken (Amaravati)", "k"),
       ("1ste-3de eeuw", "Eerste beelden in mensengedaante, in Gandhara en Mathura", "k"),
       ("5de eeuw", "De Boeddha van Sarnath houdt zijn eerste preek", "k"),
       ("6de-7de eeuw", "De reusachtige Boeddha's van Bamiyan worden uit de rotswand gehouwen", "k"),
       ("1252", "Grote Boeddha van Kamakura, Japan", "k"),
       ("2001", "De taliban vernietigen de Boeddha's van Bamiyan", "w")],
 noot="De namen in de strook komen uit de westerse kunstgeschiedenis. In India spreekt men voor deze eeuwen van de Kushana- en de Guptatijd.")

T["japanse-meesters"] = dict(
 wanneer="Van 1495 tot vandaag", waar="Japan, daarna Parijs en Vancouver",
 hoofd=[REN, NEO, MOD], ook=[HED], regio=["japan", "frankrijk"],
 lijn=[("1495", "Sesshu Toyo, *Landschap in gebroken inkt*", "k"),
       ("eind 16de eeuw", "Hasegawa Tohaku, *Pijnbomen*", "k"),
       ("1603-1868", "Edotijd: Japan leeft in vrede en sluit zich af van het buitenland", "w"),
       ("ca. 1830-1832", "Katsushika Hokusai, *De grote golf bij Kanagawa*", "k"),
       ("1853", "Een Amerikaanse vloot dwingt Japan zijn havens te openen", "w"),
       ("1857", "Utagawa Hiroshige, *Plotse regenbui boven de Ohashi-brug*", "k"),
       ("1867", "Japan heeft een eigen paviljoen op de wereldtentoonstelling in Parijs", "w"),
       ("1887", "Vincent van Gogh schildert *Brug in de regen*, naar Hiroshige", "k"),
       ("1993", "Jeff Wall, *A Sudden Gust of Wind (after Hokusai)*", "k")],
 noot="De namen in de strook komen uit de westerse kunstgeschiedenis. In Japan heten deze eeuwen de Muromachi-, de Momoyama- en de Edotijd.")

T["caravaggio"] = dict(
 wanneer="Ca. 1592-1610, met een terugblik op de renaissance", waar="Italië: Milaan, Rome, Napels",
 hoofd=[BAR], ook=[REN], regio=["italie"],
 lijn=[("1495-1498", "Leonardo da Vinci, *Het Laatste Avondmaal*", "k"),
       ("1509-1511", "Rafaël, *De School van Athene*: hoogrenaissance", "k"),
       ("1517", "Luther hangt zijn stellingen uit: begin van de Reformatie", "w"),
       ("1528", "Jacopo da Pontormo, *Kruisafneming*: maniërisme", "k"),
       ("1545-1563", "Concilie van Trente: de katholieke kerk wil beelden die gelovigen raken", "w"),
       ("ca. 1593", "Caravaggio schildert in Rome zijn eerste jongens met fruit", "k"),
       ("1601", "Caravaggio, *Het avondmaal in Emmaüs*", "k"),
       ("1610", "Caravaggio sterft, 38 jaar oud", "k")])

T["rococo"] = dict(
 wanneer="1715-1780", waar="Frankrijk: Parijs en het hof",
 hoofd=[ROC], ook=[], regio=["frankrijk"],
 lijn=[("1715", "Lodewijk XIV sterft; de adel verlaat Versailles voor de salons van Parijs", "w"),
       ("1717", "Antoine Watteau, *Pèlerinage à l'île de Cythère*", "k"),
       ("ca. 1718-1719", "Antoine Watteau, *Pierrot*", "k"),
       ("1767", "Jean-Honoré Fragonard, *Les Hasards heureux de l'escarpolette*", "k"),
       ("begin jaren 1770", "Jean-Honoré Fragonard, *La Lettre*", "k"),
       ("1789", "Franse Revolutie: de wereld van het rococo verdwijnt", "w")])

T["neoclassicisme"] = dict(
 wanneer="1780-1830", waar="Frankrijk en Rome",
 hoofd=[NEO], ook=[OUD], regio=["frankrijk", "italie"],
 lijn=[("1748", "De opgravingen in Pompeji beginnen: de Oudheid wordt weer zichtbaar", "w"),
       ("1784", "Jacques-Louis David, *Le Serment des Horaces*", "k"),
       ("1789", "Franse Revolutie", "w"),
       ("1793", "Jacques-Louis David, *La Mort de Marat*", "k"),
       ("1804", "Napoleon kroont zichzelf tot keizer", "w"),
       ("1808", "Jean-Auguste-Dominique Ingres, *Oedipus en de Sfinx*", "k"),
       ("1814", "Jean-Auguste-Dominique Ingres, *La Grande Odalisque*", "k")])

T["romantiek"] = dict(
 wanneer="1800-1840", waar="Duitsland en Frankrijk",
 hoofd=[NEO], ook=[], regio=["duits", "frankrijk"],
 lijn=[("1808-1810", "Caspar David Friedrich, *Der Mönch am Meer*", "k"),
       ("1815", "Slag bij Waterloo: einde van Napoleon", "w"),
       ("1816", "Het fregat Méduse vergaat voor de kust van West-Afrika", "w"),
       ("ca. 1818", "Caspar David Friedrich, *Der Wanderer über dem Nebelmeer*", "k"),
       ("1818-1819", "Théodore Géricault, *Le Radeau de la Méduse*", "k"),
       ("1830", "Julirevolutie in Parijs; Eugène Delacroix schildert *La Liberté guidant le peuple*", "k")])

T["modernisme"] = dict(
 wanneer="1850-1915, met een uitloper tot 1923", waar="Frankrijk, daarna Nederland en Duitsland",
 hoofd=[MOD], ook=[AVA], regio=["frankrijk"],
 lijn=[("1839", "De fotografie wordt openbaar gemaakt", "w"),
       ("1841", "Uitvinding van de verftube: schilders kunnen buiten werken", "w"),
       ("1848", "Revolutie in Frankrijk", "w"),
       ("1849-1850", "Gustave Courbet, *Un enterrement à Ornans*: realisme", "k"),
       ("1863", "Édouard Manet, *Le Déjeuner sur l'herbe*, op de Salon des Refusés", "k"),
       ("1872", "Claude Monet, *Impression, soleil levant*", "k"),
       ("1874", "Eerste tentoonstelling van de impressionisten", "k"),
       ("1888-1889", "Vincent van Gogh in Arles", "k"),
       ("1902-1904", "Paul Cézanne, *Mont Sainte-Victoire*", "k"),
       ("1910-1913", "Wassily Kandinsky en Piet Mondriaan zetten de stap naar de abstractie", "k"),
       ("1914", "Begin van de Eerste Wereldoorlog", "w")])

T["duchamp"] = dict(
 wanneer="Readymades vanaf 1913, de lezing in 1957", waar="Parijs, New York, Houston", vak=AVA,
 hoofd=[MOD, AVA], ook=[BAR, NAO, HED], regio=["frankrijk", "vs"],
 lijn=[("1656", "Diego Velázquez, *Las Meninas*", "k"),
       ("1913", "Marcel Duchamp monteert een fietswiel op een kruk", "k"),
       ("1914-1918", "Eerste Wereldoorlog", "w"),
       ("1917", "*Fountain*: een urinoir wordt ingestuurd voor een tentoonstelling in New York", "k"),
       ("1957", "Duchamp houdt in Houston de lezing *The Creative Act*", "k"),
       ("1991", "Félix González-Torres, *Untitled (Portrait of Ross in L.A.)*", "k")])

T["dada"] = dict(
 wanneer="1916-1924", waar="Zürich, New York, Berlijn, Keulen, Hannover, Parijs",
 hoofd=[AVA], ook=[], regio=["duits", "frankrijk", "vs"],
 lijn=[("1914", "Begin van de Eerste Wereldoorlog", "w"),
       ("1916", "Hugo Ball opent Cabaret Voltaire in Zürich", "k"),
       ("1917", "Marcel Duchamp, *Fountain*, in New York", "k"),
       ("1918", "Einde van de oorlog; in Duitsland begint de Weimarrepubliek", "w"),
       ("1919-1920", "Hannah Höch, *Schnitt mit dem Küchenmesser*", "k"),
       ("1923", "Hyperinflatie in Duitsland", "w"),
       ("1924", "In Parijs neemt het surrealisme het over", "k"),
       ("1937", "De nazi's stellen dada aan de schandpaal op de tentoonstelling Entartete Kunst", "w")])

T["architectuur-en-design"] = dict(
 wanneer="Van 1919 tot vandaag", waar="Duitsland, Frankrijk, Japan",
 hoofd=[AVA, NAO], ook=[HED], regio=["duits", "frankrijk", "japan"],
 lijn=[("1918", "Einde van de Eerste Wereldoorlog en revolutie in Duitsland", "w"),
       ("1919", "Het Bauhaus opent in Weimar", "k"),
       ("1924", "Marianne Brandt, *Theepot MT 49*", "k"),
       ("1925-1926", "Bauhausgebouw in Dessau", "k"),
       ("1928-1931", "Le Corbusier, *Villa Savoye*", "k"),
       ("1933", "Onder druk van de nazi's sluit het Bauhaus", "w"),
       ("1950-1955", "Le Corbusier, *Notre-Dame-du-Haut* in Ronchamp", "k"),
       ("1989", "Tadao Ando, *Kerk van het Licht*", "k"),
       ("2007", "Tadao Ando, *21_21 Design Sight* in Tokio", "k")])

T["popart"] = dict(
 wanneer="1955-1970", waar="Londen en New York",
 hoofd=[NAO], ook=[], regio=["brits", "vs"],
 lijn=[("jaren 1950", "Televisie, reclame en supermarkten veroveren het dagelijks leven", "w"),
       ("1952", "In Londen komt de Independent Group samen", "k"),
       ("1956", "Richard Hamilton, *Just what is it that makes today's homes so different, so appealing?*", "k"),
       ("1962", "Andy Warhol, *Marilyn Diptych*", "k"),
       ("1963", "Roy Lichtenstein, *Whaam!*", "k"),
       ("1964-1966", "Warhol filmt honderden bezoekers van de Factory voor zijn *Screen Tests*", "k"),
       ("1967", "*The Velvet Underground & Nico*, met de hoes van Warhol", "k")])

T["conceptuele-kunst"] = dict(
 wanneer="Vanaf 1965", waar="New York en Brussel",
 hoofd=[NAO], ook=[AVA], regio=["vs", "laag"],
 lijn=[("1917", "Marcel Duchamp, *Fountain*: het vertrekpunt", "k"),
       ("1964", "Marcel Broodthaers, *Pense-Bête*", "k"),
       ("1965", "Joseph Kosuth, *One and Three Chairs*", "k"),
       ("1967", "Sol LeWitt, *Paragraphs on Conceptual Art*", "k"),
       ("1968", "Studentenprotest in Parijs, Berlijn en de Verenigde Staten", "w"),
       ("1969", "Joseph Kosuth, *Art after Philosophy*", "k")])

T["performance"] = dict(
 wanneer="Vanaf de jaren 1960", waar="New York, Düsseldorf, Belgrado, Amsterdam",
 hoofd=[NAO], ook=[HED], regio=["oost", "vs"],
 lijn=[("jaren 1960", "Kunstenaars verzetten zich tegen het kunstwerk als koopwaar", "w"),
       ("1961", "Allan Kaprow, *Yard*: de happening", "k"),
       ("1965", "Joseph Beuys, *How to Explain Pictures to a Dead Hare*", "k"),
       ("1974", "Marina Abramović, *Rhythm 0*", "k"),
       ("1975", "Abramović en Ulay ontmoeten elkaar in Amsterdam", "k"),
       ("1977", "Abramović en Ulay, *Imponderabilia*", "k"),
       ("1980", "Abramović en Ulay, *Rest Energy*", "k"),
       ("1988", "*The Lovers: The Great Wall Walk*, hun afscheid", "k"),
       ("2010", "Marina Abramović, *The Artist Is Present*", "k")])

T["rineke-dijkstra"] = dict(
 wanneer="1991-2006, in de traditie van het geschilderde portret", waar="Nederland, met reizen naar Polen, Portugal, Engeland en Frankrijk",
 hoofd=[HED], ook=[REN, BAR, MOD], regio=["laag"],
 lijn=[("ca. 1485", "Sandro Botticelli, *De geboorte van Venus*", "k"),
       ("1644", "Johannes Verspronck, *Portret van Adriana Croes*", "k"),
       ("1839", "De fotografie wordt openbaar gemaakt", "w"),
       ("1863", "Édouard Manet, *Le Déjeuner sur l'herbe*", "k"),
       ("1991", "*Self-Portrait, Marnixbad*: het keerpunt", "k"),
       ("1992", "Begin van de *Beach Portraits*", "k"),
       ("2000-2003", "*Olivier, The French Foreign Legion*", "k"),
       ("2003-2006", "*Park Portraits*", "k")])

T["ron-mueck"] = dict(
 wanneer="Vanaf 1996, in de lange geschiedenis van de nabootsing", waar="Australië en Londen",
 hoofd=[HED], ook=[OUD, BAR, NAO], regio=["brits"],
 lijn=[("4de eeuw v.C.", "Praxiteles: het Griekse ideaal van het lichaam", "k"),
       ("ca. 1601", "Caravaggio, *De ongelovige Thomas*", "k"),
       ("1839", "Robert Cornelius maakt een van de eerste fotografische zelfportretten", "k"),
       ("eind jaren 1960", "Het hyperrealisme brengt de nabootsing terug", "k"),
       ("1970", "Masahiro Mori beschrijft de uncanny valley", "w"),
       ("1996-1997", "Ron Mueck, *Dead Dad*", "k"),
       ("1999", "Ron Mueck, *Boy*", "k"),
       ("2005", "Ron Mueck, *In Bed*", "k"),
       ("2013", "Ron Mueck, *Young Couple* en *Woman with Shopping*", "k")])

T["film"] = dict(
 wanneer="Kortfilm uit 2012, filmtaal sinds 1895", waar="Groot-Brittannië, met voorbeelden uit Rusland, de Verenigde Staten, Canada en Japan",
 hoofd=[HED], ook=[MOD, AVA, NAO], regio=["brits"],
 lijn=[("1895", "De gebroeders Lumière tonen in Parijs de eerste films aan een betalend publiek", "w"),
       ("1907", "Henri Bergson vergelijkt ons denken met de cinematograaf", "k"),
       ("jaren 1920", "Lev Koelesjov experimenteert met montage", "k"),
       ("1949", "Yasujirō Ozu, *Late Spring*", "k"),
       ("1960", "Alfred Hitchcock, *Psycho*", "k"),
       ("1961", "Arthur Lipsett, *Very Nice, Very Nice*", "k"),
       ("1983", "Gilles Deleuze, *Cinéma 1: L'image-mouvement*", "k"),
       ("2012", "Lynne Ramsay, *Swimmer*", "k")])

T["anouk-de-clercq"] = dict(
 wanneer="2020-2026", waar="België: Gent, Brussel, Leuven",
 hoofd=[HED], ook=[NAO], regio=["laag"],
 lijn=[("jaren 1960", "Kunstenaars als Nam June Paik beginnen met video te werken", "w"),
       ("1971", "Anouk De Clercq wordt geboren in Gent", "k"),
       ("2020", "*One*", "k"),
       ("2021", "*We'll find you when the sun goes black*", "k"),
       ("2023", "*Birdsong*", "k"),
       ("2026", "*Love that Moves the Sun*, in STUK in Leuven", "k")])

T["muziek"] = dict(
 wanneer="Filmmuziek uit de jaren 1970 en haar voorouders sinds 1838", waar="Verenigde Staten, met wortels in Duitsland, Parijs en Praag",
 hoofd=[NAO], ook=[NEO, MOD, AVA], regio=["vs"],
 lijn=[("1838-1839", "Frédéric Chopin, *Prelude op. 28 nr. 15*", "k"),
       ("1870", "Richard Wagner, *Die Walküre*: het leitmotiv", "k"),
       ("1893", "Antonín Dvořák, *Symfonie nr. 9*", "k"),
       ("1913", "Igor Stravinsky, *Le Sacre du printemps*", "k"),
       ("eind jaren 1920", "De geluidsfilm: muziek wordt samen met het beeld opgenomen", "w"),
       ("jaren 1930", "Europese componisten vluchten naar Hollywood en brengen hun klank mee", "w"),
       ("1960", "Bernard Herrmann, muziek bij *Psycho*", "k"),
       ("1975", "John Williams, *Jaws*", "k"),
       ("1977", "John Williams, *Star Wars*", "k")])

T["kant"] = dict(
 wanneer="1790", waar="Königsberg, Pruisen", tekstjaar=("1790", NEO),
 hoofd=[NEO], ook=[MOD], regio=["duits"],
 lijn=[("18de eeuw", "De Verlichting: denkers vertrouwen op de rede", "w"),
       ("1781", "*Kritik der reinen Vernunft*: wat kunnen we weten?", "k"),
       ("1788", "*Kritik der praktischen Vernunft*: wat moeten we doen?", "k"),
       ("1789", "Franse Revolutie", "w"),
       ("1790", "*Kritik der Urteilskraft*: het schone en het sublieme", "k"),
       ("1850-1863", "Courbet en Manet worden op de Salon lelijk gevonden", "k")])

T["sjklovski"] = dict(
 wanneer="1917", waar="Sint-Petersburg", tekstjaar=("1917", AVA),
 hoofd=[AVA], ook=[REN], regio=["oost"],
 lijn=[("1533", "Hans Holbein de Jongere, *De gezanten*", "k"),
       ("1591", "Giuseppe Arcimboldo, *Vertumnus*", "k"),
       ("ca. 1915", "De Russische formalisten onderzoeken hoe een tekst gemaakt is", "k"),
       ("1917", "Viktor Sjklovski schrijft *De kunst als procédé*", "k"),
       ("1917", "Russische Revolutie", "w")])

T["walter-benjamin"] = dict(
 wanneer="1935-1936", waar="Berlijn en Parijs", tekstjaar=("1935", AVA),
 hoofd=[AVA], ook=[REN], regio=["duits"],
 lijn=[("1503-1519", "Leonardo da Vinci, *Mona Lisa*", "k"),
       ("1515", "Albrecht Dürer, *De neushoorn*: een prent in vele exemplaren", "k"),
       ("1839", "De fotografie wordt openbaar gemaakt", "w"),
       ("1911", "De Mona Lisa wordt uit het Louvre gestolen", "w"),
       ("1933", "De nazi's komen aan de macht; Benjamin vlucht naar Parijs", "w"),
       ("1935-1936", "*Het kunstwerk in het tijdperk van zijn technische reproduceerbaarheid*", "k"),
       ("1940", "Benjamin sterft op de vlucht, aan de Spaanse grens", "w")])

T["susan-sontag"] = dict(
 wanneer="1964", waar="New York", tekstjaar=("1964", NAO),
 hoofd=[NAO], ook=[REN, NEO], regio=["vs"],
 lijn=[("ca. 1505", "Giorgione, *Het onweer*", "k"),
       ("1842", "William Turner, *Sneeuwstorm*", "k"),
       ("1964", "Susan Sontag publiceert *Against Interpretation*", "k"),
       ("jaren 1960", "Popart, happenings en nieuwe film zetten de kunstkritiek onder druk", "w"),
       ("1977", "Susan Sontag, *On Photography*", "k")])

T["roland-barthes"] = dict(
 wanneer="1980", waar="Parijs", tekstjaar=("1980", HED),
 hoofd=[HED], ook=[MOD, AVA], regio=["frankrijk"],
 lijn=[("1839", "De fotografie wordt openbaar gemaakt", "w"),
       ("1865", "Alexander Gardner fotografeert Lewis Payne", "k"),
       ("jaren 1930", "Crisisjaren in de Verenigde Staten", "w"),
       ("1936", "Dorothea Lange, *Migrant Mother*", "k"),
       ("1957", "Roland Barthes, *Mythologies*", "k"),
       ("1980", "Roland Barthes, *La Chambre claire*: studium en punctum", "k")])

T["arthur-danto"] = dict(
 wanneer="1964", waar="New York", tekstjaar=("1964", NAO),
 hoofd=[NAO], ook=[AVA, HED], regio=["vs"],
 lijn=[("1936", "Walker Evans fotografeert Allie Mae Burroughs", "k"),
       ("jaren 1960", "Massaproductie en reclame bepalen het straatbeeld", "w"),
       ("1964", "Andy Warhol toont zijn *Brillo Boxes*", "k"),
       ("1964", "Arthur Danto schrijft *The Artworld*", "k"),
       ("1981", "Sherrie Levine fotografeert de foto's van Evans opnieuw", "k"),
       ("1981", "Arthur Danto, *The Transfiguration of the Commonplace*", "k")])

T["gilles-deleuze"] = dict(
 wanneer="1987", waar="Parijs", tekstjaar=("1987", HED),
 hoofd=[HED], ook=[NEO, AVA], regio=["frankrijk"],
 lijn=[("1808", "Opstand in Madrid tegen de troepen van Napoleon", "w"),
       ("1814", "Francisco de Goya, *De derde mei 1808*", "k"),
       ("1914-1918", "Eerste Wereldoorlog", "w"),
       ("1924", "Käthe Kollwitz, *Nie wieder Krieg!*", "k"),
       ("1987", "Gilles Deleuze houdt aan de filmschool Fémis de lezing over de scheppende daad", "k")])

T["tanizaki"] = dict(
 wanneer="1933", waar="Japan", tekstjaar=("1933", AVA),
 hoofd=[AVA], ook=[REN, BAR], regio=["japan"],
 lijn=[("eind 16de eeuw", "Hasegawa Tohaku schildert in inkt en leegte", "k"),
       ("ca. 1635-1637", "Georges de La Tour, *Magdalena met de rokende vlam*", "k"),
       ("1868", "Japan opent zich voor westerse techniek", "w"),
       ("begin 20ste eeuw", "Elektrisch licht verdringt kaars en olielamp", "w"),
       ("1933", "Junichiro Tanizaki, *Lof der schaduw*", "k")])
