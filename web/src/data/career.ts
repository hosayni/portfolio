import type { Lang } from '../i18n/ui';

export type CareerKind = 'education' | 'experience' | 'certification';

export interface CareerItem {
  kind: CareerKind;
  period: string;
  current?: boolean;
  title: Record<Lang, string>;
  organization: string;
  location: string;
  description: Record<Lang, string>;
  tags?: readonly string[];
}

/** Frise du parcours, du plus récent au plus ancien. */
export const careerItems: readonly CareerItem[] = [
  {
    kind: 'education',
    period: '2024 — 2027',
    current: true,
    title: {
      fr: 'Cycle ingénieur — développement digital et systèmes d’information',
      en: 'Engineering degree — digital development and information systems',
    },
    organization: '[À COMPLÉTER : établissement]',
    location: '[Ville, pays]',
    description: {
      fr: 'Formation d’ingénieur centrée sur le développement d’applications, les systèmes d’information et l’exploitation. Projets en équipe, architecture logicielle, bases de données et DevOps.',
      en: 'Engineering programme focused on application development, information systems and operations. Team projects, software architecture, databases and DevOps.',
    },
    tags: ['Architecture', 'Bases de données', 'DevOps'],
  },
  {
    kind: 'experience',
    period: '2025 — 2026',
    current: true,
    title: {
      fr: 'Développeur full-stack — projets personnels et missions ponctuelles',
      en: 'Full-stack developer — personal projects and short engagements',
    },
    organization: 'Indépendant',
    location: 'À distance',
    description: {
      fr: 'Conception et développement d’applications web : API Flask, interfaces Astro/TypeScript, conteneurisation et déploiement sur VPS. [À COMPLÉTER : missions réelles.]',
      en: 'Design and development of web applications: Flask APIs, Astro/TypeScript interfaces, containerisation and VPS deployment. [TO COMPLETE: actual engagements.]',
    },
    tags: ['Flask', 'Astro', 'Docker'],
  },
  {
    kind: 'experience',
    period: '2025',
    title: {
      fr: 'Stage — développement web et données',
      en: 'Internship — web development and data',
    },
    organization: '[À COMPLÉTER : entreprise]',
    location: '[Ville, pays]',
    description: {
      fr: '[À COMPLÉTER : missions, stack utilisée, résultats obtenus.]',
      en: '[TO COMPLETE: assignments, stack used, results achieved.]',
    },
    tags: ['[À COMPLÉTER]'],
  },
  {
    kind: 'education',
    period: '2022 — 2024',
    title: {
      fr: 'Classes préparatoires / licence — informatique',
      en: 'Preparatory classes / bachelor — computer science',
    },
    organization: '[À COMPLÉTER : établissement]',
    location: '[Ville, pays]',
    description: {
      fr: 'Fondamentaux de l’algorithmique, des mathématiques appliquées et des systèmes. [À COMPLÉTER : intitulé exact du diplôme.]',
      en: 'Foundations of algorithms, applied mathematics and systems. [TO COMPLETE: exact degree title.]',
    },
  },
  {
    kind: 'certification',
    period: '2026',
    title: {
      fr: 'Certification — [À COMPLÉTER]',
      en: 'Certification — [TO COMPLETE]',
    },
    organization: '[Organisme]',
    location: 'En ligne',
    description: {
      fr: 'Certification obtenue ou en préparation. Remplacer par l’intitulé exact et le lien de vérification.',
      en: 'Certification obtained or in progress. Replace with the exact title and verification link.',
    },
  },
];
