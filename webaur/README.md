# WEBAUR website (v2)

Independent web design studio site — static HTML, CSS and JavaScript. No required build step.

This folder is a complete redesign of the earlier v1 site in `/workspace/webaur-site/`. v1 is left untouched.

## Local preview

From this folder:

```bash
python3 -m http.server 8766 --bind 127.0.0.1
```

Open `http://127.0.0.1:8766/`. All internal links are relative so the site can also be served from a GitHub Pages project subfolder (for example `https://user.github.io/webaur-v2/`).

## Pages

- Studio: `index.html`, `services.html`, `work.html`, `about.html`, `contact.html`, `thanks.html`, `privacy.html`, `404.html`
- Case studies: `work/barber-studio.html`, `work/detailing.html`, `work/maison-cafe.html`
- Working concept demos: `demos/barber-studio/`, `demos/detailing/`, `demos/maison-cafe/`

The three demos are independent design concepts, not paying-client work. Booking and reservation buttons scroll to a clearly labelled “concept — no real booking” note.

## Deploy

### Netlify (recommended for the contact form)

1. Connect this folder as the site root (publish directory `.`, no build command).
2. Netlify will detect the form in `contact.html` (`data-netlify="true"`, hidden `form-name`, honeypot `company-website`).
3. In Netlify → Forms, confirm the `contact` form is listed and set the notification email to a real inbox.
4. Successful submissions go to `thanks.html` (`action="thanks.html"`).
5. `_redirects` maps unknown routes to `404.html`. `netlify.toml` sets basic security headers.

### Cloudflare Pages

1. Upload this folder, output directory `.`, no build command.
2. Netlify Forms will **not** run on Cloudflare Pages. Connect Formspree (or another form endpoint) before launch — see below.
3. `_headers` is included for Cloudflare/Netlify-style header files.

### GitHub Pages

Upload the folder (or `/docs`) and enable Pages. Use relative links as already written. The contact form will not send until you add Formspree or a similar endpoint.

## Contact form configuration

**Where it lives:** `contact.html` (the `<form>` element). Prefill of the optional budget field from `?package=starter|business|premium` is in `js/main.js`.

**Netlify Forms (default):** already marked up. After deploy on Netlify, submit a test from the live URL and check the Forms inbox. The form does not pretend a message was sent unless the host actually accepted the POST and showed `thanks.html`. Opening `thanks.html` directly does not send anything; the page says so.

**Formspree (Cloudflare Pages, GitHub Pages, or any static host):**

1. Create a form at [formspree.io](https://formspree.io/) and copy the endpoint, e.g. `https://formspree.io/f/xxxxxxxx`.
2. In `contact.html`, set `action="https://formspree.io/f/xxxxxxxx"` and `method="POST"`.
3. You may keep `data-netlify` attributes; they are ignored off Netlify. You can also remove them.
4. In Formspree, set the thank-you redirect to your live `thanks.html` URL, or keep Formspree’s own confirmation page.
5. Record the endpoint in this README once it exists: `Formspree endpoint: [not configured]`.

Do not add a JavaScript “message sent” alert that fires without a real submission.

## Domain

Canonical URLs and `sitemap.xml` / `robots.txt` use the placeholder domain `https://webaur.com`. That domain was not attached to this folder at build time. Earlier registry checks (9 November 2026, Europe/Paris) suggested `webaur.com` and `webaur.fi` were not in the respective RDAP results at that moment — that is not a reservation or a trademark clearance. Point DNS at Netlify or Cloudflare Pages after the name is registered, then replace the placeholder email.

## Placeholders (replace before launch)

- Email shown as **`hello@[your-domain]`**, visually marked as a placeholder — not a live inbox. Do not present `hello@webaur.com` as active until a mailbox exists.
- No phone number or street address is listed.
- Privacy policy: legal name, Y-tunnus, postal address, and analytics provider are marked with placeholders in `privacy.html`.
- Canonical / Open Graph / sitemap host: `https://webaur.com`.
- Formspree endpoint: not configured (only needed off Netlify).
- Café and shop addresses in the demos are fictional and labelled as such.

## Pricing copy

Starter €490, Business €890, Premium €1,490. **Prices excl. VAT (Finnish VAT 25.5% added).** The final price depends on the scope of the project.

## Language

The site is in English. A small `EN` label in the header notes that Finnish can be added later. There is no `/en/` tree in this version.

## Credits

See `CREDITS.md` for every demo photograph, source URL and licence.

## What was not completed or not fully tested

- Unsplash photographer names could not be confirmed from live photo pages (pages were blocked). IDs and source URLs are listed; names should be filled in when those pages can be opened.
- Finnish language pages were not built.
- A real domain, mailbox and legal entity were not connected.
- Lighthouse and Playwright results from the local preview are recorded in the delivery report. Scores can change on a live CDN.
- No production analytics or cookie banner (none is configured).

## QA and Lighthouse (local, 9 November 2026, Europe/Paris)

Playwright was run on every studio page and all three demos at 390, 768 and 1440 CSS pixels: no console errors, no broken links or images (after lazy images were scrolled into view), no horizontal overflow (`scrollWidth > clientWidth`), mobile menus opened and closed, and internal CTAs resolved.

Lighthouse (`npx lighthouse` with headless Chrome) on a local `python3 -m http.server`, after a contrast fix on secondary text:

| Page | Form | Performance | Accessibility | Best Practices | SEO |
| --- | --- | ---: | ---: | ---: | ---: |
| Home | mobile | 96 | 100 | 100 | 100 |
| Home | desktop | 100 | 100 | 100 | 100 |
| Work | mobile | 99 | 100 | 100 | 100 |
| Work | desktop | 100 | 100 | 100 | 100 |
| Contact | mobile | 100 | 100 | 100 | 100 |
| Contact | desktop | 100 | 100 | 100 | 100 |
| Hale Barber demo | mobile | 100 | 100 | 100 | 66 |
| Hale Barber demo | desktop | 100 | 100 | 100 | 66 |

The demo SEO score is lower because those pages are marked `noindex` (they are concept projects, not studio marketing pages). Secondary text colour was darkened from the brief’s `#777A74` to `#5E615C` so body copy meets WCAG AA contrast on `#F7F7F4` (the original pair is about 4.06:1).
