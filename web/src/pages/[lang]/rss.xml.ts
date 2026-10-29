import rss from '@astrojs/rss';
import type { APIRoute } from 'astro';
import { locales, ui, type Lang } from '@/i18n/ui';
import { entrySlug, getPosts } from '@/lib/content';

export function getStaticPaths() {
  return locales.map((lang) => ({ params: { lang } }));
}

export const GET: APIRoute = async (context) => {
  const lang = context.params.lang as Lang;
  const posts = await getPosts(lang);
  const site = context.site ?? new URL('https://hosayni.com');

  return rss({
    title: `${ui[lang]['site.name']} — ${ui[lang]['blog.title']}`,
    description: ui[lang]['blog.lead'],
    site,
    items: posts.map((post) => ({
      title: post.data.title,
      description: post.data.description,
      pubDate: post.data.pubDate,
      link: `/${lang}/blog/${entrySlug(post.id)}/`,
      categories: post.data.tags,
    })),
    customData: `<language>${lang}</language>`,
  });
};
