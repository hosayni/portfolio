# Supervision

Ce document décrit la mise en place et l’exploitation de la supervision du
portfolio en production. Le site lui-même expose déjà `/api/health/` ; la
supervision ajoute une vue continue, des alertes et une page de statut.

## 1. Objectifs

- détecter une indisponibilité du site ou de l’API en moins de deux minutes ;
- vérifier le certificat TLS avant expiration ;
- alerter par un canal fiable (e-mail, Telegram ou Discord) ;
- conserver une page de statut publique simple ;
- documenter la procédure d’incident.

## 2. Stack retenue

- **Uptime Kuma** (`louislam/uptime-kuma:2.2.1`) dans un Compose séparé :
  `deploy/docker-compose.monitoring.yml`.
- Les healthchecks Docker existants restent la première ligne de défense.
- `/api/health/` sert de sonde applicative.

Limitation assumée : Uptime Kuma est auto-hébergé sur le même VPS. S’il est
hors ligne, la supervision l’est aussi. Pour une détection externe réelle,
ajouter une sonde externe gratuite (UptimeRobot, Healthchecks.io) en
complément.

## 3. Installation

Sur le VPS :

```bash
cd /opt/portfolio
docker compose -f docker-compose.monitoring.yml up -d
docker compose -f docker-compose.monitoring.yml ps
```

Si Uptime Kuma affiche `EACCES: permission denied`, corriger le volume :

```bash
docker run --rm -v portfolio-monitoring_uptime_kuma_data:/data alpine chown -R 1000:1000 /data
cd /opt/portfolio
docker compose -f docker-compose.monitoring.yml down
docker compose -f docker-compose.monitoring.yml up -d
```

Uptime Kuma est exposé uniquement sur `127.0.0.1:3001`. Accès :

```bash
ssh -L 3001:127.0.0.1:3001 deploy@5.189.129.87
# puis ouvrir http://127.0.0.1:3001
```

Premier démarrage :

1. créer le compte administrateur ;
2. activer l’authentification à deux facteurs ;
3. désactiver l’inscription publique si l’option est proposée.

## 4. Moniteurs recommandés

### 4.1 Site public

- Type : HTTP(s)
- Nom : `Portfolio — site`
- URL : `https://hosayni.com/fr/`
- Méthode : `GET`
- Intervalle : 60 s
- Codes acceptés : `200`
- Mot-clé : `Mohamed Hosayni` ou `Portfolio`
- Certificat TLS : alerte à 14 jours

### 4.2 API santé

- Type : HTTP(s)
- Nom : `Portfolio — API santé`
- URL : `https://hosayni.com/api/health/`
- Méthode : `GET`
- Intervalle : 60 s
- Codes acceptés : `200`
- Mot-clé : `"status":"ok"`

### 4.3 Certificat TLS

Uptime Kuma peut surveiller l’expiration du certificat Let’s Encrypt. Configurer
une alerte à 14 jours.

### 4.4 Docker (manuel / périodique)

```bash
ssh deploy@5.189.129.87 'cd /opt/portfolio && docker compose -f docker-compose.prod.yml ps'
```

Les services `web`, `api` et `caddy` doivent être `healthy` ou `running`.

## 5. Alertes

Configurer au moins un canal :

- e-mail via le SMTP du VPS ou un fournisseur externe ;
- Telegram (bot + chat ID) ;
- Discord (webhook) ;
- webhook générique vers un service d’astreinte.

Recommandations :

- une alerte après 2 échecs consécutifs pour éviter le bruit ;
- une notification de retour à la normale ;
- un canal distinct pour les alertes critiques.

## 6. Page de statut

Uptime Kuma permet de créer une page de statut publique, par exemple :

```text
https://status.hosayni.com
```

Si tu veux l’exposer publiquement, ajouter un sous-domaine dans le Caddyfile et
le DNS, puis router vers `uptime-kuma:3001`. Sinon, la garder privée via tunnel
SSH.

## 7. Procédure d’incident

1. Vérifier la disponibilité :

```bash
curl -fsS https://hosayni.com/api/health/
curl -fsSI https://hosayni.com/fr/
```

2. Vérifier les conteneurs :

```bash
ssh deploy@5.189.129.87 'cd /opt/portfolio && docker compose -f docker-compose.prod.yml ps'
```

3. Lire les logs :

```bash
ssh deploy@5.189.129.87 'cd /opt/portfolio && docker compose -f docker-compose.prod.yml logs --tail=100 api caddy web'
```

4. Vérifier le DNS et le certificat.
5. Si le déploiement récent est en cause, rollback :

```bash
ssh deploy@5.189.129.87 'cd /opt/portfolio && cat .deployed-tag'
ssh deploy@5.189.129.87 'cd /opt/portfolio && bash deploy.sh sha-<commit-précédent>'
```

6. Si le VPS est injoignable, utiliser la console du fournisseur.

## 8. Sauvegarde

Sauvegarder le volume Uptime Kuma :

```bash
ssh deploy@5.189.129.87 \
  'docker run --rm -v portfolio-monitoring_uptime_kuma_data:/data -v /tmp:/backup alpine \
   tar czf /backup/uptime-kuma-$(date +%F).tar.gz -C /data .'
```

Le nom exact du volume peut être vérifié avec `docker volume ls`.

## 9. Limites

- la supervision est auto-hébergée : elle ne détecte pas une panne totale du VPS ;
- pour une vraie détection externe, ajouter une sonde externe gratuite ;
- les alertes dépendent de la configuration SMTP/Telegram/Discord choisie.

## 10. Vérification

```bash
ssh -L 3001:127.0.0.1:3001 deploy@5.189.129.87
```

Puis ouvrir `http://127.0.0.1:3001` et vérifier que les deux moniteurs sont verts.