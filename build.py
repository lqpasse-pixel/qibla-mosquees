# -*- coding: utf-8 -*-
"""Génère le site statique complet dans dist/."""
import json, os, shutil, math
from data_mosquees import MOSQUEES
from blog_articles import ARTICLES
from quiz_data import QUIZ
from svg_art import scene, medaillon, motif, _girih

ICI = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ICI, "dist")
SITE_URL = "https://qibla-mosquees.netlify.app"
NOM_SITE = "Qibla — Les 20 plus belles mosquées du monde"

ETOILE = ('<svg width="22" height="22" viewBox="0 0 22 22" aria-hidden="true">'
          '<polygon points="11,1 13.4,7 20,7.6 15,12 16.6,19 11,15.4 5.4,19 7,12 2,7.6 8.6,7" '
          'fill="none" stroke="var(--or)" stroke-width="1.4"/></svg>')

def sep(titre="", sous=""):
    t = f'<p class="eyebrow" style="text-align:center;margin:0">{titre}</p>' if titre else ""
    s = f'<h2 style="text-align:center;margin:.25em 0 0">{sous}</h2>' if sous else ""
    return f'<div class="sep" role="presentation">{ETOILE}</div>{t}{s}'

# ---------------------------------------------------------------- gabarit
def page(titre, description, corps, rac="", canonique="", jsonld=None, actif=""):
    def nav_a(href, label, cle):
        cur = ' aria-current="page"' if cle == actif else ""
        return f'<a href="{rac}{href}"{cur}>{label}</a>'
    ld = f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>' if jsonld else ""
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titre}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{SITE_URL}/{canonique}">
<meta property="og:title" content="{titre}">
<meta property="og:description" content="{description}">
<meta property="og:type" content="website">
<meta property="og:locale" content="fr_FR">
<link rel="icon" type="image/svg+xml" href="{rac}assets/images/site/favicon.svg">
<link rel="stylesheet" href="{rac}assets/style.css">
{ld}
</head>
<body>
<header class="topbar">
  <div class="wrap">
    <a class="logo" href="{rac}index.html" aria-label="Accueil Qibla">
      <svg width="30" height="30" viewBox="0 0 22 22" aria-hidden="true"><polygon points="11,1 13.4,7 20,7.6 15,12 16.6,19 11,15.4 5.4,19 7,12 2,7.6 8.6,7" fill="var(--or)"/></svg>
      Qibla <b>· 20 mosquées</b>
    </a>
    <button class="burger" aria-label="Ouvrir le menu" aria-expanded="false">☰</button>
    <nav class="main" aria-label="Navigation principale">
      {nav_a("index.html","Accueil","accueil")}
      {nav_a("mosquees.html","Les 20 mosquées","liste")}
      {nav_a("blog.html","Blog","blog")}
      {nav_a("quiz.html","Quiz","quiz")}
      {nav_a("boussole.html","Boussole","boussole")}
      {nav_a("a-propos.html","À propos","apropos")}
      {nav_a("contact.html","Contact","contact")}
      <button class="btn-theme" id="btn-theme">☾ Sombre</button>
    </nav>
  </div>
</header>
{corps}
<section class="wrap nl reveal" aria-label="Newsletter">
  <p class="eyebrow">Newsletter</p>
  <h2>Une mosquée, une histoire, chaque mois</h2>
  <p class="muted" style="color:#cfc7b2">Recevez nos récits d'architecture, d'histoire et de voyage. Zéro spam, désinscription en un clic.</p>
  <form id="form-nl">
    <label for="nl-email" class="visually-hidden" style="position:absolute;left:-9999px">Votre adresse e-mail</label>
    <input id="nl-email" type="email" required placeholder="votre@email.fr" autocomplete="email">
    <button class="btn btn-or" type="submit">S'inscrire</button>
  </form>
  <p id="nl-ok" class="note" style="margin-top:10px"></p>
</section>
<footer>
  <div class="wrap">
    <div>
      <h4>Qibla</h4>
      <p>Un voyage éditorial et visuel à travers les vingt plus belles mosquées du monde : histoire, anecdotes, visites immersives et discussions.</p>
      <p class="note">Toutes les illustrations sont des œuvres originales hébergées localement — aucune dépendance externe.</p>
    </div>
    <div>
      <h4>Explorer</h4>
      <a href="{rac}mosquees.html">Les 20 mosquées</a>
      <a href="{rac}blog.html">Blog</a>
      <a href="{rac}quiz.html">Quiz</a>
      <a href="{rac}boussole.html">Boussole</a>
      <a href="{rac}a-propos.html">À propos</a>
      <a href="{rac}credits-photos.html">Crédits images</a>
      <a href="{rac}contact.html">Contact</a>
    </div>
    <div>
      <h4>Informations légales</h4>
      <a href="{rac}mentions-legales.html">Mentions légales</a>
      <a href="{rac}confidentialite.html">Politique de confidentialité</a>
      <a href="{rac}cgu.html">Conditions générales d'utilisation</a>
    </div>
  </div>
  <div class="footer-bas">© 2026 Qibla — Textes et illustrations originaux. Reproduction sur autorisation.</div>
</footer>
<div class="cookies" id="cookies" role="dialog" aria-label="Gestion des cookies">
  <span>🍪 Nous n'utilisons que des cookies de mesure d'audience anonymisée. Vous pouvez les refuser sans limiter votre visite.</span>
  <span class="boutons">
    <button class="btn btn-ligne" id="cookies-refuser" style="color:inherit">Refuser</button>
    <button class="btn btn-or" id="cookies-accepter">Accepter</button>
  </span>
</div>
<script src="{rac}assets/site.js"></script>
</body>
</html>"""

def slot_pub():
    """Emplacement réservé pour une future publicité (AdSense) : vide et invisible tant qu'aucune
    balise <ins class="adsbygoogle"> n'y est ajoutée, pour ne pas afficher de bloc vide/mercantile
    avant d'avoir du trafic. Voir credits/README, section Monétisation."""
    return '<div class="pub" role="complementary" aria-label="Emplacement publicitaire réservé"></div>'

def hero_ext(m):
    """'webp' si une photo réelle a été intégrée pour cette mosquée (voir m['photo']), sinon 'svg'."""
    return "webp" if m.get("photo") else "svg"

def carte(m, rac=""):
    return f"""<a class="carte reveal" href="{rac}mosquees/{m['slug']}/index.html"
   data-pays="{m['pays']}" data-style="{m['style']}" data-epoque="{m['epoque']}">
  <div class="arc"><div class="cadre"><img src="{rac}assets/images/{m['slug']}/hero.{hero_ext(m)}" loading="lazy"
    alt="Illustration de la {m['nom']} à {m['ville']}" width="1200" height="700"></div></div>
  <div class="corps">
    <span class="pays">{m['ville']} · {m['pays']}</span>
    <h3>{m['nom']}</h3>
    <p>{m['court']}</p>
    <span class="meta"><span>{m['style']}</span></span>
  </div>
</a>"""

# ---------------------------------------------------------------- accueil
def page_accueil():
    phares = [MOSQUEES[4], MOSQUEES[3], MOSQUEES[6], MOSQUEES[16]]  # Bleue, Hassan II, Cheikh Zayed, Nasir al-Mulk
    slides, dots = [], []
    for i, m in enumerate(phares):
        slides.append(f'<div class="slide{" on" if i==0 else ""}"><img src="assets/images/{m["slug"]}/hero.{hero_ext(m)}" alt="{m["nom"]}" {"" if i==0 else "loading=\"lazy\""}></div>')
        dots.append(f'<button class="{"on" if i==0 else ""}" aria-label="Diapositive {i+1} : {m["nom"]}"></button>')
    corps = f"""
<section class="hero" aria-label="Introduction">
  {''.join(slides)}
  <div class="voile"></div>
  <div class="inner wrap">
    <p class="eyebrow">Histoire · Architecture · Voyage</p>
    <h1>Les 20 plus belles<br>mosquées du monde</h1>
    <p class="lead">De la terre crue de Djenné aux faïences d'Iznik d'Istanbul, un voyage éditorial et immersif à travers quatorze siècles d'architecture sacrée.</p>
    <p><a class="btn btn-or" href="mosquees.html">Explorer les 20 mosquées</a>&nbsp;&nbsp;
       <a class="btn btn-ligne" href="#phares" style="color:var(--ivoire)">Les incontournables</a></p>
  </div>
  <div class="hero-dots">{''.join(dots)}</div>
</section>
<main class="wrap">
  {slot_pub()}
  <div id="phares">{sep("Sélection", "Quatre chefs-d'œuvre pour commencer")}</div>
  <p class="muted reveal" style="max-width:640px;margin:0 auto 1rem;text-align:center">Quatre édifices, quatre continents d'inspiration : l'apogée ottomane, le génie marocain contemporain, la démesure émiratie et le kaléidoscope persan.</p>
  <div class="grille">{''.join(carte(m) for m in phares)}</div>
  {sep("Le concept", "Un guide qui se lit comme un récit")}
  <div class="deux-col reveal" style="grid-template-columns:1fr 1fr;gap:34px">
    <div class="prose">
      <p>Chaque mosquée de cette collection a été choisie pour ce qu'elle raconte : une dynastie, une prouesse technique, une communauté. Pour chacune, vous trouverez une <strong>histoire complète</strong>, des <strong>anecdotes</strong> vérifiées, une <strong>galerie immersive</strong> plein écran, la <strong>localisation</strong> précise et un <strong>espace de discussion</strong> pour partager vos propres visites.</p>
      <p>Quand une visite virtuelle 360° officielle existe, elle est intégrée directement sur la page ; sinon, notre visionneuse plein écran (zoom, déplacement) prend le relais.</p>
    </div>
    <div class="prose">
      <p><strong>Filtrez par pays, style ou époque</strong> : art omeyyade d'al-Andalus, classicisme ottoman de Sinan, grès rouge moghol, banco soudano-sahélien, audaces contemporaines… Les vingt notices se répondent grâce aux suggestions « mosquées similaires » en bas de chaque page.</p>
      <p><a class="btn btn-ligne" href="a-propos.html">Notre démarche éditoriale →</a></p>
    </div>
  </div>
  {sep("Aperçu", "La collection complète")}
  <div class="grille">{''.join(carte(m) for m in MOSQUEES[:8])}</div>
  <p style="text-align:center;margin:0 0 2rem"><a class="btn btn-or" href="mosquees.html">Voir les 20 mosquées</a></p>
</main>"""
    jsonld = {"@context": "https://schema.org", "@type": "WebSite", "name": NOM_SITE,
              "url": SITE_URL, "inLanguage": "fr",
              "description": "Guide illustré des 20 plus belles mosquées du monde : histoire, anecdotes, galeries immersives et visites virtuelles."}
    return page(f"{NOM_SITE} : histoire, photos et visites",
                "Découvrez les 20 plus belles mosquées du monde : histoire, anecdotes, galeries immersives, visites virtuelles et cartes. Un guide illustré, gratuit et complet.",
                corps, canonique="", jsonld=jsonld, actif="accueil")

# ---------------------------------------------------------------- liste
def page_liste():
    pays = sorted(set(m["pays"] for m in MOSQUEES))
    styles = sorted(set(m["style"] for m in MOSQUEES))
    epoques = sorted(set(m["epoque"] for m in MOSQUEES))
    opt = lambda vals: "".join(f'<option value="{v}">{v}</option>' for v in vals)
    corps = f"""
<main class="wrap">
  <div style="padding-top:2.4rem">
    <p class="eyebrow">La collection</p>
    <h1>Les 20 mosquées</h1>
    <p class="muted" style="max-width:680px">Du VIIe siècle à nos jours, de Xi'an à Casablanca. Filtrez par pays, style architectural ou époque, ou recherchez librement.</p>
  </div>
  <div class="filtres" role="search">
    <label>Pays <select id="f-pays"><option value="">Tous</option>{opt(pays)}</select></label>
    <label>Style <select id="f-style"><option value="">Tous</option>{opt(styles)}</select></label>
    <label>Époque <select id="f-epoque"><option value="">Toutes</option>{opt(epoques)}</select></label>
    <label>Recherche <input type="search" id="f-texte" placeholder="Nom, ville…"></label>
    <span class="compte" id="f-compte">20 mosquées</span>
  </div>
  <div class="grille" id="grille-mosquees">{''.join(carte(m) for m in MOSQUEES)}</div>
  {slot_pub()}
</main>"""
    jsonld = {"@context": "https://schema.org", "@type": "ItemList",
              "name": "Les 20 plus belles mosquées du monde",
              "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": m["nom"],
                                   "url": f"{SITE_URL}/mosquees/{m['slug']}/"} for i, m in enumerate(MOSQUEES)]}
    return page("Les 20 plus belles mosquées du monde — liste complète et filtres | Qibla",
                "Liste des 20 plus belles mosquées du monde avec filtres par pays, style architectural et époque : Istanbul, Casablanca, Abou Dabi, Djenné, Ispahan…",
                corps, canonique="mosquees.html", jsonld=jsonld, actif="liste")

def disclaimer_religieux(rac=""):
    return f"""<div class="disclaimer">
  <p><strong>À propos du contenu de cette page</strong> — Ce site propose un contenu éditorial et culturel
  rédigé avec soin et le souci du respect des traditions religieuses concernées ; il ne constitue pas un
  avis théologique ou une source d'autorité religieuse. Malgré nos vérifications, des erreurs, imprécisions
  ou approximations peuvent subsister. Si vous en repérez une, merci de nous la signaler via la page
  <a href="{rac}contact.html">Contact</a> ou par e-mail à <a href="mailto:qibla.mosk@gmail.com">qibla.mosk@gmail.com</a> —
  nous la corrigerons avec gratitude.</p>
</div>"""

# ---------------------------------------------------------------- blog
def carte_article(a, rac=""):
    return f"""<a class="carte reveal" href="{rac}blog/{a['slug']}/index.html">
  <div class="corps">
    <span class="pays">{a['eyebrow']} · {a['temps_lecture']} de lecture</span>
    <h3>{a['titre']}</h3>
    <p>{a['description']}</p>
  </div>
</a>"""

def page_blog_liste():
    corps = f"""
<main class="wrap">
  <div style="padding-top:2.4rem">
    <p class="eyebrow">Le blog</p>
    <h1>Histoire et architecture islamique</h1>
    <p class="muted" style="max-width:680px">Des articles de fond pour comprendre ce qui se cache derrière les coupoles, les minarets et les motifs géométriques des mosquées présentées sur ce site.</p>
  </div>
  <div class="grille">{''.join(carte_article(a) for a in ARTICLES)}</div>
  {slot_pub()}
</main>"""
    jsonld = {"@context": "https://schema.org", "@type": "Blog", "name": "Blog Qibla — Architecture islamique",
              "blogPost": [{"@type": "BlogPosting", "headline": a["titre"], "datePublished": a["date"],
                            "url": f"{SITE_URL}/blog/{a['slug']}/"} for a in ARTICLES]}
    return page("Blog — Histoire et architecture islamique | Qibla",
                "Articles de fond sur l'histoire et l'architecture islamique : origines de la mosquée, coupoles et minarets, muqarnas et motifs géométriques.",
                corps, canonique="blog.html", jsonld=jsonld, actif="blog")

def galerie_article(a, rac):
    photos = a.get("photos", [])
    if not photos:
        return ""
    imgs = "".join(
        f'<figure><img src="{rac}assets/images/{p["chemin"]}" loading="lazy" alt="{p["description"]}" '
        f'width="700" height="467" style="width:100%;height:auto;border-radius:10px"></figure>'
        for p in photos)
    return f'<div class="quiz-choix" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px;margin:1.6rem 0">{imgs}</div>'

def page_article(a):
    rac = "../../"
    def rlien(html): return html.replace("{RAC}", rac)
    corps_html = "".join(f"<h2>{titre}</h2><p>{rlien(texte)}</p>" for titre, texte in a["corps"])
    liees = [m for m in MOSQUEES if m["slug"] in a["mosquees_liees"]]
    corps = f"""
<main class="wrap">
  <div style="padding-top:2.4rem;max-width:760px">
    <p class="fil"><a href="{rac}index.html">Accueil</a> › <a href="{rac}blog.html">Blog</a> › {a['titre']}</p>
    <p class="eyebrow">{a['eyebrow']} · {a['temps_lecture']} de lecture · {a['date']}</p>
    <h1>{a['titre']}</h1>
  </div>
  <div class="prose" style="max-width:760px">
    <p class="lead">{rlien(a['intro'])}</p>
    {galerie_article(a, rac)}
    {corps_html}
  </div>
  {slot_pub()}
  {sep("À découvrir", "Mosquées citées dans cet article")}
  <div class="grille">{''.join(carte(m, rac) for m in liees)}</div>
  <div style="max-width:760px;margin:2rem auto 0">{disclaimer_religieux(rac)}</div>
</main>"""
    jsonld = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": a["titre"],
              "description": a["description"], "datePublished": a["date"], "inLanguage": "fr",
              "url": f"{SITE_URL}/blog/{a['slug']}/"}
    return page(f"{a['titre']} | Blog Qibla", a["description"], corps, rac=rac,
                canonique=f"blog/{a['slug']}/", jsonld=jsonld, actif="blog")

# ---------------------------------------------------------------- quiz
def carte_theme_quiz(cle, t):
    return f"""<button type="button" class="carte theme-quiz reveal" data-theme="{cle}">
  <div class="corps">
    <span class="pays" style="font-size:1.4rem">{t['emoji']}</span>
    <h3>{t['titre']}</h3>
    <p>{t['description']}</p>
    <p class="note">{len(t['questions'])} questions</p>
  </div>
</button>"""

def page_quiz():
    corps = f"""
<main class="wrap">
  <div style="padding-top:2.4rem">
    <p class="eyebrow">Tester ses connaissances</p>
    <h1>Quiz Qibla</h1>
    <p class="muted" style="max-width:680px">Choisissez un thème (100 questions chacun), le nombre de questions et le nombre de joueurs — seul ou à plusieurs, à tour de rôle sur le même écran.</p>
  </div>
  <div class="grille" id="quiz-themes">{''.join(carte_theme_quiz(c, t) for c, t in QUIZ.items())}</div>

  <div id="quiz-config" class="quiz-jeu" hidden>
    <p class="eyebrow" id="quiz-config-titre"></p>
    <div class="quiz-config-bloc">
      <p class="note">Nombre de questions</p>
      <div class="quiz-choix" id="quiz-choix-nb">
        <button type="button" data-nb="10">10</button>
        <button type="button" data-nb="20">20</button>
        <button type="button" data-nb="30">30</button>
        <button type="button" data-nb="50">50</button>
      </div>
    </div>
    <div class="quiz-config-bloc">
      <p class="note">Nombre de joueurs</p>
      <div class="quiz-joueurs-nb">
        <button type="button" id="quiz-joueurs-moins" aria-label="Moins de joueurs">−</button>
        <span id="quiz-joueurs-compte">1</span>
        <button type="button" id="quiz-joueurs-plus" aria-label="Plus de joueurs">+</button>
      </div>
      <div id="quiz-joueurs-noms" class="quiz-joueurs-noms"></div>
    </div>
    <div class="quiz-actions">
      <button type="button" class="btn btn-ligne" id="quiz-config-retour">← Changer de thème</button>
      <button type="button" class="btn btn-or" id="quiz-config-demarrer">Démarrer la partie →</button>
    </div>
  </div>

  <div id="quiz-jeu" class="quiz-jeu" hidden>
    <div class="quiz-entete">
      <p class="eyebrow" id="quiz-titre-theme"></p>
      <p class="note" id="quiz-progression"></p>
    </div>
    <p class="quiz-au-tour" id="quiz-au-tour" hidden></p>
    <div id="quiz-question-zone"></div>
    <div class="quiz-actions">
      <button type="button" class="btn btn-ligne" id="quiz-quitter">← Changer de thème</button>
      <button type="button" class="btn btn-or" id="quiz-suivant" hidden>Suivant →</button>
    </div>
  </div>

  <div id="quiz-resultat" class="quiz-resultat" hidden>
    <p class="eyebrow">Résultat</p>
    <div id="quiz-classement"></div>
    <p id="quiz-message" class="muted"></p>
    <p><button type="button" class="btn btn-or" id="quiz-rejouer">Rejouer (même réglages)</button>
       <button type="button" class="btn btn-ligne" id="quiz-autre-theme">Choisir un autre thème</button></p>
  </div>

  {slot_pub()}
  <div style="max-width:760px;margin:2rem auto 0">{disclaimer_religieux()}</div>
  <script type="application/json" id="quiz-data">{json.dumps(QUIZ, ensure_ascii=False)}</script>
</main>"""
    jsonld = {"@context": "https://schema.org", "@type": "Quiz", "name": "Quiz Qibla",
              "about": "Islam, prophète Muhammad, prophètes de l'islam et mosquées célèbres"}
    return page("Quiz — Islam, prophètes et mosquées célèbres | Qibla",
                "Trois quiz de 100 questions en français, seul ou à plusieurs : l'islam et son prophète, les prophètes de l'islam, et les mosquées les plus célèbres du monde.",
                corps, canonique="quiz.html", jsonld=jsonld, actif="quiz")

# ---------------------------------------------------------------- boussole (qibla)
def page_qibla():
    corps = f"""
<main class="wrap">
  <div style="padding-top:2.4rem;max-width:720px">
    <p class="eyebrow">Trouver la Qibla</p>
    <h1>Boussole Qibla</h1>
    <p class="muted">Calculez la direction de La Mecque depuis l'endroit où vous vous trouvez, et repérez les mosquées les plus proches de vous (données OpenStreetMap).</p>
  </div>

  <div class="boussole-bloc" id="boussole-avant">
    <p class="note">Votre position n'est utilisée que dans votre navigateur, le temps du calcul : elle n'est jamais envoyée à nos serveurs (nous n'en avons pas) ni conservée.</p>
    <button type="button" class="btn btn-or" id="boussole-localiser">📍 Me géolocaliser</button>
    <p class="note" id="boussole-erreur" style="color:var(--terre)"></p>
  </div>

  <div class="boussole-bloc" id="boussole-resultat" hidden>
    <div class="boussole-cadran">
      <div class="boussole-rose"></div>
      <div class="boussole-aiguille" id="boussole-aiguille">➤</div>
    </div>
    <p class="boussole-degres" id="boussole-degres"></p>
    <p class="muted" id="boussole-instruction"></p>
    <p class="note" id="boussole-distance"></p>
  </div>

  {sep("À proximité", "Mosquées les plus proches")}
  <div id="mosquees-proches">
    <p class="note" id="proches-statut">Géolocalisez-vous pour afficher les mosquées les plus proches (recherche via OpenStreetMap).</p>
    <div id="proches-liste"></div>
  </div>

  {slot_pub()}
  <div style="max-width:760px;margin:2rem auto 0">{disclaimer_religieux()}</div>
</main>"""
    return page("Boussole Qibla — direction de La Mecque et mosquées à proximité | Qibla",
                "Calculez la direction de La Mecque (qibla) depuis votre position, et trouvez les mosquées les plus proches de vous grâce à OpenStreetMap.",
                corps, canonique="boussole.html", actif="boussole")

# ---------------------------------------------------------------- détail
def similaires(m):
    memes = [x for x in MOSQUEES if x["slug"] != m["slug"] and (x["style"] == m["style"] or x["pays"] == m["pays"])]
    if len(memes) < 3:
        memes += [x for x in MOSQUEES if x["slug"] != m["slug"] and x not in memes]
    return memes[:3]

def visite_360(m, osm):
    """VisiteVirtuelle3D : iframe si m['visite']['mode']=='iframe' (site n'interdit pas le frame),
    bouton vers le lien officiel si mode=='lien' (le site bloque l'intégration en iframe), sinon repli galerie+OSM."""
    v = m.get("visite")
    if v and v.get("mode") == "iframe":
        return (f'<iframe src="{v["url"]}" loading="lazy" allowfullscreen '
                f'title="Visite virtuelle de {m["nom"]}" style="border:0;width:100%;height:100%"></iframe>')
    if v and v.get("mode") == "lien":
        return f"""<div class="alt">
        <div>
          <p class="eyebrow">Visite virtuelle</p>
          <p style="max-width:520px">Une visite virtuelle 360° officielle existe pour ce lieu ({v["note"]}), mais son éditeur interdit l'intégration en iframe sur un site tiers. Ouvrez-la directement :</p>
          <p><a class="btn btn-or" href="{v['url']}" rel="noopener" target="_blank">Voir la visite virtuelle officielle ↗</a></p>
        </div>
      </div>"""
    return f"""<div class="alt">
        <div>
          <p class="eyebrow">Visite virtuelle</p>
          <p style="max-width:520px">Aucune visite 360° officielle n'est encore intégrée pour cette page. En attendant, explorez la <strong>galerie immersive plein écran</strong> ci-dessus, ou ouvrez le monument dans votre application de cartographie.</p>
          <p><a class="btn btn-or" href="{osm}" rel="noopener" target="_blank">Voir sur OpenStreetMap ↗</a></p>
        </div>
      </div>"""

def page_detail(m):
    rac = "../../"
    gal = [("hero", hero_ext(m), "Vue au crépuscule" if not m.get("photo") else "Vue de la mosquée")]
    for i, p in enumerate(m.get("photos_extra", []), start=2):
        gal.append((f"photo-{i}", "webp", p["description"]))
    gal += [("medaillon", "svg", "Médaillon géométrique inspiré du décor"), ("motif", "svg", "Motif d'étoiles à huit branches")]
    if not m.get("photo"):
        gal.insert(1, ("aube", "svg", "Lumière de l'aube"))
        gal.insert(2, ("nuit", "svg", "Vue de nuit"))
    galerie = "".join(
        f'<button type="button"><img src="{rac}assets/images/{m["slug"]}/{f}.{ext}" loading="lazy" '
        f'alt="{m["nom"]} — {leg}" data-grand="{rac}assets/images/{m["slug"]}/{f}.{ext}" width="1200" height="700"></button>'
        for f, ext, leg in gal)
    hist = "".join(f"<p>{p}</p>" for p in m["histoire"])
    anec = "".join(f"<li>{a}</li>" for a in m["anecdotes"])
    sim = "".join(carte(x, rac) for x in similaires(m))
    osm = f"https://www.openstreetmap.org/?mlat={m['lat']}&mlon={m['lon']}#map=17/{m['lat']}/{m['lon']}"
    booking = f"https://www.booking.com/searchresults.fr.html?ss={m['ville'].replace(' ', '%20')}%20{m['pays'].split('/')[0].strip().replace(' ', '%20')}"
    corps = f"""
<div class="bandeau">
  <img class="fond" src="{rac}assets/images/{m['slug']}/hero.{hero_ext(m)}" alt="" aria-hidden="true">
  <div class="voile"></div>
  <div class="titre wrap">
    <p class="fil"><a href="{rac}index.html">Accueil</a> › <a href="{rac}mosquees.html">Les 20 mosquées</a> › {m['nom']}</p>
    <p class="eyebrow">{m['ville']} · {m['pays']} · {m['style']}</p>
    <h1>{m['nom']}</h1>
  </div>
</div>
<main class="wrap">
  <div class="deux-col">
    <article class="prose reveal">
      {sep("Histoire", "")}
      <h2 style="margin-top:0">L'histoire</h2>
      {hist}
      {slot_pub()}
      <h2>Anecdotes &amp; faits marquants</h2>
      <ul class="anecdotes">{anec}</ul>
    </article>
    <aside>
      <div class="encart reveal">
        <p class="eyebrow" style="margin-top:0">Infos pratiques</p>
        <dl>
          <dt>Localisation</dt><dd>{m['ville']}, {m['pays']}</dd>
          <dt>Style architectural</dt><dd>{m['style']}</dd>
          <dt>Époque</dt><dd>{m['epoque']}</dd>
          <dt>Dates clés</dt><dd>{m['annee']}</dd>
          <dt>Capacité</dt><dd>{m['capacite']}</dd>
          <dt>Architecte / bâtisseurs</dt><dd>{m['architecte']}</dd>
          <dt>Coordonnées</dt><dd>{m['lat']}, {m['lon']}</dd>
        </dl>
        <div class="pub" style="margin:18px 0 0" role="complementary" aria-label="Emplacement publicitaire réservé"></div>
      </div>
    </aside>
  </div>

  {sep("Galerie", "Galerie immersive")}
  <p class="muted reveal">Cliquez sur une image pour l'ouvrir en plein écran (zoom à la molette, déplacement à la souris ou au doigt).</p>
  <div class="galerie reveal">{galerie}</div>

  {sep("Visite", "Visite virtuelle 360°")}
  <div class="visite reveal" id="visite-360">
    <div class="cadre360">{visite_360(m, osm)}</div>
    <div class="barre">🧭 Composant réutilisable <code>VisiteVirtuelle3D</code> — accepte tout lecteur 360° par iframe (Street View intérieur, Kuula, Matterport…).</div>
  </div>

  {sep("Localisation", "S'y rendre")}
  <div class="loc reveal">
    <div class="boite">
      <h3 style="margin-top:0">Coordonnées</h3>
      <table class="simple">
        <tr><th>Adresse</th><td>{m['ville']}, {m['pays']}</td></tr>
        <tr><th>Latitude</th><td>{m['lat']}</td></tr>
        <tr><th>Longitude</th><td>{m['lon']}</td></tr>
      </table>
      <p><a class="btn btn-ligne" href="{osm}" rel="noopener" target="_blank">Ouvrir la carte interactive ↗</a></p>
      <p class="note">Le site est fourni sans dépendance externe : la carte interactive s'ouvre chez OpenStreetMap. Pour une carte intégrée, activez Leaflet (voir README).</p>
    </div>
    <div class="boite">
      <h3 style="margin-top:0">Voyager vers {m['pays'].split('/')[0].strip()}</h3>
      <p class="muted">Préparez votre visite : hébergements et vols près de {m['ville']}.</p>
      <div class="affil" style="grid-template-columns:1fr">
        <a href="{booking}" rel="noopener sponsored" target="_blank"><span class="tag">Partenaire · hébergement</span><b>Hôtels à {m['ville']} →</b></a>
        <a href="#" rel="noopener sponsored"><span class="tag">Partenaire · vols (lien affilié à configurer)</span><b>Vols vers {m['pays'].split('/')[0].strip()} →</b></a>
      </div>
      <p class="note">Blocs compatibles affiliation (Booking.com, Expedia…) — identifiants à renseigner, voir README.</p>
    </div>
  </div>

  {sep("Discussion", "Commentaires")}
  <div class="commentaires reveal" id="zone-commentaires" data-slug="{m['slug']}">
    <h3 style="margin-top:0">Vous avez visité la {m['nom']} ?</h3>
    <script src="https://giscus.app/client.js"
      data-repo="lqpasse-pixel/qibla-mosquees"
      data-repo-id="R_kgDOTOkK5g"
      data-category="Announcements"
      data-category-id="DIC_kwDOTOkK5s4DAkcH"
      data-mapping="pathname"
      data-strict="0"
      data-reactions-enabled="1"
      data-emit-metadata="0"
      data-input-position="bottom"
      data-theme="preferred_color_scheme"
      data-lang="fr"
      crossorigin="anonymous"
      async>
    </script>
  </div>

  <section class="similaires">
    {sep("Continuer", "Mosquées similaires")}
    <div class="grille">{sim}</div>
  </section>
  <div style="max-width:760px;margin:2rem auto 0">{disclaimer_religieux(rac)}</div>
</main>
<div class="visionneuse" id="visionneuse" role="dialog" aria-label="Visionneuse d'images plein écran">
  <div class="scene"><img src="" alt=""></div>
  <p class="legende"></p>
  <div class="outils">
    <button id="vis-moins" aria-label="Zoom arrière">−</button>
    <button id="vis-raz">Réinitialiser</button>
    <button id="vis-plus" aria-label="Zoom avant">+</button>
    <button id="vis-fermer">Fermer ✕</button>
  </div>
</div>"""
    jsonld = {"@context": "https://schema.org", "@type": "TouristAttraction",
              "name": m["nom"], "description": m["court"],
              "address": {"@type": "PostalAddress", "addressLocality": m["ville"], "addressCountry": m["pays"]},
              "geo": {"@type": "GeoCoordinates", "latitude": m["lat"], "longitude": m["lon"]},
              "image": f"{SITE_URL}/assets/images/{m['slug']}/hero.{hero_ext(m)}",
              "url": f"{SITE_URL}/mosquees/{m['slug']}/",
              "touristType": "Architecture, histoire, spiritualité"}
    return page(f"{m['nom']} ({m['ville']}) : histoire, photos, visite virtuelle | Qibla",
                f"{m['nom']} à {m['ville']}, {m['pays']} : histoire complète, anecdotes, galerie immersive, infos pratiques ({m['style']}, {m['epoque']}) et visite virtuelle.",
                corps, rac=rac, canonique=f"mosquees/{m['slug']}/", jsonld=jsonld, actif="liste")

# ---------------------------------------------------------------- pages annexes
def page_simple(titre_meta, desc, h1, eyebrow, html, canonique, actif=""):
    corps = f"""<main class="wrap"><div style="padding-top:2.4rem;max-width:800px">
<p class="eyebrow">{eyebrow}</p><h1>{h1}</h1></div>
<div class="prose" style="max-width:800px">{html}</div></main>"""
    return page(titre_meta, desc, corps, canonique=canonique, actif=actif)

APROPOS = """
<p><strong>Qibla</strong> est un guide indépendant consacré aux vingt mosquées les plus remarquables du monde. Notre parti pris : raconter chaque édifice comme un récit — son commanditaire, ses bâtisseurs, ses légendes — plutôt qu'aligner des fiches techniques.</p>
<h2>Notre démarche</h2>
<p>Les textes sont rédigés à partir des connaissances historiques et architecturales publiées ; les anecdotes signalées comme légendes sont présentées comme telles. Le site est conçu pour être rapide, sobre et accessible : aucune ressource visuelle n'est chargée depuis un site tiers, tout est hébergé localement.</p>
<h2>Les illustrations</h2>
<p>Chaque mosquée est représentée par une série d'illustrations vectorielles originales, créées spécialement pour ce site en respectant la silhouette réelle du monument (nombre de minarets, forme des coupoles, matériaux emblématiques). Elles peuvent être remplacées à tout moment par des photographies — la page <a href="credits-photos.html">Crédits images</a> et le fichier <code>credits-photos.md</code> tracent la licence de chaque visuel.</p>
<h2>Respect des lieux</h2>
<p>Ces édifices sont avant tout des lieux de culte vivants. Nos pages « infos pratiques » rappellent les coordonnées et le contexte, mais renseignez-vous toujours sur les conditions de visite (horaires de prière, tenue, accès des non-musulmans) avant de vous déplacer.</p>"""

CONTACT = """
<p>Une correction historique, une photo à proposer, un partenariat ? Écrivez-nous.</p>
<div class="commentaires" style="max-width:640px">
<form onsubmit="event.preventDefault();this.outerHTML='<p><strong>Merci !</strong> Votre message a été préparé. Branchez ce formulaire à Formspree, Netlify Forms ou votre backend (voir README).</p>'">
<label>Votre nom<input required type="text" maxlength="60"></label>
<label>Votre e-mail<input required type="email"></label>
<label>Votre message<textarea required maxlength="3000"></textarea></label>
<p><button class="btn btn-or" type="submit">Envoyer</button></p>
</form></div>
<p class="note">Adresse éditoriale : qibla.mosk@gmail.com</p>"""

CREDITS_HTML = """
<p>Toutes les images actuellement publiées sur ce site sont des <strong>illustrations vectorielles originales</strong> créées pour Qibla. Elles sont hébergées localement dans <code>/assets/images/</code> et ne dépendent d'aucun service tiers.</p>
<table class="simple">
<tr><th>Répertoire</th><th>Contenu</th><th>Auteur</th><th>Licence</th></tr>
<tr><td>/assets/images/&lt;mosquée&gt;/</td><td>hero.svg, aube.svg, nuit.svg, medaillon.svg, motif.svg</td><td>Studio Qibla (créations originales)</td><td>Usage libre au sein de ce site</td></tr>
<tr><td>/assets/images/site/</td><td>favicon.svg, motifs décoratifs</td><td>Studio Qibla</td><td>Usage libre au sein de ce site</td></tr>
</table>
<h2>Ajouter des photographies</h2>
<p>Si vous remplacez une illustration par une photographie (Unsplash, Pexels, Pixabay, Wikimedia Commons…), vous devez : 1) télécharger le fichier dans le dossier de la mosquée concernée, 2) le référencer par chemin relatif, 3) ajouter une ligne au fichier <code>credits-photos.md</code> (source, auteur, licence). Le détail des licences compatibles figure dans ce même fichier.</p>"""

MENTIONS = """
<h2>Éditeur du site</h2>
<p>[Nom / raison sociale] — [adresse] — [e-mail]. Directeur de la publication : [nom]. <em>(Champs à compléter avant mise en ligne.)</em></p>
<h2>Hébergement</h2>
<p>[Hébergeur, adresse, téléphone] — par exemple Vercel Inc. ou Netlify Inc. selon votre déploiement.</p>
<h2>Propriété intellectuelle</h2>
<p>Les textes et illustrations de ce site sont des créations originales. Toute reproduction, intégrale ou partielle, est soumise à autorisation préalable. Les noms des monuments appartiennent au domaine public.</p>
<h2>Responsabilité</h2>
<p>Les informations (horaires, conditions de visite, capacités) sont fournies à titre indicatif et peuvent évoluer ; vérifiez auprès des institutions concernées avant tout déplacement.</p>"""

CONFID = """
<h2>Données collectées</h2>
<p>Ce site ne collecte par défaut <strong>aucune donnée personnelle côté serveur</strong>. Vos préférences (thème, consentement cookies) sont stockées uniquement dans votre navigateur (localStorage) et ne sont transmises à personne. Les commentaires sont gérés par <strong>Giscus</strong>, un service tiers qui s'appuie sur GitHub Discussions : pour commenter, vous vous connectez avec votre compte GitHub et votre message est hébergé publiquement sur le dépôt GitHub du site, selon la politique de confidentialité de GitHub.</p>
<h2>Géolocalisation (page Boussole)</h2>
<p>La page « Boussole » propose de calculer la direction de La Mecque et les mosquées à proximité à partir de votre position. Cette position est demandée via une autorisation explicite de votre navigateur, n'est utilisée que localement dans votre appareil pour le calcul, et n'est <strong>jamais envoyée à nos serveurs</strong> (nous n'en avons pas) ni conservée. La recherche des mosquées à proximité interroge en revanche <strong>OpenStreetMap</strong> (service tiers, API Overpass) avec vos coordonnées, uniquement au moment de la recherche.</p>
<h2>Cookies et mesure d'audience</h2>
<p>Un bandeau de consentement vous permet d'accepter ou de refuser la mesure d'audience. Aucune balise de mesure n'est chargée avant votre accord. Si vous activez un outil (Google Analytics 4, Plausible…), cette page devra détailler l'outil retenu, la durée de conservation et la base légale (art. 82 loi Informatique et Libertés, RGPD).</p>
<h2>Newsletter</h2>
<p>L'adresse e-mail saisie dans le formulaire d'inscription n'est utilisée que pour l'envoi de la lettre d'information. Base légale : consentement (art. 6.1.a RGPD). Désinscription possible à tout moment via le lien présent dans chaque envoi.</p>
<h2>Vos droits</h2>
<p>Conformément au RGPD, vous disposez d'un droit d'accès, de rectification, d'effacement et d'opposition. Contact : [e-mail du délégué ou de l'éditeur]. Vous pouvez introduire une réclamation auprès de la CNIL (cnil.fr).</p>"""

CGU = """
<h2>Objet</h2>
<p>Les présentes conditions encadrent l'utilisation du site Qibla, guide éditorial consacré à l'architecture des mosquées.</p>
<h2>Commentaires</h2>
<p>Les espaces de discussion sont modérés. Sont proscrits : propos haineux ou discriminatoires, spam, liens promotionnels, contenus contraires à la loi. L'éditeur se réserve le droit de supprimer tout contenu inapproprié sans préavis.</p>
<h2>Contenus</h2>
<p>Les informations publiées sont fournies de bonne foi, sans garantie d'exhaustivité. Les liens externes (cartographie, partenaires de voyage) sont proposés à titre de commodité ; l'éditeur n'est pas responsable de leurs contenus.</p>
<h2>Liens d'affiliation et publicité</h2>
<p>Certains liens peuvent être affiliés : une commission peut être perçue sur les réservations effectuées, sans surcoût pour le visiteur. Les emplacements publicitaires sont signalés comme tels.</p>"""

# ---------------------------------------------------------------- fichiers annexes
def credits_md():
    lignes = ["# Crédits images — Qibla", "",
              "Toutes les images sont hébergées localement dans `/assets/images/`. Aucune URL externe n'est utilisée au runtime.", "",
              "| Fichier | Description | Source | Auteur | Licence |",
              "|---|---|---|---|---|"]
    for m in MOSQUEES:
        p = m.get("photo")
        if p:
            lignes.append(f"| assets/images/{m['slug']}/hero.webp | {m['nom']} — {p['description']} | "
                          f"[{p['source']}]({p['url']}) | {p['auteur']} | {p['licence']} |")
        else:
            lignes.append(f"| assets/images/{m['slug']}/hero.svg | {m['nom']} — Vue au crépuscule | Création originale pour ce site | Studio Qibla | Libre au sein du projet |")
        for i, ep in enumerate(m.get("photos_extra", []), start=2):
            lignes.append(f"| assets/images/{m['slug']}/photo-{i}.webp | {m['nom']} — {ep['description']} | "
                          f"[{ep['source']}]({ep['url']}) | {ep['auteur']} | {ep['licence']} |")
        for f, d in [("aube.svg", "Vue à l'aube"), ("nuit.svg", "Vue de nuit"),
                     ("medaillon.svg", "Médaillon géométrique"), ("motif.svg", "Motif étoilé")]:
            lignes.append(f"| assets/images/{m['slug']}/{f} | {m['nom']} — {d} | Création originale pour ce site | Studio Qibla | Libre au sein du projet |")
    lignes.append("| assets/images/site/favicon.svg | Favicon étoile à 8 branches | Création originale | Studio Qibla | Libre au sein du projet |")
    for a in ARTICLES:
        for p in a.get("photos", []):
            if not p["chemin"].startswith("blog/"):
                continue
            lignes.append(f"| assets/images/{p['chemin']} | Article « {a['titre']} » — {p['description']} | "
                          f"[{p['source']}]({p['url']}) | {p['auteur']} | {p['licence']} |")
    lignes += ["",
               "## Ajouter une photographie",
               "1. Télécharger le fichier (jamais de hotlink) dans `assets/images/<slug-mosquee>/` avec un nom SEO-friendly, ex. `mosquee-hassan-ii-casablanca-facade.webp`.",
               "2. Convertir en WebP (`cwebp -q 82 photo.jpg -o photo.webp`) et garder un fallback JPEG si besoin.",
               "3. Référencer par chemin relatif uniquement.",
               "4. Ajouter une ligne à ce tableau : source (Unsplash, Pexels, Pixabay, Wikimedia Commons…), auteur, licence exacte (Unsplash License, Pexels License, CC0, CC BY-SA 4.0…).",
               "5. Pour les images générées par IA : les placer dans `assets/images/generated/` et l'indiquer dans la colonne Source."]
    return "\n".join(lignes)

README = """# Qibla — Les 20 plus belles mosquées du monde

Site statique complet, en français, sans aucune dépendance externe au runtime (100 % autonome, fonctionne hors ligne).

## Lancer en local
Ouvrez `index.html` dans un navigateur, ou servez le dossier :
```bash
cd dist && python3 -m http.server 8000
```

## Déployer
Le site est en ligne sur Netlify : https://qibla-mosquees.netlify.app, avec déploiement continu depuis
le dépôt [lqpasse-pixel/qibla-mosquees](https://github.com/lqpasse-pixel/qibla-mosquees) (branche `master`,
commande de build `python3 build.py`, dossier de publication `dist`). Chaque `git push` republie automatiquement.
- Pour brancher un nom de domaine personnalisé : Netlify → Site settings → Domain management → Add a domain.
- Si vous changez d'URL (domaine perso ou autre hébergeur), modifiez `SITE_URL` en haut de `build.py` puis
  relancez `python3 build.py` : `sitemap.xml`, `robots.txt` et les balises canoniques se régénèrent automatiquement.

## Modifier ou ajouter du contenu
Tout le contenu éditorial vit dans **`data_mosquees.py`** (une entrée par mosquée : histoire, anecdotes, infos pratiques, coordonnées). Relancez `python3 build.py` : les 20 pages, le sitemap et les crédits sont régénérés.

## Remplacer les illustrations par des photos
1. Téléchargez les fichiers dans `assets/images/<slug>/` (jamais de hotlink) — nommage SEO-friendly, format WebP privilégié.
2. Mettez à jour les `src` (ou remplacez simplement `hero.svg` par `hero.webp` et adaptez le template dans `build.py`).
3. Documentez chaque image dans `credits-photos.md` (source, auteur, licence).
4. Vérification finale : `grep -rE "https?://[^\\"]*(unsplash|pexels|wikimedia|pixabay)" dist/` ne doit rien retourner.

## Visites 360° (composant VisiteVirtuelle3D)
Sur chaque page détail, le bloc `#visite-360` accepte n'importe quel lecteur par iframe :
```html
<iframe src="URL_STREET_VIEW_OU_KUULA_OU_MATTERPORT" loading="lazy" allowfullscreen></iframe>
```
Pour Google Street View intérieur : Google Maps → le lieu → Partager → « Intégrer une carte », copier l'iframe. À défaut, la galerie immersive plein écran (zoom/pan) sert d'alternative — déjà active.

## Commentaires
Giscus est actif : les commentaires s'appuient sur les Discussions du dépôt GitHub
[lqpasse-pixel/qibla-mosquees](https://github.com/lqpasse-pixel/qibla-mosquees) (catégorie « Announcements »,
`data-mapping="pathname"` — une discussion par page). Le script est dans le bloc `#zone-commentaires` du
template `page_detail` de `build.py`. Pour le pointer vers un autre dépôt, remplacez `data-repo`, `data-repo-id`,
`data-category-id` (valeurs disponibles sur https://giscus.app une fois l'app GitHub installée sur le dépôt).

## Monétisation
- **AdSense** : remplacez les blocs `.pub` par vos balises `<ins class="adsbygoogle">` (emplacements prévus : bannière, sidebar 300×250, in-content 336×280).
- **Affiliation** : blocs « Voyager vers … » sur chaque page détail — ajoutez vos identifiants Booking.com / Expedia dans les liens.
- **Newsletter** : branchez le formulaire `#form-nl` sur Mailchimp ou Brevo (action POST du formulaire).
- **Analytics** : le point d'entrée post-consentement se trouve dans `site.js`, fonction `choixCookies` — n'y chargez GA4/Plausible qu'après accord (RGPD).

## Cartes interactives (option)
Le site reste autonome : la carte s'ouvre chez OpenStreetMap. Pour intégrer Leaflet, ajoutez ses fichiers **localement** dans `assets/vendeurs/leaflet/` (pas de CDN) et initialisez une carte avec les coordonnées présentes dans chaque page.

## Arborescence
```
dist/
├── index.html, mosquees.html, a-propos.html, contact.html, credits-photos.html
├── mentions-legales.html, confidentialite.html, cgu.html
├── mosquees/<slug>/index.html   (× 20)
├── assets/style.css, assets/site.js
├── assets/images/<slug>/{hero,aube,nuit,medaillon,motif}.svg
├── sitemap.xml, robots.txt, credits-photos.md
```
"""

# ---------------------------------------------------------------- génération
def main():
    if os.path.exists(DIST):
        shutil.rmtree(DIST)
    os.makedirs(os.path.join(DIST, "assets", "images", "site"))
    shutil.copy(os.path.join(ICI, "static", "style.css"), os.path.join(DIST, "assets", "style.css"))
    shutil.copy(os.path.join(ICI, "static", "site.js"), os.path.join(DIST, "assets", "site.js"))

    favicon = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 22 22">'
               '<rect width="22" height="22" rx="5" fill="#0d1830"/>'
               '<polygon points="11,2 13.4,7.6 19.6,8.2 15,12.4 16.4,18.6 11,15.2 5.6,18.6 7,12.4 2.4,8.2 8.6,7.6" fill="#c9a544"/></svg>')
    with open(os.path.join(DIST, "assets", "images", "site", "favicon.svg"), "w") as f:
        f.write(favicon)

    # images par mosquée
    PHOTOS_SRC = os.path.join(ICI, "assets", "images")
    for m in MOSQUEES:
        d = os.path.join(DIST, "assets", "images", m["slug"])
        os.makedirs(d)
        art = dict(m["art"]); art["ciel"] = m["art"]["ciel"]
        for nom, contenu in [("hero", scene(art, "hero")), ("aube", scene(art, "aube")),
                             ("nuit", scene(art, "nuit")), ("medaillon", medaillon(art)), ("motif", motif(art))]:
            with open(os.path.join(d, nom + ".svg"), "w") as f:
                f.write(contenu)
        if m.get("photo"):
            src = os.path.join(PHOTOS_SRC, m["slug"], "hero.webp")
            shutil.copy(src, os.path.join(d, "hero.webp"))
        for i, p in enumerate(m.get("photos_extra", []), start=2):
            src = os.path.join(PHOTOS_SRC, m["slug"], f"photo-{i}.webp")
            shutil.copy(src, os.path.join(d, f"photo-{i}.webp"))

    # images propres aux articles de blog (assets/images/blog/<slug>/photo-N.webp)
    for a in ARTICLES:
        for p in a.get("photos", []):
            if not p["chemin"].startswith("blog/"):
                continue
            src = os.path.join(PHOTOS_SRC, p["chemin"])
            dst = os.path.join(DIST, "assets", "images", p["chemin"])
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy(src, dst)

    # pages
    def ecrit(chemin, contenu):
        p = os.path.join(DIST, chemin)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w") as f:
            f.write(contenu)

    ecrit("index.html", page_accueil())
    ecrit("mosquees.html", page_liste())
    for m in MOSQUEES:
        ecrit(f"mosquees/{m['slug']}/index.html", page_detail(m))
    ecrit("blog.html", page_blog_liste())
    for a in ARTICLES:
        ecrit(f"blog/{a['slug']}/index.html", page_article(a))
    ecrit("quiz.html", page_quiz())
    ecrit("boussole.html", page_qibla())
    ecrit("a-propos.html", page_simple("À propos de Qibla — démarche éditoriale et sources",
        "La démarche éditoriale de Qibla : un guide indépendant, sourcé et autonome, consacré aux 20 plus belles mosquées du monde.",
        "À propos", "Le projet", APROPOS, "a-propos.html", "apropos"))
    ecrit("contact.html", page_simple("Contact — Qibla", "Contactez l'équipe éditoriale de Qibla : corrections, photos, partenariats.",
        "Contact", "Écrivez-nous", CONTACT, "contact.html", "contact"))
    ecrit("credits-photos.html", page_simple("Crédits images — sources et licences | Qibla",
        "Traçabilité complète des images du site : créations originales, sources et licences, et procédure pour ajouter des photographies.",
        "Crédits images", "Traçabilité", CREDITS_HTML, "credits-photos.html"))
    ecrit("mentions-legales.html", page_simple("Mentions légales — Qibla", "Mentions légales du site Qibla.",
        "Mentions légales", "Informations légales", MENTIONS, "mentions-legales.html"))
    ecrit("confidentialite.html", page_simple("Politique de confidentialité — Qibla",
        "Politique de confidentialité et RGPD : données, cookies, newsletter, vos droits.",
        "Politique de confidentialité", "Vos données", CONFID, "confidentialite.html"))
    ecrit("cgu.html", page_simple("Conditions générales d'utilisation — Qibla", "CGU du site Qibla : commentaires, contenus, affiliation.",
        "Conditions générales d'utilisation", "Règles du site", CGU, "cgu.html"))

    # sitemap + robots + crédits + README
    urls = ["", "mosquees.html", "blog.html", "quiz.html", "boussole.html", "a-propos.html", "contact.html", "credits-photos.html",
            "mentions-legales.html", "confidentialite.html", "cgu.html"] + \
           [f"mosquees/{m['slug']}/" for m in MOSQUEES] + \
           [f"blog/{a['slug']}/" for a in ARTICLES]
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + \
        "".join(f"  <url><loc>{SITE_URL}/{u}</loc><changefreq>monthly</changefreq></url>\n" for u in urls) + "</urlset>\n"
    ecrit("sitemap.xml", sitemap)
    ecrit("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n")
    ecrit("credits-photos.md", credits_md())
    ecrit("README.md", README)
    print("Site généré :", DIST)

if __name__ == "__main__":
    main()
