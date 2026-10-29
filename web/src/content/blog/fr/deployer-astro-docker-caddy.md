---
lang: fr
translationKey: deploy-astro-docker-caddy
title: Déployer Astro avec Docker et Caddy
description: Un build statique, deux conteneurs et un certificat TLS automatique — sans dépendre d’une plateforme.
pubDate: 2026-09-15
tags:
  - Astro
  - Docker
  - Caddy
  - CI/CD
draft: false
---

## Le problème

Un site Astro produit des fichiers statiques. On pourrait les copier sur un VPS
avec `scp`, mais chaque mise à jour deviendrait une opération manuelle, sans
traçabilité ni retour arrière. L’objectif est inverse : une image immuable par
commit, un déploiement reproductible et un certificat TLS qui se renouvelle
seul.

## Un build en deux étapes

Le premier étage installe les dépendances et construit le site. Le second ne
contient que nginx et les fichiers générés : l’image finale ne transporte ni
Node, ni `node_modules`.

```dockerfile
FROM node:22-alpine AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine AS runtime
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
```

Le point important est le `COPY` sélectif : `package*.json` d’abord, le reste
ensuite. Tant que les dépendances ne changent pas, Docker réutilise le cache et
le build reste rapide.

## Caddy plutôt qu’un nginx exposé

Caddy termine le TLS et route le trafic vers les conteneurs internes. Aucun
port applicatif n’est publié sur l’hôte : seul Caddy écoute sur 80 et 443.

```text
hosayni.com {
	encode zstd gzip
	root * /srv/web
	try_files {path} {path}/ /404.html
	file_server

	handle /api/* {
		reverse_proxy api:8000
	}

	header {
		Strict-Transport-Security "max-age=31536000; includeSubDomains"
		X-Content-Type-Options "nosniff"
		Referrer-Policy "strict-origin-when-cross-origin"
	}
}
```

Caddy obtient et renouvelle le certificat sans intervention. La directive
`try_files` reproduit le comportement d’un hébergement statique classique :
`/fr/projets/` sert `index.html`, et une URL inconnue tombe sur la page 404.

## Ce que ça change

- Le déploiement devient `docker compose pull && docker compose up -d`.
- Un retour arrière consiste à relancer le tag SHA précédent.
- Les en-têtes de sécurité sont centralisés au même endroit que le TLS.
- Le site reste servi même si l’API est momentanément indisponible.

## Pour aller plus loin

La pièce manquante est l’automatisation : construire les images dans GitHub
Actions, les publier sur `ghcr.io`, puis déclencher le déploiement par SSH avec
un healthcheck avant de valider la nouvelle version. C’est exactement le
pipeline décrit dans la page Infrastructure de ce site.
