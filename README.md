# Qibla — Les 20 plus belles mosquées du monde

Site statique complet, en français, sans aucune dépendance externe au runtime (100 % autonome, fonctionne hors ligne).

## Lancer en local
Ouvrez `index.html` dans un navigateur, ou servez le dossier :
```bash
cd dist && python3 -m http.server 8000
```

## Déployer
- **Netlify / Vercel / Cloudflare Pages** : glissez-déposez le dossier `dist/` (aucun build requis).
- **Hébergement classique** : envoyez le contenu de `dist/` à la racine via FTP/SFTP.
- Remplacez ensuite `https://www.exemple-mosquees.fr` par votre domaine dans `sitemap.xml`, `robots.txt` et les balises canoniques (rechercher-remplacer global), ou relancez `python3 build.py` après avoir modifié `SITE_URL`.

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
Un système de démonstration (localStorage, likes, anti-spam) est actif. Pour de vraies discussions partagées :
1. Créez un dépôt GitHub public avec Discussions activées.
2. Configurez https://giscus.app (catégorie, langue `fr`), copiez le `<script>` généré.
3. Collez-le à la place du bloc `#zone-commentaires` dans le template `page_detail` de `build.py`, puis régénérez.

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

<!-- déploiement continu Netlify testé le 2026-07-05 23:27 -->
