import type { Lang } from '../i18n/ui';

export type SkillLevel = 'advanced' | 'intermediate' | 'beginner';

export interface Skill {
  name: string;
  level: SkillLevel;
}

export interface SkillGroup {
  key: string;
  label: Record<Lang, string>;
  description: Record<Lang, string>;
  skills: Skill[];
}

/**
 * Compétences regroupées. Les niveaux restent indicatifs : ils servent à
 * hiérarchiser visuellement, jamais à porter l'information seuls (le niveau
 * est aussi écrit en toutes lettres).
 */
export const skillGroups: readonly SkillGroup[] = [
  {
    key: 'backend',
    label: { fr: 'Backend', en: 'Backend' },
    description: {
      fr: 'API, logique métier et données.',
      en: 'APIs, business logic and data.',
    },
    skills: [
      { name: 'Python', level: 'advanced' },
      { name: 'Flask', level: 'advanced' },
      { name: 'SQLAlchemy', level: 'intermediate' },
      { name: 'Pytest', level: 'intermediate' },
      { name: 'REST', level: 'advanced' },
    ],
  },
  {
    key: 'frontend',
    label: { fr: 'Frontend', en: 'Frontend' },
    description: {
      fr: 'Interfaces rapides, accessibles et typées.',
      en: 'Fast, accessible and typed interfaces.',
    },
    skills: [
      { name: 'TypeScript', level: 'intermediate' },
      { name: 'Astro', level: 'intermediate' },
      { name: 'Tailwind CSS', level: 'intermediate' },
      { name: 'HTML / CSS', level: 'advanced' },
      { name: 'Accessibilité', level: 'intermediate' },
    ],
  },
  {
    key: 'devops',
    label: { fr: 'DevOps', en: 'DevOps' },
    description: {
      fr: 'Conteneurs, automatisation et exploitation.',
      en: 'Containers, automation and operations.',
    },
    skills: [
      { name: 'Linux', level: 'intermediate' },
      { name: 'Docker', level: 'intermediate' },
      { name: 'GitHub Actions', level: 'intermediate' },
      { name: 'Caddy / nginx', level: 'intermediate' },
      { name: 'Bash', level: 'intermediate' },
    ],
  },
  {
    key: 'iot',
    label: { fr: 'IoT', en: 'IoT' },
    description: {
      fr: 'Du capteur au tableau de bord.',
      en: 'From sensor to dashboard.',
    },
    skills: [
      { name: 'ESP32', level: 'intermediate' },
      { name: 'MQTT', level: 'intermediate' },
      { name: 'Capteurs', level: 'intermediate' },
      { name: 'C / Arduino', level: 'beginner' },
    ],
  },
  {
    key: 'databases',
    label: { fr: 'Bases de données', en: 'Databases' },
    description: {
      fr: 'Modélisation, requêtes et migrations.',
      en: 'Modelling, queries and migrations.',
    },
    skills: [
      { name: 'PostgreSQL', level: 'intermediate' },
      { name: 'SQL', level: 'advanced' },
      { name: 'Redis', level: 'beginner' },
      { name: 'Modélisation', level: 'intermediate' },
    ],
  },
  {
    key: 'tools',
    label: { fr: 'Outils', en: 'Tools' },
    description: {
      fr: 'Le quotidien du développement.',
      en: 'The everyday toolkit.',
    },
    skills: [
      { name: 'Git', level: 'advanced' },
      { name: 'GitHub', level: 'advanced' },
      { name: 'Ruff', level: 'intermediate' },
      { name: 'ESLint / Prettier', level: 'intermediate' },
      { name: 'Postman', level: 'intermediate' },
    ],
  },
];
