#!/bin/bash
echo 'updating python dependencies...'
pip install -U -r requirements.txt || exit 1

echo 'running npm update'
npm update || exit 1

./scripts/migrate_and_static.sh || exit 1

echo 'done'
