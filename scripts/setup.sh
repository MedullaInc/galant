echo 'copying pre-push git hooks into .git/hooks/ ...'

echo './scripts/check-untracked.sh || exit 1' > .git/hooks/pre-push
echo 'python manage.py test' >> .git/hooks/pre-push
chmod u+x .git/hooks/pre-push

echo 'done'
