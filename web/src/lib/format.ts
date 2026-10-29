import type { Lang } from '@/i18n/ui';

const dateLocales: Record<Lang, string> = {
  fr: 'fr-FR',
  en: 'en-GB',
};

/** Date lisible et stable entre le serveur de build et le navigateur. */
export function formatDate(date: Date, lang: Lang): string {
  return new Intl.DateTimeFormat(dateLocales[lang], {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
    timeZone: 'UTC',
  }).format(date);
}

/** Estimation de lecture : ~200 mots par minute, minimum une minute. */
export function readingTime(body: string | undefined): number {
  if (!body) return 1;
  const words = body.trim().split(/\s+/).filter(Boolean).length;
  return Math.max(1, Math.round(words / 200));
}
