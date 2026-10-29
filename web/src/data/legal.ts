import type { Lang } from '../i18n/ui';

export const legalSlugs = {
  notice: { fr: 'mentions-legales', en: 'legal-notice' },
  privacy: { fr: 'confidentialite', en: 'privacy-policy' },
} as const;

export type LegalKey = keyof typeof legalSlugs;

/** Chemin localisé d'une page légale, sans requête de collection. */
export function legalPath(lang: Lang, key: LegalKey): string {
  return `/${lang}/${legalSlugs[key][lang]}/`;
}
