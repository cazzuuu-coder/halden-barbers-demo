#!/usr/bin/env python3
"""Generate bilingual WEBAUR v3 pages. Finnish is the default language at the site root; English lives in /en/."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

NAV = [
    ("index.html", "home", "Home", "Etusivu"),
    ("services.html", "services", "Services", "Palvelut"),
    ("work.html", "work", "Work", "Työt"),
    ("about.html", "about", "About", "Meistä"),
    ("contact.html", "contact", "Contact", "Yhteystiedot"),
]

PROJECTS = [
    dict(
        slug="barber-studio",
        desk="images/work/hale-desktop",
        mob="images/work/hale-mobile",
        demo="demos/barber-studio/index.html",
        en=dict(title="Hale Barber Studio", category="Barber · Editorial",
                desc="A dark, editorial concept for an independent barbershop: services, photography and an appointment invitation."),
        fi=dict(title="Hale Barber Studio", category="Parturi · Toimituksellinen",
                desc="Tumma, toimituksellinen konsepti itsenäiselle parturille: palvelut, valokuvat ja ajanvarauskutsu."),
    ),
    dict(
        slug="detailing",
        desk="images/work/alto-desktop",
        mob="images/work/alto-mobile",
        demo="demos/detailing/index.html",
        en=dict(title="Alto Detail", category="Automotive detailing",
                desc="A sophisticated detailing brand with clearly priced packages, photography and a before-and-after comparison."),
        fi=dict(title="Alto Detail", category="Autonhoito ja detailing",
                desc="Huoliteltu detailing-brändi selkeine paketteineen, kuvineen ja ennen–jälkeen-vertailuineen."),
    ),
    dict(
        slug="maison-cafe",
        desk="images/work/maison-desktop",
        mob="images/work/maison-mobile",
        demo="demos/maison-cafe/index.html",
        en=dict(title="Maison Café", category="Café · Hospitality",
                desc="A warm, typographic café site with a menu, featured items, hours, location and a reservation invitation."),
        fi=dict(title="Maison Café", category="Kahvila · Ravintola",
                desc="Lämmin, typografinen kahvilasivusto ruokalistalla, nostoilla, aukioloilla, sijainnilla ja pöytävarauskutsulla."),
    ),
]


def asset_prefix(lang, depth):
    # depth 0 = site root files (FI) or does not apply
    # For FI: depth 0 -> ''; depth 1 (work/) -> '../'
    # For EN: depth 0 (en/*.html) -> '../'; depth 1 (en/work/) -> '../../'
    if lang == "fi":
        return "../" * depth
    return "../" * (depth + 1)


def href(lang, page, dest_lang, dest_page):
    """Relative link from a page in `lang` to dest_page in dest_lang."""
    src_depth = 1 if page.startswith("work/") else 0
    dst_depth = 1 if dest_page.startswith("work/") else 0
    # Climb to site root, then down to destination.
    climb = asset_prefix(lang, src_depth)
    if dest_lang == "en":
        return f"{climb}en/{dest_page}"
    return f"{climb}{dest_page}"


def logo(lang, page):
    pre = asset_prefix(lang, 1 if page.startswith("work/") else 0)
    home = f"{pre}index.html" if lang == "fi" else f"{pre}en/index.html"
    return f'<a class="logo" href="{home}" aria-label="WEBAUR"><span class="wm">WEB<span class="wm-a">A</span>UR</span></a>'


def header(lang, page, active):
    pre = asset_prefix(lang, 1 if page.startswith("work/") else 0)
    links = []
    for dest, key, en, fi in NAV:
        label = en if lang == "en" else fi
        url = href(lang, page, lang, dest)
        cur = ' aria-current="page"' if key == active else ""
        links.append(f'<li><a href="{url}"{cur}>{label}</a></li>')
    # language switcher maps to counterpart
    fi_url = href(lang, page, "fi", page if not page.startswith("en/") else page)
    # page is stored without lang prefix
    fi_url = href(lang, page, "fi", page)
    en_url = href(lang, page, "en", page)
    if lang == "fi":
        fi_el = '<span aria-current="true">FI</span>'
        en_el = f'<a href="{en_url}" lang="en" hreflang="en">EN</a>'
    else:
        fi_el = f'<a href="{fi_url}" lang="fi" hreflang="fi">FI</a>'
        en_el = '<span aria-current="true">EN</span>'
    cta = "Start a project" if lang == "en" else "Aloita projekti"
    cta_url = href(lang, page, lang, "contact.html")
    menu = "Open menu" if lang == "en" else "Avaa valikko"
    skip = "Skip to content" if lang == "en" else "Siirry sisältöön"
    return f'''<a class="skip" href="#content">{skip}</a>
<header class="site-header">
  <div class="wrap nav">
    {logo(lang, page)}
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="nav-panel" aria-label="{menu}"><span></span><span></span></button>
    <div class="nav-panel" id="nav-panel">
      <ul class="nav-links">
        {"".join(links)}
      </ul>
      <nav class="lang-switch" aria-label="Language">{fi_el}<span class="sep" aria-hidden="true">/</span>{en_el}</nav>
      <a class="nav-cta" href="{cta_url}">{cta}</a>
    </div>
  </div>
</header>'''


def footer(lang, page):
    pre = asset_prefix(lang, 1 if page.startswith("work/") else 0)
    t = {
        "en": dict(desc="Independent web design studio. We design and build modern websites that help businesses stand out and turn visitors into customers.",
                   nav="Navigate", services="Services", contact="Contact",
                   email_l="Email (placeholder — not a live address):",
                   privacy="Privacy Policy", copy="© 2026 WEBAUR. All rights reserved.",
                   indie="Independent design studio.",
                   d="Website Design", dev="Website Development", m="Website Maintenance"),
        "fi": dict(desc="Itsenäinen verkkosunnittelustudio. Suunnittelemme ja rakennamme nykyaikaisia sivustoja, jotka auttavat yritystä erottumaan ja muuttamaan kävijät asiakkaiksi.",
                   nav="Sivusto", services="Palvelut", contact="Yhteys",
                   email_l="Sähköposti (paikkamerkki — ei ole käytössä oleva osoite):",
                   privacy="Tietosuoja", copy="© 2026 WEBAUR. Kaikki oikeudet pidätetään.",
                   indie="Itsenäinen suunnittelustudio.",
                   d="Verkkosivujen suunnittelu", dev="Verkkosivujen toteutus", m="Ylläpito"),
    }[lang]
    # typo fix: verkkosunnittelustudio -> verkkosuunnittelustudio
    if lang == "fi":
        t["desc"] = "Itsenäinen verkkosuunnittelustudio. Suunnittelemme ja rakennamme nykyaikaisia sivustoja, jotka auttavat yritystä erottumaan ja muuttamaan kävijät asiakkaiksi."
    def l(dest, label):
        return f'<li><a href="{href(lang, page, lang, dest)}">{label}</a></li>'
    fi_url = href(lang, page, "fi", page)
    en_url = href(lang, page, "en", page)
    return f'''<footer class="site-footer">
  <div class="wrap footer-grid">
    <div>
      {logo(lang, page)}
      <p class="footer-note" style="margin-top:16px;max-width:28rem">{t["desc"]}</p>
    </div>
    <div>
      <ul class="footer-col">
        <li><strong>{t["nav"]}</strong></li>
        {"".join(l(dest, (en if lang=="en" else fi)) for dest, key, en, fi in NAV)}
      </ul>
    </div>
    <div>
      <ul class="footer-col">
        <li><strong>{t["services"]}</strong></li>
        {l("services.html#design", t["d"])}
        {l("services.html#development", t["dev"])}
        {l("services.html#maintenance", t["m"])}
      </ul>
    </div>
    <div>
      <ul class="footer-col">
        <li><strong>{t["contact"]}</strong></li>
        <li>{t["email_l"]}<br><span class="placeholder">hello@[your-domain]</span></li>
        {l("privacy.html", t["privacy"])}
        <li class="lang-switch" style="margin-top:8px"><a href="{fi_url}" lang="fi" hreflang="fi"{" aria-current=\"true\"" if lang=="fi" else ""}>FI</a><span class="sep" aria-hidden="true"> / </span><a href="{en_url}" lang="en" hreflang="en"{" aria-current=\"true\"" if lang=="en" else ""}>EN</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap legal">
    <span>{t["copy"]}</span>
    <span>{t["indie"]}</span>
  </div>
</footer>'''


def cta(lang, page):
    if lang == "en":
        k, h, p, b = "START A PROJECT", "Let’s build something your customers will remember.", "Tell us about your business and what you would like to improve. We’ll take it from there.", "Start a project"
    else:
        k, h, p, b = "ALOITA PROJEKTI", "Rakennetaan jotain, jonka asiakkaasi muistavat.", "Kerro yrityksestäsi ja siitä, mitä haluaisit parantaa. Me hoidamme loput.", "Aloita projekti"
    return f'''<section class="cta-band" aria-labelledby="cta-title">
  <div class="wrap">
    <p class="eyebrow" style="color:#c5c8c2">{k}</p>
    <h2 id="cta-title" class="display" style="margin:12px 0 16px">{h}</h2>
    <p class="lead">{p}</p>
    <p style="margin-top:32px"><a class="btn btn-ink" href="{href(lang, page, lang, "contact.html")}">{b}</a></p>
  </div>
</section>'''


def pic(stem, alt, prefix, loading="lazy"):
    return f'''<picture>
  <source type="image/webp" srcset="{prefix}{stem}.webp" />
  <img src="{prefix}{stem}.jpg" alt="{alt}" loading="{loading}" decoding="async" />
</picture>'''


def device_desktop(stem, alt, prefix, loading="lazy"):
    return f'''<div class="device-desktop">
  <div class="chrome" aria-hidden="true"><i></i><i></i><i></i></div>
  <div class="screen">{pic(stem, alt, prefix, loading)}</div>
</div>'''


def device_mobile(stem, alt, prefix, loading="lazy"):
    return f'''<div class="device-mobile">
  <div class="notch" aria-hidden="true"></div>
  <div class="screen">{pic(stem, alt, prefix, loading)}</div>
</div>'''


def page_shell(lang, page, title, description, active, body):
    depth = 1 if page.startswith("work/") else 0
    pre = asset_prefix(lang, depth)
    css, js, fc = f"{pre}css/styles.css", f"{pre}js/main.js", f"{pre}js/form-config.js"
    fav, ico, apple = f"{pre}images/brand/favicon.svg", f"{pre}images/brand/favicon-32.png", f"{pre}images/brand/apple-touch-icon.png"
    path_fi = page
    path_en = f"en/{page}"
    canon_path = path_fi if lang == "fi" else path_en
    if page == "index.html":
        canon_path = "" if lang == "fi" else "en/"
        path_en = "en/"
        path_fi = ""
    canon = f"https://webaur.com/{canon_path}"
    fi_abs = f"https://webaur.com/{path_fi}"
    en_abs = f"https://webaur.com/{path_en}"
    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title}</title>
  <meta name="description" content="{description}" />
  <link rel="canonical" href="{canon}" />
  <link rel="alternate" hreflang="fi" href="{fi_abs}" />
  <link rel="alternate" hreflang="en" href="{en_abs}" />
  <link rel="alternate" hreflang="x-default" href="{fi_abs}" />
  <meta property="og:type" content="website" />
  <meta property="og:locale" content="{"fi_FI" if lang=="fi" else "en_GB"}" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{description}" />
  <meta property="og:url" content="{canon}" />
  <meta property="og:image" content="https://webaur.com/images/og/og-default.jpg" />
  <meta name="twitter:card" content="summary_large_image" />
  <link rel="icon" href="{fav}" type="image/svg+xml" />
  <link rel="icon" href="{ico}" type="image/png" sizes="32x32" />
  <link rel="apple-touch-icon" href="{apple}" />
  <link rel="stylesheet" href="{css}" />
</head>
<body>
{header(lang, page, active)}
<main id="content">
{body}
</main>
{footer(lang, page)}
<script src="{fc}"></script>
<script src="{js}" defer></script>
</body>
</html>
'''


def pricing(lang, page):
    if lang == "en":
        return f'''
<section class="section" id="pricing" aria-labelledby="pricing-title">
  <div class="wrap">
    <p class="eyebrow">PACKAGES</p>
    <h2 id="pricing-title" class="section-title" style="margin:12px 0 32px">Straightforward packages. Built around your needs.</h2>
    <div class="price-grid">
      <article class="price-card">
        <h3>Starter</h3>
        <p class="price">€490</p>
        <p class="muted">A professional one-page presence.</p>
        <ul>
          <li>One-page website</li>
          <li>Responsive design</li>
          <li>Services presentation</li>
          <li>Contact information</li>
          <li>Basic SEO setup</li>
          <li>Contact CTA</li>
        </ul>
        <a class="btn btn-ghost" href="{href(lang, page, lang, "contact.html")}?package=starter#form">Choose Starter</a>
      </article>
      <article class="price-card featured">
        <span class="popular">POPULAR</span>
        <h3>Business</h3>
        <p class="price">€890</p>
        <p class="muted">A more complete website for a growing business.</p>
        <ul>
          <li>4–6 pages</li>
          <li>Custom visual design</li>
          <li>Responsive development</li>
          <li>Contact form</li>
          <li>Services pages</li>
          <li>Maps integration where relevant</li>
          <li>SEO foundations</li>
        </ul>
        <a class="btn btn-accent" href="{href(lang, page, lang, "contact.html")}?package=business#form">Choose Business</a>
      </article>
      <article class="price-card">
        <h3>Premium</h3>
        <p class="price">€1,490</p>
        <p class="muted">A more advanced site, agreed in more detail.</p>
        <ul>
          <li>6–10 pages</li>
          <li>Advanced custom design</li>
          <li>More sophisticated page layouts</li>
          <li>Animations and interactions</li>
          <li>Analytics integration</li>
          <li>SEO foundations</li>
          <li>Additional agreed functionality</li>
        </ul>
        <a class="btn btn-ghost" href="{href(lang, page, lang, "contact.html")}?package=premium#form">Choose Premium</a>
      </article>
    </div>
    <div class="price-notes">
      <div>
        <h3>Please note</h3>
        <ul>
          <li>Prices excl. VAT (Finnish VAT 25.5% added).</li>
          <li>The final price depends on the agreed project scope.</li>
          <li>Domain registration and hosting are not included.</li>
        </ul>
      </div>
      <div>
        <h3>Not included</h3>
        <ul>
          <li>Domain and website hosting</li>
          <li>Photography or copywriting beyond the agreed scope</li>
          <li>Ongoing maintenance (available separately)</li>
          <li>Pages or features outside the chosen package</li>
        </ul>
      </div>
    </div>
    <div class="price-follow">
      <h3>Not sure which package is right for you?</h3>
      <p class="muted">Tell us about your project and we’ll help you find the right solution.</p>
      <p style="margin-top:16px"><a class="btn btn-ink" href="{href(lang, page, lang, "contact.html")}">Start a project</a></p>
    </div>
  </div>
</section>'''
    return f'''
<section class="section" id="pricing" aria-labelledby="pricing-title">
  <div class="wrap">
    <p class="eyebrow">PAKETIT</p>
    <h2 id="pricing-title" class="section-title" style="margin:12px 0 32px">Selkeät paketit. Räätälöity tarpeesi mukaan.</h2>
    <div class="price-grid">
      <article class="price-card">
        <h3>Aloitus</h3>
        <p class="price">€490</p>
        <p class="muted">Ammattimainen yhden sivun verkkoläsnäolo.</p>
        <ul>
          <li>Yhden sivun verkkosivusto</li>
          <li>Responsiivinen suunnittelu</li>
          <li>Palveluiden esittely</li>
          <li>Yhteystiedot</li>
          <li>Perustason hakukoneoptimointi</li>
          <li>Yhteydenottokehote</li>
        </ul>
        <a class="btn btn-ghost" href="{href(lang, page, lang, "contact.html")}?package=starter#form">Valitse Aloitus</a>
      </article>
      <article class="price-card featured">
        <span class="popular">SUOSITUIN</span>
        <h3>Yritys</h3>
        <p class="price">€890</p>
        <p class="muted">Täydellisempi sivusto kasvavalle yritykselle.</p>
        <ul>
          <li>4–6 sivua</li>
          <li>Räätälöity visuaalinen suunnittelu</li>
          <li>Responsiivinen toteutus</li>
          <li>Yhteydenottolomake</li>
          <li>Palvelusivut</li>
          <li>Karttaintegraatio tarvittaessa</li>
          <li>Hakukoneoptimoinnin perusta</li>
        </ul>
        <a class="btn btn-accent" href="{href(lang, page, lang, "contact.html")}?package=business#form">Valitse Yritys</a>
      </article>
      <article class="price-card">
        <h3>Premium</h3>
        <p class="price">€1,490</p>
        <p class="muted">Vaativampi sivusto, jonka sisältö sovitaan tarkemmin.</p>
        <ul>
          <li>6–10 sivua</li>
          <li>Pidemmälle viety räätälöity suunnittelu</li>
          <li>Monipuolisemmat sivuasettelut</li>
          <li>Animaatiot ja vuorovaikutus</li>
          <li>Analytiikan kytkentä</li>
          <li>Hakukoneoptimoinnin perusta</li>
          <li>Muut yhdessä sovitut toiminnot</li>
        </ul>
        <a class="btn btn-ghost" href="{href(lang, page, lang, "contact.html")}?package=premium#form">Valitse Premium</a>
      </article>
    </div>
    <div class="price-notes">
      <div>
        <h3>Huomioithan</h3>
        <ul>
          <li>Hinnat ovat ilman arvonlisäveroa (ALV 25,5 % lisätään).</li>
          <li>Lopullinen hinta määräytyy yhdessä sovitun työn laajuuden mukaan.</li>
          <li>Verkkotunnus ja palvelintila eivät sisälly hintaan.</li>
        </ul>
      </div>
      <div>
        <h3>Ei sisälly</h3>
        <ul>
          <li>Verkkotunnus ja sivuston ylläpitoalusta (hosting)</li>
          <li>Valokuvaus tai tekstien tuottaminen sovitun työn yli</li>
          <li>Jatkuva ylläpito (saatavilla erikseen)</li>
          <li>Valitun paketin ulkopuoliset sivut tai ominaisuudet</li>
        </ul>
      </div>
    </div>
    <div class="price-follow">
      <h3>Etkö ole varma, mikä paketti sopii sinulle?</h3>
      <p class="muted">Kerro projektistasi, niin autamme löytämään sopivan ratkaisun.</p>
      <p style="margin-top:16px"><a class="btn btn-ink" href="{href(lang, page, lang, "contact.html")}">Aloita projekti</a></p>
    </div>
  </div>
</section>'''


def work_projects(lang, page, layouts=True):
    pre = asset_prefix(lang, 1 if page.startswith("work/") else 0)
    concept = "Concept project" if lang == "en" else "Konseptiprojekti"
    view = "View project" if lang == "en" else "Katso projekti"
    demo_l = "View live demo" if lang == "en" else "Avaa demo"
    blocks = []
    for i, p in enumerate(PROJECTS):
        meta = p[lang]
        alt_d = f"Desktop preview of the {p['en']['title']} concept website"
        alt_m = f"Mobile preview of the {p['en']['title']} concept website"
        if lang == "fi":
            alt_d = f"{p['fi']['title']} -konseptisivuston esikatselu työpöydällä"
            alt_m = f"{p['fi']['title']} -konseptisivuston esikatselu puhelimella"
        stack = f'''<div class="device-stack project-stage">
      {device_desktop(p["desk"], alt_d, pre)}
      {device_mobile(p["mob"], alt_m, pre)}
    </div>'''
        frames = stack
        copy = f'''<div class="project-copy">
      <span class="badge">{concept}</span>
      <p class="kicker" style="margin-top:12px">{meta["category"]}</p>
      <h2>{meta["title"]}</h2>
      <p class="muted">{meta["desc"]}</p>
      <div class="project-actions">
        <a class="btn btn-ink" href="{pre}{p["demo"]}">{demo_l}</a>
        <a class="btn btn-ghost" href="{href(lang, page, lang, "work/"+p["slug"]+".html")}">{view}</a>
      </div>
    </div>'''
        if not layouts:
            blocks.append(f'<article class="project-split">{frames}{copy}</article>')
            continue
        if i == 0:
            blocks.append(f'''<article class="project-feature is-dark">
  <div class="inner">{frames}{copy}</div>
</article>''')
        elif i == 1:
            blocks.append(f'<article class="project-split">{copy}{frames}</article>')
        else:
            blocks.append(f'<article class="project-wide wrap-wide"><div class="wrap">{copy}{frames}</div></article>')
    return "\n".join(blocks)


def home(lang):
    page = "index.html"
    pre = asset_prefix(lang, 0)
    if lang == "en":
        return f'''
<section class="hero">
  <div class="wrap hero-grid">
    <div class="reveal">
      <p class="eyebrow">INDEPENDENT WEB DESIGN STUDIO</p>
      <h1 class="display">Your business deserves a website that works as hard as you do.</h1>
      <p class="lead">We design and build thoughtful, modern websites that help businesses stand out, build trust and turn visitors into customers.</p>
      <div class="btn-row">
        <a class="btn btn-ink" href="{href(lang, page, lang, "contact.html")}">Start a project</a>
        <a class="btn btn-ghost" href="{href(lang, page, lang, "work.html")}">Explore our work</a>
      </div>
      <p class="avail"><i aria-hidden="true"></i> Currently accepting new projects</p>
    </div>
    <div class="device-stack reveal" style="animation-delay:.12s">
      {device_desktop("images/work/hale-desktop", "Desktop concept preview of Hale Barber Studio", pre, "eager")}
      {device_mobile("images/work/hale-mobile", "Mobile concept preview of Hale Barber Studio", pre, "eager")}
      <p class="concept-label">Concept project — Hale Barber Studio</p>
    </div>
  </div>
</section>
<section class="section band band-line" aria-labelledby="intro-title">
  <div class="wrap split">
    <div>
      <p class="eyebrow">A BETTER DIGITAL PRESENCE</p>
      <h2 id="intro-title" class="section-title" style="margin:12px 0 16px">Your website is often your first impression.</h2>
      <p class="lead">Make it count. We create websites that reflect the quality of your business, communicate clearly and make it easy for customers to take the next step.</p>
    </div>
    <figure class="intro-visual">
      {device_desktop("images/work/maison-desktop", "Desktop concept preview of Maison Café", pre)}
      <figcaption>Concept project — Maison Café</figcaption>
    </figure>
  </div>
</section>
<section class="section" aria-labelledby="services-title">
  <div class="wrap">
    <p class="eyebrow">WHAT WE DO</p>
    <h2 id="services-title" class="section-title" style="margin:12px 0 32px">Everything you need to make a stronger impression online.</h2>
    <article class="service-block" id="design">
      <div class="num">01</div>
      <div>
        <h3>Website Design</h3>
        <p>Thoughtful visual design built around your brand, customers and business goals.</p>
      </div>
      <ul>
        <li>A look and structure that belong to your business, not a template</li>
        <li>Layouts that stay clear on a phone, a tablet and a computer</li>
        <li>A visitor can understand what you do and what to do next</li>
      </ul>
    </article>
  </div>
  <div class="service-dark">
    <article class="service-block" id="development">
      <div class="num">02</div>
      <div>
        <h3>Website Development</h3>
        <p>Fast, responsive and reliable websites that work beautifully across devices.</p>
      </div>
      <ul>
        <li>Clean front-end code that is straightforward to maintain</li>
        <li>Careful work so pages load quickly and stay readable</li>
        <li>A contact path that is ready to receive enquiries</li>
        <li>Technical foundations that help people find you</li>
      </ul>
    </article>
  </div>
  <div class="wrap">
    <article class="service-block service-framed" id="maintenance">
      <div class="num">03</div>
      <div>
        <h3>Website Maintenance</h3>
        <p>Continued support to keep your website updated, secure and performing well.</p>
      </div>
      <ul>
        <li>Updates and small content changes when you need them</li>
        <li>A named contact when something does not work as it should</li>
        <li>Periodic checks so the site stays fast and in good order</li>
      </ul>
    </article>
  </div>
</section>
<section class="section" style="padding-bottom:0" aria-labelledby="work-title">
  <div class="wrap section-head" style="margin-bottom:24px">
    <div>
      <p class="eyebrow">SELECTED CONCEPT WORK</p>
      <h2 id="work-title" class="section-title" style="margin-top:12px">Different businesses. Different digital experiences.</h2>
    </div>
    <a class="btn btn-ghost" href="{href(lang, page, lang, "work.html")}">All work</a>
  </div>
  {work_projects(lang, page)}
</section>
<section class="section" aria-labelledby="why-title">
  <div class="wrap">
    <h2 id="why-title" class="section-title" style="margin-bottom:40px">Good websites are built with intention.</h2>
    <div class="why-grid">
      <article class="why-card"><p class="idx">01</p><h3>Designed around you</h3><p class="muted">Every project should reflect the individual business, not a generic template.</p></article>
      <article class="why-card"><p class="idx">02</p><h3>Built for every screen</h3><p class="muted">A consistent experience across mobile, tablet and desktop.</p></article>
      <article class="why-card"><p class="idx">03</p><h3>Performance matters</h3><p class="muted">Fast, accessible and technically sound websites.</p></article>
      <article class="why-card"><p class="idx">04</p><h3>Clear from start to finish</h3><p class="muted">A straightforward process and transparent communication.</p></article>
    </div>
  </div>
</section>
<section class="section band band-line" aria-labelledby="process-title">
  <div class="wrap">
    <h2 id="process-title" class="section-title" style="margin-bottom:40px">From first conversation to launch.</h2>
    <ol class="timeline">
      <li><div class="dot">01</div><div><h3>Discover</h3><p class="muted">Understand the business, goals and audience.</p></div></li>
      <li><div class="dot">02</div><div><h3>Design</h3><p class="muted">Create the visual direction and structure.</p></div></li>
      <li><div class="dot">03</div><div><h3>Develop</h3><p class="muted">Build and refine the website.</p></div></li>
      <li><div class="dot">04</div><div><h3>Launch</h3><p class="muted">Test, publish and hand over the finished website.</p></div></li>
    </ol>
  </div>
</section>
{pricing(lang, page)}
{cta(lang, page)}
'''
    return f'''
<section class="hero">
  <div class="wrap hero-grid">
    <div class="reveal">
      <p class="eyebrow">ITSENÄINEN VERKKOSUUNNITTELUSTUDIO</p>
      <h1 class="display">Yrityksesi ansaitsee sivuston, joka tekee töitä yhtä tosissaan kuin sinä.</h1>
      <p class="lead">Suunnittelemme ja rakennamme harkittuja, nykyaikaisia verkkosivuja, joiden avulla yritys erottuu, herättää luottamusta ja muuttaa kävijät asiakkaiksi.</p>
      <div class="btn-row">
        <a class="btn btn-ink" href="{href(lang, page, lang, "contact.html")}">Aloita projekti</a>
        <a class="btn btn-ghost" href="{href(lang, page, lang, "work.html")}">Tutustu töihimme</a>
      </div>
      <p class="avail"><i aria-hidden="true"></i> Otamme tällä hetkellä vastaan uusia projekteja</p>
    </div>
    <div class="device-stack reveal" style="animation-delay:.12s">
      {device_desktop("images/work/hale-desktop", "Hale Barber Studio -konseptisivuston esikatselu työpöydällä", pre, "eager")}
      {device_mobile("images/work/hale-mobile", "Hale Barber Studio -konseptisivuston esikatselu puhelimella", pre, "eager")}
      <p class="concept-label">Konseptiprojekti — Hale Barber Studio</p>
    </div>
  </div>
</section>
<section class="section band band-line" aria-labelledby="intro-title">
  <div class="wrap split">
    <div>
      <p class="eyebrow">VAHVEMPI DIGITAALINEN LÄSNÄOLO</p>
      <h2 id="intro-title" class="section-title" style="margin:12px 0 16px">Verkkosivusi on usein ensivaikutelma.</h2>
      <p class="lead">Pidä siitä kiinni. Suunnittelemme sivustoja, jotka kertovat yrityksesi laadusta, viestivät selkeästi ja tekevät seuraavan askeleen helpoksi asiakkaalle.</p>
    </div>
    <figure class="intro-visual">
      {device_desktop("images/work/maison-desktop", "Maison Café -konseptisivuston esikatselu työpöydällä", pre)}
      <figcaption>Konseptiprojekti — Maison Café</figcaption>
    </figure>
  </div>
</section>
<section class="section" aria-labelledby="services-title">
  <div class="wrap">
    <p class="eyebrow">MITÄ TEEMME</p>
    <h2 id="services-title" class="section-title" style="margin:12px 0 32px">Kaikki, mitä tarvitset vahvempaan ensivaikutelmaan verkossa.</h2>
    <article class="service-block" id="design">
      <div class="num">01</div>
      <div>
        <h3>Verkkosivujen suunnittelu</h3>
        <p>Harkittu visuaalinen suunnittelu, joka rakentuu brändisi, asiakkaidesi ja liiketoimintasi tavoitteiden ympärille.</p>
      </div>
      <ul>
        <li>Ilme ja rakenne, jotka kuuluvat juuri sinun yrityksellesi — ei valmista mallipohjaa</li>
        <li>Asettelut, jotka pysyvät selkeinä puhelimessa, tabletilla ja tietokoneella</li>
        <li>Kävijä ymmärtää, mitä teet ja mitä häneltä toivotaan seuraavaksi</li>
      </ul>
    </article>
  </div>
  <div class="service-dark">
    <article class="service-block" id="development">
      <div class="num">02</div>
      <div>
        <h3>Verkkosivujen toteutus</h3>
        <p>Nopeat, responsiiviset ja luotettavat sivustot, jotka toimivat kaikilla laitteilla.</p>
      </div>
      <ul>
        <li>Siistiä front-end-koodia, jota on helppo ylläpitää</li>
        <li>Huolellinen toteutus, jotta sivut latautuvat nopeasti ja pysyvät luettavina</li>
        <li>Yhteydenottopolku, joka on valmis ottamaan viestit vastaan</li>
        <li>Tekninen perusta, joka auttaa asiakkaita löytämään sinut</li>
      </ul>
    </article>
  </div>
  <div class="wrap">
    <article class="service-block service-framed" id="maintenance">
      <div class="num">03</div>
      <div>
        <h3>Ylläpito</h3>
        <p>Jatkuvaa tukea, jotta sivustosi pysyy ajan tasalla, turvassa ja toimintakykyisenä.</p>
      </div>
      <ul>
        <li>Päivityksiä ja pieniä sisältömuutoksia tarvittaessa</li>
        <li>Nimetty yhteys, kun jokin ei toimi odotetusti</li>
        <li>Säännöllisiä tarkistuksia, jotta sivusto pysyy nopeana ja kunnossa</li>
      </ul>
    </article>
  </div>
</section>
<section class="section" style="padding-bottom:0" aria-labelledby="work-title">
  <div class="wrap section-head" style="margin-bottom:24px">
    <div>
      <p class="eyebrow">VALITTUJA KONSEPTITÖITÄ</p>
      <h2 id="work-title" class="section-title" style="margin-top:12px">Eri yrityksiä. Erilaisia digitaalisia kokemuksia.</h2>
    </div>
    <a class="btn btn-ghost" href="{href(lang, page, lang, "work.html")}">Kaikki työt</a>
  </div>
  {work_projects(lang, page)}
</section>
<section class="section" aria-labelledby="why-title">
  <div class="wrap">
    <h2 id="why-title" class="section-title" style="margin-bottom:40px">Hyvät sivustot rakennetaan harkiten.</h2>
    <div class="why-grid">
      <article class="why-card"><p class="idx">01</p><h3>Suunniteltu sinulle</h3><p class="muted">Jokainen projekti heijastaa juuri kyseistä yritystä, ei geneeristä mallipohjaa.</p></article>
      <article class="why-card"><p class="idx">02</p><h3>Toimii kaikilla näytöillä</h3><p class="muted">Yhtenäinen kokemus puhelimessa, tabletilla ja tietokoneella.</p></article>
      <article class="why-card"><p class="idx">03</p><h3>Suorituskyvyllä on väliä</h3><p class="muted">Nopeat, saavutettavat ja teknisesti huolella rakennetut sivustot.</p></article>
      <article class="why-card"><p class="idx">04</p><h3>Selkeä alusta loppuun</h3><p class="muted">Suora prosessi ja avoin viestintä.</p></article>
    </div>
  </div>
</section>
<section class="section band band-line" aria-labelledby="process-title">
  <div class="wrap">
    <h2 id="process-title" class="section-title" style="margin-bottom:40px">Ensimmäisestä keskustelusta julkaisuun.</h2>
    <ol class="timeline">
      <li><div class="dot">01</div><div><h3>Kartoitus</h3><p class="muted">Tutustumme yritykseen, tavoitteisiin ja yleisöön.</p></div></li>
      <li><div class="dot">02</div><div><h3>Suunnittelu</h3><p class="muted">Luomme visuaalisen suunnan ja rakenteen.</p></div></li>
      <li><div class="dot">03</div><div><h3>Toteutus</h3><p class="muted">Rakennamme ja hiomme sivuston.</p></div></li>
      <li><div class="dot">04</div><div><h3>Julkaisu</h3><p class="muted">Testaamme, julkaisemme ja luovutamme valmiin sivuston.</p></div></li>
    </ol>
  </div>
</section>
{pricing(lang, page)}
{cta(lang, page)}
'''


def services_page(lang):
    page = "services.html"
    if lang == "en":
        faq = [
            ("What is included in each package?", "Each package lists the pages and features that are included. If you need something that is not on the list, we will agree it separately before work begins."),
            ("Are domain and hosting included?", "No. Domain registration and website hosting are not included in the design and development packages. We can advise you on simple, reliable options."),
            ("How long does a project take?", "It depends on the scope and on how quickly we can review drafts together. We agree a timetable after the first conversation, once the work is clear — we do not quote a standard number of days in advance."),
            ("Is ongoing maintenance included?", "No. Maintenance is a separate service. The build packages cover design, development and launch of the agreed site."),
            ("Can I use my own photographs and text?", "Yes. If you already have photography or writing you would like to use, we will work with it. Additional photography or copywriting beyond the agreed scope is quoted separately."),
        ]
        body = f'''
<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow">SERVICES</p>
    <h1 class="display">Everything you need to make a stronger impression online.</h1>
    <p class="lead">Design, development and ongoing care — planned around your brand, your customers and the way you work.</p>
  </div>
</section>
<section class="section" id="design">
  <div class="wrap split">
    <div>
      <p class="kicker">01</p>
      <h2 class="section-title">Website Design</h2>
    </div>
    <div>
      <p>Thoughtful visual design built around your brand, customers and business goals.</p>
      <p class="muted" style="margin-top:16px">You receive a clear structure, considered typography and a visual system that belongs to your business. The aim is that a first-time visitor understands what you do and feels confident getting in touch.</p>
    </div>
  </div>
</section>
<section class="section" style="background:var(--dark);color:var(--bg)" id="development">
  <div class="wrap split">
    <div>
      <p class="kicker" style="color:#c5c8c2">02</p>
      <h2 class="section-title">Website Development</h2>
    </div>
    <div>
      <p>Fast, responsive and reliable websites that work beautifully across devices.</p>
      <p style="color:#c5c8c2;margin-top:16px">We build with clean front-end code, attention to loading speed and a contact path that is ready to receive enquiries. Technical SEO foundations are part of the work, not an afterthought.</p>
    </div>
  </div>
</section>
<section class="section" id="maintenance">
  <div class="wrap split">
    <div>
      <p class="kicker">03</p>
      <h2 class="section-title">Website Maintenance</h2>
    </div>
    <div>
      <p>Continued support to keep your website updated, secure and performing well.</p>
      <p class="muted" style="margin-top:16px">Once the site is live, we can look after updates, small content changes and periodic checks. Maintenance is agreed separately from the build packages.</p>
    </div>
  </div>
</section>
<section class="section band band-line">
  <div class="wrap">
    <h2 class="section-title" style="margin-bottom:32px">From first conversation to launch.</h2>
    <ol class="timeline">
      <li><div class="dot">01</div><div><h3>Discover</h3><p class="muted">Understand the business, goals and audience.</p></div></li>
      <li><div class="dot">02</div><div><h3>Design</h3><p class="muted">Create the visual direction and structure.</p></div></li>
      <li><div class="dot">03</div><div><h3>Develop</h3><p class="muted">Build and refine the website.</p></div></li>
      <li><div class="dot">04</div><div><h3>Launch</h3><p class="muted">Test, publish and hand over the finished website.</p></div></li>
    </ol>
  </div>
</section>
{pricing(lang, page)}
<section class="section" style="padding-top:0">
  <div class="wrap prose">
    <h2>Frequently asked questions</h2>
    <div class="faq">
      {"".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q,a in faq)}
    </div>
  </div>
</section>
{cta(lang, page)}
'''
        return body
    faq = [
        ("Mitä kuhunkin pakettiin sisältyy?", "Jokaisessa paketissa on lueteltu mukaan kuuluvat sivut ja ominaisuudet. Jos tarvitset jotain, mitä listassa ei ole, sovimme sen erikseen ennen työn alkua."),
        ("Sisältyvätkö verkkotunnus ja palvelintila hintaan?", "Eivät. Verkkotunnuksen rekisteröinti ja sivuston palvelintila eivät sisälly suunnittelu- ja toteutuspaketteihin. Voimme suositella yksinkertaisia ja luotettavia vaihtoehtoja."),
        ("Kuinka kauan projekti kestää?", "Se riippuu työn laajuudesta ja siitä, miten sujuvasti luonnoksia voidaan käydä yhdessä läpi. Aikataulu sovitaan ensimmäisen keskustelun jälkeen, kun työ on selvillä — emme lupaa vakioitua päivämäärää etukäteen."),
        ("Sisältyykö jatkuva ylläpito pakettiin?", "Ei. Ylläpito on erillinen palvelu. Toteutuspaketit kattavat sovitun sivuston suunnittelun, rakentamisen ja julkaisun."),
        ("Voinko käyttää omia kuvia ja tekstejä?", "Kyllä. Jos sinulla on valokuvia tai tekstejä, joita haluat käyttää, työskentelemme niiden kanssa. Sovittua laajemmat kuvaukset tai tekstityöt hinnoitellaan erikseen."),
    ]
    return f'''
<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow">PALVELUT</p>
    <h1 class="display">Kaikki, mitä tarvitset vahvempaan ensivaikutelmaan verkossa.</h1>
    <p class="lead">Suunnittelu, toteutus ja jatkuva tuki — suunniteltuna brändisi, asiakkaidesi ja tapasi työskennellä ympärille.</p>
  </div>
</section>
<section class="section" id="design">
  <div class="wrap split">
    <div>
      <p class="kicker">01</p>
      <h2 class="section-title">Verkkosivujen suunnittelu</h2>
    </div>
    <div>
      <p>Harkittu visuaalinen suunnittelu, joka rakentuu brändisi, asiakkaidesi ja liiketoimintasi tavoitteiden ympärille.</p>
      <p class="muted" style="margin-top:16px">Saat selkeän rakenteen, harkitun typografian ja visuaalisen järjestelmän, joka kuuluu juuri sinun yrityksellesi. Tavoitteena on, että ensikertalainen kävijä ymmärtää, mitä teet, ja uskaltaa ottaa yhteyttä.</p>
    </div>
  </div>
</section>
<section class="section" style="background:var(--dark);color:var(--bg)" id="development">
  <div class="wrap split">
    <div>
      <p class="kicker" style="color:#c5c8c2">02</p>
      <h2 class="section-title">Verkkosivujen toteutus</h2>
    </div>
    <div>
      <p>Nopeat, responsiiviset ja luotettavat sivustot, jotka toimivat kaikilla laitteilla.</p>
      <p style="color:#c5c8c2;margin-top:16px">Rakennamme siistillä front-end-koodilla, kiinnitämme huomiota latausnopeuteen ja varmistamme, että yhteydenottopolku on valmis. Hakukoneoptimoinnin tekninen perusta kuuluu työhön, ei jää jälkiajatukseksi.</p>
    </div>
  </div>
</section>
<section class="section" id="maintenance">
  <div class="wrap split">
    <div>
      <p class="kicker">03</p>
      <h2 class="section-title">Ylläpito</h2>
    </div>
    <div>
      <p>Jatkuvaa tukea, jotta sivustosi pysyy ajan tasalla, turvassa ja toimintakykyisenä.</p>
      <p class="muted" style="margin-top:16px">Kun sivusto on julkaistu, voimme hoitaa päivityksiä, pieniä sisältömuutoksia ja säännöllisiä tarkistuksia. Ylläpito sovitaan erikseen toteutuspaketeista.</p>
    </div>
  </div>
</section>
<section class="section band band-line">
  <div class="wrap">
    <h2 class="section-title" style="margin-bottom:32px">Ensimmäisestä keskustelusta julkaisuun.</h2>
    <ol class="timeline">
      <li><div class="dot">01</div><div><h3>Kartoitus</h3><p class="muted">Tutustumme yritykseen, tavoitteisiin ja yleisöön.</p></div></li>
      <li><div class="dot">02</div><div><h3>Suunnittelu</h3><p class="muted">Luomme visuaalisen suunnan ja rakenteen.</p></div></li>
      <li><div class="dot">03</div><div><h3>Toteutus</h3><p class="muted">Rakennamme ja hiomme sivuston.</p></div></li>
      <li><div class="dot">04</div><div><h3>Julkaisu</h3><p class="muted">Testaamme, julkaisemme ja luovutamme valmiin sivuston.</p></div></li>
    </ol>
  </div>
</section>
{pricing(lang, page)}
<section class="section" style="padding-top:0">
  <div class="wrap prose">
    <h2>Usein kysyttyä</h2>
    <div class="faq">
      {"".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q,a in faq)}
    </div>
  </div>
</section>
{cta(lang, page)}
'''


def work_page(lang):
    page = "work.html"
    if lang == "en":
        lead = "Three complete concept projects, designed and built as working websites. They are independent design concepts — not paying-client work — created to show how WEBAUR approaches different industries."
        return f'''
<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow">WORK</p>
    <h1 class="display">Different businesses. Different digital experiences.</h1>
    <p class="lead">{lead}</p>
  </div>
</section>
<section class="section" style="padding-top:0">
  {work_projects(lang, page)}
</section>
{cta(lang, page)}
'''
    lead = "Kolme valmista konseptiprojektia, jotka on suunniteltu ja rakennettu toimiviksi sivustoiksi. Ne ovat itsenäisiä suunnittelukonsepteja — eivät maksavan asiakkaan töitä — ja näyttävät, miten WEBAUR lähestyy eri toimialoja."
    return f'''
<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow">TYÖT</p>
    <h1 class="display">Eri yrityksiä. Erilaisia digitaalisia kokemuksia.</h1>
    <p class="lead">{lead}</p>
  </div>
</section>
<section class="section" style="padding-top:0">
  {work_projects(lang, page)}
</section>
{cta(lang, page)}
'''


def case_page(lang, p):
    page = f"work/{p['slug']}.html"
    pre = asset_prefix(lang, 1)
    meta = p[lang]
    concept = "Concept project" if lang == "en" else "Konseptiprojekti"
    demo_l = "View live demo" if lang == "en" else "Avaa demo"
    back = "Back to work" if lang == "en" else "Takaisin töihin"
    work_lab = "Work" if lang == "en" else "Työt"
    if lang == "en":
        brief_h, brief_p = "The brief", "This is an independent design concept. It is not a paying-client website. The goal was to show how a complete, industry-specific site can feel when design, photography and structure work together."
        find_h, find_p = "What you’ll find in the demo", "A multi-section website with its own typography, colour and photography. Booking or reservation buttons in the demo lead to a contact section clearly labelled as a concept — they do not place a real booking."
        alt_d = f"Desktop preview of {p['en']['title']}"
        alt_m = f"Mobile preview of {p['en']['title']}"
    else:
        brief_h, brief_p = "Lähtökohta", "Tämä on itsenäinen suunnittelukonsepti, ei maksavan asiakkaan sivusto. Tavoitteena oli näyttää, miltä toimialalle räätälöity kokonainen sivusto voi tuntua, kun suunnittelu, valokuvat ja rakenne pelaavat yhteen."
        find_h, find_p = "Mitä demossa on", "Usean osion sivusto omalla typografiallaan, värimaailmallaan ja kuvillaan. Demojen varauspainikkeet vievät yhteysosioon, jossa kerrotaan selvästi, että kyseessä on konsepti — ne eivät tee oikeaa varausta."
        alt_d = f"{p['fi']['title']} -konseptin esikatselu työpöydällä"
        alt_m = f"{p['fi']['title']} -konseptin esikatselu puhelimella"
    return f'''
<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow"><a href="{href(lang, page, lang, "work.html")}">{work_lab}</a> / {meta["title"]}</p>
    <span class="badge">{concept}</span>
    <h1 class="display" style="margin-top:16px">{meta["title"]}</h1>
    <p class="lead">{meta["desc"]}</p>
    <div class="btn-row" style="margin-top:24px">
      <a class="btn btn-ink" href="{pre}{p["demo"]}">{demo_l}</a>
      <a class="btn btn-ghost" href="{href(lang, page, lang, "work.html")}">{back}</a>
    </div>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="case-frames">
      {device_desktop(p["desk"], alt_d, pre)}
      {device_mobile(p["mob"], alt_m, pre)}
    </div>
    <div class="case-copy">
      <div>
        <h2>{brief_h}</h2>
        <p class="muted">{brief_p}</p>
      </div>
      <div>
        <h2>{find_h}</h2>
        <p class="muted">{find_p}</p>
      </div>
    </div>
  </div>
</section>
{cta(lang, page)}
'''


def about_page(lang):
    page = "about.html"
    if lang == "en":
        return f'''
<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow">ABOUT</p>
    <h1 class="display">Attention to the details that build trust.</h1>
    <p class="lead">WEBAUR is an independent web design studio. We help businesses improve their online presence with considered design, careful development and clear communication.</p>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap prose">
    <h2>Design quality</h2>
    <p>A website should look like your business, not like a template. We pay attention to typography, spacing, photography and hierarchy so the first impression feels intentional.</p>
    <h2>Technical care</h2>
    <p>Design only works if the site is fast, readable and reliable on every screen. We build with clean front-end code, thoughtful performance and a structure that is easy to maintain.</p>
    <h2>Clear communication</h2>
    <p>The process is straightforward: discover, design, develop, launch. You will always know what is happening and what we need from you.</p>
    <h2>Tailored solutions</h2>
    <p>Every project is planned around the individual business. We do not sell a single layout with the logo swapped.</p>
    <h2>Attention to detail</h2>
    <p>Small things — a clear button, a readable menu on a phone, a form that is honest about what happens next — are what make a site feel considered. No invented awards, client logos or years in business. The work should speak for itself.</p>
    <p><a class="btn btn-ink" href="{href(lang, page, lang, "contact.html")}" style="margin-top:8px">Start a project</a></p>
  </div>
</section>
'''
    return f'''
<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow">MEISTÄ</p>
    <h1 class="display">Huomiota niihin yksityiskohtiin, jotka rakentavat luottamusta.</h1>
    <p class="lead">WEBAUR on itsenäinen verkkosuunnittelustudio. Autamme yrityksiä vahvistamaan verkkoläsnäoloaan harkitulla suunnittelulla, huolellisella toteutuksella ja selkeällä viestinnällä.</p>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap prose">
    <h2>Suunnittelun laatu</h2>
    <p>Sivuston pitäisi näyttää sinun yritykseltäsi, ei mallipohjalta. Kiinnitämme huomiota typografiaan, tilaan, valokuviin ja hierarkiaan, jotta ensivaikutelma tuntuu harkitulta.</p>
    <h2>Tekninen huolellisuus</h2>
    <p>Suunnittelu toimii vain, jos sivusto on nopea, luettava ja luotettava kaikilla näytöillä. Rakennamme siistillä front-end-koodilla, harkitulla suorituskyvyllä ja rakenteella, jota on helppo ylläpitää.</p>
    <h2>Selkeä viestintä</h2>
    <p>Prosessi on suora: kartoitus, suunnittelu, toteutus, julkaisu. Tiedät aina, mitä tapahtuu ja mitä tarvitsemme sinulta.</p>
    <h2>Räätälöidyt ratkaisut</h2>
    <p>Jokainen projekti suunnitellaan kyseisen yrityksen ympärille. Emme myy yhtä ja samaa asettelua, johon vaihdetaan logo.</p>
    <h2>Huomio yksityiskohtiin</h2>
    <p>Pienet asiat — selkeä painike, luettava valikko puhelimessa, lomake joka kertoo rehellisesti mitä seuraavaksi tapahtuu — tekevät sivustosta harkitun. Emme keksi palkintoja, asiakaslogoja tai toimintavuosia. Työn pitää puhua puolestaan.</p>
    <p><a class="btn btn-ink" href="{href(lang, page, lang, "contact.html")}" style="margin-top:8px">Aloita projekti</a></p>
  </div>
</section>
'''


def contact_page(lang):
    page = "contact.html"
    if lang == "en":
        notice = "This form is prepared for Formspree or Netlify Forms. The current public host is GitHub Pages, which cannot process submissions on its own. Until a Formspree endpoint is added in js/form-config.js, or the site is deployed to Netlify, submitting the form will not send a message — you will see a clear note instead. Nothing is described as sent unless it actually is."
        email_p = "Prefer email? Use the address below once a domain is connected. It is a placeholder, not a live inbox."
        labels = dict(name="Name", biz="Business name", email="Email", site="Existing website (optional)", typ="Project type", bud="Approximate budget (optional)", msg="Project description", send="Send message",
                      consent='I agree that WEBAUR may use this information to respond to my enquiry. See the <a href="privacy.html">privacy policy</a>.',
                      ph="hello@[your-domain]",
                      sel="Please select", typ1="New website", typ2="Redesign", typ3="Landing page", typ4="Something else",
                      b0="Prefer not to say", b1="Starter — around €490 + VAT", b2="Business — around €890 + VAT", b3="Premium — around €1,490 + VAT", b4="Not sure yet",
                      title="Tell us about your project.", lead="Share a little about your business and what you need. We will get back to you to talk through the next step.",
                      eye="CONTACT", form_note="The form does not claim a message has been sent unless a connected service actually accepts it.")
    else:
        notice = "Lomake on valmisteltu Formspree- tai Netlify Forms -palvelua varten. Nykyinen julkinen alusta on GitHub Pages, joka ei itse käsittele lähetyksiä. Kunnes Formspree-osoite on lisätty tiedostoon js/form-config.js, tai sivusto on julkaistu Netlifyyn, lomakkeen lähettäminen ei lähetä viestiä — näet sen sijaan selkeän ilmoituksen. Viestiä ei koskaan väitetä lähetetyksi, ellei sitä ole oikeasti lähetetty."
        email_p = "Haluatko mieluummin sähköpostia? Käytä alla olevaa osoitetta, kun verkkotunnus on kytketty. Kyseessä on paikkamerkki, ei käytössä oleva postilaatikko."
        labels = dict(name="Nimi", biz="Yrityksen nimi", email="Sähköposti", site="Nykyinen verkkosivusto (valinnainen)", typ="Sivuston tyyppi", bud="Arvioitu budjetti (valinnainen)", msg="Kuvaus projektista", send="Lähetä viesti",
                      consent='Hyväksyn, että WEBAUR käyttää näitä tietoja vastatakseen kyselyyni. Lue <a href="privacy.html">tietosuojaseloste</a>.',
                      ph="hello@[your-domain]",
                      sel="Valitse", typ1="Uusi verkkosivusto", typ2="Uudistus", typ3="Laskeutumissivu", typ4="Muu",
                      b0="En halua kertoa", b1="Aloitus — noin 490 € + ALV", b2="Yritys — noin 890 € + ALV", b3="Premium — noin 1 490 € + ALV", b4="En ole vielä varma",
                      title="Kerro projektistasi.", lead="Kerro hieman yrityksestäsi ja siitä, mitä tarvitset. Otamme yhteyttä ja käymme seuraavan askeleen yhdessä läpi.",
                      eye="YHTEYSTIEDOT", form_note="Lomake ei väitä viestiä lähetetyksi, ellei kytketty palvelu ole ottanut sitä vastaan.")
    # privacy link in consent is same-folder relative — correct for both root and en/
    return f'''
<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow">{labels["eye"]}</p>
    <h1 class="display">{labels["title"]}</h1>
    <p class="lead">{labels["lead"]}</p>
  </div>
</section>
<section class="section" style="padding-top:0" id="form">
  <div class="wrap form-layout">
    <div>
      <p>{email_p}</p>
      <p style="margin:16px 0 24px"><span class="placeholder">{labels["ph"]}</span></p>
      <p class="muted">{notice}</p>
    </div>
    <form name="contact" method="POST" action="thanks.html" data-netlify="true" data-netlify-honeypot="company-website" netlify-honeypot="company-website" novalidate>
      <input type="hidden" name="form-name" value="contact" />
      <p class="hp"><label>Company website <input name="company-website" tabindex="-1" autocomplete="off" /></label></p>
      <div class="field">
        <label for="name">{labels["name"]}</label>
        <input id="name" name="name" type="text" autocomplete="name" required />
      </div>
      <div class="field">
        <label for="business">{labels["biz"]}</label>
        <input id="business" name="business" type="text" autocomplete="organization" required />
      </div>
      <div class="field">
        <label for="email">{labels["email"]}</label>
        <input id="email" name="email" type="email" autocomplete="email" required />
      </div>
      <div class="field">
        <label for="website">{labels["site"]}</label>
        <input id="website" name="website" type="url" autocomplete="url" placeholder="https://" />
      </div>
      <div class="field">
        <label for="type">{labels["typ"]}</label>
        <select id="type" name="type" required>
          <option value="">{labels["sel"]}</option>
          <option>{labels["typ1"]}</option>
          <option>{labels["typ2"]}</option>
          <option>{labels["typ3"]}</option>
          <option>{labels["typ4"]}</option>
        </select>
      </div>
      <div class="field">
        <label for="budget">{labels["bud"]}</label>
        <select id="budget" name="budget">
          <option value="">{labels["b0"]}</option>
          <option value="starter">{labels["b1"]}</option>
          <option value="business">{labels["b2"]}</option>
          <option value="premium">{labels["b3"]}</option>
          <option value="unsure">{labels["b4"]}</option>
        </select>
      </div>
      <div class="field">
        <label for="message">{labels["msg"]}</label>
        <textarea id="message" name="message" required></textarea>
      </div>
      <label class="consent">
        <input type="checkbox" name="consent" value="yes" required />
        <span>{labels["consent"]}</span>
      </label>
      <button class="btn btn-ink" type="submit">{labels["send"]}</button>
      <p class="form-note">{labels["form_note"]}</p>
      <p class="form-alert" id="form-status" hidden tabindex="-1"></p>
    </form>
  </div>
</section>
'''


def thanks_page(lang):
    if lang == "en":
        return '''
<section class="page-hero">
  <div class="wrap prose">
    <p class="eyebrow">THANK YOU</p>
    <h1 class="display">Your message is on its way.</h1>
    <p class="lead">This page is shown after a successful form submission. If you opened it directly, nothing has been sent.</p>
    <p><a class="btn btn-ink" href="index.html">Back to home</a></p>
  </div>
</section>
'''
    return '''
<section class="page-hero">
  <div class="wrap prose">
    <p class="eyebrow">KIITOS</p>
    <h1 class="display">Viestisi on matkalla.</h1>
    <p class="lead">Tämä sivu näytetään, kun lomake on lähetetty onnistuneesti. Jos avasit sivun suoraan, mitään ei ole lähetetty.</p>
    <p><a class="btn btn-ink" href="index.html">Takaisin etusivulle</a></p>
  </div>
</section>
'''


def privacy_page(lang):
    if lang == "en":
        return '''
<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow">LEGAL</p>
    <h1 class="display">Privacy Policy</h1>
    <p class="lead">This is a basic policy structure. Placeholder details are clearly marked and must be completed with real business information before launch.</p>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap prose">
    <h2>Data controller</h2>
    <p>The data controller is WEBAUR. Legal entity, business ID and postal address: <span class="placeholder">[business legal name, Y-tunnus, address]</span>.</p>
    <h2>Contact</h2>
    <p>Enquiries: <span class="placeholder">hello@[your-domain]</span> (placeholder — not a live address until a domain and mailbox are connected).</p>
    <h2>What we collect</h2>
    <p>If you submit the contact form we collect the name, business name, email, optional existing website, project type, optional budget and message you provide, plus a consent record. A honeypot field is used only to reduce spam and should be left empty.</p>
    <h2>Why we collect it</h2>
    <p>To respond to project enquiries. We do not use the form data for marketing lists unless you have separately agreed.</p>
    <h2>Processors</h2>
    <p>If the site is hosted on Netlify, form submissions are processed by Netlify Forms. If a Formspree endpoint is configured in js/form-config.js, Formspree processes the submission. Analytics: <span class="placeholder">[none configured / provider name]</span>.</p>
    <h2>Retention and rights</h2>
    <p>Enquiries are kept only as long as needed to handle the conversation and any resulting work. You may ask to access, correct or delete your data by writing to the contact address above once it is live. You may also contact a data protection authority in your country (in Finland, the Office of the Data Protection Ombudsman).</p>
    <p>Last updated: 9 November 2026.</p>
  </div>
</section>
'''
    return '''
<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow">JURIDISET TIEDOT</p>
    <h1 class="display">Tietosuojaseloste</h1>
    <p class="lead">Tämä on selosteen perusrakenne. Paikkamerkit on merkitty selvästi, ja ne tulee täydentää oikeilla yritystiedoilla ennen julkaisua.</p>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap prose">
    <h2>Rekisterinpitäjä</h2>
    <p>Rekisterinpitäjä on WEBAUR. Oikeushenkilö, Y-tunnus ja postiosoite: <span class="placeholder">[yrityksen virallinen nimi, Y-tunnus, osoite]</span>.</p>
    <h2>Yhteydenotto</h2>
    <p>Tiedustelut: <span class="placeholder">hello@[your-domain]</span> (paikkamerkki — ei ole käytössä oleva osoite, ennen kuin verkkotunnus ja postilaatikko on kytketty).</p>
    <h2>Mitä keräämme</h2>
    <p>Jos lähetät yhteydenottolomakkeen, keräämme nimen, yrityksen nimen, sähköpostin, valinnaisen nykyisen sivuston, projektin tyypin, valinnaisen budjetin ja viestin sekä suostumuksen tiedot. Honeypot-kenttää käytetään vain roskapostin vähentämiseen, ja se tulee jättää tyhjäksi.</p>
    <h2>Miksi keräämme tietoja</h2>
    <p>Jotta voimme vastata projektikyselyihin. Emme käytä lomakkeen tietoja markkinointilistoihin, ellet ole erikseen siihen suostunut.</p>
    <h2>Käsittelijät</h2>
    <p>Jos sivusto on julkaistu Netlifyyn, lomakkeen käsittelijä on Netlify Forms. Jos Formspree-osoite on määritetty tiedostossa js/form-config.js, käsittelijä on Formspree. Analytiikka: <span class="placeholder">[ei käytössä / palvelun nimi]</span>.</p>
    <h2>Säilytys ja oikeudet</h2>
    <p>Kyselyitä säilytetään vain niin kauan kuin keskustelun ja mahdollisen työn hoitaminen edellyttää. Voit pyytää tietojesi tarkastamista, korjaamista tai poistamista yllä olevaan osoitteeseen, kun se on käytössä. Voit myös olla yhteydessä tietosuojaviranomaiseen (Suomessa Tietosuojavaltuutetun toimisto).</p>
    <p>Päivitetty 9. marraskuuta 2026.</p>
  </div>
</section>
'''


def not_found_page(lang):
    if lang == "en":
        return '''
<section class="page-hero">
  <div class="wrap prose">
    <p class="eyebrow">404</p>
    <h1 class="display">This page could not be found.</h1>
    <p class="lead">The address may have changed, or the page may not exist.</p>
    <p><a class="btn btn-ink" href="index.html">Back to home</a> &nbsp; <a href="../index.html" lang="fi" hreflang="fi">Suomeksi</a></p>
  </div>
</section>
'''
    return '''
<section class="page-hero">
  <div class="wrap prose">
    <p class="eyebrow">404</p>
    <h1 class="display">Sivua ei löytynyt.</h1>
    <p class="lead">Osoite on voinut muuttua, tai sivua ei ole olemassa.</p>
    <p><a class="btn btn-ink" href="index.html">Takaisin etusivulle</a> &nbsp; <a href="en/index.html" lang="en" hreflang="en">In English</a></p>
  </div>
</section>
'''


META = {
    "en": {
        "index.html": ("WEBAUR — Independent web design studio", "WEBAUR designs and builds thoughtful, modern websites that help businesses stand out, build trust and turn visitors into customers."),
        "services.html": ("Services — WEBAUR", "Website design, development and maintenance from WEBAUR. Clear packages from €490 excl. VAT."),
        "work.html": ("Work — WEBAUR", "Concept projects by WEBAUR: Hale Barber Studio, Alto Detail and Maison Café — complete working demo websites."),
        "about.html": ("About — WEBAUR", "WEBAUR is an independent web design studio focused on design quality, technical care and clear communication."),
        "contact.html": ("Contact — WEBAUR", "Tell WEBAUR about your project. Start a conversation about a new website or a redesign."),
        "thanks.html": ("Thank you — WEBAUR", "Your message has been submitted to WEBAUR."),
        "privacy.html": ("Privacy Policy — WEBAUR", "How WEBAUR handles contact-form data, with clearly marked placeholders for legal details."),
        "404.html": ("Page not found — WEBAUR", "The page you requested could not be found."),
    },
    "fi": {
        "index.html": ("WEBAUR — Itsenäinen verkkosuunnittelustudio", "WEBAUR suunnittelee ja rakentaa harkittuja, nykyaikaisia verkkosivuja, joiden avulla yritys erottuu, herättää luottamusta ja muuttaa kävijät asiakkaiksi."),
        "services.html": ("Palvelut — WEBAUR", "Verkkosivujen suunnittelu, toteutus ja ylläpito. Selkeät paketit alkaen 490 € + ALV."),
        "work.html": ("Työt — WEBAUR", "WEBAURin konseptiprojektit: Hale Barber Studio, Alto Detail ja Maison Café — valmiit, toimivat demosivustot."),
        "about.html": ("Meistä — WEBAUR", "WEBAUR on itsenäinen verkkosuunnittelustudio, joka panostaa suunnittelun laatuun, tekniseen huolellisuuteen ja selkeään viestintään."),
        "contact.html": ("Yhteystiedot — WEBAUR", "Kerro WEBAURille projektistasi. Aloita keskustelu uudesta sivustosta tai uudistuksesta."),
        "thanks.html": ("Kiitos — WEBAUR", "Viestisi on lähetetty WEBAURille."),
        "privacy.html": ("Tietosuojaseloste — WEBAUR", "Miten WEBAUR käsittelee yhteydenottolomakkeen tietoja. Juridiset tiedot on merkitty paikkamerkeillä."),
        "404.html": ("Sivua ei löytynyt — WEBAUR", "Pyytämääsi sivua ei löytynyt."),
    },
}

ACTIVE = {
    "index.html": "home",
    "services.html": "services",
    "work.html": "work",
    "about.html": "about",
    "contact.html": "contact",
    "thanks.html": "contact",
    "privacy.html": "",
    "404.html": "",
}

BUILDERS = {
    "index.html": home,
    "services.html": services_page,
    "work.html": work_page,
    "about.html": about_page,
    "contact.html": contact_page,
    "thanks.html": thanks_page,
    "privacy.html": privacy_page,
    "404.html": not_found_page,
}


def write(rel, html):
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    print("wrote", rel)


def build():
    for lang in ("fi", "en"):
        for page, builder in BUILDERS.items():
            title, desc = META[lang][page]
            html = page_shell(lang, page, title, desc, ACTIVE[page], builder(lang))
            rel = page if lang == "fi" else f"en/{page}"
            write(rel, html)
        for p in PROJECTS:
            page = f"work/{p['slug']}.html"
            title = f"{p[lang]['title']} — {'Concept project' if lang=='en' else 'Konseptiprojekti'} — WEBAUR"
            desc = p[lang]["desc"]
            html = page_shell(lang, page, title, desc, "work", case_page(lang, p))
            rel = page if lang == "fi" else f"en/{page}"
            write(rel, html)

    pages_fi = ["", "services.html", "work.html", "about.html", "contact.html", "privacy.html", "thanks.html",
                "work/barber-studio.html", "work/detailing.html", "work/maison-cafe.html"]
    pages_en = [f"en/{p}" if p else "en/" for p in pages_fi]
    demos = ["demos/barber-studio/index.html", "demos/detailing/index.html", "demos/maison-cafe/index.html"]
    urls = "\n".join(
        f"  <url><loc>https://webaur.com/{u}</loc></url>" for u in pages_fi + pages_en + demos
    )
    (ROOT / "sitemap.xml").write_text(
        f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}
</urlset>
''',
        encoding="utf-8",
    )
    (ROOT / "robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: https://webaur.com/sitemap.xml\n", encoding="utf-8")
    (ROOT / "netlify.toml").write_text('''[build]
  publish = "."

[[headers]]
  for = "/*"
  [headers.values]
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"
    X-Frame-Options = "SAMEORIGIN"

[[headers]]
  for "/images/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"

[[headers]]
  for = "/fonts/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"
''', encoding="utf-8")
    (ROOT / "_headers").write_text('''/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  X-Frame-Options: SAMEORIGIN
''', encoding="utf-8")
    (ROOT / "_redirects").write_text("/*    /404.html    404\n", encoding="utf-8")
    print("config ok")


if __name__ == "__main__":
    build()
