(function () {
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const toggle = document.querySelector(".menu-toggle");
  const panel = document.querySelector(".nav-panel");
  const header = document.querySelector(".site-header");

  function setMenu(open) {
    if (!toggle || !panel) return;
    toggle.setAttribute("aria-expanded", String(open));
    panel.classList.toggle("is-open", open);
    document.body.classList.toggle("menu-open", open);
    if (open) {
      const first = panel.querySelector("a");
      if (first) first.focus();
    }
  }

  if (toggle && panel) {
    toggle.addEventListener("click", function () {
      setMenu(toggle.getAttribute("aria-expanded") !== "true");
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") setMenu(false);
      if (e.key === "Tab" && toggle.getAttribute("aria-expanded") === "true") {
        const focusable = [toggle].concat(Array.from(panel.querySelectorAll("a, button")));
        const first = focusable[0], last = focusable[focusable.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    });
    panel.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () { setMenu(false); });
    });
    window.addEventListener("resize", function () {
      if (window.innerWidth > 767 && toggle.getAttribute("aria-expanded") === "true") setMenu(false);
    });
  }
  if (header) {
    var onScroll = function () { header.classList.toggle("is-scrolled", window.scrollY > 8); };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }
  if (reduce) document.querySelectorAll(".reveal").forEach(function (el) { el.style.animation = "none"; });

  var params = new URLSearchParams(window.location.search);
  var pkg = (params.get("package") || "").toLowerCase();
  var budget = document.getElementById("budget");
  if (budget && pkg) {
    var options = Array.from(budget.options);
    var found = options.find(function (o) { return (o.value || "").toLowerCase().indexOf(pkg) !== -1; });
    if (found) budget.value = found.value;
  }

  var form = document.querySelector("form[name='contact']");
  if (form) {
    var cfg = window.WEBAUR_FORM || {};
    var endpoint = (cfg.formspree || "").trim();
    var alertBox = document.getElementById("form-status");
    var onNetlify = /netlify\.app$|netlify\.com$/.test(location.hostname) || document.documentElement.hasAttribute("data-netlify-host");
    if (endpoint) {
      form.setAttribute("action", endpoint);
      form.setAttribute("method", "POST");
    }

    function msg(el, text) {
      var err = el.parentElement.querySelector(".field-error");
      if (!err) {
        err = document.createElement("p");
        err.className = "field-error";
        err.id = el.id + "-error";
        el.parentElement.appendChild(err);
      }
      el.setAttribute("aria-invalid", text ? "true" : "false");
      if (text) el.setAttribute("aria-describedby", err.id);
      else el.removeAttribute("aria-describedby");
      err.textContent = text || "";
      err.hidden = !text;
    }

    var i18n = document.documentElement.lang === "fi" ? {
      required: "Tämä kenttä on pakollinen.",
      email: "Anna kelvollinen sähköpostiosoite.",
      consent: "Tarvitsemme suostumuksesi, jotta voimme vastata viestiisi.",
      unconfigured: "Lomaketta ei ole vielä kytketty lähetyspalveluun. Se toimii, kun Formspree-osoite on lisätty tiedostoon js/form-config.js, tai kun sivusto julkaistaan Netlifyyn. Mitään viestiä ei lähetetty."
    } : {
      required: "This field is required.",
      email: "Please enter a valid email address.",
      consent: "Please confirm we may use this information to reply.",
      unconfigured: "This form is not connected to a sending service yet. It will work once a Formspree endpoint is added in js/form-config.js, or when the site is hosted on Netlify. No message was sent."
    };

    form.addEventListener("submit", function (e) {
      var ok = true;
      var required = form.querySelectorAll("[required]");
      required.forEach(function (el) {
        if (el.type === "checkbox") {
          if (!el.checked) { msg(el, i18n.consent); ok = false; } else msg(el, "");
        } else if (!el.value.trim()) { msg(el, i18n.required); ok = false; }
        else if (el.type === "email" && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(el.value)) { msg(el, i18n.email); ok = false; }
        else msg(el, "");
      });
      if (!ok) { e.preventDefault(); return; }
      if (!endpoint && !onNetlify) {
        e.preventDefault();
        if (alertBox) { alertBox.hidden = false; alertBox.textContent = i18n.unconfigured; alertBox.focus(); }
      }
    });
  }
})();
