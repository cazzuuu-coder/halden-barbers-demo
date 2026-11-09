(function () {
  "use strict";

  // Sticky header: add subtle shadow on scroll
  var header = document.querySelector(".site-header");
  function onScroll() {
    if (!header) return;
    if (window.scrollY > 8) header.style.boxShadow = "0 6px 20px rgba(28,20,16,0.08)";
    else header.style.boxShadow = "none";
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  // Mobile nav
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("primary-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!open));
      nav.classList.toggle("is-open", !open);
      toggle.setAttribute("aria-label", open ? "Avaa valikko" : "Sulje valikko");
    });
    nav.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        toggle.setAttribute("aria-expanded", "false");
        nav.classList.remove("is-open");
        toggle.setAttribute("aria-label", "Avaa valikko");
      });
    });
  }

  // Menu category tabs
  var tabs = document.querySelectorAll(".menu-tab");
  var panels = document.querySelectorAll(".menu-panel");
  tabs.forEach(function (tab) {
    tab.addEventListener("click", function () {
      var cat = tab.getAttribute("data-cat");
      tabs.forEach(function (t) {
        var on = t === tab;
        t.classList.toggle("is-active", on);
        t.setAttribute("aria-selected", String(on));
      });
      panels.forEach(function (panel) {
        var match = panel.getAttribute("data-cat") === cat;
        panel.classList.toggle("is-active", match);
        if (match) panel.removeAttribute("hidden");
        else panel.setAttribute("hidden", "");
      });
    });
  });

  // Client-side order / contact form
  var form = document.getElementById("order-form");
  var success = document.getElementById("form-success");
  if (form && success) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.checkValidity()) {
        form.reportValidity();
        return;
      }
      success.hidden = false;
      form.reset();
      success.scrollIntoView({ behavior: "smooth", block: "nearest" });
    });
  }
})();
