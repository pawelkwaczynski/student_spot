#!/bin/sh
set -eu

APP_PORT="${APP_PORT:-8000}"

if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi

. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

flask --app wsgi:app init-db
flask --app wsgi:app seed-demo

exec gunicorn --workers 1 --threads 2 --timeout 60 --bind "0.0.0.0:${APP_PORT}" wsgi:app
