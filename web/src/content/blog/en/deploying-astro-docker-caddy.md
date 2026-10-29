---
lang: en
translationKey: deploy-astro-docker-caddy
title: Deploying Astro with Docker and Caddy
description: A static build, two containers and an automatic TLS certificate — without depending on a platform.
pubDate: 2026-09-15
tags:
  - Astro
  - Docker
  - Caddy
  - CI/CD
draft: false
---

## The problem

An Astro site produces static files. You could copy them to a VPS with `scp`,
but every update would become a manual operation, with no traceability and no
rollback. The goal is the opposite: an immutable image per commit, a
reproducible deployment and a TLS certificate that renews itself.

## A two-stage build

The first stage installs dependencies and builds the site. The second contains
only nginx and the generated files: the final image carries neither Node nor
`node_modules`.

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

The important part is the selective `COPY`: `package*.json` first, the rest
afterwards. As long as dependencies do not change, Docker reuses the cache and
the build stays fast.

## Caddy instead of an exposed nginx

Caddy terminates TLS and routes traffic to internal containers. No application
port is published on the host: only Caddy listens on 80 and 443.

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

Caddy obtains and renews the certificate without intervention. The `try_files`
directive reproduces classic static hosting behaviour: `/en/projects/` serves
`index.html`, and an unknown URL falls back to the 404 page.

## What changes

- Deployment becomes `docker compose pull && docker compose up -d`.
- A rollback means restarting the previous SHA tag.
- Security headers live in the same place as TLS.
- The site stays online even if the API is temporarily unavailable.

## Going further

The missing piece is automation: build images in GitHub Actions, publish them to
`ghcr.io`, then trigger the deployment over SSH with a healthcheck before
validating the new version. That is exactly the pipeline described on this
site’s Infrastructure page.
