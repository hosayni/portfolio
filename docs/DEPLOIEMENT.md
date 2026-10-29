# Déploiement

> **État :** document partiel (étape 5/10). Le Compose de production et le
> Caddyfile sont prêts. La publication des images, le workflow GitHub Actions,
> le durcissement du VPS et la procédure de rollback complète sont finalisés aux
> étapes 7 et 10.

## Prérequis

- Un VPS avec Docker et Docker Compose v2.24+.
- Le DNS de `SITE_DOMAIN` et `WWW_DOMAIN` pointant vers le VPS (ports 80/443
  ouverts).
- Les images `web` et `api` publiées sur `ghcr.io` (étape 7) :
  `ghcr.io/<owner>/portfolio-web:<tag>` et `portfolio-api:<tag>`.
- `deploy/.env` créé depuis `deploy/.env.example`, avec les secrets réels et
  `chmod 600 deploy/.env`.

## Démarrage

Depuis `deploy/` sur le VPS :

```bash
docker compose -f docker-compose.prod.yml pull
docker compose -f docker-compose.prod.yml up -d
docker compose -f docker-compose.prod.yml ps
```

Caddy obtient automatiquement les certificats Let's Encrypt. Vérifier :

```bash
curl -fsS https://<SITE_DOMAIN>/api/health/
curl -fsSI https://<SITE_DOMAIN>/fr/
```

Le premier appel peut prendre quelques secondes (émission du certificat).

## Exploitation

```bash
docker compose -f docker-compose.prod.yml logs -f --tail=100
docker compose -f docker-compose.prod.yml restart api
```

Les logs sont limités par le driver `json-file` (10 Mo × 3 fichiers par
service). Les données Caddy sont conservées dans les volumes `caddy_data` et
`caddy_config`.

## Rollback manuel

Le workflow de l'étape 7 publiera un tag par SHA de commit. Pour revenir à une
version précédente, modifier `IMAGE_TAG` dans `deploy/.env`, puis :

```bash
docker compose -f docker-compose.prod.yml pull
docker compose -f docker-compose.prod.yml up -d
```

Le healthcheck de Caddy attend que `web` et `api` soient sains avant de router
le trafic.

## À compléter

- Publication `ghcr.io` et déploiement SSH automatique (étape 7).
- Durcissement du VPS : UFW, Fail2ban, mises à jour automatiques, utilisateur
  `deploy` non-root (étape 7).
- Supervision Uptime Kuma et alertes (étape 9).
- Sauvegardes et procédure de remise en route détaillée (étape 10).
