./scripts/check-untracked.sh || exit 1

current_branch=$(git symbolic-ref HEAD | sed -e 's,.*/\(.*\),\1,')
if [[ $current_branch == 'broken' || $current_branch == 'kanban' ]]; then
  exit 0
fi

echo 'Running JS tests / coverage...'
gulp test || exit 1

./scripts/test-and-coverage.sh || exit 1
python ./scripts/measure-coverage.py || exit 1
