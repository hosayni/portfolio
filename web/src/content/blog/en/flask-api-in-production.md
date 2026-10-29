---
lang: en
translationKey: flask-api-production
title: Three safeguards for a production Flask API
description: 'Validation, rate limiting and security headers: the minimum before exposing a public form.'
pubDate: 2026-10-02
tags:
  - Flask
  - Python
  - Security
draft: false
---

## The problem

A Flask API that works locally is not an API ready for the Internet. A public
contact form attracts bots, malformed payloads and injection attempts. Three
safeguards cover the essentials.

## 1. Validate before processing

Browser-side HTML validation is a convenience, not security. The server must
revalidate every field, with explicit limits.

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

The honeypot complements validation: a hidden field that only bots fill in. If
it is filled, the request is rejected without explanation.

## 2. Rate limit

Without a limit, a script can send thousands of messages or saturate the SMTP
server. Flask-Limiter applies per IP address and per route.

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(get_remote_address, app=app, default_limits=["120 per hour"])

@app.post("/api/contact")
@limiter.limit("5 per hour")
def contact():
    ...
```

The limit must be low enough to protect, high enough not to block a legitimate
user fixing a typo.

## 3. Put headers in the right place

Security headers can be added by the proxy, but the API must remain correct even
when called directly. A single `after_request` avoids omissions.

```python
@app.after_request
def security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Cache-Control"] = "no-store"
    return response
```

## What about errors?

A public API must answer in JSON, even when everything goes wrong. A global
error handler turns exceptions into consistent responses (`{"error": "..."}`)
with the right HTTP status, without ever leaking the internal trace.

These safeguards do not make an application invulnerable, but they remove the
most common mistakes — and they can be tested, which matters as much as the code
itself.
