#!/bin/sh

python manage.py collectstatic --no-input

gunicorn django_one.wsgi:application -b 0.0.0.0:8001