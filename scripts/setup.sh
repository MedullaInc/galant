echo 'copying pre-push git hook into .git/hooks/'
echo 'python manage.py test' > .git/hooks/pre-push
chmod u+x .git/hooks/pre-push
