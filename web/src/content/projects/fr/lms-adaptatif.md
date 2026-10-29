---
lang: fr
translationKey: lms-adaptatif
title: LMS à évaluation adaptative
summary: Plateforme d’apprentissage avec parcours adaptatifs, banque de questions et évaluation personnalisée.
year: '2025'
role: Développement backend et modélisation des données
duration: 5 mois
tags:
  - Flask
  - PostgreSQL
  - TypeScript
  - Docker
stack:
  - Python 3.12
  - Flask
  - PostgreSQL
  - SQLAlchemy
  - TypeScript
  - Docker
featured: true
order: 2
repoUrl: https://github.com/hosayni/
architecture:
  - title: Interface
    items:
      - Parcours apprenant
      - Tableau de bord formateur
  - title: API
    items:
      - Flask et validation des réponses
      - Moteur de sélection des questions
  - title: Données
    items:
      - PostgreSQL (questions, tentatives)
      - Historique de maîtrise par compétence
  - title: Exploitation
    items:
      - Migrations versionnées
      - Sauvegardes et supervision
challenges:
  - 'Éviter les questions trop faciles ou trop difficiles : estimation du niveau par compétence et sélection dans une fenêtre de difficulté.'
  - 'Garantir l’équité entre apprenants : tirage reproductible, pondération par compétence et journalisation des tentatives.'
  - 'Garder des temps de réponse courts malgré l’historique : requêtes agrégées et cache des parcours calculés.'
results:
  - value: '6'
    label: compétences suivies par apprenant
  - value: '-40 %'
    label: de temps de correction manuelle [À COMPLÉTER]
  - value: '120'
    label: apprenants sur la phase de test [À COMPLÉTER]
draft: false
---

## Contexte

[À COMPLÉTER : le cadre du projet, le public visé et le problème pédagogique de
départ.]

## Le problème

[À COMPLÉTER : un même parcours pour tous, des résultats peu exploitables, une
correction chronophage.]

## La solution

Chaque question est rattachée à une compétence et à un niveau de difficulté.
Après chaque tentative, le moteur met à jour une estimation de maîtrise, puis
choisit la question suivante dans une fenêtre qui reste stimulante sans
décourager l’apprenant.

Le modèle de données sépare la banque de questions, les tentatives et les
résultats agrégés. Cette séparation permet de recalculer un parcours sans perdre
l’historique, et de fournir au formateur une vue par compétence plutôt qu’une
simple moyenne.

## Mon rôle

[À COMPLÉTER : ce que tu as conçu et développé — schéma, API, algorithme,
tests.]

## Ce que j’en retiens

[À COMPLÉTER : deux ou trois phrases sur les compromis du projet.]
