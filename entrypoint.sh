#!/usr/bin/env bash
set -e

echo ">> Running migrations..."
python manage.py migrate --noinput

echo ">> Collecting static files..."
python manage.py collectstatic --noinput || true

echo ">> Starting Gunicorn on 0.0.0.0:8000"
exec gunicorn ProjectAnimeDiary.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 3 \
  --threads 2 \
  --timeout 120 \
  --graceful-timeout 30 \
  --max-requests 1000 \
  --max-requests-jitter 200 \
  --log-level info
