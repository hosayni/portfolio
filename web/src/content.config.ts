import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

/**
 * Collections de contenu.
 *
 * Chaque entrée existe en deux fichiers (fr/ et en/) reliés par
 * `translationKey`, ce qui permet de calculer les balises hreflang et les
 * liens de changement de langue, même quand les slugs diffèrent.
 */

const lang = z.enum(['fr', 'en']);

const projects = defineCollection({
  loader: glob({ base: './src/content/projects', pattern: '**/*.{md,mdx}' }),
  schema: z.object({
    lang,
    translationKey: z.string(),
    title: z.string().max(80),
    summary: z.string().max(220),
    year: z.string(),
    role: z.string(),
    duration: z.string(),
    tags: z.array(z.string()).min(1),
    stack: z.array(z.string()).min(1),
    featured: z.boolean().default(false),
    order: z.number().int().default(0),
    demoUrl: z.string().url().optional(),
    repoUrl: z.string().url().optional(),
    architecture: z
      .array(
        z.object({
          title: z.string(),
          items: z.array(z.string()).min(1),
        }),
      )
      .min(1),
    challenges: z.array(z.string()).min(1),
    results: z
      .array(
        z.object({
          value: z.string(),
          label: z.string(),
        }),
      )
      .min(1),
    draft: z.boolean().default(false),
  }),
});

const blog = defineCollection({
  loader: glob({ base: './src/content/blog', pattern: '**/*.{md,mdx}' }),
  schema: z.object({
    lang,
    translationKey: z.string(),
    title: z.string().max(80),
    description: z.string().max(180),
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    tags: z.array(z.string()).min(1),
    draft: z.boolean().default(false),
  }),
});

const pages = defineCollection({
  loader: glob({ base: './src/content/pages', pattern: '**/*.{md,mdx}' }),
  schema: z.object({
    lang,
    translationKey: z.string(),
    slug: z.string(),
    title: z.string(),
    description: z.string(),
    updatedDate: z.coerce.date(),
  }),
});

export const collections = { projects, blog, pages };
