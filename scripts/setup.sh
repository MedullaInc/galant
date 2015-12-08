#!/bin/bash
echo 'copying pre-push git hooks into .git/hooks/ ...'

echo './scripts/git-pre-push.sh || exit 1' > .git/hooks/pre-push
chmod u+x .git/hooks/pre-push

echo 'creating venv...'
virtualenv venv || exit 1

echo 'activating...'
source venv/bin/activate || exit 1

./scripts/update_modules.sh || exit 1

echo 'running localization...'
python manage.py compilemessages || exit 1

echo 'updating exchange rates...'
python manage.py update_rates || exit 1

echo 'creating example quote / brief templates...'
python manage.py load_quote || exit 1
python manage.py load_brief || exit 1

echo 'done'
