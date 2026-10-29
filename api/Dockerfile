# ---------------------------------------------------------------------------
# API Flask : dépendances installées dans un venv, puis copiées dans une image
# d'exécution minimale. Gunicorn tourne avec un utilisateur non-root.
# ---------------------------------------------------------------------------
FROM python:3.15.0-slim-trixie AS builder

ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

# Cible de développement : ajoute les outils de test et le code source.
FROM builder AS dev

COPY requirements-dev.txt ./
RUN pip install -r requirements-dev.txt

COPY . .

RUN groupadd --system app \
    && useradd --uid 1000 --gid app --create-home --shell /bin/bash app \
    && chown -R app:app /app

USER app

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/api/health', timeout=3)"

CMD ["flask", "--app", "wsgi", "run", "--host", "0.0.0.0", "--port", "8000", "--debug"]

# Cible de production : uniquement le venv, l'application et Gunicorn.
FROM python:3.15.0-slim-trixie AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HOME=/tmp \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
COPY app ./app
COPY wsgi.py ./

RUN groupadd --system app \
    && useradd --uid 10001 --gid app --no-create-home --shell /usr/sbin/nologin app \
    && chown -R app:app /app

USER app

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/api/health', timeout=3)"

# Un seul worker avec plusieurs threads : le cache GitHub et le rate limiting
# sont en mémoire. Passer à Redis/Gunicorn multi-workers avant de scaler.
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "1", "--threads", "4", "--worker-class", "gthread", "--timeout", "30", "--graceful-timeout", "10", "--no-control-socket", "--access-logfile", "-", "--error-logfile", "-", "wsgi:app"]
