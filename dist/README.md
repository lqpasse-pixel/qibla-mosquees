# Qibla — Les 28 plus belles mosquées du monde

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
4. Vérification finale : `grep -rE "https?://[^\"]*(unsplash|pexels|wikimedia|pixabay)" dist/` ne doit rien retourner.

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
- **Newsletter** : le formulaire `#form-nl` est déjà relié à Netlify Forms (détection statique + soumission AJAX dans `site.js`) et les inscriptions arrivent dans Site settings → Forms sur app.netlify.com. La section est actuellement masquée (`hidden` sur la `<section class="wrap nl">` dans `build.py`) tant qu'aucune newsletter n'est réellement envoyée aux abonnés — retirez l'attribut `hidden` pour la republier.
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
