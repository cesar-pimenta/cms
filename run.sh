#!/bin/bash

source venv/bin/activate

python manage.py migrate
python manage.py collectstatic --noinput 2>/dev/null || true

python manage.py runserver
