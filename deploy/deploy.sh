#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# Déploiement d'une version sur le VPS.
#
# Usage (sur le VPS, depuis /opt/portfolio) :
#   bash deploy.sh <image-tag>
#
# Le tag est fourni par le workflow GitHub Actions (sha-<commit>). Le script
# tire les images, recrée les conteneurs, attend le healthcheck public, puis
# enregistre le tag déployé. En cas d'échec, il tente un rollback vers le tag
# précédent.
# ---------------------------------------------------------------------------

set -euo pipefail

DEPLOY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly DEPLOY_DIR
readonly COMPOSE=(docker compose -f docker-compose.prod.yml)

NEW_TAG="${1:-}"
if [[ -z "$NEW_TAG" || ! "$NEW_TAG" =~ ^[A-Za-z0-9._-]+$ ]]; then
  echo "Usage : bash deploy.sh <image-tag>" >&2
  exit 2
fi

cd "$DEPLOY_DIR"

if [[ ! -f .env ]]; then
  echo "ERREUR : .env introuvable dans $DEPLOY_DIR" >&2
  exit 1
fi

# Lire le domaine depuis .env sans l'exécuter.
SITE_DOMAIN="$(grep -E '^SITE_DOMAIN=' .env | tail -n 1 | cut -d '=' -f 2- | tr -d '\r')"
SITE_DOMAIN="${SITE_DOMAIN%\"}"
SITE_DOMAIN="${SITE_DOMAIN#\"}"
SITE_DOMAIN="${SITE_DOMAIN%\'}"
SITE_DOMAIN="${SITE_DOMAIN#\'}"
if [[ -z "$SITE_DOMAIN" ]]; then
  echo "ERREUR : SITE_DOMAIN manquant dans .env" >&2
  exit 1
fi

BASE_URL="https://${SITE_DOMAIN}"

PREVIOUS_TAG=""
if [[ -f .deployed-tag ]]; then
  PREVIOUS_TAG="$(tr -d '[:space:]' < .deployed-tag)"
fi

log() {
  printf '[deploy] %s\n' "$*"
}

wait_http() {
  local attempt
  for attempt in $(seq 1 36); do
    if curl -fsS --max-time 10 "$BASE_URL/api/health/" >/dev/null 2>&1 \
      && curl -fsS --max-time 10 "$BASE_URL/fr/" >/dev/null 2>&1; then
      return 0
    fi
    log "attente de la disponibilité publique ($attempt/36)…"
    sleep 5
  done
  return 1
}

fail_and_rollback() {
  local message="$1"
  echo "ERREUR : $message" >&2
  "${COMPOSE[@]}" ps || true
  "${COMPOSE[@]}" logs --tail=200 || true

  if [[ -n "$PREVIOUS_TAG" && "$PREVIOUS_TAG" != "$NEW_TAG" ]]; then
    log "tentative de rollback vers $PREVIOUS_TAG"
    if IMAGE_TAG="$PREVIOUS_TAG" "${COMPOSE[@]}" pull \
      && IMAGE_TAG="$PREVIOUS_TAG" "${COMPOSE[@]}" up -d --remove-orphans --wait --wait-timeout 180 \
      && wait_http; then
      log "rollback réussi vers $PREVIOUS_TAG"
    else
      echo "ERREUR : le rollback a échoué" >&2
    fi
  fi
  exit 1
}

log "déploiement de $NEW_TAG (précédent : ${PREVIOUS_TAG:-aucun})"

if ! IMAGE_TAG="$NEW_TAG" "${COMPOSE[@]}" pull; then
  fail_and_rollback "échec du téléchargement des images ($NEW_TAG)"
fi

if ! IMAGE_TAG="$NEW_TAG" "${COMPOSE[@]}" up -d --remove-orphans --wait --wait-timeout 180; then
  fail_and_rollback "échec du démarrage des conteneurs ($NEW_TAG)"
fi

# Recharger le reverse proxy central, qui peut garder en cache les anciennes
# adresses IP des conteneurs recréés.
if [[ -f /opt/caddy/docker-compose.yml ]]; then
  docker compose -f /opt/caddy/docker-compose.yml restart caddy >/dev/null 2>&1 || true
  sleep 5
fi

if ! wait_http; then
  fail_and_rollback "les healthchecks publics ont échoué ($NEW_TAG)"
fi

printf '%s\n' "$NEW_TAG" > .deployed-tag
"${COMPOSE[@]}" ps
docker image prune -af --filter "until=168h" >/dev/null 2>&1 || true

log "déploiement réussi : $NEW_TAG"