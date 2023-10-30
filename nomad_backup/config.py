import os

# the job we're backing up
JOB: str = os.getenv('JOB')
if not JOB:
    raise ValueError('The job must be specified.')

# path of the restic repository
REPOSITORY: str = os.getenv('REPOSITORY', '/repository')
PASSWORD_FILE: str = os.getenv('PASSWORD_FILE')
if not PASSWORD_FILE:
    # default to /secrets/password_file in nomad
    if os.getenv('NOMAD_SECRETS_DIR'):
        HOOK_PATH: str = os.getenv('NOMAD_SECRETS_DIR') + '/password_file'
    else:
        raise ValueError('PASSWORD_FILE must be set.')
# the dir we're backing up
BACKUP_PATH: str = os.getenv('BACKUP_PATH', '/backup')

# does the target job have to be running for the hook
_MUST_RUN: str = os.getenv('MUST_RUN', 'false')
MUST_RUN: bool = True if _MUST_RUN.lower() == 'true' else False
# do we have to stop the job to take the backup
# if we stop the job then we'll start it back up too
# if the job isn't running then we'll just take the backup and nothing more
_STOP_JOB: str = os.getenv('STOP_JOB', 'true')
STOP_JOB: bool = True if _STOP_JOB.lower() == 'true' else False

# hook configuration
_HOOK: str = os.getenv('HOOK', 'false')
HOOK: bool = True if _HOOK.lower() == 'true' else False
HOOK_PATH: str = os.getenv('HOOK_PATH')
if not HOOK_PATH:
    # default to /secrets/hook in nomad
    if os.getenv('NOMAD_SECRETS_DIR'):
        HOOK_PATH: str = os.getenv('NOMAD_SECRETS_DIR') + '/hook'
    # we can't run the hook if it's path isn't specified
    elif HOOK:
        raise ValueError('If a hook is used HOOK_PATH must be set.')

# remove & prune old snapshots
_FORGET: str = os.getenv('FORGET', 'true')
FORGET: bool = True if _FORGET.lower() == 'true' else False
# policy for forget
try:
    FORGET_KEEP_LAST: int = int(os.getenv('FORGET_KEEP_LAST', '-1'))
except ValueError:
    FORGET_KEEP_LAST = -1
# in resticpy None means disabled
FORGET_KEEP_LAST: int = FORGET_KEEP_LAST if FORGET_KEEP_LAST > 0 else None

try:
    FORGET_KEEP_HOURLY: int = int(os.getenv('FORGET_KEEP_HOURLY', '-1'))
except ValueError:
    FORGET_KEEP_HOURLY = -1
FORGET_KEEP_HOURLY: int = FORGET_KEEP_HOURLY if FORGET_KEEP_HOURLY > 0 else None

try:
    FORGET_KEEP_DAILY: int = int(os.getenv('FORGET_KEEP_DAILY', '-1'))
except ValueError:
    FORGET_KEEP_DAILY = -1
FORGET_KEEP_DAILY: int = FORGET_KEEP_DAILY if FORGET_KEEP_DAILY > 0 else None

try:
    FORGET_KEEP_WEEKLY: int = int(os.getenv('FORGET_KEEP_WEEKLY', '-1'))
except ValueError:
    FORGET_KEEP_WEEKLY = -1
FORGET_KEEP_WEEKLY: int = FORGET_KEEP_WEEKLY if FORGET_KEEP_WEEKLY > 0 else None

try:
    FORGET_KEEP_MONTHLY: int = int(os.getenv('FORGET_KEEP_MONTHLY', '-1'))
except ValueError:
    FORGET_KEEP_MONTHLY = -1
FORGET_KEEP_MONTHLY: int = FORGET_KEEP_MONTHLY if FORGET_KEEP_MONTHLY > 0 else None

try:
    FORGET_KEEP_YEARLY: int = int(os.getenv('FORGET_KEEP_YEARLY', '-1'))
except ValueError:
    FORGET_KEEP_YEARLY: int = -1
FORGET_KEEP_YEARLY: int = FORGET_KEEP_YEARLY if FORGET_KEEP_YEARLY > 0 else None
