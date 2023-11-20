optimized for running in docker under nomad.


pruning is performed after forgetting.

Once this gets resolved we can use workload identities: https://github.com/hashicorp/nomad/issues/18755

# creating requirements.txt

poetry export -f requirements.txt -o requirements.txt

# building

docker build . -t jaub/nomad-backup:version

# config options

## JOB
job name

## REPOSITORY
### default: /repository

restic repository path

## PASSWORD_FILE
### default: /secrets/password_file
restic password file path

## BACKUP_PATH
### default: /backup
the path to back up

## MUST_RUN
### default: false
does the job need to be running during the hook

## STOP_JOB
### default: true
should we stop the job before performing the backup

## HOOK
### default: false
do we run the hook

## HOOK_PATH
### default: /local/hook
the path of the hook script

## FORGET
### default: false
do we run a 'restic forget' after performing the backup

## FORGET_KEEP_LAST
## FORGET_KEEP_HOURLY
## FORGET_KEEP_DAILY
## FORGET_KEEP_WEEKLY
## FORGET_KEEP_MONTHLY
## FORGET_KEEP_YEARLY
### default: -1
adjust restic backup forgetting
