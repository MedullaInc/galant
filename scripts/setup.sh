echo 'copying pre-push git hooks into .git/hooks/ ...'

echo './scripts/git-pre-push.sh || exit 1' > .git/hooks/pre-push
chmod u+x .git/hooks/pre-push

echo 'done'
