./scripts/check-untracked.sh || exit 1

current_branch=$(git symbolic-ref HEAD | sed -e 's,.*/\(.*\),\1,')
if [[ $current_branch == 'broken' || $current_branch == 'kanban' || $current_branch == 'sing_theme' ]]; then
  exit 0
fi

echo 'Running JS tests / coverage...'
gulp test || exit 1
sleep 1 # prevents rsync hang on my env, no idea why -david g

echo 'Attempting rsync to remote git repo...'

function run_local() {
  trap : SIGINT;
  echo 'Failed, running local test / coverage...';
  ./scripts/test-and-coverage.sh || exit 1;
  python ./scripts/measure-coverage.py || exit 1;
  exit 0;
}

trap run_local SIGINT
if (rsync -avz -e /usr/bin/ssh .git/ stg:gallant/.git/); then
  echo 'Running remote test / coverage...'
  ssh stg 'cd gallant; ./scripts/test-remote.sh' || exit 1
else
  run_local
fi
