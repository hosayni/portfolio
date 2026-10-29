---
lang: en
translationKey: smart-farm-iot
title: Smart Farm IoT
summary: 'Connected irrigation platform: soil sensors, automatic decisions and a real-time dashboard.'
year: '2025'
role: Full-stack and IoT development
duration: 4 months
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
  - title: Field
    items:
      - Soil moisture sensors
      - ESP32 and pump relay
  - title: Messaging
    items:
      - Mosquitto MQTT broker
      - One topic per plot
  - title: Application
    items:
      - Flask API and irrigation rules
      - PostgreSQL (readings, plots)
  - title: Monitoring
    items:
      - Real-time dashboard
      - Docker Compose and healthchecks
challenges:
  - 'Making sensor readings reliable on an unstable network: local queue on the ESP32 and automatic broker reconnection.'
  - 'Avoiding unnecessary irrigation by combining soil moisture, weather forecast and per-crop thresholds.'
  - 'Keeping dashboard latency low without overloading the database: API-side aggregation and indexes on time series.'
results:
  - value: '-28%'
    label: water used on the pilot plot [TO COMPLETE]
  - value: '< 2 s'
    label: between a reading and its display
  - value: 99.5%
    label: readings received over 30 days [TO COMPLETE]
draft: false
---

## Context

[TO COMPLETE: the project setting — course, team, duration, client or pilot
plot.]

## The problem

[TO COMPLETE: the concrete problem observed in the field — manual irrigation,
water waste, no visibility over plot conditions.]

## The solution

The platform splits the problem into four independent layers. Sensors publish
readings to an MQTT broker; the Flask API consumes those messages, applies the
irrigation rules and stores time series in PostgreSQL. A dashboard shows plot
status and the history of decisions.

The rules are deliberately readable: one moisture threshold per crop, a time
window, and a guard that prevents two consecutive triggers. The goal is not to
replace the farmer, but to provide reliable information and a reversible
automatic action.

## My role

[TO COMPLETE: what you personally built — firmware, API, data model, deployment,
tests.]

## What I take away

[TO COMPLETE: two or three sentences about what you would do differently or what
you learned.]
