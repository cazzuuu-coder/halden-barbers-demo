#!/usr/bin/env python3
"""Generate Webaur HTML pages (root and /en) with relative links."""
from pathlib import Path

ROOT = Path("/workspace/webaur-site")
DOMAIN = "https://webaur.com"

def picture(prefix, stem, alt, width, height, lazy=True):
    loading = ' loading="lazy"' if lazy else ' fetchpriority="high"'
    return f'''<picture>
              <source type="image/webp" srcset="{prefix}images/work/{stem}.webp">
              <img src="{prefix}images/work/{stem}.jpg" alt="{alt}" width="{width}" height="{height}"{loading}>
            </picture>'''

def device_desktop(prefix, stem, alt, lazy=True):
    return f'''<div class="device-desktop">
          <div class="chrome" aria-hidden="true"><i></i><i></i><i></i></div>
          <div class="screen">
            {picture(prefix, stem, alt, 1440, 900, lazy=lazy)}
          </div>
        </div>'''

def device_mobile(prefix, stem, alt, lazy=True):
    return f'''<div class="device-mobile">
          <div class="notch" aria-hidden="true"></div>
          <div class="screen">
            {picture(prefix, stem, alt, 390, 844, lazy=lazy)}
          </div>
        </div>'''

ICON_DESIGN = '''<svg class="icon" viewBox="0 0 32 32" fill="none" aria-hidden="true"><rect x="4" y="6" width="24" height="16" rx="2" stroke="currentColor" stroke-width="1.6"/><path d="M11 26h10" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><path d="M16 22v4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><path d="M9 12h8M9 16h5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>'''
ICON_DEV = '''<svg class="icon" viewBox="0 0 32 32" fill="none" aria-hidden="true"><path d="M8 10l-4 6 4 6M24 10l4 6-4 6M18 8l-4 16" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'''
ICON_CARE = '''<svg class="icon" viewBox="0 0 32 32" fill="none" aria-hidden="true"><circle cx="16" cy="16" r="10" stroke="currentColor" stroke-width="1.6"/><path d="M16 10v6l4 2" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'''

def head(title, desc, canonical, prefix, current_path):
    og = f"{DOMAIN}/images/og/og-image.jpg"
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{canonical}">
  <link rel="alternate" hreflang="en" href="{canonical}">
  <link rel="alternate" hreflang="x-default" href="{canonical}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="WEBAUR">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{og}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{og}">
  <meta name="theme-color" content="#F7F7F4">
  <link rel="icon" href="{prefix}images/brand/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="{prefix}images/brand/favicon-32.png" type="image/png" sizes="32x32">
  <link rel="apple-touch-icon" href="{prefix}images/brand/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&amp;display=swap">
  <link rel="stylesheet" href="{prefix}css/styles.css">
</head>'''

def nav(p, current):
    def item(key, href, label):
        cur = ' aria-current="page"' if current == key else ''
        return f'<li><a href="{href}"{cur}>{label}</a></li>'
    home_cur = ' aria-current="page"' if current == 'home' else ''
    return f'''  <a class="skip" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="wrap nav">
      <a class="logo" href="{p['home']}"{home_cur}><span class="logo-mark" aria-hidden="true"></span>WEBAUR</a>
      <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-menu" aria-label="Open menu">
        <span></span><span></span>
      </button>
      <div class="nav-panel" id="site-menu">
        <ul class="nav-links">
          {item('home', p['home'], 'Home')}
          {item('services', p['services'], 'Services')}
          {item('work', p['work'], 'Our Work')}
          {item('about', p['about'], 'About')}
        </ul>
        <a class="nav-cta" href="{p['contact']}">Let’s Talk</a>
        <span class="lang" title="Finnish and French will be added later">EN</span>
      </div>
    </div>
  </header>'''

def footer(p):
    return f'''  <footer class="site-footer">
    <div class="wrap footer-grid">
      <div>
        <a class="logo" href="{p['home']}"><span class="logo-mark" aria-hidden="true"></span>WEBAUR</a>
        <p class="muted" style="margin-top:1rem;max-width:28ch">Premium websites for businesses that want to grow.</p>
      </div>
      <ul class="footer-col">
        <li><strong>Navigate</strong></li>
        <li><a href="{p['home']}">Home</a></li>
        <li><a href="{p['services']}">Services</a></li>
        <li><a href="{p['work']}">Our Work</a></li>
        <li><a href="{p['about']}">About</a></li>
        <li><a href="{p['contact']}">Contact</a></li>
      </ul>
      <ul class="footer-col">
        <li><strong>Services</strong></li>
        <li><a href="{p['services']}#design">Website Design</a></li>
        <li><a href="{p['services']}#development">Website Development</a></li>
        <li><a href="{p['services']}#maintenance">Website Maintenance</a></li>
      </ul>
      <ul class="footer-col">
        <li><strong>Contact</strong></li>
        <li><a class="footer-email" href="mailto:hello@webaur.com">hello@webaur.com</a></li>
        <li class="footer-note">Placeholder until the mailbox is connected.</li>
        <li style="margin-top:.7rem"><a href="{p['privacy']}">Privacy policy</a></li>
      </ul>
    </div>
    <div class="wrap legal">
      <p>© 2026 WEBAUR. An independent web design studio. A visiting address, telephone number and business ID will be published here once they exist.</p>
      <p>Starting prices are listed excl. VAT.</p>
    </div>
  </footer>
  <script src="{p['js']}" defer></script>
</body>
</html>'''

def page_shell(p, current, title, desc, canonical, main):
    return "\n".join([
        head(title, desc, canonical, p['prefix'], current),
        "<body>",
        nav(p, current),
        f'  <main id="main">\n{main}\n  </main>',
        footer(p),
    ])

def paths(kind):
    prefix = {'root': '', 'work': '../', 'en': '../', 'en_work': '../../'}[kind]
    if kind in ('root', 'work'):
        home, services, work, about, contact, privacy, thanks = (
            f'{prefix}index.html', f'{prefix}services.html', f'{prefix}work.html',
            f'{prefix}about.html', f'{prefix}contact.html', f'{prefix}privacy.html',
            f'{prefix}thanks.html',
        )
        cases = {
            'hale': f'{prefix}work/barber-studio.html',
            'autohaus': f'{prefix}work/autohaus.html',
            'maison': f'{prefix}work/maison-cafe.html',
        }
    elif kind == 'en':
        home, services, work, about, contact, privacy, thanks = (
            'index.html', 'services.html', 'work.html', 'about.html',
            'contact.html', 'privacy.html', 'thanks.html',
        )
        cases = {
            'hale': 'work/barber-studio.html',
            'autohaus': 'work/autohaus.html',
            'maison': 'work/maison-cafe.html',
        }
    else:
        home, services, work, about, contact, privacy, thanks = (
            '../index.html', '../services.html', '../work.html', '../about.html',
            '../contact.html', '../privacy.html', '../thanks.html',
        )
        cases = {
            'hale': 'barber-studio.html',
            'autohaus': 'autohaus.html',
            'maison': 'maison-cafe.html',
        }
    return {
        'prefix': prefix, 'home': home, 'services': services, 'work': work,
        'about': about, 'contact': contact, 'privacy': privacy, 'thanks': thanks,
        'cases': cases, 'js': f'{prefix}js/main.js',
    }

def home_main(p):
    pre = p['prefix']
    def project_row(key, title, industry, style, desk, mob, desk_alt, mob_alt):
        return f'''
        <a class="project-row reveal" href="{p['cases'][key]}">
          <div class="frames">
            {device_desktop(pre, desk, desk_alt)}
            {device_mobile(pre, mob, mob_alt)}
          </div>
          <div class="meta">
            <p class="badge">Concept project</p>
            <h3>{title}</h3>
            <p class="kicker">{industry}</p>
            <p class="muted" style="margin-top:.7rem">{style}</p>
          </div>
        </a>'''

    return f'''
    <section class="hero" id="hero">
      <div class="wrap-wide hero-grid">
        <div>
          <p class="eyebrow">Independent web design studio</p>
          <h1 class="display">Your business deserves<br>a <span class="hl">better</span> website.</h1>
          <p class="lead">We design and build modern websites that help businesses stand out, build trust and turn visitors into customers.</p>
          <div class="btn-row">
            <a class="btn btn-ink" href="{p['contact']}">Start a project</a>
            <a class="btn btn-ghost" href="{p['work']}">Explore our work</a>
          </div>
          <a class="scroll-indicator" href="#introduction"><span class="line" aria-hidden="true"></span> Scroll</a>
        </div>
        <div class="hero-stage reveal">
          <div class="device-stack">
            {device_desktop(pre, 'vale-desktop', 'Concept homepage for Vale Counsel, a fictional professional-services firm.', lazy=False)}
            {device_mobile(pre, 'hale-mobile', 'Mobile concept for Hale Barber Studio, a fictional barbershop.', lazy=False)}
            <span class="concept-label">Concept projects — professional services and barber</span>
          </div>
          <div class="hero-thumbs">
            <figure>
              {device_desktop(pre, 'autohaus-desktop', 'Concept homepage for Autohaus Lind, a fictional automotive workshop.', lazy=False)}
              <figcaption>Automotive · Concept project</figcaption>
            </figure>
            <figure>
              {device_desktop(pre, 'maison-desktop', 'Concept homepage for Maison Café, a fictional restaurant.', lazy=False)}
              <figcaption>Restaurant · Concept project</figcaption>
            </figure>
          </div>
        </div>
      </div>
    </section>
    <hr class="rule wrap">
    <section class="section" id="introduction">
      <div class="wrap split">
        <div>
          <p class="eyebrow">Introduction</p>
          <h2 class="section-title">Good design is more than appearance.</h2>
          <p class="lead" style="margin-top:1.1rem">Your website is often the first impression people have of your business. We make sure it communicates the quality of your services, builds confidence and makes it easy for customers to take the next step.</p>
        </div>
        <div class="intro-visual reveal">
          {device_desktop(pre, 'maison-desktop', 'Maison Café concept website, used as an introductory visual.')}
          <span class="concept-label">Concept project — Maison Café</span>
        </div>
      </div>
    </section>
    <section class="section band-2" id="services">
      <div class="wrap">
        <div class="section-head">
          <div>
            <p class="eyebrow">Services</p>
            <h2 class="section-title">Everything your website needs.</h2>
          </div>
          <a class="btn btn-ghost" href="{p['services']}">View services</a>
        </div>
        <div class="service-grid">
          <a class="service-card reveal" href="{p['services']}#design">
            {ICON_DESIGN}
            <p class="idx">Service 01</p>
            <h3>Website Design</h3>
            <p>Modern, tailored website designs that reflect your brand and make your business stand out.</p>
            <span class="more">Learn more</span>
          </a>
          <a class="service-card reveal" href="{p['services']}#development">
            {ICON_DEV}
            <p class="idx">Service 02</p>
            <h3>Website Development</h3>
            <p>Fast, responsive and carefully built websites designed to work beautifully across all devices.</p>
            <span class="more">Learn more</span>
          </a>
          <a class="service-card reveal" href="{p['services']}#maintenance">
            {ICON_CARE}
            <p class="idx">Service 03</p>
            <h3>Website Maintenance</h3>
            <p>Reliable ongoing support to keep your website updated, secure and running smoothly.</p>
            <span class="more">Learn more</span>
          </a>
        </div>
      </div>
    </section>
    <section class="section" id="work">
      <div class="wrap-wide">
        <div class="section-head wrap" style="width:100%;margin-left:0;margin-right:0">
          <div>
            <p class="eyebrow">Featured work</p>
            <h2 class="section-title">Made to make an impression.</h2>
          </div>
          <a class="btn btn-ghost" href="{p['work']}">Our work</a>
        </div>
        {project_row('hale', 'Barber Studio', 'Barber / Grooming', 'A dark, premium design for a quiet grooming studio.', 'hale-desktop', 'hale-mobile', 'Desktop concept for Barber Studio.', 'Mobile concept for Barber Studio.')}
        {project_row('autohaus', 'Autohaus', 'Automotive', 'A modern, technical and sophisticated workshop website.', 'autohaus-desktop', 'autohaus-mobile', 'Desktop concept for Autohaus.', 'Mobile concept for Autohaus.')}
        {project_row('maison', 'Maison Café', 'Restaurant', 'An elegant, warm and editorial design for a neighbourhood café.', 'maison-desktop', 'maison-mobile', 'Desktop concept for Maison Café.', 'Mobile concept for Maison Café.')}
      </div>
    </section>
    <section class="section band-2" id="why">
      <div class="wrap">
        <div class="section-head">
          <div>
            <p class="eyebrow">Why WEBAUR</p>
            <h2 class="section-title">Built around your business.</h2>
          </div>
        </div>
        <div class="why-grid">
          <article class="why-card reveal">
            <p class="idx">01</p>
            <h3>Designed for your brand</h3>
            <p>Every website is tailored to the business and its identity.</p>
          </article>
          <article class="why-card reveal">
            <p class="idx">02</p>
            <h3>Made for every screen</h3>
            <p>A seamless experience across mobile, tablet and desktop.</p>
          </article>
          <article class="why-card reveal">
            <p class="idx">03</p>
            <h3>Performance focused</h3>
            <p>Fast-loading pages and technically clean implementation.</p>
          </article>
          <article class="why-card reveal">
            <p class="idx">04</p>
            <h3>Built to generate enquiries</h3>
            <p>Clear calls to action and intuitive navigation help visitors become customers.</p>
          </article>
        </div>
      </div>
    </section>
    <section class="section" id="process">
      <div class="wrap">
        <div class="section-head">
          <div>
            <p class="eyebrow">Process</p>
            <h2 class="section-title">A straightforward process. A better result.</h2>
          </div>
        </div>
        <ol class="timeline">
          <li class="reveal">
            <span class="dot">01</span>
            <div>
              <h3>Discover</h3>
              <p class="muted">We learn about your business, goals and customers.</p>
            </div>
          </li>
          <li class="reveal">
            <span class="dot">02</span>
            <div>
              <h3>Design</h3>
              <p class="muted">We create a visual direction tailored to your brand.</p>
            </div>
          </li>
          <li class="reveal">
            <span class="dot">03</span>
            <div>
              <h3>Build</h3>
              <p class="muted">We develop, test and refine your website.</p>
            </div>
          </li>
          <li class="reveal">
            <span class="dot">04</span>
            <div>
              <h3>Launch</h3>
              <p class="muted">Your website goes live, ready to welcome new customers.</p>
            </div>
          </li>
        </ol>
      </div>
    </section>
    <section class="section" id="pricing" style="padding-top:0">
      <div class="wrap">
        <div class="section-head">
          <div>
            <p class="eyebrow">Pricing</p>
            <h2 class="section-title">Clear packages. No unnecessary complexity.</h2>
            <p class="muted" style="margin-top:.7rem">Starting prices, excl. VAT.</p>
          </div>
        </div>
        <div class="price-grid">
          <article class="price-card reveal">
            <h3>Starter</h3>
            <p class="price">€490 <span>excl. VAT</span></p>
            <ul>
              <li>One-page website</li>
              <li>Responsive design</li>
              <li>Contact information</li>
              <li>Essential SEO setup</li>
              <li>Basic contact functionality</li>
            </ul>
            <a class="btn btn-ghost" href="{p['contact']}">Start a project</a>
          </article>
          <article class="price-card featured reveal">
            <h3>Business</h3>
            <p class="price">€890 <span>excl. VAT</span></p>
            <ul>
              <li>4–6 pages</li>
              <li>Custom design</li>
              <li>Contact form</li>
              <li>Service pages</li>
              <li>Basic SEO setup</li>
              <li>Mobile optimization</li>
            </ul>
            <a class="btn btn-ink" href="{p['contact']}">Start a project</a>
          </article>
          <article class="price-card reveal">
            <h3>Premium</h3>
            <p class="price">€1,490 <span>excl. VAT</span></p>
            <ul>
              <li>6–10 pages</li>
              <li>Advanced custom design</li>
              <li>More advanced functionality</li>
              <li>SEO foundations</li>
              <li>Analytics setup</li>
              <li>Additional integrations as agreed</li>
            </ul>
            <a class="btn btn-ghost" href="{p['contact']}">Start a project</a>
          </article>
        </div>
        <p class="muted" style="margin-top:1.4rem;text-align:center">Every project is different. Contact us for a tailored quote.</p>
      </div>
    </section>
    <section class="cta-band" id="cta">
      <div class="wrap">
        <p class="eyebrow" style="color:var(--lime)">A first conversation</p>
        <h2 class="section-title" style="margin:.6rem 0 1rem">Let’s build something better.</h2>
        <p class="lead">Have a project in mind? Tell us about your business and let’s create a website that makes a difference.</p>
        <div class="btn-row" style="margin-top:1.6rem">
          <a class="btn btn-ink" href="{p['contact']}">Start your project</a>
        </div>
      </div>
    </section>
'''

def services_main(p):
    return f'''
    <section class="page-hero">
      <div class="wrap">
        <p class="eyebrow">Services</p>
        <h1 class="display">Everything your website needs.</h1>
        <p class="lead">Website design, development and maintenance — planned, built and handed over so your business can use the site with confidence.</p>
      </div>
    </section>
    <section class="section" style="padding-top:0" id="design">
      <div class="wrap split">
        <div>
          <p class="idx kicker">Service 01</p>
          <h2 class="section-title">Website Design</h2>
        </div>
        <div class="prose" style="max-width:none">
          <p>Modern, tailored website designs that reflect your brand and make your business stand out. We start with your services, your customers and the impression you want to make, then set type, colour and layout so the site feels considered rather than templated.</p>
          <p>You receive a clear visual direction, page layouts designed for a phone first, and a revision round agreed in the proposal. We do not promise unlimited design changes.</p>
        </div>
      </div>
    </section>
    <hr class="rule wrap">
    <section class="section" id="development">
      <div class="wrap split">
        <div>
          <p class="idx kicker">Service 02</p>
          <h2 class="section-title">Website Development</h2>
        </div>
        <div class="prose" style="max-width:none">
          <p>Fast, responsive and carefully built websites designed to work beautifully across all devices. We implement the design in clean HTML, CSS and JavaScript, test on common screen sizes, and launch on a domain and hosting arrangement that belongs to you.</p>
          <p>This includes responsive design, essential or foundational SEO (titles, descriptions, headings, a sitemap and robots file), contact form integration that is actually connected and tested, and attention to website performance — compact images, tidy code and a light page weight. Booking tools or other integrations are included when they are appropriate and agreed in the quote. We do not promise guaranteed Google rankings or guaranteed sales.</p>
        </div>
      </div>
    </section>
    <hr class="rule wrap">
    <section class="section" id="maintenance">
      <div class="wrap split">
        <div>
          <p class="idx kicker">Service 03</p>
          <h2 class="section-title">Website Maintenance</h2>
        </div>
        <div class="prose" style="max-width:none">
          <p>Reliable ongoing support to keep your website updated, secure and running smoothly. A care plan can cover availability, agreed content updates and coordination of hosting. The scope is written into the agreement so both sides know what is included — and what is billed separately.</p>
        </div>
      </div>
    </section>
    <section class="section band-2">
      <div class="wrap">
        <p class="eyebrow">How a project runs</p>
        <h2 class="section-title" style="margin:.6rem 0 1.6rem">A straightforward process. A better result.</h2>
        <ol class="timeline">
          <li><span class="dot">01</span><div><h3>Discover</h3><p class="muted">We learn about your business, goals and customers.</p></div></li>
          <li><span class="dot">02</span><div><h3>Design</h3><p class="muted">We create a visual direction tailored to your brand.</p></div></li>
          <li><span class="dot">03</span><div><h3>Build</h3><p class="muted">We develop, test and refine your website.</p></div></li>
          <li><span class="dot">04</span><div><h3>Launch</h3><p class="muted">Your website goes live, ready to welcome new customers.</p></div></li>
        </ol>
      </div>
    </section>
    <section class="cta-band">
      <div class="wrap">
        <h2 class="section-title">Let’s build something better.</h2>
        <p class="lead" style="margin-top:1rem">Have a project in mind? Tell us about your business and let’s create a website that makes a difference.</p>
        <div class="btn-row" style="margin-top:1.6rem">
          <a class="btn btn-ink" href="{p['contact']}">Start your project</a>
        </div>
      </div>
    </section>
'''

def work_main(p):
    pre = p['prefix']
    def row(key, title, industry, style, desk, mob, da, ma):
        return f'''
        <a class="project-row reveal" href="{p['cases'][key]}">
          <div class="frames">
            {device_desktop(pre, desk, da)}
            {device_mobile(pre, mob, ma)}
          </div>
          <div class="meta">
            <p class="badge">Concept project</p>
            <h3>{title}</h3>
            <p class="kicker">{industry}</p>
            <p class="muted" style="margin-top:.7rem">{style}</p>
          </div>
        </a>'''
    return f'''
    <section class="page-hero">
      <div class="wrap">
        <p class="eyebrow">Our work</p>
        <h1 class="display">Made to make an impression.</h1>
        <p class="lead">These are original concept projects — design studies built as real pages, not client commissions and not generated pictures dropped into a template. Real client work will appear here only with written permission.</p>
      </div>
    </section>
    <section class="section" style="padding-top:0">
      <div class="wrap-wide">
        {row('hale', 'Barber Studio', 'Barber / Grooming', 'A dark, premium design for a quiet grooming studio.', 'hale-desktop', 'hale-mobile', 'Desktop concept for Barber Studio.', 'Mobile concept for Barber Studio.')}
        {row('autohaus', 'Autohaus', 'Automotive', 'A modern, technical and sophisticated workshop website.', 'autohaus-desktop', 'autohaus-mobile', 'Desktop concept for Autohaus.', 'Mobile concept for Autohaus.')}
        {row('maison', 'Maison Café', 'Restaurant', 'An elegant, warm and editorial design for a neighbourhood café.', 'maison-desktop', 'maison-mobile', 'Desktop concept for Maison Café.', 'Mobile concept for Maison Café.')}
      </div>
    </section>
'''

def case_main(p, data):
    pre = p['prefix']
    features = "".join(f"<li>{f}</li>" for f in data['features'])
    return f'''
    <section class="page-hero">
      <div class="wrap">
        <p class="badge">Concept project</p>
        <p class="eyebrow" style="margin-top:1rem">{data['industry']}</p>
        <h1 class="display">{data['title']}</h1>
        <p class="lead">{data['lead']}</p>
      </div>
    </section>
    <section class="wrap case-frames reveal">
      {device_desktop(pre, data['desk'], data['desk_alt'])}
      {device_mobile(pre, data['mob'], data['mob_alt'])}
    </section>
    <section class="wrap case-copy">
      <div>
        <h2>Design objective</h2>
        <p class="muted">{data['objective']}</p>
      </div>
      <div>
        <h2>Target audience</h2>
        <p class="muted">{data['audience']}</p>
      </div>
      <div>
        <h2>Design approach</h2>
        <p class="muted">{data['approach']}</p>
      </div>
      <div>
        <h2>Key features</h2>
        <ul class="muted" style="padding-left:1.1rem;display:grid;gap:.35rem">{features}</ul>
      </div>
    </section>
    <section class="wrap prose" style="padding-bottom:4rem">
      <p><a href="{p['work']}">Back to our work</a> · <a href="{p['contact']}">Start a project</a></p>
    </section>
'''

CASES = {
    'barber-studio': dict(
        title='Barber Studio',
        lead='A dark, premium concept for a grooming studio — built as a real page, labelled honestly as a study, not a client.',
        industry='Barber / Grooming',
        desk='hale-desktop', mob='hale-mobile',
        desk_alt='Desktop mockup of the Barber Studio concept.',
        mob_alt='Mobile mockup of the Barber Studio concept.',
        objective='Show how a small barbershop can feel considered and calm online, without relying on generic stock photography.',
        audience='Independent barbers and grooming studios that want a quiet, premium first impression on a phone and on a wide screen.',
        approach='A near-black ground, a display serif, a restrained gold accent and a short service list. Hours are present; no real address is invented. Booking is described as a connection to a tool the shop would already use.',
        features=['Dark premium visual system', 'Clear service list and visit information', 'Mobile-first typographic layout', 'Space for a real booking integration later'],
    ),
    'autohaus': dict(
        title='Autohaus',
        lead='A modern, technical and sophisticated concept for an automotive workshop.',
        industry='Automotive',
        desk='autohaus-desktop', mob='autohaus-mobile',
        desk_alt='Desktop mockup of the Autohaus concept.',
        mob_alt='Mobile mockup of the Autohaus concept.',
        objective='Give a workshop a site a mechanic would be willing to send — service data and a next step, not a brochure carousel.',
        audience='Independent garages and service workshops whose customers need hours, inspection, tyres and a way to request a slot.',
        approach='A light technical grid, monospaced labels and a four-step explanation of a visit. A signal red is used on actions and index numbers, not as a wash across the page.',
        features=['Technical grid and service snapshot', 'Clear next-step call to action', 'Responsive layout for the workshop floor and the office', 'Room for a real enquiry or booking form'],
    ),
    'maison-cafe': dict(
        title='Maison Café',
        lead='An elegant, warm and editorial concept for a neighbourhood restaurant and café.',
        industry='Restaurant',
        desk='maison-desktop', mob='maison-mobile',
        desk_alt='Desktop mockup of the Maison Café concept.',
        mob_alt='Mobile mockup of the Maison Café concept.',
        objective='Prove a café can feel generous with type, paper colour and a readable menu, without a folder of stock food photographs.',
        audience='Cafés and small restaurants whose guests need the menu, the hours and a sense of the room before they visit.',
        approach='A cream ground, a display serif and two simple lists. Prices are typographic, not badges. The page states clearly that the café is fictional and that nothing can be reserved here.',
        features=['Editorial typography and menu layout', 'Hours and visit information', 'Warm, restrained colour', 'A place for a tested form or booking link on a live project'],
    ),
}

def about_main(p):
    return f'''
    <section class="page-hero">
      <div class="wrap">
        <p class="eyebrow">About</p>
        <h1 class="display">Small studio. Big attention to detail.</h1>
        <p class="lead">WEBAUR is an independent web design studio. We help businesses establish a stronger online presence through modern websites and personal service.</p>
      </div>
    </section>
    <section class="section" style="padding-top:0">
      <div class="wrap prose">
        <p>The work is focused on quality, clear communication and practical results — a site that looks considered, loads quickly and makes it obvious what to do next. We use contemporary tools where they help, and we remain responsible for what goes live.</p>
        <p>The studio is starting with businesses in Finland and is designed to expand into France and other European markets when the work and the contracts are ready. We do not invent a large team, a long company history, awards or visitor statistics. When registration details exist, they will be published plainly here.</p>
        <p><a href="{p['contact']}">If you have a project in mind, tell us about it.</a></p>
      </div>
    </section>
'''

def contact_main(p):
    return f'''
    <section class="page-hero">
      <div class="wrap">
        <p class="eyebrow">Contact</p>
        <h1 class="display">Tell us about your project.</h1>
        <p class="lead">We would love to hear about your business and what you are looking to achieve.</p>
      </div>
    </section>
    <section class="section" style="padding-top:0">
      <div class="wrap form-layout">
        <div>
          <p>You can also write to <a href="mailto:hello@webaur.com"><strong>hello@webaur.com</strong></a>. That address is a placeholder until the professional mailbox is connected; until then, the form below is the reliable way to reach us once the site is hosted on Netlify.</p>
          <p class="muted" style="margin-top:1.2rem">There is no public telephone number or visiting address on this site yet. Those will be added when they exist.</p>
        </div>
        <form name="contact" method="POST" action="{p['thanks']}" data-netlify="true" data-netlify-honeypot="bot-field" netlify>
          <input type="hidden" name="form-name" value="contact">
          <p class="hp" aria-hidden="true">
            <label>Leave this field empty <input type="text" name="bot-field" tabindex="-1" autocomplete="off"></label>
          </p>
          <div class="field">
            <label for="name">Name</label>
            <input id="name" name="name" type="text" autocomplete="name" required>
          </div>
          <div class="field">
            <label for="business">Business name</label>
            <input id="business" name="business" type="text" autocomplete="organization">
          </div>
          <div class="field">
            <label for="email">Email</label>
            <input id="email" name="email" type="email" autocomplete="email" required>
          </div>
          <div class="field">
            <label for="project-type">Type of project</label>
            <select id="project-type" name="project-type" required>
              <option value="">Please select</option>
              <option value="new-website">A new website</option>
              <option value="redesign">A redesign</option>
              <option value="design">Website design only</option>
              <option value="maintenance">Website maintenance</option>
              <option value="not-sure">Not sure yet</option>
            </select>
          </div>
          <div class="field">
            <label for="budget">Estimated budget</label>
            <select id="budget" name="budget">
              <option value="not-sure">To be discussed</option>
              <option value="starter">Around the Starter package (€490 excl. VAT)</option>
              <option value="business">Around the Business package (€890 excl. VAT)</option>
              <option value="premium">Around the Premium package (€1,490 excl. VAT)</option>
              <option value="custom">A tailored quote</option>
            </select>
          </div>
          <div class="field">
            <label for="message">Project description</label>
            <textarea id="message" name="message" required></textarea>
          </div>
          <label class="consent">
            <input type="checkbox" name="privacy-consent" value="yes" required>
            <span>I have read the <a href="{p['privacy']}">privacy policy</a> and I agree that WEBAUR may use the details in this form to reply to me.</span>
          </label>
          <p class="form-note">A hidden honeypot field is included as spam protection. The form is built for Netlify Forms and will send once this site is hosted on Netlify. A Formspree alternative for Cloudflare Pages is described in the project README.</p>
          <button class="btn btn-ink" type="submit">Send the message</button>
        </form>
      </div>
    </section>
'''

def privacy_main(p):
    return f'''
    <section class="page-hero">
      <div class="wrap">
        <p class="eyebrow">Privacy</p>
        <h1 class="display">Privacy policy</h1>
        <p class="lead">This is a draft notice for a studio that is still being registered. Highlighted brackets mark facts that must be replaced with real details before this is relied on as a legal document. It is not legal advice.</p>
      </div>
    </section>
    <section class="section" style="padding-top:0">
      <div class="wrap prose">
        <p>Controller (to be completed): <span class="placeholder">[Legal name of the business]</span>, <span class="placeholder">[Business ID]</span>, <span class="placeholder">[Registered address]</span>. Contact: the form on this site, and <span class="placeholder">hello@webaur.com</span> once the mailbox is connected.</p>
        <h2>What this site collects</h2>
        <p>If you use the contact form, we process your name, business name, email, type of project, estimated budget, project description, and the consent you give, in order to reply and, if we work together, to prepare an offer. The legal basis intended here is your consent, and — once a project is being discussed — steps at your request before a contract (GDPR Article 6(1)(a) and 6(1)(b)).</p>
        <p>A honeypot field is included only to catch automated spam. It should be left empty.</p>
        <h2>Form service</h2>
        <p>When the site is hosted on Netlify, form submissions are processed by Netlify (Netlify Forms). Netlify then acts as a processor. A data-processing arrangement with that provider still needs to be put in place. If the site is hosted on Cloudflare Pages instead, Formspree or another form service would process the submissions, and that provider’s terms and location of processing must be checked first.</p>
        <h2>Cookies and analytics</h2>
        <p>This site does not set marketing cookies and does not include an analytics script at the time of writing. If that changes, this notice will be updated, and consent will be asked where the law requires it.</p>
        <h2>How long, and your rights</h2>
        <p>Enquiry messages are kept only as long as needed to reply and to keep a reasonable record of the conversation, then deleted or archived with a limit still to be set in <span class="placeholder">[retention period]</span>. You may ask for access, correction, deletion, or restriction, and you may withdraw consent for an enquiry at any time. You may complain to the Office of the Data Protection Ombudsman in Finland (tietosuoja.fi).</p>
        <h2>Children</h2>
        <p>This site is meant for adults acting for a business. It is not directed at children.</p>
        <p>Last updated: 9 November 2026.</p>
      </div>
    </section>
'''

def thanks_main(p):
    return f'''
    <section class="page-hero">
      <div class="wrap">
        <p class="eyebrow">Sent</p>
        <h1 class="display">Thank you.</h1>
        <p class="lead">If this site is already on Netlify and the form is active, your message is with the studio. We will reply personally. If you were testing the static files on your computer, the form has not gone anywhere yet — deploy to Netlify first, then send a test.</p>
        <div class="btn-row" style="margin-top:2rem">
          <a class="btn btn-ink" href="{p['home']}">Back to the home page</a>
          <a class="btn btn-ghost" href="{p['work']}">Explore our work</a>
        </div>
      </div>
    </section>
'''

def notfound_page(p):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Page not found — WEBAUR</title>
  <meta name="robots" content="noindex">
  <meta name="theme-color" content="#F7F7F4">
  <link rel="icon" href="{p['prefix']}images/brand/favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&amp;display=swap">
  <link rel="stylesheet" href="{p['prefix']}css/styles.css">
  <style>.lost {{ min-height: 80vh; display:flex; align-items:center; }}</style>
</head>
<body>
  <main id="main" class="lost">
    <div class="wrap">
      <p class="eyebrow">404</p>
      <h1 class="display">This page is not here.</h1>
      <p class="lead" style="margin:1rem 0 1.8rem">The link may be old, or the address may have been typed with a slip. The studio home page is still in the usual place.</p>
      <a class="btn btn-ink" href="{p['home']}">Go to the home page</a>
    </div>
  </main>
</body>
</html>
'''

def write(path, text):
    path = ROOT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    print('wrote', path.relative_to(ROOT))

def build_tree(folder):
    prefix_folder = (folder + '/') if folder else ''
    base_canon = DOMAIN  # en copies canonicalise to root
    pages = [
        ('index.html', 'home', 'WEBAUR — Website design for small businesses',
         'WEBAUR is an independent web design studio. We design and build modern websites that help businesses stand out, build trust and turn visitors into customers. Starting prices, excl. VAT.',
         f'{DOMAIN}/', home_main),
        ('services.html', 'services', 'Services — Website design, development and maintenance — WEBAUR',
         'Website design, development and maintenance for businesses. Responsive design, SEO foundations, contact forms and performance — without guaranteed rankings.',
         f'{DOMAIN}/services.html', services_main),
        ('work.html', 'work', 'Our Work — Concept projects — WEBAUR',
         'Concept projects from WEBAUR: Barber Studio, Autohaus and Maison Café. Original website design studies, not client commissions.',
         f'{DOMAIN}/work.html', work_main),
        ('about.html', 'about', 'About — WEBAUR',
         'Small studio. Big attention to detail. WEBAUR is an independent web design studio helping businesses establish a stronger online presence.',
         f'{DOMAIN}/about.html', about_main),
        ('contact.html', 'contact', 'Contact — Tell us about your project — WEBAUR',
         'Tell WEBAUR about your project. Write through the contact form or hello@webaur.com once the mailbox is connected.',
         f'{DOMAIN}/contact.html', contact_main),
        ('privacy.html', 'privacy', 'Privacy policy — WEBAUR',
         'How WEBAUR intends to handle contact-form messages. Placeholders mark details that still need a registered business.',
         f'{DOMAIN}/privacy.html', privacy_main),
        ('thanks.html', 'contact', 'Thank you — WEBAUR',
         'Your message has been recorded if this site is hosted on Netlify with forms enabled.',
         f'{DOMAIN}/thanks.html', thanks_main),
    ]
    p_page = paths('root' if folder == '' else 'en')
    for filename, current, title, desc, canonical, body_fn in pages:
        html = page_shell(p_page, current, title, desc, canonical, body_fn(p_page))
        if filename == 'thanks.html':
            html = html.replace('<meta name="description"', '<meta name="robots" content="noindex">\n  <meta name="description"', 1)
        write(prefix_folder + filename, html)

    p_work = paths('work' if folder == '' else 'en_work')
    for slug, data in CASES.items():
        title = f"{data['title']} — Concept project — WEBAUR"
        desc = data['lead']
        canonical = f"{DOMAIN}/work/{slug}.html"
        html = page_shell(p_work, 'work', title, desc, canonical, case_main(p_work, data))
        write(prefix_folder + f'work/{slug}.html', html)

    p_404 = paths('root' if folder == '' else 'en')
    write(prefix_folder + '404.html', notfound_page(p_404))

def main():
    build_tree('')
    build_tree('en')

if __name__ == '__main__':
    main()
