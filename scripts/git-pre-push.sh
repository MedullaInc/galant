./scripts/check-untracked.sh || exit 1

current_branch=$(git symbolic-ref HEAD | sed -e 's,.*/\(.*\),\1,')
if [[ $current_branch == 'broken' ]]; then
  exit 0
fi

./scripts/test-and-coverage.sh || exit 1
python ./scripts/measure-coverage.py || exit 1