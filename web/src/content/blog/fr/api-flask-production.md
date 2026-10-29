---
lang: fr
translationKey: flask-api-production
title: Trois garde-fous pour une API Flask en production
description: 'Validation, limitation de débit et en-têtes de sécurité : le minimum avant d’exposer un formulaire public.'
pubDate: 2026-10-02
tags:
  - Flask
  - Python
  - Sécurité
draft: false
---

## Le problème

Une API Flask qui fonctionne en local n’est pas une API prête pour Internet. Un
formulaire de contact public attire les robots, les charges utiles malformées et
les tentatives d’injection. Trois garde-fous suffisent à couvrir l’essentiel.

## 1. Valider avant de traiter

La validation HTML côté navigateur est une commodité, pas une sécurité. Le
serveur doit revalider chaque champ, avec des limites explicites.

```python
from flask import request

MAX_MESSAGE = 5_000

def read_contact_payload() -> dict[str, str]:
    payload = request.get_json(silent=True) or {}
    name = str(payload.get("name", "")).strip()
    email = str(payload.get("email", "")).strip()
    message = str(payload.get("message", "")).strip()

    if not name or len(name) > 120:
        raise ValueError("invalid_name")
    if "@" not in email or len(email) > 254:
        raise ValueError("invalid_email")
    if not message or len(message) > MAX_MESSAGE:
        raise ValueError("invalid_message")

    return {"name": name, "email": email, "message": message}
```

Le honeypot complète la validation : un champ caché que seuls les robots
remplissent. S’il est rempli, la requête est rejetée sans explication.

## 2. Limiter le débit

Sans limitation, un script peut envoyer des milliers de messages ou saturer le
serveur SMTP. Flask-Limiter s’applique par adresse IP et par route.

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(get_remote_address, app=app, default_limits=["120 per hour"])

@app.post("/api/contact")
@limiter.limit("5 per hour")
def contact():
    ...
```

La limite doit être assez basse pour protéger, assez haute pour ne pas bloquer
un utilisateur légitime qui corrige une faute de frappe.

## 3. Poser les en-têtes au bon endroit

Les en-têtes de sécurité peuvent être ajoutés par le proxy, mais l’API doit
rester correcte même si elle est appelée directement. Un `after_request` unique
évite les oublis.

```python
@app.after_request
def security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Cache-Control"] = "no-store"
    return response
```

## Et les erreurs ?

Une API publique doit répondre en JSON, même quand tout va mal. Un gestionnaire
d’erreurs global transforme les exceptions en réponses cohérentes
(`{"error": "..."}`) avec le bon code HTTP, sans jamais divulguer la trace
interne.

Ces garde-fous ne rendent pas une application invulnérable, mais ils éliminent
les erreurs les plus fréquentes — et ils se testent, ce qui compte autant que le
code lui-même.
