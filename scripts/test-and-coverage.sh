echo 'Erasing python coverage data...'
./venv/bin/coverage erase
./venv/bin/coverage run --concurrency=multiprocessing manage.py test --parallel 4 --noinput || { rm .coverage*local*; exit 1; }
./venv/bin/coverage combine
