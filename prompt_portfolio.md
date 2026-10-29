# Prompt à donner à l'IA : développement complet d'un portfolio professionnel (Astro + Flask + DevOps)

> Copie tout le contenu ci-dessous (à partir de « RÔLE ») et colle-le dans l'IA de ton choix. Remplace les valeurs entre `[crochets]` avant de l'envoyer.

---

## RÔLE

Tu es un ingénieur logiciel senior full-stack et DevOps. Tu m'accompagnes pour concevoir, développer, tester et déployer mon portfolio professionnel. Tu écris du code propre, commenté, sécurisé et prêt pour la production. Tu expliques brièvement tes choix techniques.

## CONTEXTE

-   Je suis étudiant ingénieur en développement digital et systèmes d'information.
-   Je possède un **VPS** Ubuntu 24.04 et un nom de domaine \[hosayni.com\].
-   Je veux un portfolio **professionnel, très bien référencé (SEO)**, rapide, bilingue **français / anglais**, qui met aussi en valeur mes compétences **DevOps**.
-   Le code est hébergé sur **GitHub**, et le déploiement est **automatisé avec GitHub Actions** (CI/CD) vers mon VPS.
-   Mes informations : nom \[Mohamed Hosayni\], titre \[Ingénieur en développement digital et system d informations\], email hosayni92@gmail.com, GitHub https://github.com/hosayni/ , LinkedIn \[linkedin/hosayni.
-   Mes projets à présenter (exemples) : \[Smart Farm IoT (plateforme d'irrigation IoT), plateforme LMS avec évaluation adaptative, autres...a ajouetr plustard\].

## OBJECTIF

Livrer un dépôt GitHub complet, documenté, avec un pipeline CI/CD fonctionnel, déployable sur mon VPS en HTTPS.

## STACK IMPOSÉE

| Couche | Technologie |
| --- | --- |
| Frontend (site public) | **Astro** (dernière version stable) + **TypeScript strict** + **Tailwind CSS** |
| Backend (petite API) | **Python 3.12 + Flask** (gunicorn en production) |
| Conteneurisation | **Docker** + **Docker Compose** (images multi-stage) |
| Reverse proxy / HTTPS | **Caddy** (certificats Let's Encrypt automatiques) |
| CI/CD | **GitHub Actions** + **GitHub Container Registry (ghcr.io)** |
| Qualité | ESLint, Prettier, `astro check`, Ruff, Pytest, Playwright (E2E basique), Lighthouse CI |
| Monitoring | Uptime Kuma (conteneur optionnel) |

Si tu penses qu'un choix est mauvais, dis-le avant de coder et propose une alternative justifiée.

## ARCHITECTURE CIBLE

```
Internet → Caddy (80/443, HTTPS)
             ├── /        → conteneur "web"  (nginx:alpine servant le build statique Astro)
             └── /api/*   → conteneur "api"  (Flask + gunicorn, port interne 8000)
```

Structure de dépôt (monorepo) :

```
portfolio/
├── web/                 # Astro
│   ├── src/
│   │   ├── components/
│   │   ├── layouts/     # BaseLayout.astro (SEO)
│   │   ├── pages/       # fr/ et en/
│   │   ├── content/     # projets et articles en Markdown/MDX (content collections)
│   │   ├── i18n/        # dictionnaires fr.json / en.json
│   │   └── styles/
│   ├── public/          # robots.txt, favicon, cv.pdf, og-image
│   ├── astro.config.mjs
│   ├── Dockerfile
│   └── package.json
├── api/                 # Flask
│   ├── app/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── services/    # github.py, mail.py
│   │   └── config.py
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
├── deploy/
│   ├── docker-compose.prod.yml
│   ├── Caddyfile
│   └── .env.example
├── .github/
│   ├── workflows/ci.yml
│   ├── workflows/deploy.yml
│   ├── dependabot.yml
│   └── pull_request_template.md
├── docker-compose.yml   # développement local
├── README.md
└── docs/DEPLOIEMENT.md
```

## FONCTIONNALITÉS DU SITE

### Pages et sections

1.  **Accueil** : présentation, photo, accroche, boutons (voir projets, contacter, télécharger le CV).
2.  **Projets** : grille filtrable par technologie ; chaque projet a une **page détaillée** (contexte, problème, architecture avec schéma, stack, difficultés rencontrées, résultats, captures, liens démo et GitHub).
3.  **Compétences** regroupées (Backend, Frontend, DevOps, IoT, Bases de données, Outils).
4.  **Parcours** : formation, expériences, certifications (timeline).
5.  **Blog technique** en Markdown/MDX (tags, temps de lecture, table des matières, coloration syntaxique, flux RSS).
6.  **Contact** : formulaire (nom, email, message) avec validation, **honeypot anti-spam**, limitation de débit, confirmation visuelle.
7.  **Page « Infrastructure »** : schéma du pipeline CI/CD et de l'architecture, avec badges (statut du workflow GitHub Actions, uptime).
8.  Pages **404** et **mentions légales / confidentialité**.

### Fonctionnalités transverses

-   **Bilingue FR/EN** : routage `/fr/` et `/en/`, sélecteur de langue, balises `hreflang`, détection douce de la langue.
-   **Mode sombre / clair** (préférence système + bouton, sans flash au chargement).
-   Design **responsive mobile-first**, **accessible** (WCAG AA : contrastes, navigation clavier, `aria-*`, `prefers-reduced-motion`).
-   Animations légères (apparition au scroll) sans bibliothèque lourde.
-   **Projets GitHub dynamiques** : l'API Flask récupère mes dépôts épinglés ou sélectionnés via l'API GitHub, avec **cache** (ex. 1 h) ; le site fonctionne même si l'API est indisponible (contenu de repli statique).
-   **Analytics respectueux de la vie privée** (Plausible ou Umami, auto-hébergé), sans bannière de cookies si possible.

## API FLASK

Endpoints :

-   `GET /api/health` : retourne `{"status":"ok","version":"..."}` (utilisé par les healthchecks Docker et le monitoring).
-   `GET /api/projects` : liste de dépôts GitHub (nom, description, langages, étoiles, dernière mise à jour, URL), avec cache.
-   `POST /api/contact` : valide (email, longueur du message), rejette si le honeypot est rempli, applique un **rate limiting** (Flask-Limiter), envoie l'email via SMTP (variables d'environnement) et répond en JSON.

Exigences : application factory, configuration par variables d'environnement, CORS restreint à mon domaine, en-têtes de sécurité, gestion d'erreurs JSON propre, logs structurés, aucun secret dans le code, tests Pytest (≥ 80 % de couverture sur les routes).

## EXIGENCES SEO (prioritaires)

-   Composant `BaseLayout.astro` avec : `<title>` et meta description uniques, balise **canonical**, **Open Graph**, **Twitter Cards**, `hreflang`, `lang` sur `<html>`.
-   **Données structurées JSON-LD** : `Person` (accueil), `CreativeWork`/`SoftwareSourceCode` (projets), `BlogPosting` (articles), `BreadcrumbList`.
-   `sitemap.xml` (`@astrojs/sitemap`), `robots.txt`, flux RSS du blog.
-   URLs propres, un seul `<h1>` par page, hiérarchie de titres cohérente.
-   Images optimisées (`astro:assets`, WebP/AVIF, `width`/`height`, lazy loading, `alt` pertinents), polices auto-hébergées avec `font-display: swap`.
-   Objectif Lighthouse **≥ 95** (Performance, Accessibilité, Bonnes pratiques, SEO) ; Core Web Vitals verts.
-   Compression (Brotli/gzip) et cache longue durée sur les assets fingerprintés, via Caddy/nginx.

## DOCKER

-   `web/Dockerfile` : multi-stage (build `node:22-alpine` → servir avec `nginx:alpine`), utilisateur non-root si possible, config nginx avec cache et en-têtes.
-   `api/Dockerfile` : `python:3.12-slim`, dépendances figées, utilisateur non-root, gunicorn, `HEALTHCHECK`.
-   `docker-compose.yml` (dev) avec rechargement à chaud ; `deploy/docker-compose.prod.yml` (images tirées depuis ghcr.io, `restart: unless-stopped`, réseau interne, healthchecks, limites de ressources, volumes pour les données Caddy).
-   `.dockerignore` soignés.

## CI/CD GITHUB ACTIONS

### `ci.yml` : sur chaque pull request et push (hors main)

-   Job **web** : `npm ci` (avec cache), ESLint, Prettier check, `astro check`, build, tests Playwright basiques.
-   Job **api** : Python 3.12, installation avec cache pip, Ruff, Pytest avec couverture.
-   Job **lighthouse** : Lighthouse CI sur le build avec seuils de score.
-   Job **sécurité** : CodeQL, `npm audit`, `pip-audit`.
-   Les jobs indépendants tournent en parallèle ; `concurrency` pour annuler les exécutions obsolètes.

### `deploy.yml` : sur push vers `main` (après CI verte)

1.  Construire les images `web` et `api` avec `docker/build-push-action` (cache GitHub Actions) et les pousser sur **ghcr.io** avec les tags `latest` et le SHA du commit.
2.  Se connecter au VPS en **SSH** (clé dédiée stockée dans les GitHub Secrets), copier `deploy/` si nécessaire, exécuter `docker compose pull && docker compose up -d`.
3.  Vérifier un **healthcheck** (`curl` sur `/api/health` et la page d'accueil) ; en cas d'échec, **rollback** vers l'image précédente.
4.  Nettoyer les anciennes images (`docker image prune`).
5.  Utiliser un **environment** GitHub « production ».

Autres : `dependabot.yml` (npm, pip, docker, github-actions), protection de la branche `main` (PR obligatoire, CI verte), commits conventionnels.

## SÉCURITÉ ET VPS

Fournis aussi un guide de durcissement du VPS : utilisateur non-root avec sudo, authentification SSH par clé uniquement (mot de passe et root désactivés), **UFW** (22, 80, 443), **Fail2ban**, mises à jour automatiques (`unattended-upgrades`), installation de Docker, gestion des secrets (`.env` hors dépôt, permissions 600), sauvegardes.

## MÉTHODE DE TRAVAIL (important)

1.  **Avant de coder**, pose-moi au maximum 5 questions de clarification si une information manque, puis propose un plan en étapes numérotées.
2.  Avance **étape par étape** : après chaque étape, donne les fichiers complets (chemin + contenu), les commandes à exécuter et comment vérifier que ça marche. Attends mon « ok » avant de passer à l'étape suivante.
3.  Étapes attendues : (1) initialisation du dépôt et de la structure, (2) frontend Astro de base + layout SEO + i18n, (3) pages et contenu, (4) API Flask + tests, (5) Dockerisation, (6) CI, (7) CD + préparation du VPS, (8) optimisation SEO/performance, (9) monitoring, (10) documentation.
4.  Donne le **code complet** des fichiers (pas de « ... » ni de « le reste est identique »).
5.  Utilise des **versions actuelles et stables** des dépendances ; signale tout ce que tu n'es pas sûr d'avoir à jour.
6.  Indique clairement chaque **commande destinée au VPS** et chaque **secret à créer dans GitHub**.
7.  Le contenu textuel (présentation, descriptions) est à écrire avec des placeholders `[À COMPLÉTER]` que je remplirai.

## LIVRABLES FINAUX

-   Dépôt complet fonctionnel en local (`docker compose up`) et en production.
-   `README.md` clair (présentation, stack, lancement local, structure, déploiement) avec badges CI.
-   `docs/DEPLOIEMENT.md` : procédure complète de mise en production et de rollback.
-   Checklist finale : HTTPS actif, redirection www → non-www, sitemap soumis à Google Search Console, scores Lighthouse, tests au vert.

## CONTRAINTES

-   Gratuit ou open source uniquement (hors VPS et domaine déjà achetés).
-   Pas de secrets, mots de passe ou clés dans le code ou dans l'historique Git.
-   Code lisible, structuré, commenté en français ou en anglais de façon cohérente.
-   Priorité : **SEO, performance, sécurité, maintenabilité**.

Commence par me poser tes questions de clarification, puis propose le plan d'ensemble.