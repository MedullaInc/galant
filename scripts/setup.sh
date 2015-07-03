echo 'copying pre-push git hooks into .git/hooks/ ...'

echo './scripts/check-untracked.sh || exit 1' > .git/hooks/pre-push
echo './scripts/test-and-coverage.sh || exit 1' >> .git/hooks/pre-push
echo 'python ./scripts/measure-coverage.py || exit 1' >> .git/hooks/pre-push
chmod u+x .git/hooks/pre-push

echo 'done'
