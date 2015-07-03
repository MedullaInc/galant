echo 'Erasing coverage data...'
./venv/bin/coverage erase
./venv/bin/coverage run --omit="venv/*" manage.py test || exit 1

