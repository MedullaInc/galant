./scripts/check-untracked.sh || exit 1

current_branch=$(git symbolic-ref HEAD | sed -e 's,.*/\(.*\),\1,')
if [[ $current_branch == 'broken' ]]; then
  exit 0
fi

echo 'Running JS tests / coverage...'
gulp test || exit 1

rsync -avz -e ssh .git/ stg:gallant/.git/
ssh stg 'cd gallant; ./scripts/test-remote.sh'
