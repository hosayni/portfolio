# API Flask — portfolio

API du portfolio : santé, dépôts GitHub avec cache et formulaire de contact.
Elle est consommée par le site Astro via `/api/*` (proxy Vite en développement,
Caddy en production).

## Prérequis

- Python 3.12 ou plus récent (le projet est testé avec 3.13 en local) ;
- un serveur SMTP pour l'envoi réel des messages (facultatif en développement).

## Installation

```bash
cd api
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
```

La configuration se fait par variables d'environnement. Copier le modèle à la
racine du dépôt, puis renseigner les valeurs locales :

```bash
cp ../.env.example ../.env
```

L'API lit `api/.env` puis le `.env` de la racine, sans écraser les variables
déjà définies par le shell (Docker, CI, production). Ne jamais committer `.env`.

En développement, `MAIL_SUPPRESS_SEND=true` par défaut : le message est
journalisé mais aucun e-mail n'est envoyé. Mettre `MAIL_SUPPRESS_SEND=false` et
renseigner `SMTP_*` pour un envoi réel.

## Lancement

```bash
cd api
.venv/bin/flask --app wsgi run --port 8000
```

Ou avec le serveur de développement Flask (rechargement automatique) :

```bash
.venv/bin/flask --app wsgi run --debug --port 8000
```

Le site Astro relaie automatiquement `/api` vers `http://localhost:8000` en
développement. Pour une autre cible :

```bash
cd web
API_PROXY_TARGET=http://localhost:8001 npm run dev
```

## Endpoints

| Méthode | Route            | Description                                              |
| ------- | ---------------- | -------------------------------------------------------- |
| `GET`   | `/api/health`    | État, version, environnement et uptime.                  |
| `GET`   | `/api/projects`  | Dépôts GitHub publics, enrichis (langages, étoiles, URL). |
| `POST`  | `/api/contact`   | Message validé, anti-spam, rate limiting, envoi SMTP.    |

```bash
curl -s http://localhost:8000/api/health
curl -s http://localhost:8000/api/projects

curl -s -X POST http://localhost:8000/api/contact \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Camille Martin",
    "email": "camille@example.com",
    "message": "Bonjour, je souhaite discuter d’un projet avec vous.",
    "consent": true,
    "lang": "fr",
    "website": ""
  }'
```

Toutes les erreurs sont en JSON : `{"error": "code", "message": "..."}`. Les
erreurs de validation ajoutent un objet `fields`.

### GET /api/projects

- dépôts publics, hors forks et archives ;
- liste blanche optionnelle via `GITHUB_REPOS`, sinon les dépôts les plus
  récemment poussés ;
- trois langages principaux par dépôt ;
- cache mémoire d'une heure (`GITHUB_CACHE_TTL`) ;
- si GitHub échoue, le cache périmé est servi avec `"stale": true` ; sans cache,
  l'API répond `503` et le site garde ses projets statiques.

### POST /api/contact

- `name` : 2 à 120 caractères ;
- `email` : format et longueur validés ;
- `message` : 20 à 5 000 caractères ;
- `consent` : obligatoire (RGPD) ;
- `website` : honeypot, doit rester vide ;
- rate limiting par IP (`CONTACT_RATE_LIMIT`, 5 par heure par défaut) ;
- envoi SMTP synchrone, avec timeout.

## Tests et qualité

```bash
cd api
.venv/bin/pytest
.venv/bin/ruff check .
.venv/bin/ruff format --check .
```

La couverture est mesurée sur `app/` et le seuil est fixé à 80 % dans
`pyproject.toml`. Les tests simulent GitHub et SMTP : aucun appel réseau réel.

## Structure

```text
api/
├── app/
│   ├── __init__.py          # factory, CORS, en-têtes, logs, erreurs
│   ├── config.py            # configuration par environnement
│   ├── errors.py            # erreurs JSON homogènes
│   ├── extensions.py        # Flask-Limiter
│   ├── logging_config.py    # logs JSON
│   ├── validation.py        # validation du formulaire
│   ├── routes/              # health, projects, contact
│   └── services/            # GitHub (cache) et SMTP
├── tests/                   # Pytest, mocks réseau/SMTP
├── pyproject.toml           # Ruff, Pytest, couverture
├── requirements.txt         # dépendances épinglées
├── requirements-dev.txt
└── wsgi.py                  # point d'entrée Gunicorn
```

## Sécurité et limites connues

- CORS restreint à `CORS_ORIGINS` (liste séparée par des virgules) ;
- en-têtes `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`,
  `Permissions-Policy`, CSP et HSTS derrière HTTPS ;
- corps limité à 16 Ko, erreurs `413` en JSON ;
- aucune donnée personnelle (nom, e-mail, message) dans les logs ;
- `ProxyFix` activé par `TRUST_PROXY=true` uniquement derrière un proxy de
  confiance, pour que le rate limiting utilise l'IP réelle ;
- au démarrage en production, l'API refuse de démarrer si `SECRET_KEY`,
  `SMTP_HOST`, `SMTP_FROM`, `CONTACT_TO`, `CORS_ORIGINS` manquent ou si
  `MAIL_SUPPRESS_SEND=true` (aucun e-mail ne partirait).

Le cache GitHub et le rate limiting utilisent la mémoire du processus. Avec
plusieurs workers Gunicorn ou plusieurs instances, configurer un stockage
partagé (`RATELIMIT_STORAGE_URI=redis://...`, cache Redis) ou limiter à un
worker. L'envoi SMTP est synchrone : pour un fort trafic, le déporter dans une
file de tâches.

## Variables utiles

| Variable | Défaut | Rôle |
| --- | --- | --- |
| `APP_ENV` | `development` | Active les contrôles de production. |
| `APP_VERSION` | `0.1.0` | Version renvoyée par `/api/health`. |
| `SECRET_KEY` | valeur d'exemple | Obligatoire et unique en production. |
| `CORS_ORIGINS` | localhost + hosayni.com | Origines autorisées. |
| `CONTACT_RATE_LIMIT` | `5 per hour` | Quota du formulaire. |
| `GITHUB_USERNAME` | `hosayni` | Compte GitHub interrogé. |
| `GITHUB_TOKEN` | vide | Token en lecture seule, recommandé. |
| `GITHUB_REPOS` | vide | Liste blanche ordonnée des dépôts. |
| `GITHUB_CACHE_TTL` | `3600` | Durée du cache, en secondes. |
| `SMTP_*` | — | Connexion et expéditeur SMTP. |
| `CONTACT_TO` | — | Destinataire des messages. |
| `MAIL_SUPPRESS_SEND` | `true` en dev | Journalise sans envoyer. |
| `TRUST_PROXY` | `false` | Lit l'IP derrière Caddy/nginx. |
