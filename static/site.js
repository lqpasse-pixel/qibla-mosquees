/* Qibla — scripts du site (aucune dépendance externe) */
(function () {
  "use strict";
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  /* ---------- thème clair / sombre ---------- */
  var racine = document.documentElement;
  var themeMemo = localStorage.getItem("qibla-theme");
  if (themeMemo) racine.dataset.theme = themeMemo;
  var btnTheme = $("#btn-theme");
  function libelleTheme() { if (btnTheme) btnTheme.textContent = racine.dataset.theme === "sombre" ? "☀ Clair" : "☾ Sombre"; }
  if (btnTheme) {
    libelleTheme();
    btnTheme.addEventListener("click", function () {
      racine.dataset.theme = racine.dataset.theme === "sombre" ? "" : "sombre";
      localStorage.setItem("qibla-theme", racine.dataset.theme);
      libelleTheme();
    });
  }

  /* ---------- menu mobile ---------- */
  var burger = $(".burger");
  if (burger) burger.addEventListener("click", function () {
    var nav = $("nav.main"); nav.classList.toggle("open");
    burger.setAttribute("aria-expanded", nav.classList.contains("open"));
  });

  /* ---------- slider du héros ---------- */
  var slides = $$(".hero .slide");
  if (slides.length > 1) {
    var dots = $$(".hero-dots button"), i = 0, timer;
    function va(n) {
      slides[i].classList.remove("on"); if (dots[i]) dots[i].classList.remove("on");
      i = (n + slides.length) % slides.length;
      slides[i].classList.add("on"); if (dots[i]) dots[i].classList.add("on");
    }
    function auto() { timer = setInterval(function () { va(i + 1); }, 5200); }
    dots.forEach(function (d, n) { d.addEventListener("click", function () { clearInterval(timer); va(n); auto(); }); });
    if (!matchMedia("(prefers-reduced-motion: reduce)").matches) auto();
  }

  /* ---------- apparition au défilement ---------- */
  if ("IntersectionObserver" in window) {
    var obs = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("vu"); obs.unobserve(e.target); } });
    }, { threshold: 0.12 });
    $$(".reveal").forEach(function (el) { obs.observe(el); });
  } else { $$(".reveal").forEach(function (el) { el.classList.add("vu"); }); }

  /* ---------- filtres de la liste ---------- */
  var grille = $("#grille-mosquees");
  if (grille) {
    var fPays = $("#f-pays"), fStyle = $("#f-style"), fEpoque = $("#f-epoque"), fTexte = $("#f-texte"), compte = $("#f-compte");
    function filtre() {
      var n = 0;
      $$(".carte", grille).forEach(function (c) {
        var ok = (!fPays.value || c.dataset.pays === fPays.value) &&
                 (!fStyle.value || c.dataset.style === fStyle.value) &&
                 (!fEpoque.value || c.dataset.epoque === fEpoque.value) &&
                 (!fTexte.value || (c.textContent || "").toLowerCase().indexOf(fTexte.value.toLowerCase()) !== -1);
        c.style.display = ok ? "" : "none"; if (ok) n++;
      });
      compte.textContent = n + (n > 1 ? " mosquées" : " mosquée");
    }
    [fPays, fStyle, fEpoque].forEach(function (el) { el.addEventListener("change", filtre); });
    fTexte.addEventListener("input", filtre);
    filtre();
  }

  /* ---------- visionneuse immersive (zoom / pan) ---------- */
  var vis = $("#visionneuse");
  if (vis) {
    var vImg = $("img", vis), vLeg = $(".legende", vis), scene = $(".scene", vis);
    var z = 1, px = 0, py = 0, drag = null;
    function applique() { vImg.style.transform = "translate(" + px + "px," + py + "px) scale(" + z + ")"; }
    function ouvre(src, alt) {
      vImg.src = src; vImg.alt = alt; vLeg.textContent = alt;
      z = 1; px = py = 0; applique(); vis.classList.add("on"); document.body.style.overflow = "hidden";
    }
    function ferme() { vis.classList.remove("on"); document.body.style.overflow = ""; }
    $$(".galerie button").forEach(function (b) {
      b.addEventListener("click", function () { var im = $("img", b); ouvre(im.dataset.grand || im.src, im.alt); });
    });
    $("#vis-fermer").addEventListener("click", ferme);
    $("#vis-plus").addEventListener("click", function () { z = Math.min(z * 1.35, 8); applique(); });
    $("#vis-moins").addEventListener("click", function () { z = Math.max(z / 1.35, 0.4); applique(); });
    $("#vis-raz").addEventListener("click", function () { z = 1; px = py = 0; applique(); });
    scene.addEventListener("wheel", function (e) { e.preventDefault(); z = Math.min(8, Math.max(0.4, z * (e.deltaY < 0 ? 1.12 : 0.9))); applique(); }, { passive: false });
    scene.addEventListener("pointerdown", function (e) { drag = { x: e.clientX - px, y: e.clientY - py }; scene.setPointerCapture(e.pointerId); });
    scene.addEventListener("pointermove", function (e) { if (drag) { px = e.clientX - drag.x; py = e.clientY - drag.y; applique(); } });
    scene.addEventListener("pointerup", function () { drag = null; });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") ferme(); });
  }

  /* ---------- bandeau cookies (RGPD) ---------- */
  var bandeau = $("#cookies");
  if (bandeau && !localStorage.getItem("qibla-cookies")) bandeau.classList.add("on");
  function choixCookies(v) {
    localStorage.setItem("qibla-cookies", v); bandeau.classList.remove("on");
    if (v === "accepte") { /* Point d'entrée analytics : charger ici GA4 ou Plausible. */ }
  }
  var ca = $("#cookies-accepter"), cr = $("#cookies-refuser");
  if (ca) ca.addEventListener("click", function () { choixCookies("accepte"); });
  if (cr) cr.addEventListener("click", function () { choixCookies("refuse"); });

  /* ---------- newsletter (démonstration) ---------- */
  var nl = $("#form-nl");
  if (nl) nl.addEventListener("submit", function (e) {
    e.preventDefault();
    $("#nl-ok").textContent = "Merci ! Adresse enregistrée localement (brancher Mailchimp ou Brevo — voir README).";
    nl.reset();
  });
})();
