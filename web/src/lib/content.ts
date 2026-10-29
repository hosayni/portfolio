import { getCollection, type CollectionEntry } from 'astro:content';
import type { Lang } from '@/i18n/ui';

export type ProjectEntry = CollectionEntry<'projects'>;
export type BlogEntry = CollectionEntry<'blog'>;
export type PageEntry = CollectionEntry<'pages'>;

/** Slug public d'une entrée : `fr/smart-farm-iot` → `smart-farm-iot`. */
export function entrySlug(id: string): string {
  const segments = id.split('/');
  return segments[segments.length - 1] ?? id;
}

/** Projets publiés d'une langue, triés par ordre éditorial. */
export async function getProjects(lang: Lang): Promise<ProjectEntry[]> {
  const entries = await getCollection('projects', ({ data }) => data.lang === lang && !data.draft);
  return entries.sort((a, b) => a.data.order - b.data.order);
}

/** Projets mis en avant pour l'accueil. */
export async function getFeaturedProjects(lang: Lang, limit = 2): Promise<ProjectEntry[]> {
  const projects = await getProjects(lang);
  const featured = projects.filter((entry) => entry.data.featured);
  return (featured.length > 0 ? featured : projects).slice(0, limit);
}

/** Articles publiés d'une langue, du plus récent au plus ancien. */
export async function getPosts(lang: Lang): Promise<BlogEntry[]> {
  const entries = await getCollection('blog', ({ data }) => data.lang === lang && !data.draft);
  return entries.sort((a, b) => b.data.pubDate.getTime() - a.data.pubDate.getTime());
}

/**
 * Slugs de la même entrée dans chaque langue, pour les balises hreflang.
 * `translationKey` relie les fichiers fr/ et en/ même quand les slugs diffèrent.
 */
export async function getAlternateSlugs(
  kind: 'projects' | 'blog' | 'pages',
  translationKey: string,
  currentLang: Lang,
): Promise<Partial<Record<Lang, string>>> {
  const result: Partial<Record<Lang, string>> = {};

  if (kind === 'pages') {
    const pages = await getCollection('pages');
    for (const entry of pages) {
      if (entry.data.translationKey !== translationKey) continue;
      if (entry.data.lang === currentLang) continue;
      result[entry.data.lang] = entry.data.slug;
    }
    return result;
  }

  const entries =
    kind === 'projects' ? await getCollection('projects') : await getCollection('blog');

  for (const entry of entries) {
    if (entry.data.translationKey !== translationKey) continue;
    if (entry.data.lang === currentLang) continue;
    result[entry.data.lang] = entrySlug(entry.id);
  }
  return result;
}
