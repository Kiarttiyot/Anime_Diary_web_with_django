#!/usr/bin/env bash
set -e

echo ">> Running migrations..."
python manage.py migrate --noinput

# Collect static (ถ้ามี)
if [ -d "static" ] || [ -n "${STATIC_ROOT:-}" ]; then
  echo ">> Collecting static files..."
  python manage.py collectstatic --noinput || true
fi

echo ">> Starting Django dev server at 0.0.0.0:8000"
exec python manage.py runserver 0.0.0.0:8000