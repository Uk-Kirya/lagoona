#!/bin/bash
set -e

# Кол-во воркеров = 2 * cores + 1
CORES=$(nproc || echo 4)
WORKERS=$((2 * CORES + 1))

echo "Running migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn with $WORKERS workers..."
exec gunicorn kd.wsgi:application --bind 0.0.0.0:8000 --workers $WORKERS