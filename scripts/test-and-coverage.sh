echo 'Erasing coverage data...'
./venv/bin/coverage erase
python ./scripts/test-nose-picker.py || exit 1
./venv/bin/coverage combine

