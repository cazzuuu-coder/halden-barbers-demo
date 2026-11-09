#!/usr/bin/env python3
"""Generate WEBAUR v2 studio pages. Run from /workspace/webaur-v2."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def pic(src_stem, alt, sizes="(min-width: 900px) 720px, 100vw", loading="lazy"):
    # stems live under images/work or relative prefix already included
    return f'''<picture>
  <source type="image/webp" srcset="{src_stem}.webp" />
  <img src="{src_stem}.jpg" alt="{alt}" loading="{loading}" decoding="async" sizes="{sizes}" />
</picture>'''

def logo(prefix=""):
    return f'''<a class="logo" href="{prefix}index.html" aria-label="WEBAUR home"><span class="wm">WEB<span class="wm-a">A</span>UR</span></a>'''

NAV = [
    ("index.html", "Home"),
    ("services.html", "Services"),
    ("work.html", "Our Work"),
    ("about.html", "About"),
    ("contact.html", "Contact"),
]

def header(active, prefix=""):
    links = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == active else ""
        links.append(f'<li><a href="{prefix}{href}"{cur}>{label}</a></li>')
    return f'''<a class="skip" href="#content">Skip to content</a>
<header class="site-header">
  <div class="wrap nav">
    {logo(prefix)}
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="nav-panel" aria-label="Open menu"><span></span><span></span></button>
    <div class="nav-panel" id="nav-panel">
      <ul class="nav-links">
        {"".join(links)}
      </ul>
      <span class="lang" title="English is the current language. Finnish can be added later.">EN</span>
      <a class="nav-cta" href="{prefix}contact.html">Let’s Talk</a>
    </div>
  </div>
</header>'''

def footer(prefix=""):
    return f'''<footer class="site-footer">
  <div class="wrap footer-grid">
    <div>
      {logo(prefix)}
      <p class="footer-note" style="margin-top:16px;max-width:28rem">Independent web design studio. We design and build modern websites that help businesses stand out and turn visitors into customers.</p>
    </div>
    <div>
      <ul class="footer-col">
        <li><strong>Navigate</strong></li>
        <li><a href="{prefix}index.html">Home</a></li>
        <li><a href="{prefix}services.html">Services</a></li>
        <li><a href="{prefix}work.html">Our Work</a></li>
        <li><a href="{prefix}about.html">About</a></li>
        <li><a href="{prefix}contact.html">Contact</a></li>
      </ul>
    </div>
    <div>
      <ul class="footer-col">
        <li><strong>Services</strong></li>
        <li><a href="{prefix}services.html#design">Website Design</a></li>
        <li><a href="{prefix}services.html#development">Website Development</a></li>
        <li><a href="{prefix}services.html#maintenance">Website Maintenance</a></li>
      </ul>
    </div>
    <div>
      <ul class="footer-col">
        <li><strong>Contact</strong></li>
        <li>Email (placeholder — not a live address):<br><span class="placeholder">hello@[your-domain]</span></li>
        <li><a href="{prefix}privacy.html">Privacy Policy</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap legal">
    <span>© 2026 WEBAUR. All rights reserved.</span>
    <span>Independent design studio.</span>
  </div>
</footer>'''

def cta(prefix=""):
    return f'''<section class="cta-band" aria-labelledby="cta-title">
  <div class="wrap">
    <p class="eyebrow" style="color:#b4b7b2">START A PROJECT</p>
    <h2 id="cta-title" class="display" style="margin:12px 0 16px">Ready to give your business a better website?</h2>
    <p class="lead">Tell us a little about your business and what you’re looking for. We’ll take it from there.</p>
    <p style="margin-top:32px"><a class="btn btn-ink" href="{prefix}contact.html">Let’s talk</a></p>
  </div>
</section>'''

def page(title, description, path, active, body, prefix="", og=None):
    css = f"{prefix}css/styles.css"
    js = f"{prefix}js/main.js"
    canon = "https://webaur.com/" + ("" if path == "index.html" else path)
    fav = f"{prefix}images/brand/favicon.svg"
    ico32 = f"{prefix}images/brand/favicon-32.png"
    apple = f"{prefix}images/brand/apple-touch-icon.png"
    og_img = og or f"{prefix}images/og/og-default.jpg"
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title}</title>
  <meta name="description" content="{description}" />
  <link rel="canonical" href="{canon}" />
  <meta property="og:type" content="website" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{description}" />
  <meta property="og:url" content="{canon}" />
  <meta property="og:image" content="https://webaur.com/images/og/og-default.jpg" />
  <meta name="twitter:card" content="summary_large_image" />
  <link rel="icon" href="{fav}" type="image/svg+xml" />
  <link rel="icon" href="{ico32}" type="image/png" sizes="32x32" />
  <link rel="apple-touch-icon" href="{apple}" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="{css}" />
</head>
<body>
{header(active, prefix)}
<main id="content">
{body}
</main>
{footer(prefix)}
<script src="{js}" defer></script>
</body>
</html>
'''

def device_desktop(stem, alt, loading="lazy", prefix=""):
    return f'''<div class="device-desktop">
  <div class="chrome" aria-hidden="true"><i></i><i></i><i></i></div>
  <div class="screen">{pic(prefix + stem, alt, loading=loading)}</div>
</div>'''

def device_mobile(stem, alt, loading="lazy", prefix=""):
    return f'''<div class="device-mobile">
  <div class="notch" aria-hidden="true"></div>
  <div class="screen">{pic(prefix + stem, alt, loading=loading)}</div>
</div>'''

PROJECTS = [
    dict(
        slug="barber-studio",
        title="Hale Barber Studio",
        category="Barber · Editorial",
        desc="A dark, editorial concept for an independent barbershop: services, photography and an appointment CTA.",
        demo="demos/barber-studio/index.html",
        desk="images/work/hale-desktop",
        mob="images/work/hale-mobile",
    ),
    dict(
        slug="detailing",
        title="Alto Detail",
        category="Automotive detailing",
        desc="A sophisticated detailing brand with packages, photography and a before-and-after comparison.",
        demo="demos/detailing/index.html",
        desk="images/work/alto-desktop",
        mob="images/work/alto-mobile",
    ),
    dict(
        slug="maison-cafe",
        title="Maison Café",
        category="Café · Hospitality",
        desc="A warm, typographic café site with menu, hours, location and a reservation invitation.",
        demo="demos/maison-cafe/index.html",
        desk="images/work/maison-desktop",
        mob="images/work/maison-mobile",
    ),
]

def project_row(p, prefix=""):
    return f'''<article class="project-row">
  <div class="frames">
    {device_desktop(p["desk"], f'Desktop preview of the {p["title"]} concept website', prefix=prefix)}
    {device_mobile(p["mob"], f'Mobile preview of the {p["title"]} concept website', prefix=prefix)}
  </div>
  <div>
    <span class="badge">Concept project</span>
    <p class="kicker" style="margin-top:12px">{p["category"]}</p>
    <h2>{p["title"]}</h2>
    <p class="muted">{p["desc"]}</p>
    <div class="project-actions">
      <a class="btn btn-ink" href="{prefix}{p["demo"]}">Open demo</a>
      <a class="btn btn-ghost" href="{prefix}work/{p["slug"]}.html">View project</a>
    </div>
  </div>
</article>'''

PRICING = '''
<section class="section" id="pricing" aria-labelledby="pricing-title">
  <div class="wrap">
    <div class="section-head">
      <div>
        <p class="eyebrow">OUR PACKAGES</p>
        <h2 id="pricing-title" class="section-title" style="margin-top:12px">Clear pricing. No unnecessary complexity.</h2>
      </div>
    </div>
    <div class="price-grid">
      <article class="price-card">
        <h3>Starter</h3>
        <p class="price">€490</p>
        <p class="muted">For businesses that need a professional online presence.</p>
        <ul>
          <li>One-page website</li>
          <li>Responsive design</li>
          <li>Contact information</li>
          <li>Services presentation</li>
          <li>Basic SEO setup</li>
          <li>Contact button</li>
        </ul>
        <a class="btn btn-ghost" href="CONTACT?package=starter#form">Choose Starter</a>
      </article>
      <article class="price-card featured">
        <span class="popular">POPULAR</span>
        <h3>Business</h3>
        <p class="price">€890</p>
        <p class="muted">For businesses that need a more complete website.</p>
        <ul>
          <li>4–6 pages</li>
          <li>Custom design</li>
          <li>Responsive development</li>
          <li>Contact form</li>
          <li>Services pages</li>
          <li>Google Maps integration where relevant</li>
          <li>SEO foundations</li>
        </ul>
        <a class="btn btn-accent" href="CONTACT?package=business#form">Choose Business</a>
      </article>
      <article class="price-card">
        <h3>Premium</h3>
        <p class="price">€1,490</p>
        <p class="muted">For businesses that want a more advanced website.</p>
        <ul>
          <li>6–10 pages</li>
          <li>More advanced custom design</li>
          <li>Advanced page layouts</li>
          <li>Animations and interactions</li>
          <li>Analytics integration</li>
          <li>SEO foundations</li>
          <li>Additional functionality where agreed</li>
        </ul>
        <a class="btn btn-ghost" href="CONTACT?package=premium#form">Choose Premium</a>
      </article>
    </div>
    <p class="muted" style="margin-top:24px">Prices excl. VAT (Finnish VAT 25.5% added). The final price depends on the scope of the project.</p>
    <p style="margin-top:12px">Need something different? Get in touch and we’ll create a solution around your business.</p>
  </div>
</section>
'''

# ---------- pages ----------
home = f'''
<section class="hero">
  <div class="wrap hero-grid">
    <div class="reveal">
      <p class="eyebrow">INDEPENDENT WEB DESIGN STUDIO</p>
      <h1 class="display">Your business deserves a better website.</h1>
      <p class="lead">We design and build modern websites that help businesses stand out, build trust and turn visitors into customers.</p>
      <div class="btn-row">
        <a class="btn btn-ink" href="contact.html">Start a project</a>
        <a class="btn btn-ghost" href="work.html">Explore our work</a>
      </div>
      <p class="avail"><i aria-hidden="true"></i> Currently accepting new projects</p>
    </div>
    <div class="device-stack reveal" style="animation-delay:.12s">
      {device_desktop("images/work/hale-desktop", "Desktop concept preview of Hale Barber Studio, a WEBAUR design", loading="eager")}
      {device_mobile("images/work/hale-mobile", "Mobile concept preview of Hale Barber Studio", loading="eager")}
      <p class="concept-label">Concept project — Hale Barber Studio</p>
    </div>
  </div>
</section>
<section class="section band band-line" aria-labelledby="intro-title">
  <div class="wrap split">
    <div>
      <p class="eyebrow">WHAT WE DO</p>
      <h2 id="intro-title" class="section-title" style="margin:12px 0 16px">Good design is more than appearance.</h2>
    </div>
    <div>
      <p class="lead">Your website is often the first impression customers have of your business. We create digital experiences that communicate quality, make information easy to find and help visitors take the next step.</p>
    </div>
  </div>
</section>
<section class="section" aria-labelledby="services-title">
  <div class="wrap">
    <p class="eyebrow">OUR SERVICES</p>
    <h2 id="services-title" class="section-title" style="margin:12px 0 32px">Everything your website needs.</h2>
    <article class="service-block" id="design">
      <div class="num">01</div>
      <div>
        <h3>Website Design</h3>
        <p>Modern, professional websites designed around your brand, customers and business goals.</p>
      </div>
      <ul>
        <li>Custom visual design</li>
        <li>Responsive layouts</li>
        <li>User experience</li>
        <li>Brand consistency</li>
      </ul>
    </article>
  </div>
  <div class="service-dark">
    <article class="service-block" id="development">
      <div class="num">02</div>
      <div>
        <h3>Website Development</h3>
        <p>Fast, reliable websites built to work beautifully across phones, tablets and computers.</p>
      </div>
      <ul>
        <li>Front-end development</li>
        <li>Mobile optimization</li>
        <li>Performance optimization</li>
        <li>Contact forms</li>
        <li>Technical SEO foundations</li>
      </ul>
    </article>
  </div>
  <div class="wrap">
    <article class="service-block service-framed" id="maintenance">
      <div class="num">03</div>
      <div>
        <h3>Website Maintenance</h3>
        <p>Keep your website secure, updated and working as it should.</p>
      </div>
      <ul>
        <li>Website updates</li>
        <li>Technical support</li>
        <li>Content changes</li>
        <li>Performance checks</li>
      </ul>
    </article>
  </div>
</section>
<section class="section" aria-labelledby="work-title">
  <div class="wrap">
    <div class="section-head">
      <div>
        <p class="eyebrow">SELECTED WORK</p>
        <h2 id="work-title" class="section-title" style="margin-top:12px">Made to make an impression.</h2>
      </div>
      <a class="btn btn-ghost" href="work.html">All work</a>
    </div>
    {"".join(project_row(p) for p in PROJECTS)}
  </div>
</section>
<section class="section band band-line" aria-labelledby="why-title">
  <div class="wrap">
    <p class="eyebrow">WHY WEBAUR</p>
    <h2 id="why-title" class="section-title" style="margin:12px 0 32px">Built around your business.</h2>
    <div class="why-grid">
      <article class="why-card"><p class="idx">01</p><h3>Designed for your brand</h3><p class="muted">Every website is designed around the identity and needs of your business.</p></article>
      <article class="why-card"><p class="idx">02</p><h3>Made for every screen</h3><p class="muted">Your website will work smoothly on mobile, tablet and desktop.</p></article>
      <article class="why-card"><p class="idx">03</p><h3>Performance matters</h3><p class="muted">Fast loading and clean development help create a better user experience.</p></article>
      <article class="why-card"><p class="idx">04</p><h3>Focused on results</h3><p class="muted">Clear structure and strong calls to action help visitors understand your business and get in touch.</p></article>
    </div>
  </div>
</section>
<section class="section" aria-labelledby="process-title">
  <div class="wrap">
    <p class="eyebrow">HOW WE WORK</p>
    <h2 id="process-title" class="section-title" style="margin:12px 0 40px">A straightforward process.</h2>
    <ol class="timeline">
      <li><div class="dot">01</div><div><h3>Discover</h3><p class="muted">We learn about your business, goals and customers.</p></div></li>
      <li><div class="dot">02</div><div><h3>Design</h3><p class="muted">We create a visual direction and website structure.</p></div></li>
      <li><div class="dot">03</div><div><h3>Build</h3><p class="muted">We develop and optimize your website.</p></div></li>
      <li><div class="dot">04</div><div><h3>Launch</h3><p class="muted">Your website goes live and is ready for customers.</p></div></li>
    </ol>
  </div>
</section>
{PRICING.replace("CONTACT", "contact.html")}
{cta()}
'''

services_page = f'''
<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow">SERVICES</p>
    <h1 class="display">Everything your website needs.</h1>
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
      <p>Modern, professional websites designed around your brand, customers and business goals.</p>
      <ul class="muted" style="margin-top:16px;list-style:disc;padding-left:18px;display:grid;gap:8px">
        <li>Custom visual design</li><li>Responsive layouts</li><li>User experience</li><li>Brand consistency</li>
      </ul>
      <p class="muted" style="margin-top:16px">A clear structure, considered typography and photography that belongs to your business — not a generic template.</p>
    </div>
  </div>
</section>
<section class="section" style="background:var(--dark);color:var(--bg)" id="development">
  <div class="wrap split">
    <div>
      <p class="kicker" style="color:#b4b7b2">02</p>
      <h2 class="section-title">Website Development</h2>
    </div>
    <div>
      <p>Fast, reliable websites built to work beautifully across phones, tablets and computers.</p>
      <ul style="margin-top:16px;list-style:disc;padding-left:18px;display:grid;gap:8px;color:#b4b7b2">
        <li>Front-end development</li><li>Mobile optimization</li><li>Performance optimization</li><li>Contact forms</li><li>Technical SEO foundations</li>
      </ul>
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
      <p>Keep your website secure, updated and working as it should.</p>
      <ul class="muted" style="margin-top:16px;list-style:disc;padding-left:18px;display:grid;gap:8px">
        <li>Website updates</li><li>Technical support</li><li>Content changes</li><li>Performance checks</li>
      </ul>
    </div>
  </div>
</section>
<section class="section band band-line">
  <div class="wrap">
    <p class="eyebrow">HOW WE WORK</p>
    <h2 class="section-title" style="margin:12px 0 32px">A straightforward process.</h2>
    <ol class="timeline">
      <li><div class="dot">01</div><div><h3>Discover</h3><p class="muted">We learn about your business, goals and customers.</p></div></li>
      <li><div class="dot">02</div><div><h3>Design</h3><p class="muted">We create a visual direction and website structure.</p></div></li>
      <li><div class="dot">03</div><div><h3>Build</h3><p class="muted">We develop and optimize your website.</p></div></li>
      <li><div class="dot">04</div><div><h3>Launch</h3><p class="muted">Your website goes live and is ready for customers.</p></div></li>
    </ol>
  </div>
</section>
{PRICING.replace("CONTACT", "contact.html")}
{cta()}
'''

work_page = f'''
<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow">OUR WORK</p>
    <h1 class="display">Made to make an impression.</h1>
    <p class="lead">Three complete concept projects, designed and built as working websites. They are independent design concepts — not paying-client work — created to show how WEBAUR approaches different industries.</p>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap">
    {"".join(project_row(p) for p in PROJECTS)}
  </div>
</section>
{cta()}
'''

def case_page(p):
    prefix = "../"
    return f'''
<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow"><a href="../work.html">Our Work</a> / {p["title"]}</p>
    <span class="badge">Concept project</span>
    <h1 class="display" style="margin-top:16px">{p["title"]}</h1>
    <p class="lead">{p["desc"]}</p>
    <div class="btn-row" style="margin-top:24px">
      <a class="btn btn-ink" href="../{p["demo"]}">Open demo</a>
      <a class="btn btn-ghost" href="../work.html">Back to work</a>
    </div>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="case-frames">
      {device_desktop(p["desk"], f'Desktop preview of {p["title"]}', prefix=prefix)}
      {device_mobile(p["mob"], f'Mobile preview of {p["title"]}', prefix=prefix)}
    </div>
    <div class="case-copy">
      <div>
        <h2>The brief</h2>
        <p class="muted">This is an independent design concept. It is not a paying-client website. The goal was to show how a complete, industry-specific site can feel when design, photography and structure work together.</p>
      </div>
      <div>
        <h2>What you’ll find in the demo</h2>
        <p class="muted">A multi-section website with its own typography, colour and photography. Booking or reservation buttons in the demo lead to a contact section clearly labelled as a concept — they do not place a real booking.</p>
      </div>
    </div>
  </div>
</section>
{cta(prefix)}
'''

about = f'''
<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow">ABOUT</p>
    <h1 class="display">Attention to the details that build trust.</h1>
    <p class="lead">WEBAUR is an independent web design studio. We help businesses improve their online presence with considered design, careful development and clear communication.</p>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap prose">
    <h2>Good design</h2>
    <p>A website should look like your business, not like a template. We pay attention to typography, spacing, photography and hierarchy so the first impression feels intentional.</p>
    <h2>Technical quality</h2>
    <p>Design only works if the site is fast, readable and reliable on every screen. We build with clean front-end code, thoughtful performance and a structure that is easy to maintain.</p>
    <h2>Clear communication</h2>
    <p>We keep the process straightforward: discover, design, build, launch. You will always know what is happening and what we need from you.</p>
    <h2>Helping businesses be found</h2>
    <p>We focus on making information easy to find and the next step obvious — a call, a visit, a message. No invented awards, client logos or years in business. The work should speak for itself.</p>
    <p><a class="btn btn-ink" href="contact.html" style="margin-top:8px">Start a project</a></p>
  </div>
</section>
'''

contact = f'''
<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow">CONTACT</p>
    <h1 class="display">Tell us about your project.</h1>
    <p class="lead">Share a little about your business and what you need. We will get back to you to talk through the next step.</p>
  </div>
</section>
<section class="section" style="padding-top:0" id="form">
  <div class="wrap form-layout">
    <div>
      <p>Prefer email? Use the address below once a domain is connected. It is a placeholder, not a live inbox.</p>
      <p style="margin:16px 0 24px"><span class="placeholder">hello@[your-domain]</span></p>
      <p class="muted">The form is set up for <strong>Netlify Forms</strong>. It will submit after the site is hosted on Netlify. On other hosts, connect Formspree or another form endpoint — see the README for where that configuration lives.</p>
    </div>
    <form name="contact" method="POST" action="thanks.html" data-netlify="true" data-netlify-honeypot="company-website" netlify-honeypot="company-website">
      <input type="hidden" name="form-name" value="contact" />
      <p class="hp"><label>Company website <input name="company-website" tabindex="-1" autocomplete="off" /></label></p>
      <div class="field">
        <label for="name">Name</label>
        <input id="name" name="name" type="text" autocomplete="name" required />
      </div>
      <div class="field">
        <label for="business">Business name</label>
        <input id="business" name="business" type="text" autocomplete="organization" required />
      </div>
      <div class="field">
        <label for="email">Email</label>
        <input id="email" name="email" type="email" autocomplete="email" required />
      </div>
      <div class="field">
        <label for="type">Type of website</label>
        <select id="type" name="type" required>
          <option value="">Please select</option>
          <option>New website</option>
          <option>Redesign</option>
          <option>Landing page</option>
          <option>Something else</option>
        </select>
      </div>
      <div class="field">
        <label for="budget">Approximate budget (optional)</label>
        <select id="budget" name="budget">
          <option value="">Prefer not to say</option>
          <option>Starter — around €490 + VAT</option>
          <option>Business — around €890 + VAT</option>
          <option>Premium — around €1,490 + VAT</option>
          <option>Not sure yet</option>
        </select>
      </div>
      <div class="field">
        <label for="message">Project description</label>
        <textarea id="message" name="message" required></textarea>
      </div>
      <label class="consent">
        <input type="checkbox" name="consent" value="yes" required />
        <span>I agree that WEBAUR may use this information to respond to my enquiry. See the <a href="privacy.html">privacy policy</a>.</span>
      </label>
      <button class="btn btn-ink" type="submit">Send message</button>
      <p class="form-note">This form does not pretend to send a message until it is submitted to a connected host (Netlify Forms, or Formspree — documented in README.md).</p>
    </form>
  </div>
</section>
'''

thanks = '''
<section class="page-hero">
  <div class="wrap prose">
    <p class="eyebrow">THANK YOU</p>
    <h1 class="display">Your message is on its way.</h1>
    <p class="lead">This page is shown after a successful form submission. If you opened it directly, nothing has been sent.</p>
    <p><a class="btn btn-ink" href="index.html">Back to home</a></p>
  </div>
</section>
'''

privacy = '''
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
    <p>If you submit the contact form we collect the name, business name, email, project type, optional budget and message you provide, plus a consent record. A honeypot field is used only to reduce spam and should be left empty.</p>
    <h2>Why we collect it</h2>
    <p>To respond to project enquiries. We do not use the form data for marketing lists unless you have separately agreed.</p>
    <h2>Processors</h2>
    <p>When the site is hosted on Netlify, form submissions are processed by Netlify Forms. If the site is hosted elsewhere, Formspree or another form provider may be used — see README.md. Analytics: <span class="placeholder">[none configured / provider name]</span>.</p>
    <h2>Retention and rights</h2>
    <p>Enquiries are kept only as long as needed to handle the conversation and any resulting work. You may ask to access, correct or delete your data by writing to the contact address above once it is live. You may also contact a data protection authority in your country (in Finland, the Office of the Data Protection Ombudsman).</p>
    <p>Last updated: 9 November 2026.</p>
  </div>
</section>
'''

not_found = '''
<section class="page-hero">
  <div class="wrap prose">
    <p class="eyebrow">404</p>
    <h1 class="display">This page could not be found.</h1>
    <p class="lead">The address may have changed, or the page may not exist.</p>
    <p><a class="btn btn-ink" href="index.html">Back to home</a></p>
  </div>
</section>
'''

def write(rel, html):
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    print("wrote", rel)

write("index.html", page("WEBAUR — Independent web design studio", "WEBAUR designs and builds modern websites that help businesses stand out, build trust and turn visitors into customers.", "index.html", "index.html", home))
write("services.html", page("Services — WEBAUR", "Website design, development and maintenance from WEBAUR, with clear packages from €490 excl. VAT.", "services.html", "services.html", services_page))
write("work.html", page("Our Work — WEBAUR", "Concept projects by WEBAUR: Hale Barber Studio, Alto Detail and Maison Café — complete working demo websites.", "work.html", "work.html", work_page))
write("about.html", page("About — WEBAUR", "WEBAUR is an independent web design studio focused on good design, technical quality and clear communication.", "about.html", "about.html", about))
write("contact.html", page("Contact — WEBAUR", "Tell WEBAUR about your project. Start a conversation about a new website or a redesign.", "contact.html", "contact.html", contact))
write("thanks.html", page("Thank you — WEBAUR", "Your message has been submitted to WEBAUR.", "thanks.html", "contact.html", thanks))
write("privacy.html", page("Privacy Policy — WEBAUR", "How WEBAUR handles contact-form data, with clearly marked placeholders for legal details.", "privacy.html", "", privacy))
write("404.html", page("Page not found — WEBAUR", "The page you requested could not be found.", "404.html", "", not_found))
for p in PROJECTS:
    write(f"work/{p['slug']}.html", page(f"{p['title']} — Concept project — WEBAUR", p["desc"], f"work/{p['slug']}.html", "work.html", case_page(p), prefix="../"))

# sitemap, robots, netlify
pages = ["", "services.html", "work.html", "about.html", "contact.html", "privacy.html", "thanks.html",
         "work/barber-studio.html", "work/detailing.html", "work/maison-cafe.html",
         "demos/barber-studio/index.html", "demos/detailing/index.html", "demos/maison-cafe/index.html"]
urls = "\n".join(f"  <url><loc>https://webaur.com/{u}</loc></url>" for u in pages)
(ROOT / "sitemap.xml").write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}
</urlset>
''', encoding="utf-8")
(ROOT / "robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: https://webaur.com/sitemap.xml\n", encoding="utf-8")
(ROOT / "netlify.toml").write_text('''[build]
  publish = "."

[[redirects]]
  from = "/en/*"
  to = "/:splat"
  status = 301

[[headers]]
  for = "/*"
  [headers.values]
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"
    X-Frame-Options = "SAMEORIGIN"

[[headers]]
  for = "/images/*"
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
