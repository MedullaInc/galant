echo 'Erasing python coverage data...'
./venv/bin/coverage erase
python ./scripts/test-nose-picker.py || { rm .coverage*local*; exit 1; }
./venv/bin/coverage combine

