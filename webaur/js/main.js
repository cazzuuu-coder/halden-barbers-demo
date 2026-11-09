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

  // Preselect budget when arriving from a package button.
  var params = new URLSearchParams(window.location.search);
  var pkg = (params.get("package") || "").toLowerCase();
  var budget = document.getElementById("budget");
  if (budget && pkg) {
    var map = {
      starter: "Starter — around €490 + VAT",
      business: "Business — around €890 + VAT",
      premium: "Premium — around €1,490 + VAT"
    };
    if (map[pkg]) budget.value = map[pkg];
  }

  if (reduce) document.querySelectorAll(".reveal").forEach(function (el) { el.style.animation = "none"; });
})();
