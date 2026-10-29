import { defaultLang, languages, ui, type Lang, type UIKey } from './ui';

/** Vérifie qu'une valeur inconnue est bien une locale supportée. */
export function isLang(value: unknown): value is Lang {
  return typeof value === 'string' && Object.prototype.hasOwnProperty.call(languages, value);
}

/** Déduit la langue à partir du premier segment de l'URL (/fr/, /en/…). */
export function getLangFromUrl(url: URL): Lang {
  const [first] = url.pathname.split('/').filter(Boolean);
  return isLang(first) ? first : defaultLang;
}

/**
 * Retire le préfixe de langue d'un chemin et normalise le slash final.
 * `/fr/projets/` → `/projets/`, `/en` → `/`, `/` → `/`.
 */
export function stripLocale(pathname: string): string {
  const segments = pathname.split('/').filter(Boolean);
  if (isLang(segments[0])) {
    segments.shift();
  }
  return segments.length === 0 ? '/' : `/${segments.join('/')}/`;
}

/** Construit un chemin localisé. `localizePath('en', '/projets/')` → `/en/projets/`. */
export function localizePath(lang: Lang, path = '/'): string {
  const clean = stripLocale(path.startsWith('/') ? path : `/${path}`);
  return clean === '/' ? `/${lang}/` : `/${lang}${clean}`;
}

/** Retourne la fonction de traduction pour une langue donnée. */
export function useTranslations(lang: Lang): (key: UIKey) => string {
  return (key) => ui[lang][key] ?? ui[defaultLang][key];
}

/** Variantes de la page courante dans toutes les langues, pour les balises hreflang. */
export function getAlternates(pathname: string): { lang: Lang; href: string }[] {
  const path = stripLocale(pathname);
  return (Object.keys(languages) as Lang[]).map((lang) => ({
    lang,
    href: localizePath(lang, path),
  }));
}
