/**
 * Dictionnaires de traduction du site.
 *
 * Un seul fichier pour les deux langues : les clés sont vérifiées à la
 * compilation, et le dictionnaire anglais doit couvrir exactement les mêmes
 * clés que le français. Ajouter une clé dans `fr` provoque donc une erreur
 * TypeScript tant que `en` n'est pas complété.
 */

export const languages = {
  fr: {
    label: 'Français',
    short: 'FR',
    htmlLang: 'fr',
    ogLocale: 'fr_FR',
  },
  en: {
    label: 'English',
    short: 'EN',
    htmlLang: 'en',
    ogLocale: 'en_US',
  },
} as const;

export type Lang = keyof typeof languages;
export type UIKey = keyof typeof fr;

export const defaultLang: Lang = 'fr';
export const locales = Object.keys(languages) as Lang[];

const fr = {
  // Navigation ------------------------------------------------------------
  'nav.label': 'Navigation principale',
  'nav.home': 'Accueil',
  'nav.projects': 'Projets',
  'nav.skills': 'Compétences',
  'nav.career': 'Parcours',
  'nav.blog': 'Blog',
  'nav.contact': 'Contact',

  // Accessibilité ---------------------------------------------------------
  'a11y.skip': 'Aller au contenu principal',
  'a11y.themeDark': 'Passer en thème sombre',
  'a11y.themeLight': 'Passer en thème clair',
  'a11y.lang': 'Changer de langue',
  'a11y.external': '(s’ouvre dans un nouvel onglet)',

  // Identité --------------------------------------------------------------
  'site.name': 'Mohamed Hosayni',
  'site.role': 'Ingénieur en développement digital et systèmes d’information',

  // Accueil — hero --------------------------------------------------------
  'home.meta.description':
    'Portfolio de Mohamed Hosayni, ingénieur en développement digital et systèmes d’information : projets web, DevOps et IoT.',
  'hero.eyebrow': 'Développement web · Systèmes d’information · DevOps',
  'hero.title': 'Je conçois des applications web rapides, accessibles et durables.',
  'hero.lead':
    'Étudiant ingénieur en développement digital et systèmes d’information. Je travaille du composant d’interface jusqu’au pipeline de déploiement — [À COMPLÉTER : ta spécialité en une phrase].',
  'hero.ctaProjects': 'Voir les projets',
  'hero.ctaContact': 'Me contacter',
  'hero.ctaCv': 'Télécharger le CV (PDF)',
  'hero.availability': 'Ouvert aux stages et alternances',
  'hero.focusLabel': 'Focus',
  'hero.focus': 'Web · DevOps · IoT',
  'hero.locationLabel': 'Basé à',
  'hero.location': '[Ville, pays]',
  'hero.stackLabel': 'Stack principale',
  'hero.stack': 'Astro · Flask · Docker',
  'hero.portraitNote': '[PHOTO — remplacer par un portrait]',

  // Accueil — projets -----------------------------------------------------
  'home.projects.eyebrow': 'Sélection',
  'home.projects.title': 'Des projets pensés de bout en bout',
  'home.projects.lead':
    'Du cadrage au déploiement, en passant par les tests et la supervision. [À COMPLÉTER : une phrase sur ta démarche.]',
  'home.projects.all': 'Tous les projets',

  // Accueil — approche ----------------------------------------------------
  'home.approach.eyebrow': 'Méthode',
  'home.approach.title': 'Concevoir, construire, exploiter',
  'home.approach.lead':
    'Un produit ne s’arrête pas au code : il se mesure aussi à sa lisibilité, à sa vitesse et à la sérénité de son exploitation.',
  'approach.design.title': 'Concevoir',
  'approach.design.desc':
    'Cadrer le besoin, modéliser les données, choisir la solution la plus simple qui tient dans le temps.',
  'approach.build.title': 'Construire',
  'approach.build.desc':
    'Écrire un code typé et testé, avec des composants réutilisables et une expérience accessible à tous.',
  'approach.operate.title': 'Exploiter',
  'approach.operate.desc':
    'Conteneuriser, automatiser les déploiements, surveiller la disponibilité et documenter les procédures.',

  // Accueil — contact -----------------------------------------------------
  'home.contact.eyebrow': 'Contact',
  'home.contact.title': 'Un projet, une alternance, une question ?',
  'home.contact.lead':
    'Le formulaire arrive à l’étape suivante. En attendant, écrivez-moi directement par email.',
  'home.contact.cta': 'Écrire un message',

  // Pages ----------------------------------------------------------------
  'projects.title': 'Projets',
  'projects.lead':
    'Chaque projet détaille le contexte, le problème, l’architecture, les difficultés rencontrées et les résultats. [À COMPLÉTER]',
  'skills.title': 'Compétences',
  'skills.lead':
    'Backend, frontend, DevOps, IoT, bases de données et outils : les technologies que j’utilise, avec leur niveau de maîtrise. [À COMPLÉTER]',
  'career.title': 'Parcours',
  'career.lead':
    'Formation, expériences et certifications, présentées sous forme de frise chronologique. [À COMPLÉTER]',
  'blog.title': 'Blog technique',
  'blog.lead':
    'Notes de terrain sur le développement, le déploiement et l’exploitation d’applications. [À COMPLÉTER]',
  'contact.title': 'Contact',
  'contact.lead':
    'Le formulaire (validation, honeypot et limitation de débit) sera ajouté à l’étape suivante. En attendant : hosayni92@gmail.com.',

  // Divers ---------------------------------------------------------------
  'common.comingSoon':
    '[À COMPLÉTER] Cette section sera remplie avec le contenu réel à l’étape suivante du projet.',
  'common.backHome': 'Retour à l’accueil',

  // Pied de page ----------------------------------------------------------
  'footer.tagline':
    'Ingénieur en développement digital et systèmes d’information — web, DevOps et IoT.',
  'footer.explore': 'Explorer',
  'footer.contact': 'Contact',
  'footer.navLabel': 'Liens de pied de page',
  'footer.builtWith': 'Construit avec Astro, Flask et Docker, déployé par GitHub Actions.',
  'footer.source': 'Code source',
  'footer.rights': 'Tous droits réservés.',

  // 404 ------------------------------------------------------------------
  'notFound.title': 'Page introuvable',
  'notFound.lead':
    'La page demandée n’existe pas ou a été déplacée. Utilisez le lien ci-dessous pour revenir à l’accueil.',
  'notFound.cta': 'Revenir à l’accueil',
} as const;

const en: Record<UIKey, string> = {
  // Navigation ------------------------------------------------------------
  'nav.label': 'Main navigation',
  'nav.home': 'Home',
  'nav.projects': 'Projects',
  'nav.skills': 'Skills',
  'nav.career': 'Career',
  'nav.blog': 'Blog',
  'nav.contact': 'Contact',

  // Accessibilité ---------------------------------------------------------
  'a11y.skip': 'Skip to main content',
  'a11y.themeDark': 'Switch to dark theme',
  'a11y.themeLight': 'Switch to light theme',
  'a11y.lang': 'Change language',
  'a11y.external': '(opens in a new tab)',

  // Identité --------------------------------------------------------------
  'site.name': 'Mohamed Hosayni',
  'site.role': 'Digital development and information systems engineer',

  // Accueil — hero --------------------------------------------------------
  'home.meta.description':
    'Portfolio of Mohamed Hosayni, digital development and information systems engineer: web, DevOps and IoT projects.',
  'hero.eyebrow': 'Web development · Information systems · DevOps',
  'hero.title': 'I build fast, accessible and maintainable web applications.',
  'hero.lead':
    'Engineering student in digital development and information systems. I work from the interface component all the way to the deployment pipeline — [TO COMPLETE: your specialty in one sentence].',
  'hero.ctaProjects': 'View projects',
  'hero.ctaContact': 'Get in touch',
  'hero.ctaCv': 'Download résumé (PDF)',
  'hero.availability': 'Open to internships and apprenticeships',
  'hero.focusLabel': 'Focus',
  'hero.focus': 'Web · DevOps · IoT',
  'hero.locationLabel': 'Based in',
  'hero.location': '[City, country]',
  'hero.stackLabel': 'Core stack',
  'hero.stack': 'Astro · Flask · Docker',
  'hero.portraitNote': '[PHOTO — replace with a portrait]',

  // Accueil — projets -----------------------------------------------------
  'home.projects.eyebrow': 'Selected work',
  'home.projects.title': 'Projects designed end to end',
  'home.projects.lead':
    'From discovery to deployment, including testing and monitoring. [TO COMPLETE: one sentence about your approach.]',
  'home.projects.all': 'All projects',

  // Accueil — approche ----------------------------------------------------
  'home.approach.eyebrow': 'Method',
  'home.approach.title': 'Design, build, operate',
  'home.approach.lead':
    'A product does not stop at the code: it is also measured by its readability, its speed and how calmly it can be operated.',
  'approach.design.title': 'Design',
  'approach.design.desc':
    'Frame the need, model the data, and choose the simplest solution that will last.',
  'approach.build.title': 'Build',
  'approach.build.desc':
    'Write typed and tested code, with reusable components and an experience accessible to everyone.',
  'approach.operate.title': 'Operate',
  'approach.operate.desc':
    'Containerise, automate deployments, monitor availability and document the procedures.',

  // Accueil — contact -----------------------------------------------------
  'home.contact.eyebrow': 'Contact',
  'home.contact.title': 'A project, an apprenticeship, a question?',
  'home.contact.lead':
    'The form arrives in the next step. In the meantime, write to me directly by email.',
  'home.contact.cta': 'Send a message',

  // Pages ----------------------------------------------------------------
  'projects.title': 'Projects',
  'projects.lead':
    'Each project covers the context, the problem, the architecture, the challenges faced and the results. [TO COMPLETE]',
  'skills.title': 'Skills',
  'skills.lead':
    'Backend, frontend, DevOps, IoT, databases and tools: the technologies I use, with my level of proficiency. [TO COMPLETE]',
  'career.title': 'Career',
  'career.lead': 'Education, experience and certifications, presented as a timeline. [TO COMPLETE]',
  'blog.title': 'Technical blog',
  'blog.lead': 'Field notes on building, deploying and operating applications. [TO COMPLETE]',
  'contact.title': 'Contact',
  'contact.lead':
    'The form (validation, honeypot and rate limiting) will be added in the next step. Until then: hosayni92@gmail.com.',

  // Divers ---------------------------------------------------------------
  'common.comingSoon':
    '[TO COMPLETE] This section will be filled with the real content in the next step of the project.',
  'common.backHome': 'Back to home',

  // Pied de page ----------------------------------------------------------
  'footer.tagline': 'Digital development and information systems engineer — web, DevOps and IoT.',
  'footer.explore': 'Explore',
  'footer.contact': 'Contact',
  'footer.navLabel': 'Footer links',
  'footer.builtWith': 'Built with Astro, Flask and Docker, deployed by GitHub Actions.',
  'footer.source': 'Source code',
  'footer.rights': 'All rights reserved.',

  // 404 ------------------------------------------------------------------
  'notFound.title': 'Page not found',
  'notFound.lead':
    'The requested page does not exist or has been moved. Use the link below to go back home.',
  'notFound.cta': 'Back to home',
};

export const ui: Record<Lang, Record<UIKey, string>> = { fr, en };
