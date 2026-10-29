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

