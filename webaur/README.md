# WEBAUR studio website

A static, multi-page site for WEBAUR, an independent web design studio. Plain HTML, CSS and JavaScript — no build step.

English is the current language (`lang="en"` on every page). The same pages are also copied under `en/`, with canonical URLs pointing at the root English pages, so Finnish (`/fi/`) and French (`/fr/`) can be added later without moving assets. When those languages exist, add `hreflang` alternates on every page and decide whether the root URL should redirect by language or stay English.

Placeholder production domain in `sitemap.xml`, `robots.txt`, canonical tags and Open Graph URLs: `https://webaur.com`. Replace this everywhere once a real domain is connected.

## Pages

- `index.html` — home
- `services.html` — packages and care plans
- `work.html` — concept projects
- `about.html`
- `contact.html` — Netlify form
- `privacy.html` — draft notice with placeholders
- `thanks.html` — form confirmation (`noindex`)
- `404.html`
- `work/barber-studio.html`, `work/autohaus.html`, `work/maison-cafe.html`
- `en/` — structural copy of the above
- `concepts/` — the original concept sites used for screenshots (`noindex`; not in the sitemap)

All internal links and asset paths are relative, so the site also works from a subfolder such as `https://user.github.io/repo/webaur/`.

## Concept mockups

The work images are not stock or generic AI pictures. Four small sites were built as real HTML (`concepts/hale-barber`, `concepts/autohaus`, `concepts/maison-cafe`, `concepts/vale-counsel`), opened in a browser at 1440×900 and 390×844, and saved as WebP with JPEG fallbacks. Every project is labelled **Concept project**. There are no invented testimonials, statistics, awards, address, phone number, business ID or social profiles.

## Contact form (Netlify Forms)

`contact.html` is a real Netlify form:

- `name="contact"` and `data-netlify="true"`
- hidden `form-name` field
- honeypot field `bot-field` (`data-netlify-honeypot`)
- Fields: Name, Business name, Email, Type of project, Estimated budget, Project description
- `action="thanks.html"`
- required privacy-consent checkbox and a link to the privacy policy
- Alternative contact shown as `hello@webaur.com` (placeholder until the mailbox is configured)

After a Netlify deploy, send a test message and confirm it appears under **Site configuration → Forms**, and that the thank-you page loads. Until the site is on Netlify, submitting the form from a local folder or another host will not deliver mail.

### Formspree alternative (Cloudflare Pages)

Cloudflare Pages does not provide Netlify Forms.

1. Create a form at [Formspree](https://formspree.io/) and confirm the mailbox.
2. On `contact.html` (and `en/contact.html`), change the `<form>` tag to something like:

   ```html
   <form action="https://formspree.io/f/YOUR_FORM_ID" method="POST">
   ```

3. Remove `data-netlify`, `netlify`, the hidden `form-name` field, and the Netlify honeypot (or keep a unused field; Formspree has its own spam tools).
4. Set `action` to Formspree, and either use Formspree’s redirect to `thanks.html` (`_next` hidden field) or their AJAX mode.
5. Read Formspree’s data-processing and region options, update the privacy notice, and send a test.

Basin and Web3Forms are similar alternatives. Choose one EU-friendly option and name it in the privacy notice and in client contracts.

## Deploy

### Netlify, drag and drop

1. Sign in at [Netlify](https://app.netlify.com/).
2. Go to **Sites → Add new site → Deploy manually** and drop the unzipped site folder (the folder that contains `index.html`, not a parent folder).
3. Open the generated `*.netlify.app` URL, walk every page, and send a test form.

### Netlify, Git

1. Put this folder in a Git repository (GitHub, GitLab or Bitbucket).
2. In Netlify: **Add new site → Import an existing project**, pick the repo.
3. Build command: leave empty. Publish directory: the folder that contains `index.html` (`.` if the repo root is this site).
4. Deploy and test the form.

### Cloudflare Pages

1. In [Cloudflare](https://dash.cloudflare.com/), open **Workers & Pages → Create → Pages**.
2. Connect the Git repository, or upload the folder.
3. Build command: empty. Output directory: `/` (this folder).
4. Connect the form through Formspree or another service, as above — do not expect Netlify Forms to run here.

### Custom domain

1. Register the domain with a registrar (see the name check notes in the hand-off; a registry “not found” is not a reservation).
2. In Netlify: **Domain management → Add a domain**, or in Cloudflare Pages: **Custom domains**.
3. At the registrar, either:
   - use the host’s nameservers (simplest with Cloudflare), or
   - add the `A` / `ALIAS` / `CNAME` records the host shows for the apex and `www`.
4. Wait for DNS and for HTTPS to show as active.
5. Replace `https://webaur.com` in `sitemap.xml`, `robots.txt`, canonical tags and Open Graph image URLs if the real domain is different.
6. Do not host a paying client’s production site on GitHub Pages or on a free plan that can be withdrawn without notice. This studio site should also sit on a stable, preferably paid, plan once it is public.

## Professional email

Set up a mailbox on the same domain (for example `hello@webaur.com` or `casper@WEBAUR.com`) before putting the address on the site.

Options:

- **Zoho Mail** — often a reasonable start for a single domain; check current pricing and whether the free tier still exists in your country.
- **Google Workspace** — paid, familiar, good if you already use Google.
- **Mailbox from the registrar or a Finnish/EU host** — sometimes the simplest if the domain is already there.

Whoever hosts the mail, add at least:

- **MX** records, exactly as the mail host lists them.
- **SPF** — a TXT record on the apex, naming only the services that may send as you.
- **DKIM** — the TXT record(s) the mail host generates.
- **DMARC** — a TXT record at `_dmarc`, starting conservatively (for example `p=none` with an aggregate report address), then tightening once mail flows.

Wait for DNS to propagate, then send and receive a test from a phone and from a webmail window. Only then replace the placeholders in the footer, the contact page and the privacy notice. Put both the studio address and Casper’s own name on outgoing client mail.

## Checklist — still needs real business details or external setup

- [ ] Confirm the name and domains yourself (YTJ / PRH trade name, TMview, EUIPO, Traficom, the registrar). A check made on 9 November 2026 is not a reservation.
- [ ] Register the business (typically a sole trader first), VAT, and prepayment register as advised separately.
- [ ] Register `WEBAUR.com` and/or `WEBAUR.fi` if you still want them after those checks, then connect DNS.
- [ ] Create the professional mailbox (MX, SPF, DKIM, DMARC) and put the real address on the site.
- [ ] Fill every highlighted placeholder in `privacy.html` (legal name, business ID, address, email, retention period) and have the notice reviewed if you need it to be a legal document.
- [ ] Add a visiting address and phone only if they are real.
- [ ] Deploy to Netlify or Cloudflare Pages on a stable plan, connect the domain, and turn on HTTPS.
- [ ] Activate and **test** the contact form (Netlify Forms or Formspree).
- [ ] Put a data-processing arrangement in place with the form host.
- [ ] Replace the placeholder domain in `sitemap.xml`, `robots.txt`, canonical and Open Graph tags if needed.
- [ ] Write `/fi/` and `/fr/` translations when you are ready, and hook up `hreflang`.
- [ ] Add analytics only with a documented tool and consent where required.
- [ ] Publish real client work only with written permission.
- [ ] Keep the written 590 € reference offer, deposit terms and contracts off this site until they exist as documents.
- [ ] Optional: social profiles, once they are real and named consistently.

## Local preview

Any static server is enough, for example:

```bash
python3 -m http.server 8080
```

Then open `http://127.0.0.1:8080/`.

## Licence and credit

Concept projects are fictional and labelled as such. Do not present them as client work. Site copy and design are for WEBAUR / Casper.
