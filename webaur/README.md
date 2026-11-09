# WEBAUR website (v3)

Independent web design studio site — static HTML, CSS and JavaScript. No required build step.

Finnish is the default language at the site root. English lives in `/en/`. v2 remains untouched in `/workspace/webaur-v2/`.

## Local preview (including the GitHub Pages subdirectory)

The public project is hosted under a subdirectory:

`/halden-barbers-demo/webaur/`

All internal links, images, fonts, CSS, JavaScript and demos use relative paths so they work in that folder, not only at a domain root.

To preview the same way:

```bash
# from a parent folder that contains halden-barbers-demo/webaur/
python3 -m http.server 8768 --bind 127.0.0.1
```

Open `http://127.0.0.1:8768/halden-barbers-demo/webaur/`.

## Languages

- Finnish (default): `index.html`, `services.html`, `work.html`, `about.html`, `contact.html`, `privacy.html`, `thanks.html`, `404.html`, and `work/*.html`
- English: the same files under `en/`
- Every studio page has an `hreflang` set (`fi`, `en`, `x-default` → Finnish) and a FI / EN switcher that maps to the counterpart page
- French can be added later as `/fr/` without rebuilding the system
- Concept demos keep their own brand language (they are fictional identities). Portfolio descriptions around them are translated.

The Finnish copy was written to sound like natural professional Finnish, not a line-by-line machine translation. A native speaker should still proofread it before launch.

## Pages and demos

- Studio pages as listed above, in both languages
- Case studies: `work/barber-studio.html`, `work/detailing.html`, `work/maison-cafe.html` (and `en/work/…`)
- Working concept demos: `demos/barber-studio/`, `demos/detailing/`, `demos/maison-cafe/` (`noindex`, labelled as concepts; booking buttons do not place a real booking)

## Deploy

### GitHub Pages (current host)

Upload this folder so that it is served from `/halden-barbers-demo/webaur/`. There is no build command. GitHub Pages will not process the contact form — configure Formspree first (below).

GitHub Pages uses the root `404.html` (Finnish) for unknown URLs. The English 404 is at `en/404.html`.

### Custom domain

After a domain is connected, point it at the host and serve this folder at the domain root (or keep the subfolder and update canonical URLs). Replace the placeholder host `https://webaur.com` in `sitemap.xml`, `robots.txt` and the canonical/hreflang/Open Graph tags. Then set a real mailbox and replace `hello@[your-domain]`.

### Netlify

Publish directory `.`, no build command. Netlify Forms will detect the form in `contact.html` and `en/contact.html`. Set a notification email. `_redirects` and `netlify.toml` are included.

### Cloudflare Pages

Publish directory `.`, no build command. Use Formspree; Netlify Forms will not run.

## Contact form

**Where it lives:** `contact.html` and `en/contact.html`. Shared behaviour is in `js/main.js`. The endpoint is configured in `js/form-config.js`.

**GitHub Pages cannot process form posts.** Until a sending service is connected, the form validates the fields and then shows an honest message: nothing was sent. It never claims a successful send.

**Formspree (recommended for GitHub Pages and Cloudflare Pages):**

1. Create a form at [formspree.io](https://formspree.io/) and copy the endpoint, e.g. `https://formspree.io/f/xxxxxxxx`.
2. Set `window.WEBAUR_FORM.formspree` in `js/form-config.js`.
3. In Formspree, set the thank-you redirect to your live `thanks.html` (or `en/thanks.html`) URL, or keep Formspree’s confirmation page.
4. Record the endpoint here once it exists: `Formspree endpoint: [not configured]`.

**Netlify Forms:** leave `formspree` as an empty string and deploy to Netlify. The forms already include `data-netlify`, a honeypot and a consent field.

Budget can be pre-filled with `?package=starter|business|premium#form`.

## Pricing

Starter / Aloitus €490, Business / Yritys €890 (popular), Premium €1,490.

**Prices excl. VAT (Finnish VAT 25.5% added).** The final price depends on the agreed scope. Domain registration and hosting are **not** included, nor are photography or copywriting beyond the agreed scope, ongoing maintenance, or features outside the chosen package.

## Placeholders (replace before launch)

- Email shown as **`hello@[your-domain]`**, visually marked — not a live inbox
- No phone number or street address
- Privacy policy: legal name, Y-tunnus, postal address, and analytics provider
- Canonical / Open Graph / sitemap host: `https://webaur.com`
- Formspree endpoint: not configured
- Café, shop and workshop locations in the demos are fictional and labelled as such

## Credits

See `CREDITS.md` for every demo photograph, source URL and licence.

Self-hosted typefaces: [Geist](https://vercel.com/font) (SIL Open Font License) and [Manrope](https://www.fontsquirrel.com/fonts/manrope) (SIL Open Font License).

## What was not completed or not fully tested

- A native Finnish speaker should proofread all Finnish studio copy
- Unsplash photographer names could not always be confirmed from live photo pages (IDs and licences are in CREDITS.md)
- Formspree is not yet connected, so a live submission has not been performed on production
- A real domain, mailbox and legal entity were not connected
- Concept demos are not fully translated (they are fictional brand sites)
- Lighthouse scores are from a local server, not a CDN
- drool.design could not be fully captured (the page returned an interstitial / timed out); principles were taken from the other references and from the studio’s publicly known typographic approach
