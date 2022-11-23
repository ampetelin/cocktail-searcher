#!/bin/bash

set -e

if [ "$1" = 'gunicorn' ]; then
  echo ">>> Run migrations"
  python manage.py migrate --no-input

  echo -e "\n>>> Collecting django static files"
  python manage.py collectstatic --no-input

  echo -e "\n>>> Compiling message files"
  python manage.py compilemessages

  echo -e "\n>>> Run Gunicorn"
  exec "$@"
fi

exec "$@"