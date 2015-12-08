#!/bin/bash
echo 'running migrate...'
python manage.py migrate || exit 1

echo 'running gulp tasks'
gulp || exit 1

echo 'collecting static files...'
python manage.py collectstatic -l --noinput || exit 1