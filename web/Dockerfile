# ---------------------------------------------------------------------------
# Site Astro : build Node, service statique nginx non-root.
# Les versions sont figées pour rendre les builds reproductibles.
# ---------------------------------------------------------------------------
FROM node:26.12-alpine3.24 AS base

ENV CI=true \
    NPM_CONFIG_FUND=false \
    NPM_CONFIG_UPDATE_NOTIFIER=false

WORKDIR /app

# Les dépendances sont installées dans une couche séparée : elle n'est
# reconstruite que lorsque package.json ou package-lock.json change.
COPY package.json package-lock.json ./
RUN npm ci

COPY . .

# Cible utilisée par docker-compose.yml : le code source est monté par-dessus
# /app et Vite recharge à chaud. Le volume node_modules est initialisé depuis
# cette image, d'où le chown pour que l'utilisateur node puisse y écrire.
FROM base AS dev

RUN chown -R node:node /app
USER node

EXPOSE 4321

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

# Cible de production : le build statique est copié dans nginx.
FROM base AS build

# Valeurs injectées par la CI de déploiement. Les valeurs par défaut gardent un
# build local identique à la CI de validation.
ARG SITE_URL=https://hosayni.com
ARG PUBLIC_CONTACT_ENABLED=true
ENV SITE_URL=$SITE_URL \
    PUBLIC_CONTACT_ENABLED=$PUBLIC_CONTACT_ENABLED

RUN npm run build

FROM nginx:1.30.6-alpine3.24 AS runtime

ENV NGINX_ENTRYPOINT_QUIET_LOGS=1

COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY nginx/default.conf /etc/nginx/conf.d/default.conf
COPY nginx/security-headers.conf /etc/nginx/snippets/security-headers.conf
COPY --from=build /app/dist /usr/share/nginx/html

# nginx écoute sur 8080 et écrit son PID/caches dans /tmp : aucun privilège
# root n'est nécessaire dans le conteneur.
USER nginx

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD wget -qO- http://127.0.0.1:8080/healthz || exit 1

CMD ["nginx", "-g", "daemon off;"]
