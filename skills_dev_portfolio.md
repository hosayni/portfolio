# SKILLS.md : compétences et standards de développement pour le portfolio

> À donner à l'IA en complément de `prompt_portfolio.md`.
> Ce fichier définit **comment** elle doit coder : design CSS, bonnes pratiques frontend, backend, DevOps, SEO, accessibilité, sécurité, tests et méthode de travail.
> Règle : en cas de conflit, le prompt principal prime sur ce fichier.

---

## 1. Design et styles CSS

### 1.1 Direction artistique recommandée
Style **moderne, sobre et professionnel** : beaucoup d'espace blanc, typographie soignée, une seule couleur d'accent, animations discrètes. Pas de décoration gratuite.

Alternatives (à choisir **une seule** et à appliquer partout) :
| Style | Caractéristiques | Pour qui |
|---|---|---|
| **Minimal / éditorial** (recommandé) | Fond clair ou très sombre, grande typo, grille aérée | Profil sérieux, lisible |
| **Dark tech** | Fond sombre, accent néon discret, police mono pour les détails | Profil DevOps, IoT, cybersécurité |
| **Glassmorphism léger** | Cartes translucides, flou d'arrière-plan, dégradés doux | Effet moderne, à utiliser avec modération |
| **Néo-brutalisme** | Bordures épaisses, couleurs franches, ombres décalées | Personnalité marquée |
| **Bento grid** | Cartes de tailles variées en mosaïque | Présentation de projets |

### 1.2 Design tokens (variables CSS)
Toujours définir les couleurs, espacements et rayons en variables, avec un thème clair et sombre.

```css
:root {
  /* Couleurs */
  --bg: #ffffff;
  --surface: #f6f7f9;
  --text: #14161a;
  --text-muted: #5b6270;
  --border: #e3e6eb;
  --accent: #3b5bfd;
  --accent-contrast: #ffffff;

  /* Typographie */
  --font-sans: "Inter", system-ui, -apple-system, "Segoe UI", sans-serif;
  --font-mono: "JetBrains Mono", ui-monospace, Menlo, monospace;
  --fs-sm: clamp(0.85rem, 0.82rem + 0.15vw, 0.95rem);
  --fs-base: clamp(1rem, 0.96rem + 0.2vw, 1.125rem);
  --fs-h3: clamp(1.25rem, 1.1rem + 0.7vw, 1.6rem);
  --fs-h2: clamp(1.6rem, 1.3rem + 1.4vw, 2.4rem);
  --fs-h1: clamp(2.2rem, 1.6rem + 3vw, 4rem);

  /* Espacements (échelle de 4px) */
  --space-1: 0.25rem; --space-2: 0.5rem; --space-3: 0.75rem;
  --space-4: 1rem;    --space-6: 1.5rem; --space-8: 2rem;
  --space-12: 3rem;   --space-16: 4rem;  --space-24: 6rem;

  /* Forme et élévation */
  --radius-sm: 6px; --radius-md: 12px; --radius-lg: 20px;
  --shadow-sm: 0 1px 2px rgb(0 0 0 / 0.06);
  --shadow-md: 0 8px 24px rgb(0 0 0 / 0.08);

  --container: 72rem;
  --transition: 180ms cubic-bezier(0.2, 0.6, 0.2, 1);
  color-scheme: light dark;
}

:root[data-theme="dark"] {
  --bg: #0d0f12;
  --surface: #151820;
  --text: #eceef2;
  --text-muted: #9aa3b2;
  --border: #262b36;
  --accent: #7c93ff;
  --accent-contrast: #0d0f12;
  --shadow-md: 0 8px 24px rgb(0 0 0 / 0.4);
}

@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg: #0d0f12; --surface: #151820; --text: #eceef2;
    --text-muted: #9aa3b2; --border: #262b36;
    --accent: #7c93ff; --accent-contrast: #0d0f12;
  }
}
```

### 1.3 Base globale
```css
*, *::before, *::after { box-sizing: border-box; }
html { scroll-behavior: smooth; -webkit-text-size-adjust: 100%; }
body {
  margin: 0; background: var(--bg); color: var(--text);
  font: var(--fs-base)/1.65 var(--font-sans);
  -webkit-font-smoothing: antialiased;
}
img, svg, video { max-width: 100%; height: auto; display: block; }
a { color: var(--accent); text-underline-offset: 0.2em; }
h1, h2, h3 { line-height: 1.15; letter-spacing: -0.02em; text-wrap: balance; }
p { text-wrap: pretty; max-width: 68ch; }
:focus-visible { outline: 3px solid var(--accent); outline-offset: 3px; border-radius: 4px; }

.container { width: min(100% - 2rem, var(--container)); margin-inline: auto; }
.section { padding-block: clamp(3rem, 8vw, 7rem); }

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation: none !important; transition: none !important; scroll-behavior: auto !important; }
}
```

### 1.4 Composants types
```css
/* Carte projet */
.card {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: var(--radius-md); padding: var(--space-6);
  transition: transform var(--transition), box-shadow var(--transition), border-color var(--transition);
}
.card:hover { transform: translateY(-4px); box-shadow: var(--shadow-md); border-color: var(--accent); }

/* Boutons */
.btn {
  display: inline-flex; align-items: center; gap: var(--space-2);
  padding: 0.75rem 1.25rem; border-radius: var(--radius-sm);
  font-weight: 600; text-decoration: none; border: 1px solid transparent;
  background: var(--accent); color: var(--accent-contrast); cursor: pointer;
  transition: filter var(--transition), transform var(--transition);
}
.btn:hover { filter: brightness(1.1); transform: translateY(-1px); }
.btn--ghost { background: transparent; color: var(--text); border-color: var(--border); }

/* Badge / tag technologie */
.tag {
  font: 500 var(--fs-sm)/1 var(--font-mono); padding: 0.35rem 0.6rem;
  border: 1px solid var(--border); border-radius: 999px; color: var(--text-muted);
}

/* Grille responsive */
.grid { display: grid; gap: var(--space-6); grid-template-columns: repeat(auto-fill, minmax(min(100%, 18rem), 1fr)); }
```

### 1.5 Techniques à maîtriser et utiliser
- **Mobile-first**, avec `clamp()`, `min()`, `max()` pour la fluidité ; CSS Grid et Flexbox ; `aspect-ratio`; `gap`.
- **Container queries** (`@container`) pour les composants autonomes.
- **Logical properties** (`margin-inline`, `padding-block`) pour le support RTL/i18n.
- **Animations** : `transform` et `opacity` uniquement (GPU), apparition au scroll via `IntersectionObserver` ou `animation-timeline: view()` avec solution de repli.
- **Thème sans flash** : script inline minuscule dans le `<head>` qui applique `data-theme` avant le rendu.
- **Tailwind CSS** : utilisé avec les tokens ci-dessus (étendre `theme` dans la config), classes utilitaires pour la mise en page, `@apply` rarement.
- **Polices** auto-hébergées (WOFF2, sous-ensemble latin), `font-display: swap`, 2 familles maximum.
- **Icônes** en SVG inline ou sprite, jamais de police d'icônes.

### 1.6 Règles de design
1. Une couleur d'accent, des neutres pour le reste ; contraste de texte ≥ **4,5:1** (3:1 pour le grand texte).
2. Hiérarchie visuelle claire : une seule action principale par section.
3. Cohérence : mêmes espacements, rayons et ombres partout.
4. Lisibilité : 60 à 75 caractères par ligne, interligne de 1,5 à 1,7.
5. Zones tactiles ≥ 44×44 px.
6. Pas de texte dans les images, pas de carrousel automatique, pas de pop-up intrusif.

---

## 2. Frontend (Astro + TypeScript)

- **Astro** : composants `.astro`, *content collections* avec schéma Zod pour projets et articles, îlots interactifs (`client:visible` / `client:idle`) seulement quand nécessaire, `astro:assets` pour les images.
- **TypeScript strict** : pas de `any`, types partagés, `astro check` en CI.
- **i18n** : dictionnaires JSON typés, routes `/fr/` et `/en/`, `hreflang`, contenus traduits côte à côte.
- **Structure** : composants petits et réutilisables, un layout de base, aucune logique métier dans les templates.
- **JavaScript minimal** : préférer HTML/CSS ; pas de bibliothèque lourde pour une animation simple.
- **Formulaires** : validation HTML5 + validation serveur, messages d'erreur accessibles (`aria-live`), état de chargement et de succès.
- **Gestion d'erreur** : contenu de repli si l'API est indisponible.

---

## 3. Backend (Python + Flask)

- **Application factory**, blueprints, configuration par variables d'environnement (`config.py`).
- **Validation** des entrées (schémas Pydantic ou validation manuelle stricte), réponses JSON cohérentes (`{"error": "..."}` + code HTTP adapté).
- **Sécurité** : Flask-Limiter (rate limiting), CORS restreint, en-têtes de sécurité, pas de `debug=True` en production, requêtes sortantes avec timeout.
- **Cache** : mémoire ou fichier avec durée de vie (ex. 1 h pour l'API GitHub), gestion des quotas.
- **Logs structurés** (JSON), niveaux adaptés, aucune donnée personnelle sensible dans les logs.
- **Tests Pytest** : client de test Flask, mock des appels externes, cas d'erreur, couverture ≥ 80 %.
- **Typage** : annotations de type, `ruff` pour lint et format.

---

## 4. DevOps

- **Git** : branches courtes, pull requests petites, commits conventionnels, `main` protégée.
- **Docker** : multi-stage, images minimales, utilisateur non-root, `HEALTHCHECK`, `.dockerignore`, versions épinglées, scan avec Trivy.
- **Docker Compose** : réseaux séparés, aucun port publié sauf Caddy, `restart: unless-stopped`, limites de ressources, volumes nommés.
- **GitHub Actions** : cache des dépendances, jobs parallèles, `concurrency`, permissions minimales (`permissions:`), environments avec approbation, secrets uniquement via `secrets.*`, actions épinglées sur une version majeure (ou SHA).
- **Déploiement** : zéro intervention manuelle, healthcheck après déploiement, rollback par tag SHA.
- **Infrastructure** : Caddy pour HTTPS automatique, UFW, Fail2ban, mises à jour automatiques, utilisateur `deploy` non-root, SSH par clé.
- **Observabilité** : Uptime Kuma, `docker compose logs`, alertes (email ou Telegram).
- **Reproductibilité** : tout est dans Git (sauf secrets) ; documentation de la remise en route du VPS.

---

## 5. SEO technique

- Balises : `<title>` (≤ 60 caractères), meta description (≤ 160), canonical, Open Graph, Twitter Cards, `hreflang`.
- **JSON-LD** : `Person`, `WebSite`, `BlogPosting`, `BreadcrumbList`, `CreativeWork`.
- `sitemap.xml`, `robots.txt`, flux RSS, URLs propres et stables, redirections 301.
- Un seul `<h1>`, titres hiérarchisés, texte réel et utile, maillage interne entre projets et articles.
- Images : `alt`, dimensions explicites, formats modernes, `loading="lazy"` hors zone visible, `fetchpriority="high"` pour l'image principale.
- **Core Web Vitals** : LCP < 2,5 s, CLS < 0,1, INP < 200 ms.
- Mesure : Lighthouse, PageSpeed Insights, Google Search Console.

---

## 6. Accessibilité (WCAG 2.2 AA)

- HTML sémantique (`header`, `nav`, `main`, `section`, `footer`), lien d'évitement « Aller au contenu ».
- Navigation 100 % clavier, focus visible, ordre logique.
- Libellés de formulaires associés (`label for`), erreurs annoncées, `aria-*` seulement quand le HTML natif ne suffit pas.
- Contrastes conformes, information jamais portée par la couleur seule.
- `prefers-reduced-motion` respecté, textes agrandissables jusqu'à 200 %.
- Test avec axe DevTools et au lecteur d'écran.

---

## 7. Sécurité applicative

- Aucune clé ni mot de passe dans le code ; `.env` dans `.gitignore` ; fichier `.env.example` fourni.
- Validation et échappement de toutes les entrées ; protection anti-spam (honeypot, rate limiting).
- En-têtes : `Content-Security-Policy`, `X-Content-Type-Options`, `Referrer-Policy`, `Strict-Transport-Security`, `Permissions-Policy`.
- Dépendances surveillées (Dependabot, `npm audit`, `pip-audit`).
- Principe du moindre privilège (conteneurs, tokens GitHub, utilisateur SSH).
- Conformité de base : mentions légales, politique de confidentialité, pas de traceurs sans consentement.

---

## 8. Tests et qualité

- **Frontend** : ESLint, Prettier, `astro check`, Playwright (parcours : accueil, changement de langue, contact), Lighthouse CI avec seuils.
- **Backend** : Pytest, Ruff.
- **Pipeline** : aucun merge si la CI est rouge.
- Revue de code avant fusion (même seul : relire sa propre pull request).
- Définition de « terminé » : fonctionne en local et en production, testé, documenté, accessible, rapide.

---

## 9. Documentation

- `README.md` : objectif, stack, lancement local, structure, variables d'environnement, déploiement, badges CI.
- `docs/DEPLOIEMENT.md` : procédure complète et rollback.
- Schéma d'architecture (Mermaid dans le README).
- Commentaires utiles : expliquer le **pourquoi**, pas le **quoi**.
- Journal des décisions techniques (ADR) court pour les choix importants.

---

## 10. Méthode de travail attendue de l'IA

1. **Comprendre** : poser au plus 5 questions si une information manque, puis proposer un plan.
2. **Avancer par petites étapes** : un sujet à la fois, avec validation avant la suite.
3. **Livrer du code complet** : chemin du fichier, contenu entier, commandes, vérification attendue. Jamais de `...`.
4. **Expliquer brièvement** les choix, et signaler les compromis.
5. **Signaler les incertitudes** (versions, comportements récents) au lieu d'inventer.
6. **Prévenir des risques** : commandes destructrices, modifications SSH, secrets à protéger.
7. **Vérifier** avant de conclure : lint, tests, build, healthcheck.
8. **Rester simple** : la solution la plus simple qui répond au besoin l'emporte sur la plus sophistiquée.

---

## 11. Checklist finale de livraison

- [ ] Design cohérent, thème clair/sombre, responsive de 320 px à 1920 px
- [ ] Bilingue FR/EN avec `hreflang`
- [ ] Lighthouse ≥ 95 sur les 4 catégories (mobile)
- [ ] Données structurées validées, sitemap et robots.txt en place
- [ ] Accessibilité vérifiée (clavier, contrastes, lecteur d'écran)
- [ ] CI verte, déploiement automatique, healthcheck et rollback testés
- [ ] HTTPS actif, `www` redirigé, en-têtes de sécurité présents
- [ ] Aucun secret dans l'historique Git
- [ ] README et guide de déploiement à jour
- [ ] Site soumis à Google Search Console
