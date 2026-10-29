---
lang: fr
translationKey: smart-farm-iot
title: Smart Farm IoT
summary: 'Plateforme d’irrigation connectée : capteurs de sol, décisions automatiques et tableau de bord temps réel.'
year: '2025'
role: Développement full-stack et IoT
duration: 4 mois
tags:
  - IoT
  - Python
  - MQTT
  - Flask
  - PostgreSQL
stack:
  - ESP32
  - Python 3.12
  - Flask
  - MQTT (Mosquitto)
  - PostgreSQL
  - Docker
  - Chart.js
featured: true
order: 1
repoUrl: https://github.com/hosayni/
demoUrl: https://github.com/hosayni/
architecture:
  - title: Terrain
    items:
      - Capteurs d’humidité du sol
      - ESP32 et relais de pompe
  - title: Messagerie
    items:
      - Broker MQTT Mosquitto
      - Un topic par parcelle
  - title: Application
    items:
      - API Flask et règles d’irrigation
      - PostgreSQL (mesures, parcelles)
  - title: Supervision
    items:
      - Tableau de bord temps réel
      - Docker Compose et healthchecks
challenges:
  - 'Fiabiliser la remontée de mesures sur un réseau instable : file d’attente locale sur l’ESP32 et reconnexion automatique au broker.'
  - 'Éviter les irrigations inutiles en combinant humidité du sol, prévision météo et seuils par culture.'
  - 'Garder une latence faible sur le tableau de bord sans surcharger la base : agrégation côté API et index sur les séries temporelles.'
results:
  - value: '-28 %'
    label: d’eau consommée sur la parcelle pilote [À COMPLÉTER]
  - value: '< 2 s'
    label: entre la mesure et son affichage
  - value: 99,5 %
    label: de mesures reçues sur 30 jours [À COMPLÉTER]
draft: false
---

## Contexte

[À COMPLÉTER : le cadre du projet — cursus, équipe, durée, commanditaire ou
parcelle pilote.]

## Le problème

[À COMPLÉTER : le problème concret observé sur le terrain — irrigation
manuellement déclenchée, gaspillage d’eau, absence de visibilité sur l’état des
parcelles.]

## La solution

La plateforme découpe le problème en quatre couches indépendantes. Les capteurs
publient leurs mesures sur un broker MQTT ; l’API Flask consomme ces messages,
applique les règles d’irrigation et persiste les séries temporelles dans
PostgreSQL. Un tableau de bord affiche l’état des parcelles et l’historique des
décisions.

Les règles restent volontairement lisibles : un seuil d’humidité par culture,
une fenêtre horaire, et un garde-fou qui empêche deux déclenchements
consécutifs. Le but n’est pas de remplacer l’agriculteur, mais de lui donner une
information fiable et une action automatique réversible.

## Mon rôle

[À COMPLÉTER : ce que tu as réalisé personnellement — firmware, API, modèle de
données, déploiement, tests.]

## Ce que j’en retiens

[À COMPLÉTER : deux ou trois phrases sur ce que tu ferais différemment ou ce que
tu as appris.]
