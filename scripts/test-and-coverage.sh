echo 'Erasing python coverage data...'
./venv/bin/coverage erase
./venv/bin/coverage run manage.py test --noinput || { rm .coverage*local*; exit 1; }

