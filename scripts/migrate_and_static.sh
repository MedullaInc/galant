#!/bin/bash

source ./venv/bin/activate

echo 'running migrate...'
python manage.py migrate || exit 1

echo 'running gulp static'
gulp static || exit 1

echo 'collecting static files...'
python manage.py collectstatic -l --noinput || exit 1