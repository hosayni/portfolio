// @ts-check
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';

/**
 * URL publique du site. Surchargée par la variable d'environnement SITE_URL
 * en CI/production, pour que les balises canonical et le sitemap restent justes.
 */
const site = process.env.SITE_URL ?? 'https://hosayni.com';

export default defineConfig({
  site,
  // URLs canoniques avec slash final : /fr/, /fr/projets/, etc.
  trailingSlash: 'always',
  // La racine redirige vers le français. Astro génère une page de secours
  // (meta refresh + lien) ; nginx et Caddy appliquent un vrai 301 HTTP.
  redirects: {
    '/': { status: 301, destination: '/fr/' },
  },
  i18n: {
    defaultLocale: 'fr',
    locales: ['fr', 'en'],
    routing: {
      // Le français est préfixé comme l'anglais : /fr/ et /en/.
      prefixDefaultLocale: true,
      // « / » redirige automatiquement vers « /fr/ ».
      redirectToDefaultLocale: true,
    },
  },
  markdown: {
    shikiConfig: {
      // Deux thèmes : les couleurs sont exposées en variables CSS, puis
      // sélectionnées par le thème actif dans global.css.
      themes: { light: 'github-light', dark: 'github-dark' },
      defaultColor: false,
    },
  },
  vite: {
    plugins: [tailwindcss()],
    server: {
      // En développement, le front appelle /api/* sur son propre domaine :
      // Vite relaie vers Flask. En production, Caddy fait le même routage.
      proxy: {
        '/api': {
          target: process.env.API_PROXY_TARGET ?? 'http://localhost:8000',
          changeOrigin: true,
        },
      },
    },
  },
  integrations: [
    mdx(),
    sitemap({
      // Alternates FR/EN dans le sitemap pour les moteurs de recherche.
      i18n: {
        defaultLocale: 'fr',
        locales: {
          fr: 'fr',
          en: 'en',
        },
      },
    }),
  ],
});
