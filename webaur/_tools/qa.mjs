import { chromium } from "/workspace/node_modules/playwright/index.mjs";
import fs from "fs";
import path from "path";

const BASE = "http://127.0.0.1:8768/halden-barbers-demo/webaur/";
const ROOT = "/workspace/webaur-v3";
const PREV = path.join(ROOT, "previews");
const CRIT = path.join(ROOT, "_tools/critique");
fs.mkdirSync(PREV, { recursive: true });
fs.mkdirSync(CRIT, { recursive: true });

const PAGES = [
  "index.html","services.html","work.html","about.html","contact.html",
  "thanks.html","privacy.html","404.html",
  "work/barber-studio.html","work/detailing.html","work/maison-cafe.html",
  "en/index.html","en/services.html","en/work.html","en/about.html","en/contact.html",
  "en/thanks.html","en/privacy.html","en/404.html",
  "en/work/barber-studio.html","en/work/detailing.html","en/work/maison-cafe.html",
  "demos/barber-studio/index.html","demos/detailing/index.html","demos/maison-cafe/index.html",
];
const WIDTHS = [390, 768, 1440];
const join = (base, rel) => new URL(rel, base).href;

const results = { pages: {}, previews: [], failures: [] };
const browser = await chromium.launch({
  executablePath: "/usr/bin/google-chrome",
  args: ["--no-sandbox", "--disable-dev-shm-usage", "--hide-scrollbars"],
  headless: true,
});

for (const width of WIDTHS) {
  const height = width === 390 ? 844 : width === 768 ? 1024 : 900;
  for (const rel of PAGES) {
    const url = join(BASE, rel);
    const key = `${rel}@${width}`;
    const rec = { url, width, console: [], broken: [], overflow: false, menu: null, switcher: null, cta: [] };
    const context = await browser.newContext({ viewport: { width, height }, deviceScaleFactor: 1 });
    const page = await context.newPage();
    const logs = [];
    page.on("console", (m) => {
      if (["error", "warning"].includes(m.type())) logs.push({ type: m.type(), text: m.text() });
    });
    page.on("requestfailed", (r) => {
      const u = r.url();
      if (!u.includes("favicon.ico")) rec.broken.push({ url: u, err: r.failure(), kind: "request" });
    });
    const resp = await page.goto(url, { waitUntil: "networkidle", timeout: 45000 });
    rec.status = resp ? resp.status() : null;
    await page.evaluate(async () => {
      const h = Math.max(document.body.scrollHeight, document.documentElement.scrollHeight);
      for (let y = 0; y < h; y += 700) {
        window.scrollTo(0, y);
        await new Promise((r) => setTimeout(r, 30));
      }
      window.scrollTo(0, 0);
      await Promise.all(Array.from(document.images).map((img) => {
        try { img.loading = "eager"; } catch (e) {}
        return img.decode ? img.decode().catch(() => null) : Promise.resolve();
      }));
    });
    await page.waitForTimeout(120);
    rec.console = logs.filter((e) => !e.text.includes("favicon.ico"));
    const imgs = await page.evaluate(() =>
      Array.from(document.images).map((img) => ({ src: img.currentSrc || img.src, ok: img.complete && img.naturalWidth > 0 }))
    );
    for (const img of imgs) if (!img.ok) rec.broken.push({ url: img.src, kind: "image" });
    const hrefs = await page.evaluate(() => Array.from(document.querySelectorAll("a[href]")).map((a) => a.getAttribute("href")));
    for (const href of hrefs) {
      if (!href || href.startsWith("mailto:") || href.startsWith("tel:") || href.startsWith("javascript:")) continue;
      if (href.startsWith("#")) {
        if (href === "#") continue;
        const exists = await page.evaluate((id) => !!(document.getElementById(id.slice(1)) || document.querySelector(id)), href);
        rec.cta.push({ href, ok: !!exists });
        if (!exists) rec.broken.push({ url: href, kind: "hash" });
        continue;
      }
      const abs = join(url, href);
      const host = new URL(abs).host;
      if (host !== "127.0.0.1:8768") {
        rec.cta.push({ href, ok: true, external: true });
        continue;
      }
      try {
        const r = await context.request.get(abs, { timeout: 15000 });
        const ok = r.status() < 400;
        rec.cta.push({ href, ok, status: r.status() });
        if (!ok) rec.broken.push({ url: href, status: r.status(), kind: "link" });
      } catch (e) {
        rec.cta.push({ href, ok: false });
        rec.broken.push({ url: href, err: String(e), kind: "link" });
      }
    }
    const overflow = await page.evaluate(() => {
      const doc = document.documentElement;
      const body = document.body;
      return {
        doc: doc.scrollWidth > doc.clientWidth + 1,
        body: body.scrollWidth > body.clientWidth + 1,
        scrollWidth: Math.max(doc.scrollWidth, body.scrollWidth),
        clientWidth: doc.clientWidth,
      };
    });
    rec.overflow = overflow.doc || overflow.body;
    rec.overflow_detail = overflow;
    if (width === 390) {
      const toggle = await page.$(".menu-toggle");
      if (toggle && (await toggle.isVisible())) {
        await toggle.click();
        await page.waitForTimeout(150);
        const after = await page.evaluate(() => {
          const open = document.querySelector(".nav-panel.is-open, .nav-links.is-open");
          const s = open ? getComputedStyle(open) : null;
          return { open: !!open, display: s && s.display, expanded: document.querySelector(".menu-toggle")?.getAttribute("aria-expanded") };
        });
        await toggle.click();
        await page.waitForTimeout(150);
        const closed = await page.evaluate(() => {
          const open = document.querySelector(".nav-panel.is-open, .nav-links.is-open");
          return { open: !!open, expanded: document.querySelector(".menu-toggle")?.getAttribute("aria-expanded") };
        });
        rec.menu = {
          opened: after.open && after.expanded === "true" && after.display !== "none",
          closed: !closed.open && closed.expanded === "false",
          after, closed_state: closed,
        };
      } else if (!rel.startsWith("demos/") && !rel.includes("thanks") /* demos also have menu */) {
        rec.menu = { opened: false, closed: false, error: "toggle not visible" };
      }
    }
    // language switcher (studio pages only)
    if (!rel.startsWith("demos/")) {
      const sw = await page.evaluate(() => {
        const root = document.querySelector(".lang-switch");
        if (!root) return { present: false };
        const fi = root.querySelector('a[hreflang="fi"], a[lang="fi"], span[aria-current="true"]');
        const en = root.querySelector('a[hreflang="en"], a[lang="en"], span[aria-current="true"]');
        const links = Array.from(root.querySelectorAll("a")).map((a) => a.getAttribute("href"));
        return { present: true, links, htmlLang: document.documentElement.lang };
      });
      rec.switcher = sw;
      if (sw.present && (!sw.links || sw.links.length < 1)) {
        rec.switcher.ok = false;
      } else if (sw.present) {
        // resolve counterpart
        rec.switcher.ok = true;
        for (const h of sw.links) {
          const abs = join(url, h);
          const r = await context.request.get(abs, { timeout: 15000 });
          if (r.status() >= 400) { rec.switcher.ok = false; rec.broken.push({ url: h, status: r.status(), kind: "switcher" }); }
        }
      } else {
        rec.switcher = { present: false, ok: false };
      }
    }
    results.pages[key] = rec;
    const issues = [];
    if (rec.console.length) issues.push("console");
    if (rec.broken.length) issues.push("broken");
    if (rec.overflow) issues.push("overflow");
    if (width === 390 && rec.menu && !(rec.menu.opened && rec.menu.closed)) issues.push("menu");
    if (rec.switcher && rec.switcher.ok === false) issues.push("switcher");
    if (issues.length) results.failures.push({ key, issues, broken: rec.broken, overflow: rec.overflow_detail, menu: rec.menu, switcher: rec.switcher, console: rec.console });
    console.log(`${key.padEnd(46)} status=${rec.status} issues=${issues.join(",") || "ok"}`);
    await context.close();
  }
}

const shots = [
  ["en/index.html", 1440, 900, "preview-home-desktop-en.png"],
  ["en/index.html", 390, 844, "preview-home-mobile-en.png"],
  ["index.html", 1440, 900, "preview-home-desktop-fi.png"],
  ["work.html", 1440, 900, "preview-work-desktop.png"],
  ["demos/barber-studio/index.html", 1440, 900, "preview-demo-barber-desktop.png"],
  ["demos/detailing/index.html", 1440, 900, "preview-demo-detailing-desktop.png"],
  ["demos/maison-cafe/index.html", 1440, 900, "preview-demo-maison-desktop.png"],
];
for (const [rel, w, h, name] of shots) {
  const context = await browser.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: 2 });
  const page = await context.newPage();
  await page.goto(join(BASE, rel), { waitUntil: "networkidle", timeout: 45000 });
  await page.waitForTimeout(500);
  const dest = path.join(PREV, name);
  await page.screenshot({ path: dest, fullPage: false });
  await page.screenshot({ path: path.join(CRIT, name.replace("preview-", "full-")), fullPage: true });
  results.previews.push(dest);
  console.log("preview", dest, fs.statSync(dest).size);
  await context.close();
}

await browser.close();
fs.writeFileSync(path.join(ROOT, "_tools/qa-results.json"), JSON.stringify(results, null, 2));
console.log("failures", results.failures.length);
process.exit(results.failures.length ? 1 : 0);
