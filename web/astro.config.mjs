// @ts-check
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
  // La racine redirige vers le français. Astro génère une page de redirection
  // statique (meta refresh + lien), servie par nginx sans configuration dédiée.
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
  vite: {
    plugins: [tailwindcss()],
  },
});
