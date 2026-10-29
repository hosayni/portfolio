---
lang: en
translationKey: lms-adaptatif
title: Adaptive assessment LMS
summary: Learning platform with adaptive paths, a question bank and personalised assessment.
year: '2025'
role: Backend development and data modelling
duration: 5 months
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
      - Learner path
      - Instructor dashboard
  - title: API
    items:
      - Flask and answer validation
      - Question selection engine
  - title: Data
    items:
      - PostgreSQL (questions, attempts)
      - Mastery history per skill
  - title: Operations
    items:
      - Versioned migrations
      - Backups and monitoring
challenges:
  - 'Avoiding questions that are too easy or too hard: per-skill level estimation and selection within a difficulty window.'
  - 'Ensuring fairness between learners: reproducible draw, skill weighting and attempt logging.'
  - 'Keeping response times short despite the history: aggregate queries and cached computed paths.'
results:
  - value: '6'
    label: skills tracked per learner
  - value: '-40%'
    label: manual grading time [TO COMPLETE]
  - value: '120'
    label: learners in the test phase [TO COMPLETE]
draft: false
---

## Context

[TO COMPLETE: the project setting, the target audience and the initial learning
problem.]

## The problem

[TO COMPLETE: one path for everyone, barely actionable results, time-consuming
grading.]

## The solution

Each question is linked to a skill and a difficulty level. After every attempt,
the engine updates a mastery estimate, then picks the next question within a
window that stays challenging without discouraging the learner.

The data model separates the question bank, attempts and aggregated results.
That separation makes it possible to recompute a path without losing history,
and to give instructors a per-skill view instead of a single average.

## My role

[TO COMPLETE: what you designed and built — schema, API, algorithm, tests.]

## What I take away

[TO COMPLETE: two or three sentences about the project trade-offs.]
