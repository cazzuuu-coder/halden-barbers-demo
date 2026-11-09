#!/usr/bin/env python3
"""Playwright QA + official preview screenshots for WEBAUR v2."""
import json, os, sys
from pathlib import Path
from urllib.parse import urljoin, urlparse

from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8766/"
ROOT = Path("/workspace/webaur-v2")
PREV = ROOT / "previews"
PREV.mkdir(exist_ok=True)
OUT = ROOT / "_tools" / "qa-results.json"

PAGES = [
    "index.html",
    "services.html",
    "work.html",
    "about.html",
    "contact.html",
    "thanks.html",
    "privacy.html",
    "404.html",
    "work/barber-studio.html",
    "work/detailing.html",
    "work/maison-cafe.html",
    "demos/barber-studio/index.html",
    "demos/detailing/index.html",
    "demos/maison-cafe/index.html",
]
WIDTHS = [390, 768, 1440]
IGNORE_CONSOLE = ("favicon.ico",)

def ok_console(msg):
    text = msg.text
    return not any(s in text for s in IGNORE_CONSOLE)

def main():
    results = {"pages": {}, "previews": [], "failures": []}
    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path="/usr/bin/google-chrome",
            args=["--no-sandbox", "--disable-dev-shm-usage", "--hide-scrollbars"],
            headless=True,
        )
        for width in WIDTHS:
            height = 844 if width == 390 else (1024 if width == 768 else 900)
            for rel in PAGES:
                url = urljoin(BASE, rel)
                key = f"{rel}@{width}"
                rec = {"url": url, "width": width, "console": [], "broken": [], "overflow": False, "menu": None, "cta": []}
                context = browser.new_context(viewport={"width": width, "height": height}, device_scale_factor=1)
                page = context.new_page()
                logs = []
                page.on("console", lambda m: logs.append({"type": m.type, "text": m.text}) if m.type in ("error", "warning") else None)
                failed = []
                page.on("requestfailed", lambda r: failed.append({"url": r.url, "err": r.failure}) )
                resp = page.goto(url, wait_until="networkidle", timeout=45000)
                rec["status"] = resp.status if resp else None
                if rec["status"] and rec["status"] >= 400:
                    rec["broken"].append({"url": url, "status": rec["status"]})
                page.wait_for_timeout(200)
                rec["console"] = [e for e in logs if ok_console(e["text"])]
                # broken images
                imgs = page.evaluate("""() => Array.from(document.images).map(img => ({src: img.currentSrc||img.src, ok: img.complete && img.naturalWidth>0}))""")
                for img in imgs:
                    if not img["ok"]:
                        rec["broken"].append({"url": img["src"], "kind": "image"})
                # links
                hrefs = page.evaluate("""() => Array.from(document.querySelectorAll('a[href]')).map(a => a.getAttribute('href'))""")
                for href in hrefs:
                    if href is None or href.startswith(("#", "mailto:", "tel:", "javascript:")):
                        if href and href.startswith("#") and href != "#":
                            exists = page.evaluate("(id) => !!document.getElementById(id) || !!document.querySelector(id)", href)
                            rec["cta"].append({"href": href, "ok": bool(exists)})
                            if not exists:
                                rec["broken"].append({"url": href, "kind": "hash"})
                        continue
                    absu = urljoin(url, href)
                    parsed = urlparse(absu)
                    if parsed.netloc not in ("127.0.0.1:8766", "localhost:8766") and parsed.scheme in ("http", "https"):
                        # external: skip fetch except we still record
                        rec["cta"].append({"href": href, "ok": True, "external": parsed.netloc not in ("127.0.0.1:8766","")})
                        continue
                    rec["cta"].append({"href": href, "ok": None})
                # resolve internal links via request
                for c in rec["cta"]:
                    if c.get("ok") is None:
                        target = urljoin(url, c["href"])
                        try:
                            r = context.request.get(target, timeout=15000)
                            c["ok"] = r.status < 400
                            c["status"] = r.status
                            if r.status >= 400:
                                rec["broken"].append({"url": c["href"], "status": r.status, "kind": "link"})
                        except Exception as e:
                            c["ok"] = False
                            rec["broken"].append({"url": c["href"], "err": str(e), "kind": "link"})
                # overflow
                overflow = page.evaluate("""() => {
                  const doc = document.documentElement;
                  const body = document.body;
                  return {
                    doc: doc.scrollWidth > doc.clientWidth + 1,
                    body: body.scrollWidth > body.clientWidth + 1,
                    scrollWidth: Math.max(doc.scrollWidth, body.scrollWidth),
                    clientWidth: doc.clientWidth
                  };
                }""")
                rec["overflow"] = overflow["doc"] or overflow["body"]
                rec["overflow_detail"] = overflow
                # mobile menu at 390
                if width == 390:
                    toggle = page.query_selector(".menu-toggle")
                    if toggle and toggle.is_visible():
                        before = page.evaluate("""() => {
                          const p = document.querySelector('.nav-panel, .nav-links');
                          if(!p) return {exists:false};
                          const s = getComputedStyle(p);
                          return {exists:true, display:s.display, expanded: document.querySelector('.menu-toggle')?.getAttribute('aria-expanded')};
                        }""")
                        toggle.click()
                        page.wait_for_timeout(150)
                        after = page.evaluate("""() => {
                          const p = document.querySelector('.nav-panel.is-open, .nav-links.is-open, .nav-panel, .nav-links');
                          const open = document.querySelector('.nav-panel.is-open, .nav-links.is-open');
                          const s = open ? getComputedStyle(open) : getComputedStyle(p);
                          return {open: !!open, display:s.display, expanded: document.querySelector('.menu-toggle')?.getAttribute('aria-expanded')};
                        }""")
                        # close
                        toggle.click()
                        page.wait_for_timeout(150)
                        closed = page.evaluate("""() => {
                          const open = document.querySelector('.nav-panel.is-open, .nav-links.is-open');
                          return {open: !!open, expanded: document.querySelector('.menu-toggle')?.getAttribute('aria-expanded')};
                        }""")
                        rec["menu"] = {"opened": after.get("open") and after.get("expanded")=="true" and after.get("display")!="none",
                                       "closed": (not closed.get("open")) and closed.get("expanded")=="false",
                                       "before": before, "after": after, "closed_state": closed}
                    else:
                        rec["menu"] = {"opened": False, "closed": False, "error": "toggle not visible"}
                results["pages"][key] = rec
                issues = []
                if rec["console"]:
                    issues.append("console")
                if rec["broken"]:
                    issues.append("broken")
                if rec["overflow"]:
                    issues.append("overflow")
                if width==390 and rec["menu"] and not (rec["menu"].get("opened") and rec["menu"].get("closed")):
                    issues.append("menu")
                if issues:
                    results["failures"].append({"key": key, "issues": issues, "broken": rec["broken"], "overflow": rec.get("overflow_detail"), "menu": rec["menu"], "console": rec["console"]})
                print(f"{key:40} status={rec['status']} issues={issues or 'ok'} broken={len(rec['broken'])} overflow={rec['overflow']}")
                context.close()

        # official previews
        shots = [
            ("index.html", 1440, 900, "preview-home-desktop.png", False),
            ("index.html", 390, 844, "preview-home-mobile.png", False),
            ("work.html", 1440, 900, "preview-work-desktop.png", False),
            ("demos/barber-studio/index.html", 1440, 900, "preview-demo-barber-desktop.png", False),
            ("demos/detailing/index.html", 1440, 900, "preview-demo-detailing-desktop.png", False),
            ("demos/maison-cafe/index.html", 1440, 900, "preview-demo-maison-desktop.png", False),
        ]
        # also full-page critique shots (kept in _tools, not official previews)
        critique = ROOT / "_tools" / "critique"
        critique.mkdir(exist_ok=True)
        for rel, w, h, name, full in shots:
            context = browser.new_context(viewport={"width": w, "height": h}, device_scale_factor=2)
            page = context.new_page()
            page.goto(urljoin(BASE, rel), wait_until="networkidle", timeout=45000)
            page.wait_for_timeout(400)
            dest = PREV / name
            page.screenshot(path=str(dest), full_page=False)
            # full page critique
            page.screenshot(path=str(critique / name.replace("preview-", "full-")), full_page=True)
            results["previews"].append(str(dest))
            print("preview", dest, dest.stat().st_size)
            context.close()
        browser.close()
    OUT.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print("failures", len(results["failures"]))
    return 0 if not results["failures"] else 1

if __name__ == "__main__":
    sys.exit(main())
