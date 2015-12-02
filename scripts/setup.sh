#!/bin/bash
echo 'copying pre-push git hooks into .git/hooks/ ...'

echo './scripts/git-pre-push.sh || exit 1' > .git/hooks/pre-push
chmod u+x .git/hooks/pre-push

echo 'creating venv...'
virtualenv venv || exit 1

echo 'activating...'
source venv/bin/activate || exit 1

echo 'installing dependencies...'
pip install -r requirements.txt || exit 1

echo 'running migrate...'
python manage.py migrate || exit 1

echo 'collecting static files...'
python manage.py collectstatic || exit 1

echo 'running localization...'
python manage.py compilemessages || exit 1

echo 'updating exchange rates...'
python manage.py update_rates || exit 1

echo 'creating example quote / brief templates...'
python manage.py load_quote || exit 1
python manage.py load_brief || exit 1

echo 'running npm install'
npm install || exit 1

echo 'running gulp tasks'
gulp || exit 1

echo 'done'
