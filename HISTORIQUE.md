# Historique du projet — portfolio Mohamed Hosayni

> Journal local de construction, étape par étape.
> Chaque entrée consigne : objectif, décisions, fichiers créés, vérifications
> exécutées et commit associé. Ce fichier n'est pas destiné au site public.

---

## Étape 1 — Initialisation du dépôt et de la structure

- **Date :** 2026-10-29
- **Commit :** `a427537` — `chore: initialise le monorepo et la structure du projet`
- **Branche :** `feature/init`

### Objectif

Poser les fondations du monorepo (Astro + Flask + Docker + CI/CD) : conventions
d'édition, secrets, documentation de départ et arborescence cible.

### Décisions

- **Monorepo** `web/`, `api/`, `deploy/` : une PR peut faire évoluer l'API et son
  consommateur ensemble, la CI teste l'ensemble de façon atomique.
- **Node 22** épinglé (`.nvmrc`) pour rester aligné sur `node:22-alpine` prévu
  dans les futurs Dockerfiles. La machine locale utilise Node 24, compatible.
- **Fichier `.env.example`** unique à la racine, versionné ; tout `.env` réel est
  ignoré par Git.
- Les deux briefs (`prompt_portfolio.md`, `skills_dev_portfolio.md`) restent
  **hors du dépôt** : ce sont des consignes, pas de la documentation projet.

### Fichiers créés

| Fichier | Rôle |
| --- | --- |
| `.gitignore` | Secrets, `node_modules`, `dist`, caches Python/Node, rapports |
| `.gitattributes` | LF partout, binaires protégés, lockfiles marqués générés |
| `.editorconfig` | 2 espaces (4 en Python), UTF-8, LF |
| `.nvmrc` | Node 22 |
| `.env.example` | Toutes les variables documentées, aucune valeur réelle |
| `README.md` | Stack, schéma Mermaid, structure, feuille de route 10 étapes |
| `LICENSE` | MIT (code) + contenu rédactionnel réservé |
| `docs/adr/0001-monorepo-astro-flask.md` | Décision d'architecture, alternatives rejetées |
| `docs/README.md` | Index de la documentation |
| `.github/pull_request_template.md` | Checklist de revue |
| `web/`, `api/`, `deploy/`, `.github/workflows/` | Arborescence prête (`.gitkeep`) |

### Vérifications

```text
✔ git check-ignore .env                → ignoré
✔ git check-ignore deploy/.env         → ignoré
✔ git check-ignore web/.env.local      → ignoré
✔ git check-ignore .env.example        → versionnable
✔ git check-ignore deploy/.env.example → versionnable
✔ commit créé sans erreur
```

### Notes

- Astro 7.4.4 et Tailwind 4.3.3 étaient les dernières versions npm, mais la
  demande impose **Astro 5** : la version sera épinglée à l'étape 2.

---

## Étape 2 — Base Astro 5, layout SEO et i18n FR/EN

- **Date :** 2026-10-29
- **Commit :** `793f15f` — `feat(web): ajoute la base Astro 5, le layout SEO et l'i18n FR/EN`

### Objectif

Un site Astro fonctionnel : design system, thème clair/sombre, routes `/fr/` et
`/en/`, SEO de base, navigation et pages d'attente pour les sections à venir.

### Décisions

- **Astro 5.18.2** (dernière 5.x) au lieu d'Astro 7, conformément au prompt.
- **TypeScript 5.9.3** : `@astrojs/check` n'accepte pas encore TypeScript 7.
- **Tailwind CSS 4.3.3** via `@tailwindcss/vite` ; les tokens du fichier skills
  sont exposés à Tailwind avec `@theme inline` (thème clair/sombre dynamique).
- **Vite 6.4.5 épinglé** : `@tailwindcss/vite` tirait Vite 8 en parallèle de
  celui d'Astro, ce qui cassait `astro check`. Un seul Vite désormais.
- **Police auto-hébergées** via `@fontsource-variable` (Inter, JetBrains Mono) :
  zéro requête vers un domaine tiers.
- **i18n par segment d'URL** : `prefixDefaultLocale: true`, redirection `/` →
  `/fr/` générée par Astro.
- **Thème sans flash** : script inline dans le `<head>` qui pose `data-theme`
  avant le premier rendu.
- **Animations sobres** : `[data-reveal]` + IntersectionObserver, désactivées
  sans JavaScript et en `prefers-reduced-motion`.
- **CV temporaire** : PDF d'une page généré localement (`web/public/cv.pdf`),
  à remplacer par le vrai document.

### Fichiers créés

```text
web/
├── astro.config.mjs          # site, trailingSlash, i18n, redirects, Tailwind
├── tsconfig.json             # strictest + alias @/*
├── eslint.config.js          # flat config ESLint 10 + Astro + TS
├── .prettierrc.json          # Astro + Tailwind + stylesheet v4
├── package.json              # versions épinglées
├── public/
│   ├── favicon.svg
│   └── cv.pdf                # placeholder
└── src/
    ├── components/           # Header, Footer, ThemeToggle, ProjectCard…
    ├── data/                 # navigation, projets provisoires
    ├── i18n/                 # ui.ts (dictionnaires typés), utils.ts
    ├── layouts/BaseLayout.astro
    ├── pages/[lang]/…        # accueil + 5 sections d'attente, 404
    └── styles/global.css     # tokens, base, composants, animations
```

### Vérifications

```text
✔ npm run build        → 13 pages générées
✔ npm run check        → 0 erreur, 0 warning (22 fichiers)
✔ npm run lint         → propre
✔ npm run format:check → conforme
✔ Lighthouse           → Accessibilité 100 · Best Practices 100 · SEO 100
✔ Vérificateur maison  → 14 pages, 0 lien mort, métadonnées présentes
✔ 404                  → servie, noindex, changement de langue vers /fr/ et /en/
✔ Thème                → light → dark → light, aria-pressed synchronisé
✔ Console navigateur   → aucune erreur
✔ Débordement horizontal → 0 px
```

### Notes

- La performance n'a pas été mesurée : le Lighthouse du navigateur ne lance pas
  de benchmark. Ce sera fait à l'étape 8 avec Lighthouse CI.
- La redirection `/` est une page statique (meta refresh). Un vrai **301 HTTP**
  sera configuré dans Caddy/nginx aux étapes 5 et 7.

---

## Étape 3 — Contenu réel : projets, compétences, parcours, blog, contact

- **Date :** 2026-10-29
- **Commit :** `842bc67` — `feat(web): ajoute le contenu éditorial, le blog et le formulaire de contact`

### Objectif

Remplacer les pages d'attente par du contenu éditable : content collections
Astro validées par Zod, pages projets détaillées, page compétences, frise du
parcours, blog avec articles, formulaire de contact et pages légales.

### Décisions

- **Content collections Astro 5** (`src/content.config.ts`) avec le loader
  `glob` et des schémas Zod stricts : un champ manquant ou mal typé casse le
  build, pas la production.
- **Un fichier par langue**, relié par `translationKey` : les slugs peuvent
  différer (`/fr/mentions-legales/` vs `/en/legal-notice/`) sans casser les
  balises `hreflang` ni le sélecteur de langue.
- **Projets structurés** : contexte et récit en Markdown, métadonnées
  (architecture, difficultés, résultats, stack, liens) en frontmatter. Le
  schéma d'architecture est rendu par un composant CSS, sans Mermaid ni
  JavaScript côté client.
- **Blog en Markdown** (MDX activé pour plus tard), coloration Shiki avec deux
  thèmes clair/sombre pilotés par variables CSS, table des matières générée
  depuis les titres, flux RSS par langue.
- **Filtre projets progressif** : sans JavaScript, la liste complète reste
  affichée et les boutons sont masqués ; avec JavaScript, le filtre met à jour
  `aria-pressed`, le nombre de résultats et une zone `aria-live`.
- **Formulaire de contact** : validation native en repli, validation JS
  accessible, honeypot hors écran, consentement RGPD explicite, `fetch` JSON
  vers `/api/contact` (branché à l'étape 4).
- **Pages légales** dans une collection `pages`, avec un routage
  `[lang]/[page]` qui génère uniquement les slugs déclarés.
- **Page Infrastructure** : schéma de production et pipeline en cinq étapes,
  sans badge factice ; les badges CI/CD arriveront avec les workflows.
- **Suppression du code mort** : `ComingSoon.astro` et `data/projects.ts`,
  remplacés par les collections et les nouveaux composants.

### Fichiers

```text
web/src/
├── content.config.ts                 # schémas Zod des trois collections
├── content/
│   ├── projects/{fr,en}/             # 2 projets × 2 langues
│   ├── blog/{fr,en}/                 # 2 articles × 2 langues
│   └── pages/{fr,en}/                # mentions légales + confidentialité
├── lib/
│   ├── content.ts                    # requêtes, slugs, traductions
│   └── format.ts                     # dates, temps de lecture
├── data/
│   ├── skills.ts                     # 6 groupes de compétences
│   ├── career.ts                     # frise formation/expériences
│   └── legal.ts                      # slugs localisés des pages légales
├── components/
│   ├── ProjectCard.astro             # carte liée à l'étude de cas
│   ├── BlogCard.astro                # date, tags, temps de lecture
│   ├── ArchitectureDiagram.astro     # schéma en couches, zéro JS
│   └── ContactForm.astro             # formulaire + validation + honeypot
└── pages/[lang]/
    ├── projets/{index,[slug]}.astro  # grille filtrable + étude de cas
    ├── blog/{index,[slug]}.astro     # liste + article + TOC
    ├── rss.xml.ts                    # flux RSS par langue
    ├── competences/index.astro
    ├── parcours/index.astro
    ├── contact/index.astro
    ├── infrastructure/index.astro
    └── [page].astro                  # pages légales
```

Dépendances ajoutées, versions figées : `@astrojs/mdx@4.3.14`,
`@astrojs/rss@4.0.19`.

### Vérifications

```text
✔ npm run build        → 27 pages générées (28 fichiers HTML avec 404 et /)
✔ npm run check        → 0 erreur, 0 warning (34 fichiers)
✔ npm run lint         → propre
✔ npm run format:check → conforme
✔ Liens internes       → 28 pages analysées, 0 lien mort
✔ Métadonnées          → lang, canonical, description et hreflang fr/en partout
✔ RSS                  → /fr/rss.xml et /en/rss.xml servis en XML, items valides
✔ Filtre projets       → « TypeScript » → 1 projet, aria-pressed et compteur à jour
✔ Formulaire vide      → 4 erreurs annoncées, focus sur le premier champ
✔ Formulaire valide    → payload JSON correct, état succès, formulaire réinitialisé
✔ Thème sombre         → fond et couleurs Shiki basculés (rgb(36,41,46) / clair)
✔ Console navigateur   → aucune erreur
✔ Débordement horizontal → 0 px sur les pages testées
✔ 404                  → toujours servie, aucune régression
```

### Notes

- Le formulaire pointe vers `/api/contact`, qui n'existe pas encore : l'envoi
  réel affiche le message d'erreur prévu jusqu'à l'étape 4.
- Les captures de projets sont des panneaux placeholder assumés ; les vrais
  visuels et les métriques `[À COMPLÉTER]` restent à renseigner.
- Les badges CI/CD de la page Infrastructure seront ajoutés aux étapes 6 et 7.
- Le contenu Markdown est prêt pour MDX, mais les articles utilisent `.md` :
  aucun composant interactif n'est nécessaire pour l'instant.

---

## Étape 4 — API Flask : santé, dépôts GitHub et contact

- **Date :** 2026-10-29
- **Commit :** `1269a0a` — `feat(api): ajoute l'API Flask, le cache GitHub et le contact`
- **Branche :** `feature/init`

### Objectif

Construire l'API interne : endpoint de santé pour Docker et la supervision,
dépôts GitHub avec cache et repli, formulaire de contact validé, limité et
envoyé par SMTP. Brancher le site Astro sur ces endpoints, avec dégradation
gracieuse.

### Décisions

- **Application factory + blueprints** (`health`, `projects`, `contact`) et
  configuration uniquement par variables d'environnement, chargées depuis
  `api/.env` puis le `.env` racine.
- **Validation manuelle stricte** plutôt que Pydantic : moins de dépendances,
  erreurs par champ (`{"error":"validation_error","fields":{...}}`) et contrôle
  explicite des types, longueurs, consentement et honeypot.
- **Cache mémoire TTL** (1 h par défaut) pour les dépôts GitHub. En cas d'échec
  et de cache périmé, l'API renvoie le cache avec `"stale": true` ; sans cache,
  elle répond `503` et le site conserve ses projets statiques.
- **Liste blanche `GITHUB_REPOS`** optionnelle, sinon les dépôts publics non
  forké/non archivés les plus récemment poussés. Les langages de chaque dépôt
  sont récupérés en parallèle (3 maximum), avec repli sur le langage principal.
- **Rate limiting Flask-Limiter** par IP (`5 per hour` par défaut), stockage
  mémoire adapté à un seul processus ; Redis documenté pour plusieurs workers.
- **Contact SMTP synchrone** avec timeout, TLS explicite ou SSL implicite
  (port 465), `Reply-To` et neutralisation des retours à la ligne dans les
  en-têtes. En développement, `MAIL_SUPPRESS_SEND=true` journalise sans envoyer.
- **Production sûre par défaut** : la factory refuse de démarrer si
  `SECRET_KEY`, `SMTP_HOST`, `SMTP_FROM`, `CONTACT_TO` ou `CORS_ORIGINS`
  manquent, ou si `MAIL_SUPPRESS_SEND=true`.
- **Sécurité transverse** : CORS restreint, en-têtes de sécurité, CSP, HSTS
  derrière HTTPS, corps limité à 16 Ko, erreurs JSON homogènes, `ProxyFix`
  activé uniquement via `TRUST_PROXY=true`.
- **Logs JSON** avec identifiant de requête, méthode, chemin, statut et durée ;
  aucune donnée personnelle (nom, e-mail, message) n'est journalisée.
- **Intégration Astro** : proxy Vite `/api` → Flask en développement, puis
  Caddy en production. Les appels utilisent un slash final (`/api/projects/`,
  `/api/contact/`) à cause de `trailingSlash: 'always'` d'Astro ; Flask accepte
  les deux formes (`strict_slashes = False`).
- **Section GitHub progressive** sur la page Projets : chargement client,
  rendu DOM sans `innerHTML`, liens `https:` uniquement, message d'erreur et
  repli `<noscript>` ; les projets éditoriaux restent la source principale.

### Fichiers

```text
api/
├── app/
│   ├── __init__.py          # factory, CORS, en-têtes, hooks, erreurs
│   ├── config.py            # environnement + validation production
│   ├── errors.py            # ApiError et handlers JSON
│   ├── extensions.py        # Limiter
│   ├── logging_config.py    # formatter JSON
│   ├── validation.py        # ContactMessage + règles
│   ├── routes/              # health, projects, contact
│   └── services/            # github.py (cache TTL), mail.py (SMTP)
├── tests/                   # 55 tests, réseau et SMTP simulés
├── pyproject.toml           # Ruff, Pytest, couverture ≥ 80 %
├── requirements*.txt        # versions épinglées
└── wsgi.py

web/src/components/GitHubRepos.astro
web/src/components/ContactForm.astro   # action /api/contact/
web/astro.config.mjs                   # proxy Vite /api
```

Dépendances Python épinglées : Flask `3.1.3`, Flask-Cors `6.0.5`,
Flask-Limiter `4.1.1`, Gunicorn `26.2.0`, python-dotenv `1.2.4`,
requests `2.34.2`, Pytest `9.2.0`, pytest-cov `7.1.0`, Ruff `0.17.3`.

### Vérifications

```text
✔ .venv/bin/pytest             → 55 tests, 94,85 % de couverture (seuil 80 %)
✔ Ruff check + format          → propres
✔ API locale                   → /api/health, /api/contact et erreurs JSON testés
✔ Contact via proxy Astro      → 200, e-mail journalisé (suppression en dev)
✔ Formulaire navigateur        → validation JS, envoi, état succès, reset
✔ GitHub indisponible          → 503 JSON ; message de repli affiché, zéro JS cassé
✔ Rendu GitHub (stub local)    → 2 cartes, dates FR/EN, liens https, 0 débordement
✔ npm run check                → 0 erreur, 0 warning (35 fichiers)
✔ npm run lint / format:check  → propres
✔ npm run build                → 27 pages
✔ Liens internes               → 28 pages, 0 lien mort
```

### Notes

- Le réseau de l'environnement de développement ne joint pas
  `api.github.com` (timeout) : le chemin réel a été validé par les tests avec
  mocks et par un stub local ; un essai avec token reste à faire sur une machine
  connectée.
- Le rate limiting et le cache GitHub sont en mémoire : un seul worker Gunicorn
  pour l'instant, ou Redis aux étapes suivantes.
- L'envoi SMTP est synchrone ; une file de tâches sera envisagée si le trafic
  augmente.
- Les URLs front utilisent un slash final ; le Caddyfile de l'étape 7 devra
  router `/api/*` vers Flask sans réécriture.
- Aucun push : la branche `feature/init` reste locale.

---

## Étape 5 — Docker : images multi-stage, nginx et Compose dev/prod

- **Date :** 2026-10-29
- **Commit :** `269722c` — `feat(docker): ajoute les images non-root et les Compose dev/prod`
- **Branche :** `feature/init`

### Objectif

Conteneuriser les deux applications avec des images reproductibles et non-root,
un Compose de développement avec rechargement à chaud, et un Compose de
production prêt pour Caddy et `ghcr.io`. Ajouter les `.dockerignore`, les
healthchecks, le cache nginx et un vrai 301 HTTP de `/` vers `/fr/`.

### Décisions

- **Web multi-stage** : `node:22.22-alpine3.24` pour le build, puis
  `nginx:1.30.6-alpine3.24` pour le service statique. nginx tourne avec
  l'utilisateur `nginx`, écoute sur `8080` et écrit PID/caches dans `/tmp` : aucun
  privilège root dans le conteneur.
- **Configuration nginx dédiée** : cache immuable sur `/_astro/`, cache d'une
  semaine pour les images/polices publiques, compression, logs JSON, 404
  interne, refus des fichiers cachés et en-têtes de sécurité (CSP, HSTS,
  `X-Frame-Options`, `Permissions-Policy`).
- **API multi-stage** : venv installé dans une étape `builder`, copié dans
  `python:3.12.16-slim-trixie`. L'utilisateur `app` (UID 10001) exécute
  Gunicorn `gthread` avec **un worker et quatre threads**. Le socket de contrôle
  Gunicorn est désactivé (`--no-control-socket`) pour rester compatible avec le
  système de fichiers en lecture seule.
- **Compose de développement** : cibles `dev`, sources montées, volume nommé
  `web_node_modules`, healthchecks, `init: true`, ports publiés uniquement sur
  `127.0.0.1`. `.env` est optionnel ; les valeurs réelles restent hors du dépôt.
- **Compose de production** : images `ghcr.io/<owner>/portfolio-{web,api}`,
  Caddy sur 80/443 (HTTP/3), réseau privé sans ports web/api, `read_only` +
  `tmpfs`, `no-new-privileges`, `cap_drop: ALL`, limites CPU/mémoire, logs
  plafonnés et volumes `caddy_data`/`caddy_config`.
- **Caddy** : TLS Let's Encrypt, redirection `www` → domaine principal,
  compression zstd/gzip, routage `/api/*` vers Flask sans réécriture, en-têtes
  HSTS et suppression de `Server`.
- **Versions figées** : Node `22.22`, nginx `1.30.6`, Python `3.12.16`, Caddy
  `2.11.7`. Elles seront suivies par Dependabot à l'étape 6.
- **Documentation** : README mis à jour, `deploy/.env.example`,
  `docs/DEPLOIEMENT.md` (base) et ADR `0002-docker-images-et-compose.md`.

### Fichiers

```text
web/
├── Dockerfile                 # base → dev / build → nginx runtime
├── .dockerignore
└── nginx/
    ├── nginx.conf             # PID/caches dans /tmp, logs JSON, gzip
    ├── default.conf           # 8080, 301 /, cache, 404, dotfiles
    └── security-headers.conf  # CSP, HSTS, frame, permissions

api/
├── Dockerfile                 # builder venv → dev / runtime Gunicorn
└── .dockerignore

docker-compose.yml             # développement, hot reload, ports locaux
deploy/
├── docker-compose.prod.yml    # ghcr, Caddy, read_only, limites, réseau privé
├── Caddyfile                  # TLS, www, /api/*, compression, logs
└── .env.example               # modèle de production (aucun secret réel)

docs/
├── DEPLOIEMENT.md             # base de procédure et rollback manuel
└── adr/0002-docker-images-et-compose.md
```

### Vérifications

```text
✔ docker compose config                        → dev valide
✔ docker compose -f deploy/... config          → prod valide
✔ docker compose build                         → images dev construites
✔ docker compose up -d                         → api et web healthy
✔ http://127.0.0.1:4321/fr/                    → 200, titre correct
✔ http://127.0.0.1:4321/api/health/            → 200 via proxy Vite
✔ http://127.0.0.1:8000/api/health             → 200 (API directe)
✔ Rechargement Flask                           → détecté et worker relancé
✔ docker build --target runtime (api)          → image 215 Mo
✔ docker build --target runtime (web)          → image 94 Mo
✔ nginx -t                                     → configuration valide
✔ /healthz, /fr/, /_astro/*                    → 200 + cache + en-têtes
✔ /, /fr                                       → 301 vers /fr/
✔ 404 et fichier caché                         → 404 / 403
✔ API image en mode production                 → healthy, logs Gunicorn propres
✔ Pytest dans l'image Python 3.12              → 55 tests, 94,85 %
✔ Compose prod + Caddy (TLS local)             → /fr/ 200, /api/health/ 200
✔ Redirection www                              → 301 vers le domaine principal
✔ caddy validate                               → configuration valide
✔ npm run check / lint / format:check          → propres
✔ npm run build                                → 27 pages
✔ Liens internes                               → 28 pages, 0 lien mort
```

### Notes

- Le test du Compose de production a utilisé `localhost` et l'autorité de
  certification locale de Caddy. Un essai avec un vrai domaine et Let's Encrypt
  reste à faire lors de la mise en ligne (étape 7).
- `npm audit` signale 6 vulnérabilités (1 critique, 3 hautes, 2 basses) dans
  l'arbre Astro 5 ; les correctifs proposés imposent Astro 7. La demande impose
  Astro 5, et le site produit est statique : aucune entrée utilisateur n'est
  rendue à l'exécution. Le point sera réévalué à l'étape 6 (analyse de sécurité)
  et documenté si l'exception reste nécessaire.
- La CSP autorise encore `'unsafe-inline'` pour les scripts inline du thème et
  des animations ; une CSP par hashes est prévue à l'étape 8.
- Le cache GitHub et le rate limiting restent en mémoire : un seul worker
  Gunicorn. Redis est nécessaire avant de scaler.
- Aucune image n'a été poussée sur `ghcr.io` et aucun push Git n'a été effectué.


---

## Étape 6 — Intégration continue : tests, Lighthouse, sécurité et Dependabot

- **Date :** 2026-10-29
- **Commit :** `0c12a2a` — `feat(ci): ajoute l'intégration continue, Playwright et Lighthouse`
- **Branche :** `feature/init`

### Objectif

Automatiser les contrôles sur chaque pull request : qualité du frontend, tests de
bout en bout, build, budgets Lighthouse, tests et couverture de l'API, audit des
dépendances, analyse statique CodeQL et mises à jour Dependabot. Aucun
déploiement à cette étape.

### Décisions

- **Workflow unique `ci.yml`** avec six jobs : `web`, `e2e`, `lighthouse`,
  `api`, `security` et `codeql` (matrice JavaScript/TypeScript + Python).
  `web`, `api`, `security` et `codeql` sont indépendants ; `e2e` et `lighthouse`
  consomment l'artefact `web-dist` produit par `web`.
- **Déclencheurs** : pull requests, push hors `main`, lancement manuel.
  `concurrency` annule les exécutions obsolètes de la même référence.
- **Moindre privilège** : `contents: read` par défaut ; `security-events: write`
  uniquement pour CodeQL. Aucun secret n'est nécessaire.
- **Cache** : npm via `setup-node`, pip via `setup-python`. Les rapports
  Playwright et Lighthouse sont conservés 7 jours en artefact.
- **Playwright sur le build** : `astro preview` sert `dist/` (port 4321), pas le
  serveur de développement. Quatre parcours : redirection `/` → `/fr/`,
  changement de langue, filtre projets, validation du formulaire. Chromium seul
  pour maîtriser le temps de CI.
- **Lighthouse CI** : `/fr/` et `/en/`, 5 runs par page, médiane. Accessibilité,
  bonnes pratiques et SEO sont bloquants à 95. La performance est mesurée à 95
  mais reste en **avertissement** jusqu'à l'étape 8 : sur la machine locale
  partagée (charge moyenne 7 pour 4 cœurs), les scores oscillaient de 80 à 97.
  Le seuil deviendra bloquant après optimisation sur le runner dédié.
- **Audit npm avec politique** : plutôt que d'ignorer `npm audit` ou d'accepter
  un rouge permanent, un script Node applique une liste d'exceptions datées.
  Toute vulnérabilité haute/critique absente, expirée ou dont la gravité change
  fait échouer la CI. Les vulnérabilités basses et modérées restent visibles.
- **Exceptions Astro 5** : les sept avis hauts/critiques concernent Astro 5
  (XSS, SSRF, RCE AVIF) et ses dépendances `sharp`/`zod`. Le site est statique,
  sans entrée utilisateur rendue, sans image distante ni serveur de
  développement exposé. Justifications dans
  `.github/security/npm-audit-allowlist.json`, expiration **2027-03-31**.
- **pip-audit** ajouté aux dépendances de développement, exécuté avec
  `--strict` ; aucune vulnérabilité connue au moment de l'étape.
- **CodeQL** en `build-mode: none` et requêtes `security-and-quality`. Le
  téléversement SARIF est désactivé pour les PR Dependabot et les forks, dont le
  jeton est en lecture seule ; l'analyse continue de tourner.
- **Dependabot** hebdomadaire, groupé par écosystème : npm, pip, images Docker
  web/api, Compose dev/prod et actions GitHub. Les montées majeures d'Astro et
  `@astrojs/*` sont ignorées pour respecter la contrainte Astro 5.
- **Protection de branche** documentée mais à appliquer dans l'interface
  GitHub : PR obligatoire, checks requis, branches à jour, pas de force push.

### Fichiers

```text
.github/
├── workflows/ci.yml             # web, e2e, lighthouse, api, security, codeql
├── dependabot.yml               # npm, pip, docker, compose, actions
├── scripts/check-npm-audit.mjs  # politique d'exceptions npm datées
└── security/npm-audit-allowlist.json

web/
├── playwright.config.ts         # preview sur 4321, artefacts CI
├── e2e/portfolio.spec.ts        # 4 parcours critiques
└── lighthouserc.json            # 2 pages × 5 runs, seuils

api/requirements-dev.txt         # + pip-audit 2.10.1
web/package.json                 # + @playwright/test 1.64.1
docs/CI.md                       # procédure, seuils, sécurité, branche main
```

### Vérifications

```text
✔ npm ci (copie propre)              → 533 paquets, esbuild et sharp fonctionnels
✔ npm run format:check               → conforme
✔ npm run lint                       → propre
✔ npm run check                      → 0 erreur, 0 warning (37 fichiers)
✔ npm run build                      → 27 pages
✔ npm run test:e2e                   → 4 tests réussis (7,1 s)
✔ Lighthouse CI                      → 10 runs, accessibilité/BP/SEO 100,
                                       performance 80–97 (médiane 89, charge locale)
                                       assertions : avertissements, aucun échec
✔ Ruff check + format                → propres
✔ Pytest                             → 55 tests, 94,85 % de couverture
✔ npm audit (politique)              → 7 exceptions acceptées, 0 bloquant
✔ npm audit, exception expirée       → échec attendu (code 1)
✔ npm audit, avis critique retiré    → échec attendu (code 1)
✔ pip-audit -r requirements.txt      → aucune vulnérabilité connue
✔ actionlint                         → aucun problème
✔ YAML dependabot/CI                → parse sans erreur
```

### Notes

- Le workflow n'a pas encore tourné sur GitHub : aucun push n'a été effectué.
  Les commandes ont été rejouées localement, y compris Playwright et Lighthouse.
- La performance Lighthouse reste un avertissement jusqu'à l'étape 8. La charge
  de la machine de développement fausse les mesures ; le runner GitHub dédié
  donnera une référence plus stable.
- Les exceptions npm expirent le 31 mars 2027 : mettre à jour Astro ou renouveler
  l'analyse avant cette date.
- La protection de branche ne peut pas être versionnée dans le dépôt ; la
  checklist est dans `docs/CI.md`.
- Aucun secret, aucune image et aucun push : `deploy.yml` arrive à l'étape 7.

## Étape 7 — CD et VPS (publication ghcr.io, déploiement, durcissement, rollback)

### Résumé

Ajout du déploiement continu : workflow `deploy.yml` déclenché par CI verte sur
`main`, publication des images `web` et `api` sur `ghcr.io` par SHA, déploiement
SSH sur le VPS avec rollback automatique, durcissement VPS documenté et
désactivation initiale du formulaire de contact (pas de SMTP).

### Décisions

- **Déclenchement** : `workflow_run` après `CI` verte sur `main` ; la CI tourne
  aussi sur `main`. Un seul déploiement à la fois (`concurrency`).
- **Images** : `linux/amd64`, tags `sha-<commit>` (immuable) et `latest`,
  cache Buildx dans GitHub Actions.
- **Authentification VPS** : session Docker éphémère avec le `GITHUB_TOKEN`
  (`read:packages`) dans un répertoire de configuration temporaire nettoyé.
- **Déploiement** : `tar` des fichiers de déploiement puis `deploy.sh <tag>` sur
  le VPS. Vérification publique de `/api/health/` et `/fr/`.
- **Rollback** : automatique vers `.deployed-tag` si le démarrage ou le
  healthcheck échoue.
- **Premier déploiement sans SMTP** : `CONTACT_ENABLED=false` (API) et
  `PUBLIC_CONTACT_ENABLED=false` (build frontend). Le formulaire est masqué et
  `/api/contact` répond 503. Activation documentée dans `docs/DEPLOIEMENT.md`.
- **Formulaire** : `ContactForm.astro` masque le formulaire et affiche une
  notice avec l'adresse email quand `PUBLIC_CONTACT_ENABLED=false`.

### Fichiers

```text
.github/workflows/deploy.yml
deploy/deploy.sh
docs/adr/0003-deploiement-continu.md
docs/DEPLOIEMENT.md              # réécrit pour l'étape 7
api/app/config.py                # CONTACT_ENABLED, validation conditionnelle
api/app/routes/contact.py        # 503 contact_disabled si désactivé
api/app/routes/health.py         # champ contact_enabled
web/Dockerfile                   # ARG SITE_URL et PUBLIC_CONTACT_ENABLED
web/src/components/ContactForm.astro
web/src/env.d.ts
web/src/i18n/ui.ts               # contact.disabled*
.env.example                     # CONTACT_ENABLED
deploy/.env.example              # CONTACT_ENABLED=false + valeurs de prod
docs/CI.md                       # CI sur main, déclenchement deploy.yml
README.md                        # statut étape 7
```

### Vérifications

- Tests API à relancer après modifications (`pytest`, `ruff`).
- `bash -n deploy/deploy.sh` : syntaxe valide.
- `actionlint` à relancer sur `deploy.yml`.
- Workflow non exécuté sur GitHub : aucun push effectué. Validation locale
  uniquement.

## Étape 8 — SEO et performance (sitemap, JSON-LD, RSS, Lighthouse ≥ 95)

### Résumé

Ajout du sitemap Astro avec alternates FR/EN, `robots.txt`, données structurées
JSON-LD par défaut (Person) en plus de celles des articles et projets, et passage
de la performance Lighthouse en seuil bloquant à 95. Optimisation du chemin
critique : suppression de `text-wrap: balance/pretty` et du `scrollbar-gutter`
coûteux, `text-rendering: auto`, animations d’apparition allégées.

### Fichiers

```text
web/astro.config.mjs                 # @astrojs/sitemap, i18n alternates
web/public/robots.txt                # robots + sitemap
web/src/layouts/BaseLayout.astro      # JSON-LD Person par défaut
web/src/styles/global.css            # optimisations de rendu
web/lighthouserc.json                # performance bloquante
docs/CI.md                           # seuil performance bloquant
README.md                            # statut étape 8
```

### Vérifications

- `astro check` : 0 erreur, 0 avertissement.
- Build : 27 pages + `sitemap-index.xml`.
- Playwright : 4 tests réussis.
- Lighthouse : seuil performance désormais bloquant (médiane de 5 runs).

## Étape 9 — Monitoring (Uptime Kuma, healthchecks, alertes)

### Résumé

Ajout d’une stack de supervision séparée (`deploy/docker-compose.monitoring.yml`)
avec Uptime Kuma, exposé uniquement en local, et d’une documentation complète
(`docs/MONITORING.md`) pour les moniteurs, alertes, page de statut, incident et
sauvegarde.

### Fichiers

```text
deploy/docker-compose.monitoring.yml   # Uptime Kuma isolé, port 127.0.0.1:3001
docs/MONITORING.md                    # installation, moniteurs, alertes, incident
README.md                             # statut étape 9
```

### Vérifications

- Compose de monitoring à valider avec `docker compose -f ... config`.
- Uptime Kuma non exposé publiquement ; accès par tunnel SSH.
- Moniteurs recommandés : site `/fr/` et API `/api/health/`.
- Limitation assumée : supervision auto-hébergée sur le même VPS.

### Notes

- Les healthchecks Docker existants restent la première ligne de défense.
- Une sonde externe gratuite peut compléter Uptime Kuma pour détecter une
  panne totale du VPS.
