./scripts/check-untracked.sh || exit 1

echo 'rsyncing to remote git repo...'
rsync -avz -e ssh .git/ stg:gallant/.git/ || exit 1
echo 'running remote test / coverage...'
ssh stg '
cd gallant;
export DJANGO_SETTINGS_MODULE=gallant.settings.stg_ec2;
git checkout .;
source ./venv/bin/activate;
python manage.py test --parallel --noinput -k;
'