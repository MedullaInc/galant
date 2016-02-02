export DJANGO_SETTINGS_MODULE=gallant.settings.stg_ec2
git checkout .

echo 'Erasing python coverage data...'
./venv/bin/coverage erase
./venv/bin/coverage run --concurrency=multiprocessing manage.py test --parallel --noinput || { rm .coverage*local*; exit 1; }
./venv/bin/coverage combine
python ./scripts/measure-coverage.py || exit 1
