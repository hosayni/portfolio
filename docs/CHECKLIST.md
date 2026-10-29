# Checklist de livraison

Cette checklist résume l’état du projet et les vérifications à effectuer avant
de considérer le portfolio comme livré.

## 1. Étapes complétées

- [x] 1. Initialisation — dépôt, conventions, structure, documentation
- [x] 2. Frontend — Astro 5, TypeScript strict, Tailwind, SEO, i18n FR/EN, thème
- [x] 3. Pages et contenu — collections, projets, compétences, parcours, blog, contact, légal
- [x] 4. API Flask — santé, projets GitHub avec cache, contact validé et limité
- [x] 5. Docker — images multi-stage non-root, Compose dev/prod, Caddy
- [x] 6. CI — GitHub Actions, Playwright, Lighthouse, audits, CodeQL, Dependabot
- [x] 7. CD et VPS — publication ghcr.io, déploiement SSH, rollback, durcissement
- [x] 8. SEO et performance — JSON-LD, sitemap, RSS, Lighthouse ≥ 95
- [x] 9. Monitoring — Uptime Kuma, healthchecks, alertes
- [x] 10. Documentation — guide de déploiement, checklist de livraison

## 2. Vérifications techniques

### Frontend

- [ ] `cd web && npm ci`
- [ ] `npm run format:check`
- [ ] `npm run lint`
- [ ] `npm run check`
- [ ] `npm run build`
- [ ] `npm run test:e2e`
- [ ] Lighthouse CI : performance, accessibilité, bonnes pratiques, SEO ≥ 95

### API

- [ ] `cd api && .venv/bin/ruff check .`
- [ ] `.venv/bin/ruff format --check .`
- [ ] `.venv/bin/pytest`
- [ ] couverture ≥ 80 %

### Sécurité

- [ ] `npm audit` conforme à la politique d’exceptions
- [ ] `pip-audit -r api/requirements.txt --strict`
- [ ] CodeQL sans alerte bloquante
- [ ] aucun secret dans le dépôt

### Docker

- [ ] `docker compose up --build` fonctionne en local
- [ ] `docker compose -f deploy/docker-compose.prod.yml config` valide
- [ ] images non-root
- [ ] healthchecks présents

### Déploiement

- [ ] DNS `hosayni.com` et `www.hosayni.com` → `5.189.129.87`
- [ ] VPS durci (SSH par clé, UFW, mises à jour)
- [ ] `/opt/portfolio/.env` présent, permissions `600`
- [ ] secrets GitHub configurés
- [ ] environnement `production` créé
- [ ] protection de branche `main` active
- [ ] CI verte sur `main`
- [ ] `deploy.yml` réussi
- [ ] site accessible en HTTPS

### Monitoring

- [ ] Uptime Kuma installé
- [ ] moniteur site vert
- [ ] moniteur API vert
- [ ] alerte configurée
- [ ] accès par tunnel SSH vérifié

## 3. Vérifications fonctionnelles

- [ ] `/` redirige vers `/fr/`
- [ ] `/fr/` et `/en/` s’affichent
- [ ] changement de langue fonctionne
- [ ] filtre projets fonctionne
- [ ] formulaire de contact valide les champs
- [ ] `/api/health/` répond `status: ok`
- [ ] projets GitHub se chargent ou dégradation gracieuse
- [ ] RSS disponible
- [ ] sitemap disponible
- [ ] robots.txt disponible

## 4. Documents à consulter

- [README.md](../README.md)
- [HISTORIQUE.md](../HISTORIQUE.md)
- [docs/CI.md](CI.md)
- [docs/DEPLOIEMENT.md](DEPLOIEMENT.md)
- [docs/MONITORING.md](MONITORING.md)
- [docs/adr/](adr/)

## 5. Limites assumées

- in-memory GitHub cache et rate limiting : un seul worker Gunicorn ;
- CSP autorise encore `'unsafe-inline'` pour les scripts inline ;
- exceptions npm Astro 5 expirent le 31 mars 2027 ;
- supervision auto-hébergée : panne totale du VPS non détectée sans sonde externe ;
- contenu rédactionnel à compléter (`[À COMPLÉTER]`).

## 6. État final

Le projet est considéré comme livré lorsque :

- la CI est verte sur `main` ;
- le déploiement automatique fonctionne ;
- le site est accessible en HTTPS ;
- les moniteurs sont verts ;
- la documentation est à jour.

Date de validation : [À COMPLÉTER]  
Validé par : [À COMPLÉTER]