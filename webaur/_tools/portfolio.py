# -*- coding: utf-8 -*-
"""Rebuild Work, case studies, and home selected-work using the new demo screenshots."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_pages as b
from build_pages import (
    asset_prefix, href, cta, page_shell, header, footer, write, ROOT,
    pricing, BUILDERS, META, ACTIVE,
)

def shot(stem, alt, prefix, loading="lazy", kind="desktop"):
    if kind == "desktop":
        w, h = 1440, 900
        small, sw = f"{prefix}{stem}-800", 800
        large_w = 1440
        sizes = "(min-width: 1100px) 960px, 100vw"
    else:
        w, h = 780, 1688
        small, sw = f"{prefix}{stem}-390", 390
        large_w = 780
        sizes = "(min-width: 1100px) 200px, 40vw"
    av = f"{small}.avif {sw}w, {prefix}{stem}.avif {large_w}w"
    wp = f"{prefix}{stem}.webp {large_w}w"
    jp = f"{prefix}{stem}.jpg {large_w}w"
    return f'''<picture>
  <source type="image/avif" srcset="{av}" sizes="{sizes}" />
  <source type="image/webp" srcset="{wp}" sizes="{sizes}" />
  <img src="{prefix}{stem}.jpg" srcset="{jp}" sizes="{sizes}" width="{w}" height="{h}" alt="{alt}" loading="{loading}" decoding="async" />
</picture>'''


def desk(stem, alt, prefix, loading="lazy"):
    return f'''<div class="device-desktop">
  <div class="chrome" aria-hidden="true"><i></i><i></i><i></i></div>
  <div class="screen">{shot(stem, alt, prefix, loading, "desktop")}</div>
</div>'''


def phone(stem, alt, prefix, loading="lazy"):
    return f'''<div class="device-mobile">
  <div class="notch" aria-hidden="true"></div>
  <div class="screen">{shot(stem, alt, prefix, loading, "mobile")}</div>
</div>'''


PROJECTS = [
    {
        "slug": "barber-studio",
        "folder": "hale",
        "tone": "folio-hale",
        "num": "01",
        "demo": "demos/barber-studio/index.html",
        "wordmark": "Hale",
        "wordmark_sub": "Barber Studio",
        "fonts": [
            ("Instrument Serif", "display", "The hour is yours."),
            ("Figtree", "body", "Cuts, colour and a chair that is yours for the hour."),
        ],
        "palette": [
            ("#efeae2", "Bone"),
            ("#e4ddd1", "Bone 2"),
            ("#1a1814", "Ink"),
            ("#24352c", "Forest"),
            ("#3f5a4a", "Moss"),
        ],
        "pages": [
            {"id": "home", "file": "demos/barber-studio/index.html", "en_name": "Home", "fi_name": "Etusivu",
             "en_h": "The hour is yours.",
             "fi_h": "The hour is yours.",
             "en": "A split hero: a quiet chair, a bone-coloured field, and a short promise. The first screen already feels like a studio, not a template.",
             "fi": "Jaettu hero: hiljainen tuoli, luunvärinen kenttä ja lyhyt lupaus. Ensimmäinen näyttö tuntuu studiolta, ei valmiilta mallilta."},
            {"id": "services", "file": "demos/barber-studio/services.html", "en_name": "Services", "fi_name": "Palvelut",
             "en_h": "The menu.",
             "fi_h": "The menu.",
             "en": "A service list with example prices. The typography treats the menu as editorial, not a cramped table.",
             "fi": "Palvelulista esimerkkihinnoin. Typografia käsittelee listaa toimituksellisena, ei ahtaana taulukkona."},
            {"id": "barbers", "file": "demos/barber-studio/barbers.html", "en_name": "Barbers", "fi_name": "Parturit",
             "en_h": "Aino Vartiainen.",
             "fi_h": "Aino Vartiainen.",
             "en": "A single fictional barber, introduced with a portrait and a short bio. The person in the photograph is a stock model; the name and studio are invented.",
             "fi": "Yksi kuvitteellinen parturi, esitelty muotokuvalla ja lyhyellä esittelyllä. Valokuvan henkilö on mallikuva; nimi ja studio ovat keksittyjä."},
            {"id": "gallery", "file": "demos/barber-studio/gallery.html", "en_name": "Gallery", "fi_name": "Galleria",
             "en_h": "The room, close in.",
             "fi_h": "The room, close in.",
             "en": "A close look at the room and the work: chairs, tools, light. The photography carries the brand more than slogans do.",
             "fi": "Lähikuvaa huoneesta ja työstä: tuolit, välineet, valo. Valokuvat kantavat brändiä enemmän kuin iskulauseet."},
            {"id": "visit", "file": "demos/barber-studio/visit.html", "en_name": "Visit", "fi_name": "Vierailu",
             "en_h": "How a visit would work.",
             "fi_h": "How a visit would work.",
             "en": "Address, hours and a visit invitation, clearly labelled as a concept. Nothing here places a real booking.",
             "fi": "Osoite, aukiolo ja vierailukutsu, merkitty selvästi konseptiksi. Mikään tällä sivulla ei tee oikeaa varausta."},
        ],
        "en": {
            "title": "Hale Barber Studio",
            "category": "Barber",
            "intro": "A five-page concept for an independent barbershop. The site is built around a quiet hour in the chair: bone, forest green, and photography of the room rather than stock smiles.",
            "direction": "Editorial and still. Instrument Serif for the voice, Figtree for the body, a bone field with forest-green bands. The layout leaves air around the work.",
            "features": [
                "Five pages: home, services, barbers, gallery, visit",
                "A service menu with example prices",
                "A staff portrait and a close gallery of the room",
                "A visit page that does not pretend to take real bookings",
            ],
            "decisions": [
                "A typographic wordmark instead of a drawn logo",
                "Photography of the room and the work, not lifestyle posing",
                "A reservation path that stays honest about being a concept",
            ],
            "audience": "An independent barbershop that wants a site with the same care as the cut — small, specific, and calm rather than loud or promotional.",
            "brief": "Design a complete barbershop website that could stand as a commissioned piece: its own identity, several real pages, and a visit experience that does not invent bookings or reviews.",
            "objective": "Show how WEBAUR would approach a small service business: typography, photography and a clear path, without a generic template look.",
            "feature_note": "The visit page explains how an appointment would work and states plainly that this is a concept. No form here claims to confirm a booking.",
            "decisions_long": [
                ("Let the type carry the brand.", "Instrument Serif is used for the voice of the studio; Figtree keeps the body readable. The wordmark is typographic, so the identity can live in the layout rather than a separate mark."),
                ("Photograph the room, not a campaign.", "The gallery and the hero are about chairs, light and tools. That feels closer to a real shop than a set of posed portraits."),
                ("Stay honest at the point of contact.", "A live business would need a real booking tool. This concept stops short of pretending one exists."),
            ],
        },
        "fi": {
            "title": "Hale Barber Studio",
            "category": "Parturi",
            "intro": "Viisisivuinen konsepti itsenäiselle parturille. Sivusto rakentuu rauhalliselle hetkelle tuolissa: luunväri, metsänvihreä ja kuvia huoneesta, ei valmiskuvien hymyistä.",
            "direction": "Toimituksellinen ja rauhallinen. Instrument Serif äänelle, Figtree leipätekstille, luunvärinen pinta ja metsänvihreät kaistat. Asettelu jättää työlle tilaa.",
            "features": [
                "Viisi sivua: etusivu, palvelut, parturit, galleria, vierailu",
                "Palveluvalikko esimerkkihinnoin",
                "Henkilöesittely ja lähikuvagalleria huoneesta",
                "Vierailusivu, joka ei teeskentele oikeaa ajanvarausta",
            ],
            "decisions": [
                "Typografinen wordmark piirretyn logon sijaan",
                "Kuvia huoneesta ja työstä, ei lifestyle-poseerauksia",
                "Varauspolku, joka pysyy rehellisenä konseptina",
            ],
            "audience": "Itsenäinen parturi, joka haluaa sivuston yhtä huolellisen kuin leikkaus — pienen, tarkan ja rauhallisen, ei äänekästä mainontaa.",
            "brief": "Suunnitella kokonainen parturisivusto, joka kestäisi tilaustyönä: oma identiteetti, useita oikeita sivuja ja vierailukokemus ilman keksittyjä varauksia tai arvosteluja.",
            "objective": "Näyttää, miten WEBAUR lähestyisi pientä palveluyritystä: typografia, valokuvat ja selkeä polku, ilman geneeristä mallipohjaa.",
            "feature_note": "Vierailusivu kertoo, miten ajanvaraus toimisi, ja toteaa suoraan, että kyseessä on konsepti. Mikään lomake ei väitä vahvistavansa varausta.",
            "decisions_long": [
                ("Anna typografian kantaa brändiä.", "Instrument Serif on studion ääni, Figtree pitää leipätekstin luettavana. Wordmark on typografinen, jotta identiteetti elää asettelussa eikä erillisessä merkkissä."),
                ("Kuvaa huonetta, ei kampanjaa.", "Galleria ja hero kertovat tuoleista, valosta ja välineistä. Se on lähempänä oikeaa liikettä kuin poseeratut muotokuvat."),
                ("Pysy rehellisenä yhteydenotossa.", "Oikea liike tarvitsisi oikean varausvälineen. Tämä konsepti ei teeskentele, että sellainen on jo olemassa."),
            ],
        },
    },
    {
        "slug": "detailing",
        "folder": "alto",
        "tone": "folio-alto",
        "num": "02",
        "demo": "demos/detailing/index.html",
        "wordmark": "ALTO",
        "wordmark_sub": "DETAIL",
        "fonts": [
            ("Big Shoulders Display / Text", "display", "A quieter shine."),
            ("Source Sans 3", "body", "Essential, Signature and Atelier — packages stated in the open."),
        ],
        "palette": [
            ("#edeeef", "Showroom"),
            ("#f7f7f6", "Paper"),
            ("#121417", "Ink"),
            ("#8f2a1c", "Oxide red"),
        ],
        "pages": [
            {"id": "home", "file": "demos/detailing/index.html", "en_name": "Home", "fi_name": "Etusivu",
             "en_h": "A quieter shine.",
             "fi_h": "A quieter shine.",
             "en": "A showroom-grey opening with a low car and a short line. The first impression is a bay, not a brochure grid.",
             "fi": "Showroom-harmaa avaus, matala auto ja lyhyt rivi. Ensimmäinen vaikutelma on halli, ei esitehila."},
            {"id": "services", "file": "demos/detailing/services.html", "en_name": "Services", "fi_name": "Palvelut",
             "en_h": "Essential, Signature, Atelier.",
             "fi_h": "Essential, Signature, Atelier.",
             "en": "Three packages with example prices from €189. The range is readable at a glance, without hiding the cost behind a “get a quote” wall.",
             "fi": "Kolme pakettia esimerkkihinnoin alkaen 189 €. Valikoima on luettavissa heti, ilman että hinta piilotetaan tarjouspyynnön taakse."},
            {"id": "results", "file": "demos/detailing/results.html", "en_name": "Results", "fi_name": "Tulokset",
             "en_h": "The same car, twice.",
             "fi_h": "The same car, twice.",
             "desk_id": "results-slider",
             "en": "Before-and-after sliders are the main feature of this page. The before frames are processed versions of the same photograph — not a different car, and not a documented client job. The page says so.",
             "fi": "Ennen–jälkeen-liukusäätimet ovat sivun päätoiminto. Ennen-kuvat ovat saman valokuvan käsiteltyjä versioita — eivät toista autoa eivätkä dokumentoitua asiakastyötä. Sivu sanoo tämän suoraan."},
            {"id": "process", "file": "demos/detailing/process.html", "en_name": "Process", "fi_name": "Prosessi",
             "en_h": "A day in the bay.",
             "fi_h": "A day in the bay.",
             "en": "The work is walked through as a day in the bay, so the service feels like a sequence rather than a list of buzzwords.",
             "fi": "Työ käydään läpi päivänä hallissa, jotta palvelu tuntuu vaiheilta eikä pelkiltä iskusanoilta."},
            {"id": "contact", "file": "demos/detailing/contact.html", "en_name": "Contact", "fi_name": "Yhteys",
             "en_h": "Request a place in the bay.",
             "fi_h": "Request a place in the bay.",
             "en": "A request form and contact details, labelled as a concept. It does not invent a waiting list or a finished booking.",
             "fi": "Pyyntölomake ja yhteystiedot, merkitty konseptiksi. Sivu ei keksi jonotuslistaa tai valmista varausta."},
        ],
        "en": {
            "title": "Alto Detail",
            "category": "Automotive detailing",
            "intro": "A showroom-like concept for a detailing studio: grey, oxide red, and cars photographed as objects in a bay. The site is five pages, including a results page built around before-and-after sliders.",
            "direction": "Cinematic and industrial. Big Shoulders for the automotive voice, Source Sans 3 for the reading text, showroom grey with an oxide-red accent.",
            "features": [
                "Five pages: home, services, results, process, contact",
                "Three named packages with example prices",
                "Interactive before-and-after sliders, honestly captioned",
                "A process page that walks through a day in the bay",
            ],
            "decisions": [
                "A typographic mark that reads like a manufacturer name",
                "Comparisons that admit the “before” is a treated frame",
                "Prices on the page, not hidden behind a quote form",
            ],
            "audience": "A detailing studio that wants to look as precise as the work — closer to a showroom than to a loud auto-shop advert.",
            "brief": "Build a complete detailing website with a distinct brand, priced packages, a visual comparison, and a contact path that does not invent results.",
            "objective": "Show how WEBAUR would treat a technical service brand: photography, typography and a feature (the slider) that actually does something.",
            "feature_note": "The sliders compare two treatments of the same photograph. They are illustrative, not proof of a paid job.",
            "decisions_long": [
                ("Give the brand a manufacturer’s voice.", "Big Shoulders is wide and mechanical; Source Sans 3 keeps packages and process notes easy to read. Oxide red is used sparingly, like a painted brake caliper."),
                ("Make the comparison honest.", "A slider is convincing only if the caption is true. Both sides are the same photograph; the “before” is a processed frame, and the page says so."),
                ("Put the price where the package is.", "Essential, Signature and Atelier are listed with example figures so a visitor can judge the offering without a gate."),
            ],
        },
        "fi": {
            "title": "Alto Detail",
            "category": "Autonhoito ja detailing",
            "intro": "Showroom-henkinen konsepti detailing-studiolle: harmaa, oksidinpunainen ja autot kuvattuna esineinä hallissa. Viisi sivua, joukossa tulossivu ennen–jälkeen-liukusäätimineen.",
            "direction": "Elokuvallinen ja teollinen. Big Shoulders automaiselle äänelle, Source Sans 3 lukutekstille, showroom-harmaa ja oksidinpunainen aksentti.",
            "features": [
                "Viisi sivua: etusivu, palvelut, tulokset, prosessi, yhteys",
                "Kolme nimettyä pakettia esimerkkihinnoin",
                "Toimivat ennen–jälkeen-liukusäätimet, rehellisesti kuvailtuina",
                "Prosessisivu, joka kulkee päivän hallissa",
            ],
            "decisions": [
                "Typografinen merkki, joka lukeutuu kuin valmistajan nimi",
                "Vertailut, jotka myöntävät “ennen”-kuvan olevan käsitelty",
                "Hinnat sivulla, ei tarjouslomakkeen takana",
            ],
            "audience": "Detailing-studio, joka haluaa näyttää yhtä täsmälliseltä kuin työ — lähempänä showroomia kuin äänekästä autohuoltomainosta.",
            "brief": "Rakentaa kokonainen detailing-sivusto omalla brändillä, hinnoitelluilla paketeilla, visuaalisella vertailulla ja yhteydenottopolulla, joka ei keksi tuloksia.",
            "objective": "Näyttää, miten WEBAUR käsittelisi teknistä palvelubrändiä: valokuvat, typografia ja toiminto (liukusäädin), joka tekee oikeasti jotain.",
            "feature_note": "Liukusäätimet vertaavat saman valokuvan kahta käsittelyä. Ne ovat havainnollistavia, eivät todiste maksavasta työstä.",
            "decisions_long": [
                ("Anna brändille valmistajan ääni.", "Big Shoulders on leveä ja mekaaninen; Source Sans 3 pitää paketit ja prosessitekstit luettavina. Oksidinpunaista käytetään säästeliäästi, kuin maalattua jarrusatulaa."),
                ("Pidä vertailu rehellisenä.", "Liukusäädin vakuuttaa vain, jos kuvateksti on totta. Molemmat puolet ovat sama valokuva; “ennen” on käsitelty kehys, ja sivu sanoo sen."),
                ("Laita hinta paketin viereen.", "Essential, Signature ja Atelier on listattu esimerkkiluvuin, jotta kävijä voi arvioida tarjonnan ilman porttia."),
            ],
        },
    },
    {
        "slug": "maison-cafe",
        "folder": "maison",
        "tone": "folio-maison",
        "num": "03",
        "demo": "demos/maison-cafe/index.html",
        "wordmark": "Maison",
        "wordmark_sub": "Café",
        "fonts": [
            ("Bodoni Moda", "display", "A quiet table."),
            ("Manrope", "body", "Pastry, coffee and a room that holds the afternoon."),
        ],
        "palette": [
            ("#f3e6d0", "Parchment"),
            ("#e8d4b8", "Parchment 2"),
            ("#fbf6ec", "Foam"),
            ("#1c1510", "Ink"),
            ("#3a4632", "Bottle green"),
            ("#8e4024", "Copper"),
        ],
        "pages": [
            {"id": "home", "file": "demos/maison-cafe/index.html", "en_name": "Home", "fi_name": "Etusivu",
             "en_h": "A quiet table.",
             "fi_h": "A quiet table.",
             "en": "A conservatory table and a short invitation. The opening is photographic and typographic, closer to a journal than a food-delivery page.",
             "fi": "Talvipuutarhapöytä ja lyhyt kutsu. Avaus on valokuvallinen ja typografinen, lähempänä julkaisua kuin noutoruokasivua."},
            {"id": "menu", "file": "demos/maison-cafe/menu.html", "en_name": "Menu", "fi_name": "Ruokalista",
             "en_h": "The list.",
             "fi_h": "The list.",
             "en": "Coffee, pastry and plates set as an editorial list. Prices are example figures for the concept, not a live kitchen.",
             "fi": "Kahvi, leivonnaiset ja annokset toimituksellisena listana. Hinnat ovat konseptin esimerkkejä, eivät elävän keittiön listaa."},
            {"id": "story", "file": "demos/maison-cafe/story.html", "en_name": "Story", "fi_name": "Tarina",
             "en_h": "The house is a study.",
             "fi_h": "The house is a study.",
             "en": "A longer piece about the house and the room. It is written as atmosphere, and it does not invent a founding year or a family history presented as fact.",
             "fi": "Pidempi teksti talosta ja huoneesta. Se on kirjoitettu tunnelmaksi, eikä se keksi perustamisvuotta tai sukuhistoriaa faktana."},
            {"id": "visit", "file": "demos/maison-cafe/visit.html", "en_name": "Visit", "fi_name": "Vierailu",
             "en_h": "Come in only in the story.",
             "fi_h": "Come in only in the story.",
             "en": "Hours and a visit invitation, stated clearly: this is a story, not a street address you can walk to. No reservation is placed.",
             "fi": "Aukiolo ja vierailukutsu, sanottu suoraan: tämä on tarina, ei katuosoite johon voi kävellä. Pöytää ei varata."},
        ],
        "en": {
            "title": "Maison Café",
            "category": "Café",
            "intro": "A four-page café concept in parchment, bottle green and copper. The site is built like a short journal: a table, a menu, a story, and a visit page that admits it is only in the story.",
            "direction": "Warm and typographic. Bodoni Moda for the display voice, Manrope for the body, a parchment ground with bottle-green bands and a copper accent.",
            "features": [
                "Four pages: home, menu, story, visit",
                "An editorial menu with example prices",
                "A longer story page about the house",
                "A visit page that does not invent a real door on a real street",
            ],
            "decisions": [
                "A high-contrast serif as the café’s voice",
                "Food photography used in sequences, not as a tiled catalogue",
                "Hospitality copy that stays fictional and clearly labelled",
            ],
            "audience": "An independent café or small restaurant that wants a site with the same warmth as the room — slower and more considered than a delivery listing.",
            "brief": "Design a complete café website with its own identity, a readable menu, a sense of place, and a visit path that does not invent reservations.",
            "objective": "Show how WEBAUR would approach hospitality: type, photography and pacing, without turning the café into a template storefront.",
            "feature_note": "The visit page is explicit: you come in only in the story, not on a street. There is no real table to book.",
            "decisions_long": [
                ("Let a serif set the temperature.", "Bodoni Moda gives the name and headlines a printed quality; Manrope keeps the menu and the story comfortable to read. Copper is used like a warm metal, not a neon accent."),
                ("Treat the menu as a publication.", "Items are set in a list with space, not in a crowded grid of cards. The photography supports the list rather than replacing it."),
                ("Do not invent a door.", "A real café would publish a real address and a real booking path. This concept keeps the invitation and tells you it is fictional."),
            ],
        },
        "fi": {
            "title": "Maison Café",
            "category": "Kahvila",
            "intro": "Nelisivuinen kahvilakonsepti pergamentilla, pullonvihreällä ja kuparilla. Sivusto on rakennettu kuin lyhyt julkaisu: pöytä, lista, tarina ja vierailusivu, joka myöntää elävänsä vain tarinassa.",
            "direction": "Lämmin ja typografinen. Bodoni Moda näyttöäänelle, Manrope leipätekstille, pergamenttipinta, pullonvihreät kaistat ja kuparinen aksentti.",
            "features": [
                "Neljä sivua: etusivu, ruokalista, tarina, vierailu",
                "Toimituksellinen ruokalista esimerkkihinnoin",
                "Pidempi tarinasivu talosta",
                "Vierailusivu, joka ei keksi oikeaa ovea oikealle kadulle",
            ],
            "decisions": [
                "Voimakas serif kahvilan äänenä",
                "Ruokakuvat jaksoina, ei laatoitettuna katalogina",
                "Vieraanvarainen teksti, joka pysyy kuvitteellisena ja merkittynä",
            ],
            "audience": "Itsenäinen kahvila tai pieni ravintola, joka haluaa sivuston yhtä lämpimän kuin huone — hitaamman ja harkitumman kuin noutolista.",
            "brief": "Suunnitella kokonainen kahvilasivusto omalla identiteetillä, luettavalla listalla, paikan tuntuella ja vierailupolulla, joka ei keksi varauksia.",
            "objective": "Näyttää, miten WEBAUR lähestyisi ravintola-alaa: typografia, valokuvat ja rytmi, ilman että kahvilasta tulee mallipohjainen julkisivu.",
            "feature_note": "Vierailusivu on suora: sisään tullaan vain tarinassa, ei kadulla. Pöytää ei ole varattavissa.",
            "decisions_long": [
                ("Anna serifin asettaa lämpötila.", "Bodoni Moda antaa nimelle ja otsikoille painetun laadun; Manrope pitää listan ja tarinan miellyttävinä lukea. Kuparia käytetään kuin lämmintä metallia, ei neonaksenttia."),
                ("Käsittele listaa julkaisuna.", "Annokset on ladottu tilaa jättävään listaan, ei ahdettuun korttiruudukkoon. Valokuvat tukevat listaa eivätkä korvaa sitä."),
                ("Älä keksi ovea.", "Oikea kahvila julkaisisi oikean osoitteen ja oikean varauspolun. Tämä konsepti pitää kutsun ja kertoo, että se on kuvitteellinen."),
            ],
        },
    },
]


def _alt(lang, title, page_name, kind):
    if lang == "en":
        return f"{'Desktop' if kind=='desktop' else 'Mobile'} preview of the {title} {page_name} page"
    return f"{title} — {page_name}, {'työpöytä' if kind=='desktop' else 'puhelin'}"


def _stem(p, page_id, kind, desk_id=None):
    ident = desk_id or page_id
    return f"images/work/{p['folder']}/{ident}-{kind}"


def thumbs(p, lang, pre):
    items = []
    inner = [pg for pg in p["pages"] if pg["id"] != "home"][:3]
    for pg in inner:
        name = pg["fi_name"] if lang == "fi" else pg["en_name"]
        alt = _alt(lang, p[lang]["title"], name, "desktop")
        items.append(
            f'''<figure>
  <a href="{pre}{pg["file"]}">{desk(_stem(p, pg["id"], "desktop", pg.get("desk_id")), alt, pre)}</a>
  <figcaption>{name}</figcaption>
</figure>'''
        )
    return '<div class="folio-thumbs">' + "".join(items) + "</div>"


def meta_cols(p, lang):
    m = p[lang]
    if lang == "en":
        h = ("Design direction", "Main features", "Design decisions")
    else:
        h = ("Suunnittelusuunta", "Keskeiset ominaisuudet", "Suunnitteluratkaisut")
    feats = "".join(f"<li>{x}</li>" for x in m["features"])
    decs = "".join(f"<li>{x}</li>" for x in m["decisions"])
    return f'''<div class="folio-meta">
  <div>
    <h3>{h[0]}</h3>
    <p class="muted">{m["direction"]}</p>
  </div>
  <div>
    <h3>{h[1]}</h3>
    <ul>{feats}</ul>
  </div>
  <div>
    <h3>{h[2]}</h3>
    <ul>{decs}</ul>
  </div>
</div>'''


def actions(p, lang, page):
    pre = asset_prefix(lang, 1 if page.startswith("work/") else 0)
    demo = "View live demo" if lang == "en" else "Avaa live-demo"
    case = "Read the case study" if lang == "en" else "Lue projektiesittely"
    more = "View project" if lang == "en" else "Katso projekti"
    if page == "index.html":
        case_lab = more
    else:
        case_lab = case
    return f'''<div class="folio-actions">
  <a class="btn btn-ink" href="{pre}{p["demo"]}">{demo}</a>
  <a class="btn btn-ghost" href="{href(lang, page, lang, "work/"+p["slug"]+".html")}">{case_lab}</a>
</div>'''


def folio_block(p, lang, page, mode="full"):
    pre = asset_prefix(lang, 1 if page.startswith("work/") else 0)
    m = p[lang]
    title = m["title"]
    concept = "Concept project" if lang == "en" else "Konseptiprojekti"
    alt_d = _alt(lang, title, p["pages"][0]["en_name"] if lang == "en" else p["pages"][0]["fi_name"], "desktop")
    alt_m = _alt(lang, title, p["pages"][0]["en_name"] if lang == "en" else p["pages"][0]["fi_name"], "mobile")
    loading = "eager" if (mode == "full" and p["num"] == "01") or (mode == "home" and p["num"] == "01" and page == "index.html") else "lazy"
    stage = f'''<div class="device-stack folio-stage">
  {desk(_stem(p, "home", "desktop"), alt_d, pre, loading)}
  {phone(_stem(p, "home", "mobile"), alt_m, pre, loading)}
</div>'''

    head = f'''<div class="folio-head">
  <div class="folio-kicker-row">
    <span class="folio-num">{p["num"]}</span>
    <span class="badge">{concept}</span>
    <span class="kicker" style="margin:0">{m["category"]}</span>
  </div>
  <h2 class="folio-title" id="{p["folder"]}-title">{title}</h2>
  <p class="lead folio-intro">{m["intro"]}</p>
</div>'''

    # Varied layouts
    if mode == "home":
        body = f'''{head}{stage}{thumbs(p, lang, pre)}
<p class="muted" style="max-width:42rem">{m["direction"]}</p>
{actions(p, lang, page)}'''
    elif p["tone"] == "folio-alto":
        # Type first, then cinematic stage, thumbs include slider, then meta
        body = f'''{head}{stage}
<div class="wrap" style="margin-bottom:48px">
  <p class="kicker">{"Key feature" if lang=="en" else "Keskeinen toiminto"}</p>
  <h3 class="folio-title" style="font-size:clamp(28px,3.5vw,44px);margin:8px 0 16px">{"The same car, twice." if lang=="en" else "Sama auto, kahdesti."}</h3>
  <p class="muted" style="max-width:42rem;margin-bottom:24px">{p[lang]["feature_note"]}</p>
  {desk(_stem(p, "results", "desktop", "results-slider"), _alt(lang, title, "Results" if lang=="en" else "Tulokset", "desktop"), pre)}
</div>
{thumbs(p, lang, pre)}
{meta_cols(p, lang)}
{actions(p, lang, page)}'''
    elif p["tone"] == "folio-maison":
        body = f'''<div class="split" style="align-items:end;margin-bottom:8px">
  {head}
</div>
{stage}
{thumbs(p, lang, pre)}
{meta_cols(p, lang)}
{actions(p, lang, page)}'''
    else:
        body = f'''{head}{stage}{thumbs(p, lang, pre)}{meta_cols(p, lang)}{actions(p, lang, page)}'''

    return f'''<section class="folio-project {p["tone"]}" id="{p["folder"]}" aria-labelledby="{p["folder"]}-title">
  <div class="wrap">
    {body}
  </div>
</section>'''


def home_teaser(lang, page):
    pre = asset_prefix(lang, 0)
    concept = "Concept project" if lang == "en" else "Konseptiprojekti"
    case_lab = "Read the case study" if lang == "en" else "Lue projektiesittely"
    lines = {
        "hale": {
            "en": "A five-page concept for an independent barbershop.",
            "fi": "Viisisivuinen konsepti itsenäiselle parturille.",
        },
        "alto": {
            "en": "A detailing concept with priced packages and honest before-and-after sliders.",
            "fi": "Detailing-konsepti paketteineen ja ennen–jälkeen-vertailuineen.",
        },
        "maison": {
            "en": "A four-page café concept, built like a short journal.",
            "fi": "Nelisivuinen kahvilakonsepti, rakennettu kuin lyhyt julkaisu.",
        },
    }
    cards = []
    for i, p in enumerate(PROJECTS):
        m = p[lang]
        title = m["title"]
        alt_d = _alt(lang, title, p["pages"][0]["en_name"] if lang == "en" else p["pages"][0]["fi_name"], "desktop")
        alt_m = _alt(lang, title, p["pages"][0]["en_name"] if lang == "en" else p["pages"][0]["fi_name"], "mobile")
        loading = "eager" if i == 0 else "lazy"
        case = href(lang, page, lang, "work/" + p["slug"] + ".html")
        phone_html = phone(_stem(p, "home", "mobile"), alt_m, pre, loading) if i == 0 else ""
        cards.append(
            f"""<article class="teaser-{p['folder']}">
  <div class="device-stack">
    {desk(_stem(p, "home", "desktop"), alt_d, pre, loading)}
    {phone_html}
  </div>
  <div class="teaser-copy">
    <div class="folio-kicker-row" style="margin:0">
      <span class="badge">{concept}</span>
      <span class="kicker" style="margin:0">{m["category"]}</span>
    </div>
    <h3 id="{p['folder']}-teaser-title"><a href="{case}">{title}</a></h3>
    <p class="teaser-line">{lines[p["folder"]][lang]}</p>
    <a class="teaser-link" href="{case}">{case_lab}</a>
  </div>
</article>"""
        )
    return '<div class="home-teaser">' + "\n".join(cards) + "</div>"


def work_projects(lang, page, layouts=True, mode=None):
    if mode is None:
        mode = "home" if page == "index.html" else "full"
    wrap = "home-folio" if mode == "home" else "folio"
    blocks = [folio_block(p, lang, page, mode=mode) for p in PROJECTS]
    return f'<div class="{wrap}">' + "\n".join(blocks) + "</div>"


def work_page(lang):
    page = "work.html"
    if lang == "en":
        lead = "Three complete concept projects, each built as a multi-page brand site. They are independent design concepts — not paying-client work — made to show how WEBAUR would approach different businesses."
        eyebrow, title = "WORK", "Different businesses. Different digital experiences."
    else:
        lead = "Kolme valmista konseptiprojektia, kukin rakennettu monisivuisena brändisivustona. Ne ovat itsenäisiä suunnittelukonsepteja — eivät maksavan asiakkaan töitä — ja näyttävät, miten WEBAUR lähestyisi eri yrityksiä."
        eyebrow, title = "TYÖT", "Eri yrityksiä. Erilaisia digitaalisia kokemuksia."
    return f'''
<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow">{eyebrow}</p>
    <h1 class="display">{title}</h1>
    <p class="lead">{lead}</p>
  </div>
</section>
{work_projects(lang, page, mode="full")}
{cta(lang, page)}
'''


def swatches(p):
    bits = []
    for hexv, name in p["palette"]:
        bits.append(f'<div class="swatch"><i style="background:{hexv}"></i><span>{name}<br />{hexv}</span></div>')
    return '<div class="swatches">' + "".join(bits) + "</div>"


def type_spec(p):
    blocks = []
    for name, role, sample in p["fonts"]:
        cls = "type-display" if role == "display" else "type-body"
        fam = "Georgia, 'Times New Roman', serif" if role == "display" else "system-ui, sans-serif"
        blocks.append(
            f'''<div>
  <p><strong>{name}</strong></p>
  <p class="{cls}" style="font-family:{fam}">{sample}</p>
  <p class="muted" style="margin-top:6px;font-size:13px">Shown here in a system stand-in. The live demo loads {name}.</p>
</div>'''
        )
    return '<div class="type-spec">' + "".join(blocks) + "</div>"


def wordmark(p):
    if p["folder"] == "alto":
        return f'''<p class="type-display" style="font-family:system-ui,sans-serif;letter-spacing:.08em;font-weight:700">{p["wordmark"]} <span style="font-weight:500;letter-spacing:.22em;font-size:.38em;vertical-align:super">{p["wordmark_sub"]}</span></p>'''
    if p["folder"] == "maison":
        return f'''<p class="type-display" style="font-family:Georgia,serif;font-style:italic">{p["wordmark"]} <span style="font-style:normal;font-size:.42em;letter-spacing:.18em;text-transform:uppercase;vertical-align:middle">{p["wordmark_sub"]}</span></p>'''
    return f'''<p class="type-display" style="font-family:Georgia,serif">{p["wordmark"]} <span style="font-size:.4em;letter-spacing:.16em;text-transform:uppercase;vertical-align:middle">{p["wordmark_sub"]}</span></p>'''


def walk_items(p, lang, pre):
    items = []
    for i, pg in enumerate(p["pages"]):
        name = pg["fi_name"] if lang == "fi" else pg["en_name"]
        copy = pg["fi"] if lang == "fi" else pg["en"]
        heading = pg["fi_h"] if lang == "fi" else pg["en_h"]
        alt_d = _alt(lang, p[lang]["title"], name, "desktop")
        alt_m = _alt(lang, p[lang]["title"], name, "mobile")
        desk_id = pg.get("desk_id")
        open_demo = "Open this page" if lang == "en" else "Avaa tämä sivu"
        pair = f'''<div class="walk-pair">
  {desk(_stem(p, pg["id"], "desktop", desk_id), alt_d, pre)}
  {phone(_stem(p, pg["id"], "mobile"), alt_m, pre)}
</div>'''
        text = f'''<div class="walk-copy">
  <p class="kicker">{name}</p>
  <h3>{heading}</h3>
  <p class="muted">{copy}</p>
  <p style="margin-top:16px"><a class="btn btn-ghost" href="{pre}{pg["file"]}">{open_demo}</a></p>
</div>'''
        cls = "walk-item is-alt" if i % 2 else "walk-item"
        if i % 2:
            items.append(f'<article class="{cls}">{text}{pair}</article>')
        else:
            items.append(f'<article class="{cls}">{pair}{text}</article>')
    return '<div class="walk">' + "\n".join(items) + "</div>"


def case_page(lang, p):
    page = f"work/{p['slug']}.html"
    pre = asset_prefix(lang, 1)
    m = p[lang]
    concept = "Concept project" if lang == "en" else "Konseptiprojekti"
    demo_l = "View live demo" if lang == "en" else "Avaa live-demo"
    back = "Back to work" if lang == "en" else "Takaisin töihin"
    work_lab = "Work" if lang == "en" else "Työt"
    if lang == "en":
        labels = {
            "brief": "The brief",
            "objective": "Objective",
            "audience": "Audience",
            "identity": "Brand identity",
            "palette": "Palette",
            "type": "Typefaces",
            "mark": "Wordmark",
            "walk": "Page by page",
            "feat": "Key features",
            "dec": "Design decisions",
            "honest": "This is a concept project. It is not a paying-client website, and it does not invent customers, reviews or results.",
        }
    else:
        labels = {
            "brief": "Lähtökohta",
            "objective": "Tavoite",
            "audience": "Yleisö",
            "identity": "Brändi-identiteetti",
            "palette": "Väripaletti",
            "type": "Kirjasimet",
            "mark": "Wordmark",
            "walk": "Sivu sivulta",
            "feat": "Keskeiset ominaisuudet",
            "dec": "Suunnitteluratkaisut",
            "honest": "Tämä on konseptiprojekti. Se ei ole maksavan asiakkaan sivusto, eikä se keksi asiakkaita, arvosteluja tai tuloksia.",
        }
    feats = "".join(f"<li>{x}</li>" for x in m["features"])
    decisions = "".join(
        f"<article><h3>{h}</h3><p class='muted'>{txt}</p></article>" for h, txt in m["decisions_long"]
    )
    alt_d = _alt(lang, m["title"], "Home" if lang == "en" else "Etusivu", "desktop")
    alt_m = _alt(lang, m["title"], "Home" if lang == "en" else "Etusivu", "mobile")
    return f'''
<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow"><a href="{href(lang, page, lang, "work.html")}">{work_lab}</a> / {m["title"]}</p>
    <span class="badge">{concept}</span>
    <h1 class="display" style="margin-top:16px">{m["title"]}</h1>
    <p class="lead">{m["intro"]}</p>
    <div class="btn-row" style="margin-top:24px">
      <a class="btn btn-ink" href="{pre}{p["demo"]}">{demo_l}</a>
      <a class="btn btn-ghost" href="{href(lang, page, lang, "work.html")}">{back}</a>
    </div>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="device-stack folio-stage">
      {desk(_stem(p, "home", "desktop"), alt_d, pre, "eager")}
      {phone(_stem(p, "home", "mobile"), alt_m, pre, "eager")}
    </div>
    <div class="case-copy">
      <div>
        <h2>{labels["brief"]}</h2>
        <p class="muted">{m["brief"]}</p>
      </div>
      <div>
        <h2>{labels["objective"]}</h2>
        <p class="muted">{m["objective"]}</p>
      </div>
      <div>
        <h2>{labels["audience"]}</h2>
        <p class="muted">{m["audience"]}</p>
      </div>
    </div>
    <p class="muted" style="margin-top:24px">{labels["honest"]}</p>
  </div>
</section>
<section class="section band band-line" aria-labelledby="id-title">
  <div class="wrap">
    <p class="eyebrow">{labels["identity"]}</p>
    <h2 id="id-title" class="section-title" style="margin:12px 0 8px">{m["title"]}</h2>
    <div class="case-identity">
      <div>
        <h3>{labels["palette"]}</h3>
        {swatches(p)}
        <h3 style="margin-top:32px">{labels["type"]}</h3>
        {type_spec(p)}
      </div>
      <div>
        <h3>{labels["mark"]}</h3>
        {wordmark(p)}
        <p class="muted" style="margin-top:16px">{m["direction"]}</p>
      </div>
    </div>
  </div>
</section>
<section class="section" aria-labelledby="walk-title">
  <div class="wrap">
    <p class="eyebrow">{labels["walk"]}</p>
    <h2 id="walk-title" class="section-title" style="margin:12px 0 40px">{m["title"]}</h2>
    {walk_items(p, lang, pre)}
  </div>
</section>
<section class="section band band-line">
  <div class="wrap">
    <h2>{labels["feat"]}</h2>
    <ul class="feature-list">{feats}</ul>
    <p class="muted">{m["feature_note"]}</p>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <h2 style="margin-bottom:24px">{labels["dec"]}</h2>
    <div class="why-grid">{decisions}</div>
    <div class="btn-row" style="margin-top:40px">
      <a class="btn btn-ink" href="{pre}{p["demo"]}">{demo_l}</a>
      <a class="btn btn-ghost" href="{href(lang, page, lang, "work.html")}">{back}</a>
    </div>
  </div>
</section>
{cta(lang, page)}
'''


def home(lang):
    # Keep the existing home structure; only swap screenshot paths and the selected-work presentation.
    page = "index.html"
    pre = asset_prefix(lang, 0)
    hale = PROJECTS[0]
    maison = PROJECTS[2]
    if lang == "en":
        hero_alt_d = "Desktop concept preview of Hale Barber Studio"
        hero_alt_m = "Mobile concept preview of Hale Barber Studio"
        maison_alt = "Desktop concept preview of Maison Café"
        hero = ("INDEPENDENT WEB DESIGN STUDIO",
                "Your business deserves a website that works as hard as you do.",
                "We design and build thoughtful, modern websites that help businesses stand out, build trust and turn visitors into customers.",
                "Start a project", "Explore our work", "Currently accepting new projects",
                "Concept project — Hale Barber Studio")
        intro = ("A BETTER DIGITAL PRESENCE", "Your website is often your first impression.",
                 "Make it count. We create websites that reflect the quality of your business, communicate clearly and make it easy for customers to take the next step.",
                 "Concept project — Maison Café")
        services_h = ("WHAT WE DO", "Everything you need to make a stronger impression online.",
                      "Website Design", "Thoughtful visual design built around your brand, customers and business goals.",
                      ["A look and structure that belong to your business, not a template",
                       "Layouts that stay clear on a phone, a tablet and a computer",
                       "A visitor can understand what you do and what to do next"],
                      "Website Development", "Fast, responsive and reliable websites that work beautifully across devices.",
                      ["Clean front-end code that is straightforward to maintain",
                       "Careful work so pages load quickly and stay readable",
                       "A contact path that is ready to receive enquiries",
                       "Technical foundations that help people find you"],
                      "Website Maintenance", "Continued support to keep your website updated, secure and performing well.",
                      ["Updates and small content changes when you need them",
                       "A named contact when something does not work as it should",
                       "Periodic checks so the site stays fast and in good order"])
        work_h = ("SELECTED CONCEPT WORK", "Different businesses. Different digital experiences.", "See all work")
        why_h = "Good websites are built with intention."
        why = [("Designed around you", "Every project should reflect the individual business, not a generic template."),
               ("Built for every screen", "A consistent experience across mobile, tablet and desktop."),
               ("Performance matters", "Fast, accessible and technically sound websites."),
               ("Clear from start to finish", "A straightforward process and transparent communication.")]
        process_h = "From first conversation to launch."
        process = [("Discover", "Understand the business, goals and audience."),
                   ("Design", "Create the visual direction and structure."),
                   ("Develop", "Build and refine the website."),
                   ("Launch", "Test, publish and hand over the finished website.")]
        s1, s2, s3 = "design", "development", "maintenance"
    else:
        hero_alt_d = "Hale Barber Studio -konseptisivuston esikatselu työpöydällä"
        hero_alt_m = "Hale Barber Studio -konseptisivuston esikatselu puhelimella"
        maison_alt = "Maison Café -konseptisivuston esikatselu työpöydällä"
        hero = ("ITSENÄINEN VERKKOSUUNNITTELUSTUDIO",
                "Yrityksesi ansaitsee sivuston, joka tekee töitä yhtä tosissaan kuin sinä.",
                "Suunnittelemme ja rakennamme harkittuja, nykyaikaisia verkkosivuja, joiden avulla yritys erottuu, herättää luottamusta ja muuttaa kävijät asiakkaiksi.",
                "Aloita projekti", "Tutustu töihimme", "Otamme tällä hetkellä vastaan uusia projekteja",
                "Konseptiprojekti — Hale Barber Studio")
        intro = ("VAHVEMPI DIGITAALINEN LÄSNÄOLO", "Verkkosivusi on usein ensivaikutelma.",
                 "Pidä siitä kiinni. Suunnittelemme sivustoja, jotka kertovat yrityksesi laadusta, viestivät selkeästi ja tekevät seuraavan askeleen helpoksi asiakkaalle.",
                 "Konseptiprojekti — Maison Café")
        services_h = ("MITÄ TEEMME", "Kaikki, mitä tarvitset vahvempaan ensivaikutelmaan verkossa.",
                      "Verkkosivujen suunnittelu", "Harkittu visuaalinen suunnittelu, joka rakentuu brändisi, asiakkaidesi ja liiketoimintasi tavoitteiden ympärille.",
                      ["Ilme ja rakenne, jotka kuuluvat juuri sinun yrityksellesi — ei valmista mallipohjaa",
                       "Asettelut, jotka pysyvät selkeinä puhelimessa, tabletilla ja tietokoneella",
                       "Kävijä ymmärtää, mitä teet ja mitä häneltä toivotaan seuraavaksi"],
                      "Verkkosivujen toteutus", "Nopeat, responsiiviset ja luotettavat sivustot, jotka toimivat kaikilla laitteilla.",
                      ["Siistiä front-end-koodia, jota on helppo ylläpitää",
                       "Huolellinen toteutus, jotta sivut latautuvat nopeasti ja pysyvät luettavina",
                       "Yhteydenottopolku, joka on valmis ottamaan viestit vastaan",
                       "Tekninen perusta, joka auttaa asiakkaita löytämään sinut"],
                      "Ylläpito", "Jatkuvaa tukea, jotta sivustosi pysyy ajan tasalla, turvassa ja toimintakykyisenä.",
                      ["Päivityksiä ja pieniä sisältömuutoksia tarvittaessa",
                       "Nimetty yhteys, kun jokin ei toimi odotetusti",
                       "Säännöllisiä tarkistuksia, jotta sivusto pysyy nopeana ja kunnossa"])
        work_h = ("VALITTUJA KONSEPTITÖITÄ", "Eri yrityksiä. Erilaisia digitaalisia kokemuksia.", "Katso kaikki työt")
        why_h = "Hyvät sivustot rakennetaan harkiten."
        why = [("Suunniteltu sinulle", "Jokainen projekti heijastaa juuri kyseistä yritystä, ei geneeristä mallipohjaa."),
               ("Toimii kaikilla näytöillä", "Yhtenäinen kokemus puhelimessa, tabletilla ja tietokoneella."),
               ("Suorituskyvyllä on väliä", "Nopeat, saavutettavat ja teknisesti huolella rakennetut sivustot."),
               ("Selkeä alusta loppuun", "Suora prosessi ja avoin viestintä.")]
        process_h = "Ensimmäisestä keskustelusta julkaisuun."
        process = [("Kartoitus", "Tutustumme yritykseen, tavoitteisiin ja yleisöön."),
                   ("Suunnittelu", "Luomme visuaalisen suunnan ja rakenteen."),
                   ("Toteutus", "Rakennamme ja hiomme sivuston."),
                   ("Julkaisu", "Testaamme, julkaisemme ja luovutamme valmiin sivuston.")]
        s1, s2, s3 = "design", "development", "maintenance"

    why_html = "".join(
        f'<article class="why-card"><p class="idx">0{i}</p><h3>{t}</h3><p class="muted">{d}</p></article>'
        for i, (t, d) in enumerate(why, 1)
    )
    process_html = "".join(
        f'<li><div class="dot">0{i}</div><div><h3>{t}</h3><p class="muted">{d}</p></div></li>'
        for i, (t, d) in enumerate(process, 1)
    )
    lis1 = "".join(f"<li>{x}</li>" for x in services_h[4])
    lis2 = "".join(f"<li>{x}</li>" for x in services_h[7])
    lis3 = "".join(f"<li>{x}</li>" for x in services_h[10])

    return f'''
<section class="hero">
  <div class="wrap hero-grid">
    <div class="reveal">
      <p class="eyebrow">{hero[0]}</p>
      <h1 class="display">{hero[1]}</h1>
      <p class="lead">{hero[2]}</p>
      <div class="btn-row">
        <a class="btn btn-ink" href="{href(lang, page, lang, "contact.html")}">{hero[3]}</a>
        <a class="btn btn-ghost" href="{href(lang, page, lang, "work.html")}">{hero[4]}</a>
      </div>
      <p class="avail"><i aria-hidden="true"></i> {hero[5]}</p>
    </div>
    <div class="device-stack reveal" style="animation-delay:.12s">
      {desk("images/work/hale/home-desktop", hero_alt_d, pre, "eager")}
      {phone("images/work/hale/home-mobile", hero_alt_m, pre, "eager")}
      <p class="concept-label">{hero[6]}</p>
    </div>
  </div>
</section>
<section class="section band band-line" aria-labelledby="intro-title">
  <div class="wrap split">
    <div>
      <p class="eyebrow">{intro[0]}</p>
      <h2 id="intro-title" class="section-title" style="margin:12px 0 16px">{intro[1]}</h2>
      <p class="lead">{intro[2]}</p>
    </div>
    <figure class="intro-visual">
      {desk("images/work/maison/home-desktop", maison_alt, pre)}
      <figcaption>{intro[3]}</figcaption>
    </figure>
  </div>
</section>
<section class="section" aria-labelledby="services-title">
  <div class="wrap">
    <p class="eyebrow">{services_h[0]}</p>
    <h2 id="services-title" class="section-title" style="margin:12px 0 32px">{services_h[1]}</h2>
    <article class="service-block" id="{s1}">
      <div class="num">01</div>
      <div>
        <h3>{services_h[2]}</h3>
        <p>{services_h[3]}</p>
      </div>
      <ul>{lis1}</ul>
    </article>
  </div>
  <div class="service-dark">
    <article class="service-block" id="{s2}">
      <div class="num">02</div>
      <div>
        <h3>{services_h[5]}</h3>
        <p>{services_h[6]}</p>
      </div>
      <ul>{lis2}</ul>
    </article>
  </div>
  <div class="wrap">
    <article class="service-block service-framed" id="{s3}">
      <div class="num">03</div>
      <div>
        <h3>{services_h[8]}</h3>
        <p>{services_h[9]}</p>
      </div>
      <ul>{lis3}</ul>
    </article>
  </div>
</section>
<section class="section home-work" aria-labelledby="work-title">
  <div class="wrap">
    <div class="section-head">
      <div>
        <p class="eyebrow">{work_h[0]}</p>
        <h2 id="work-title" class="section-title" style="margin-top:12px">{work_h[1]}</h2>
      </div>
    </div>
    {home_teaser(lang, page)}
    <div class="home-teaser-foot">
      <a class="btn btn-ink" href="{href(lang, page, lang, "work.html")}">{work_h[2]}</a>
    </div>
  </div>
</section>
<section class="section" aria-labelledby="why-title">
  <div class="wrap">
    <h2 id="why-title" class="section-title" style="margin-bottom:40px">{why_h}</h2>
    <div class="why-grid">{why_html}</div>
  </div>
</section>
<section class="section band band-line" aria-labelledby="process-title">
  <div class="wrap">
    <h2 id="process-title" class="section-title" style="margin-bottom:40px">{process_h}</h2>
    <ol class="timeline">{process_html}</ol>
  </div>
</section>
{pricing(lang, page)}
{cta(lang, page)}
'''


def main():
    for proj in PROJECTS:
        for lang in ("fi", "en"):
            proj[lang].setdefault("desc", proj[lang]["intro"])
    b.PROJECTS = PROJECTS
    b.work_page = work_page
    b.work_projects = work_projects
    b.case_page = case_page
    b.home = home
    b.BUILDERS["index.html"] = home
    b.BUILDERS["work.html"] = work_page
    META["fi"]["work.html"] = (
        "Työt — WEBAUR",
        "WEBAURin konseptiprojektit: Hale Barber Studio, Alto Detail ja Maison Café — monisivuiset, toimivat demosivustot.",
    )
    META["en"]["work.html"] = (
        "Work — WEBAUR",
        "Concept projects by WEBAUR: Hale Barber Studio, Alto Detail and Maison Café — multi-page working demo websites.",
    )
    b.build()


if __name__ == "__main__":
    main()
