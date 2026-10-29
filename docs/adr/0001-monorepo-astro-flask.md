# ADR 0001 — Monorepo Astro + Flask, conteneurisé et déployé par CI/CD

- **Statut :** accepté
- **Date :** 2026-10-29
- **Décisionnaire :** Mohamed Hosayni

## Contexte

Le portfolio doit être :

- très bien référencé et rapide (contenu essentiellement statique) ;
- bilingue FR/EN avec du contenu éditorial (projets, articles) ;
- doté d'une petite partie dynamique : lecture des dépôts GitHub, formulaire de contact ;
- déployé automatiquement sur un VPS Ubuntu 24.04 avec HTTPS ;
- une vitrine des compétences DevOps, pas seulement du rendu visuel.

## Décision

1. **Un monorepo** contenant `web/` (Astro), `api/` (Flask) et `deploy/`.
   Une seule PR peut faire évoluer le contrat d'API et son consommateur, et la CI
   teste l'ensemble de façon atomique.
2. **Frontend statique avec Astro.** Le HTML est généré au build : rien à exécuter
   côté serveur pour les pages, ce qui simplifie la sécurité et maximise les
   performances. Les îlots interactifs restent limités au strict nécessaire.
3. **TypeScript strict + Tailwind CSS.** Typage des collections de contenu et des
   dictionnaires i18n ; Tailwind configuré avec les design tokens du projet.
4. **API Flask séparée**, réduite à trois endpoints (`/api/health`,
   `/api/projects`, `/api/contact`). Flask est imposé et suffit largement ;
   l'API est isolée dans son conteneur pour ne jamais exposer le processus
   applicatif au trafic statique.
5. **Conteneurs séparés + Caddy** en reverse proxy TLS. Les images sont
   multi-stage, non-root, et publiées sur `ghcr.io` avec un tag SHA pour
   permettre un rollback exact.
6. **CI/CD GitHub Actions.** La CI est un prérequis de merge ; le déploiement
   n'a lieu qu'après une CI verte sur `main`, avec healthcheck et rollback.

## Alternatives écartées

| Alternative | Raison du rejet |
| --- | --- |
| Next.js / Nuxt (SSR) | Serveur Node à maintenir pour un site presque entièrement statique ; Astro livre moins de JavaScript. |
| Un seul dépôt frontend + API sans conteneur | Déploiement moins reproductible, pas de rollback par image, et le VPS devrait gérer Node **et** Python. |
| Django | Plus lourd que nécessaire pour trois endpoints ; Flask correspond au besoin et au périmètre imposé. |
| Site 100 % statique sans API | Impossible de garder un token GitHub côté serveur ni d'envoyer des emails sans exposer un secret. |
| Netlify / Vercel | Le VPS et le nom de domaine sont déjà disponibles ; l'objectif inclut la maîtrise du déploiement et du HTTPS. |

## Conséquences

**Positives**

- Pages servies en statique : surface d'attaque et coût d'hébergement réduits.
- Build reproductible, image immuable par commit, rollback trivial.
- Le pipeline lui-même illustre les compétences DevOps revendiquées.

**Négatives / à surveiller**

- Deux écosystèmes (Node et Python) à maintenir : Dependabot et `pip-audit` /
  `npm audit` sont indispensables.
- Le rendu dynamique des projets dépend de l'API : un contenu de repli statique
  doit exister et être testé.
- Le build frontend et l'image doivent rester alignés sur la même version de
  Node (`.nvmrc`, Dockerfile, CI).
