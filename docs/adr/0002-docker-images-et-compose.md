# ADR 0002 — Images Docker et Compose de développement/production

- **Date :** 2026-10-29
- **Statut :** accepté
- **Contexte :** étape 5, conteneurisation du monorepo Astro + Flask.

## Contexte

Le site doit se lancer avec une seule commande en local (`docker compose up`) et
être déployable sur un VPS derrière Caddy. Les contraintes sont : images
multi-stage, utilisateurs non-root, builds reproductibles, healthchecks, cache
des assets, réseau privé en production et aucun secret dans les images.

## Décision

- **Web** : build `node:22.22-alpine3.24` → `nginx:1.30.6-alpine3.24`. nginx
  tourne avec l'utilisateur `nginx`, écoute sur `8080` et place PID/caches dans
  `/tmp`. La configuration dédiée définit le cache long des assets `/_astro/`,
  les en-têtes de sécurité et une page 404 interne.
- **API** : dépendances installées dans un venv dans une étape `builder`, puis
  copiées dans `python:3.12.16-slim-trixie`. L'utilisateur `app` (UID 10001)
  exécute Gunicorn en mode `gthread` avec **un worker et quatre threads**.
- **Développement** : `docker-compose.yml` construit les cibles `dev`, monte les
  sources et lance Astro/Flask avec rechargement à chaud. Un volume nommé
  conserve `node_modules`.
- **Production** : `deploy/docker-compose.prod.yml` tire les images de
  `ghcr.io`, ne publie que les ports de Caddy, place web/api sur un réseau privé,
  active `read_only` + `tmpfs`, `no-new-privileges`, `cap_drop: ALL` et des
  limites CPU/mémoire. Caddy conserve ses données dans des volumes nommés.
- **Versions** : images de base épinglées par version mineure/patch
  (`node:22.22-alpine3.24`, `nginx:1.30.6-alpine3.24`,
  `python:3.12.16-slim-trixie`, `caddy:2.11.7-alpine`).

## Conséquences

- Le cache GitHub et le rate limiting restent en mémoire : **ne pas augmenter le
  nombre de workers** sans ajouter Redis. C'est documenté dans le Compose et le
  Dockerfile.
- `read_only` impose que Gunicorn n'écrive pas dans le home ; le socket de
  contrôle Gunicorn est désactivé (`--no-control-socket`).
- La CSP autorise encore `'unsafe-inline'` pour les scripts inline du thème et
  des animations. Une CSP par hashes est prévue à l'étape 8.
- Le Compose de production est prêt, mais la publication `ghcr.io`, le workflow
  de déploiement et le guide VPS restent à l'étape 7.

## Alternatives rejetées

- **nginx en root** : plus simple, mais contraire à l'exigence de moindre
  privilège.
- **Image `nginxinc/nginx-unprivileged`** : adaptée, mais ajoute un registre et
  une variante d'image supplémentaire ; la configuration locale sur
  `nginx:alpine` garde une base officielle unique.
- **Plusieurs workers Gunicorn** : le rate limiting et le cache ne seraient plus
  cohérents entre processus.
- **Docker Compose unique pour dev et prod** : les cycles de vie, les ports et
  les secrets sont trop différents ; deux fichiers explicites sont plus sûrs.
