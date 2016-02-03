./scripts/check-untracked.sh || exit 1

current_branch=$(git symbolic-ref HEAD | sed -e 's,.*/\(.*\),\1,')
if [[ $current_branch == 'broken' ]]; then
  exit 0
fi

echo 'Running JS tests / coverage...'
gulp test || exit 1

echo 'rsyncing to remote git repo...'
rsync -avz -e ssh .git/ stg:gallant/.git/
echo 'running remote test / coverage...'
ssh stg 'cd gallant; ./scripts/test-remote.sh'
