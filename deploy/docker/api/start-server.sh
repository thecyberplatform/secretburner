#!/bin/sh
if [[ -z ${WORKERS} ]]; then
    WORKERS=1
fi

if [[ "${APP_ENV}" != "local" ]]; then
    echo "Starting Production ASGI"

    python /app/manage.py migrate &&
    python /app/manage.py createcachetable &&
    daphne -p 80 -b 0.0.0.0 config.asgi:application

else
    echo "Starting Local Run Server"
    python /app/manage.py migrate &&
    python /app/manage.py createcachetable &&
    python /app/manage.py runserver 0.0.0.0:8000
fi
