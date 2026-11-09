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
    } else {
      toggle.focus();
    }
  }

  if (toggle && panel) {
    toggle.addEventListener("click", function () {
      setMenu(toggle.getAttribute("aria-expanded") !== "true");
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") {
        setMenu(false);
      }
      if (e.key === "Tab" && toggle.getAttribute("aria-expanded") === "true") {
        const focusable = [toggle].concat(Array.from(panel.querySelectorAll("a, button, [tabindex]:not([tabindex='-1'])")));
        const first = focusable[0];
        const last = focusable[focusable.length - 1];
        if (e.shiftKey && document.activeElement === first) {
          e.preventDefault();
          last.focus();
        } else if (!e.shiftKey && document.activeElement === last) {
          e.preventDefault();
          first.focus();
        }
      }
    });
    panel.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () { setMenu(false); });
    });
    window.addEventListener("resize", function () {
      if (window.innerWidth > 820 && toggle.getAttribute("aria-expanded") === "true") {
        toggle.setAttribute("aria-expanded", "false");
        panel.classList.remove("is-open");
        document.body.classList.remove("menu-open");
      }
    });
  }

  if (!reduce && "IntersectionObserver" in window) {
    const io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-in");
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });
    document.querySelectorAll(".reveal").forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll(".reveal").forEach(function (el) { el.classList.add("is-in"); });
  }

  if (header) {
    var onScroll = function () {
      header.classList.toggle("is-scrolled", window.scrollY > 8);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }
})();
