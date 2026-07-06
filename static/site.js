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

  /* ---------- quiz (mode local, à tour de rôle) ---------- */
  var qData = $("#quiz-data");
  if (qData) {
    var QUIZ = JSON.parse(qData.textContent);
    var zoneThemes = $("#quiz-themes"), zoneConfig = $("#quiz-config"), zoneJeu = $("#quiz-jeu"), zoneResultat = $("#quiz-resultat");
    var configTitre = $("#quiz-config-titre"), choixNb = $("#quiz-choix-nb"), joueursCompteEl = $("#quiz-joueurs-compte"), joueursNomsEl = $("#quiz-joueurs-noms");
    var titreTheme = $("#quiz-titre-theme"), progression = $("#quiz-progression"), auTour = $("#quiz-au-tour"), zoneQuestion = $("#quiz-question-zone");
    var btnSuivant = $("#quiz-suivant"), btnQuitter = $("#quiz-quitter"), btnRejouer = $("#quiz-rejouer"), btnAutreTheme = $("#quiz-autre-theme");

    var themeCourant = null, nbQuestions = 10, nbJoueurs = 1;
    var questions = [], joueurs = [], iQuestion = 0, iJoueur = 0, aRepondu = false;

    function melange(tableau) {
      var t = tableau.slice();
      for (var i = t.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1));
        var tmp = t[i]; t[i] = t[j]; t[j] = tmp;
      }
      return t;
    }

    /* étape 1 : choix du thème -> écran de configuration */
    $$(".theme-quiz", zoneThemes).forEach(function (b) {
      b.addEventListener("click", function () {
        themeCourant = b.dataset.theme;
        configTitre.textContent = QUIZ[themeCourant].titre + " — configuration de la partie";
        zoneThemes.hidden = true; zoneConfig.hidden = false;
        majJoueursNoms();
      });
    });

    $$("button", choixNb).forEach(function (b) {
      b.addEventListener("click", function () {
        nbQuestions = +b.dataset.nb;
        $$("button", choixNb).forEach(function (x) { x.classList.remove("on"); });
        b.classList.add("on");
      });
    });
    $$("button", choixNb)[0].classList.add("on");

    function majJoueursNoms() {
      joueursCompteEl.textContent = nbJoueurs;
      var html = "";
      for (var i = 1; i <= nbJoueurs; i++) {
        html += '<input type="text" maxlength="24" placeholder="Joueur ' + i + '" data-joueur="' + i + '">';
      }
      joueursNomsEl.innerHTML = html;
    }
    $("#quiz-joueurs-moins").addEventListener("click", function () { if (nbJoueurs > 1) { nbJoueurs--; majJoueursNoms(); } });
    $("#quiz-joueurs-plus").addEventListener("click", function () { if (nbJoueurs < 8) { nbJoueurs++; majJoueursNoms(); } });

    $("#quiz-config-retour").addEventListener("click", function () {
      zoneConfig.hidden = true; zoneThemes.hidden = false;
    });

    /* étape 2 : démarrage de la partie */
    $("#quiz-config-demarrer").addEventListener("click", function () {
      var noms = $$("input", joueursNomsEl).map(function (inp, i) { return inp.value.trim() || ("Joueur " + (i + 1)); });
      joueurs = noms.map(function (n) { return { nom: n, score: 0 }; });
      var t = QUIZ[themeCourant];
      questions = melange(t.questions).slice(0, Math.min(nbQuestions, t.questions.length));
      iQuestion = 0; iJoueur = 0;
      zoneConfig.hidden = true; zoneResultat.hidden = true; zoneJeu.hidden = false;
      titreTheme.textContent = t.titre;
      afficheQuestion();
    });

    function afficheQuestion() {
      aRepondu = false;
      var q = questions[iQuestion];
      progression.textContent = "Question " + (iQuestion + 1) + " / " + questions.length;
      if (joueurs.length > 1) {
        auTour.hidden = false;
        auTour.textContent = "Au tour de : " + joueurs[iJoueur].nom + " (score : " + joueurs[iJoueur].score + ")";
      } else {
        auTour.hidden = true;
      }
      var html = '<h3>' + q.q + '</h3><div class="quiz-options">';
      q.options.forEach(function (opt, i) {
        html += '<button type="button" class="quiz-opt" data-i="' + i + '">' + opt + '</button>';
      });
      html += '</div><p class="quiz-explication" id="quiz-explication" hidden></p>';
      zoneQuestion.innerHTML = html;
      btnSuivant.hidden = true;
      $$(".quiz-opt", zoneQuestion).forEach(function (b) {
        b.addEventListener("click", function () { repond(+b.dataset.i, q); });
      });
    }

    function repond(i, q) {
      if (aRepondu) return;
      aRepondu = true;
      if (i === q.reponse) joueurs[iJoueur].score++;
      $$(".quiz-opt", zoneQuestion).forEach(function (b, idx) {
        b.disabled = true;
        if (idx === q.reponse) b.classList.add("bonne");
        else if (idx === i) b.classList.add("mauvaise");
      });
      if (q.explication) { var ex = $("#quiz-explication"); ex.textContent = q.explication; ex.hidden = false; }
      btnSuivant.hidden = false;
    }

    btnSuivant.addEventListener("click", function () {
      iJoueur = (iJoueur + 1) % joueurs.length;
      iQuestion++;
      if (iQuestion < questions.length) afficheQuestion();
      else termine();
    });

    function termine() {
      zoneJeu.hidden = true; zoneResultat.hidden = false;
      var classes = joueurs.slice().sort(function (a, b) { return b.score - a.score; });
      var max = classes[0].score;
      var html = '<table class="simple" style="margin:0 auto;max-width:420px;text-align:left">';
      classes.forEach(function (j, i) {
        html += '<tr><td>' + (i + 1) + (j.score === max ? ' 🏆' : '') + '</td><td>' + j.nom + '</td><td>' + j.score + ' / ' + questions.length + '</td></tr>';
      });
      html += '</table>';
      $("#quiz-classement").innerHTML = html;
      var pct = max / questions.length;
      var msg = joueurs.length > 1
        ? (classes.filter(function (j) { return j.score === max; }).length > 1 ? "Égalité en tête !" : classes[0].nom + " remporte la partie !")
        : (pct === 1 ? "Score parfait, bravo !" : pct >= 0.7 ? "Très bon score !" : pct >= 0.4 ? "Pas mal, tu peux retenter ta chance." : "Rejoue pour améliorer ton score !");
      $("#quiz-message").textContent = msg;
    }

    btnQuitter.addEventListener("click", function () {
      zoneJeu.hidden = true; zoneThemes.hidden = false;
    });
    btnRejouer.addEventListener("click", function () {
      joueurs.forEach(function (j) { j.score = 0; });
      var t = QUIZ[themeCourant];
      questions = melange(t.questions).slice(0, Math.min(nbQuestions, t.questions.length));
      iQuestion = 0; iJoueur = 0;
      zoneResultat.hidden = true; zoneJeu.hidden = false;
      afficheQuestion();
    });
    btnAutreTheme.addEventListener("click", function () {
      zoneResultat.hidden = true; zoneThemes.hidden = false;
    });
  }
})();
