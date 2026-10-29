# ADR 0003 — Déploiement continu par SHA et rollback automatique

- **Date :** 2026-10-29
- **Statut :** accepté
- **Contexte :** étape 7, publication ghcr.io et déploiement sur VPS.

## Contexte

Le Compose de production (étape 5) tire des images depuis `ghcr.io` par tag.
Il faut automatiser la publication et la mise en production sans secret dans le
dépôt, avec un rollback si le nouveau déploiement échoue. Le VPS est déjà
équipé de Docker ; l'utilisateur `deploy` non-root exécute les commandes.

## Décision

- **Déclenchement** : `deploy.yml` est déclenché par `workflow_run` après une
  CI verte sur `main`. La CI est également exécutée sur `main` pour valider le
  commit fusionné avant déploiement.
- **Images** : construction multi-architectures `linux/amd64` pour `web` et
  `api`, publiées sur `ghcr.io/${owner}/portfolio-{web,api}` avec deux tags :
  `sha-<commit>` (immuable) et `latest`. Le cache Buildx est stocké dans le
  cache GitHub Actions.
- **Authentification VPS** : le workflow ouvre une session Docker éphémère sur
  le VPS avec le `GITHUB_TOKEN` à portée `read:packages`, dans un répertoire de
  configuration temporaire nettoyé à la fin. Aucun jeton n'est persisté sur le
  VPS.
- **Déploiement** : copie de `docker-compose.prod.yml`, `Caddyfile` et
  `deploy.sh` par `tar` sur SSH, puis exécution de `deploy.sh <tag>` sur le
  VPS. Le script tire les images, recrée les conteneurs avec `--wait`, vérifie
  les endpoints publics `/api/health/` et `/fr/`, puis enregistre le tag dans
  `.deployed-tag`.
- **Rollback** : si le démarrage ou le healthcheck échoue, `deploy.sh` tente de
  revenir au tag précédent enregistré, puis vérifie à nouveau la disponibilité.
- **Nettoyage** : `docker image prune -af --filter "until=168h"` après un
  déploiement réussi. Un seul déploiement à la fois via `concurrency`.
- **Environnement GitHub** : job `deploy` dans l'environnement `production`
  avec URL publique, permettant une approbation manuelle facultative.
- **Premier déploiement sans SMTP** : `CONTACT_ENABLED=false` dans
  `deploy/.env.example` permet de démarrer l'API sans serveur mail ; le
  formulaire est masqué et `/api/contact` répond 503. Le frontend est masqué au
  build via `PUBLIC_CONTACT_ENABLED` (false par défaut dans le workflow).

## Conséquences

- Chaque commit sur `main` produit une image immuable et un déploiement
  automatique si la CI est verte.
- Le rollback automatique couvre les échecs de démarrage et de healthcheck, mais
  pas les régressions fonctionnelles silencieuses ; celles-ci nécessitent un
  rollback manuel (`bash deploy.sh <tag>`).
- Le VPS doit disposer de `curl`, `docker` et `docker compose v2`. L'utilisateur
  `deploy` doit appartenir au groupe `docker`.
- Les images GHCR sont privées par défaut ; le workflow s'authentifie avec un
  jeton éphémère. Pour un déploiement hors workflow, créer un PAT en lecture ou
  rendre les packages publics.

## Alternatives rejetées

- **Déclenchement sur `push: main` dans le même workflow** : dupliquerait la CI
  ou risquerait de déployer sans vérification.
- **Publication sur le VPS via `docker build`** : perd l'immuabilité et le cache
  CI, et expose les secrets de build.
- **Rollback par `docker compose down` puis ancienne version** : augmente la
  fenêtre d'indisponibilité ; le script garde l'ancien conteneur jusqu'au
  démarrage du nouveau.
- **Secrets SMTP obligatoires au premier déploiement** : bloquerait la mise en
  ligne initiale ; le drapeau `CONTACT_ENABLED` découple le démarrage de
  l'activation du formulaire.