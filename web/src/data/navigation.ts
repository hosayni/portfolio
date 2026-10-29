import type { UIKey } from '../i18n/ui';

export interface NavItem {
  key: UIKey;
  path: string;
}

/**
 * Navigation principale. Les chemins sont relatifs à la racine du site :
 * la langue est ajoutée au rendu par `localizePath()`.
 */
export const navItems = [
  { key: 'nav.home', path: '/' },
  { key: 'nav.projects', path: '/projets/' },
  { key: 'nav.skills', path: '/competences/' },
  { key: 'nav.career', path: '/parcours/' },
  { key: 'nav.blog', path: '/blog/' },
  { key: 'nav.contact', path: '/contact/' },
] as const satisfies readonly NavItem[];
