import type { Lang } from '../i18n/ui';

export interface ProjectTeaser {
  slug: string;
  year: string;
  tags: readonly string[];
  title: Record<Lang, string>;
  summary: Record<Lang, string>;
}

/**
 * Projets mis en avant sur l'accueil.
 * À l'étape 3, ce tableau sera remplacé par une content collection Astro
 * (Markdown/MDX) avec un schéma Zod, afin que le contenu soit éditable
 * sans toucher au code.
 */
export const featuredProjects: readonly ProjectTeaser[] = [
  {
    slug: 'smart-farm-iot',
    year: '2025',
    tags: ['IoT', 'Python', 'MQTT', 'Flask'],
    title: {
      fr: 'Smart Farm IoT',
      en: 'Smart Farm IoT',
    },
    summary: {
      fr: 'Plateforme d’irrigation connectée : capteurs de sol, décisions automatiques et tableau de bord temps réel. [À COMPLÉTER : périmètre et résultats.]',
      en: 'Connected irrigation platform: soil sensors, automatic decisions and a real-time dashboard. [TO COMPLETE: scope and results.]',
    },
  },
  {
    slug: 'lms-adaptatif',
    year: '2025',
    tags: ['Flask', 'PostgreSQL', 'TypeScript'],
    title: {
      fr: 'LMS à évaluation adaptative',
      en: 'Adaptive assessment LMS',
    },
    summary: {
      fr: 'Plateforme d’apprentissage avec parcours adaptatifs et évaluation personnalisée. [À COMPLÉTER : périmètre et résultats.]',
      en: 'Learning platform with adaptive paths and personalised assessment. [TO COMPLETE: scope and results.]',
    },
  },
];
