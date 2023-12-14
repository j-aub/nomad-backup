import restic
import os
import logging
import locale

from nomad_backup import config

logger = logging.getLogger(__name__)

# must we use full paths! Backup is done after chdir so offsets will be
# wrong
restic.repository = config.REPOSITORY
restic.password_file = config.PASSWORD_FILE
# in docker this doesn't make sense
restic.use_cache = False

# log_backup_result & helpers from https://github.com/mtlynch/mtlynch-backup/
def human_size(bytes, units=[' bytes', ' KB', ' MB', ' GB', ' TB']):
    return str(bytes) + units[0] if bytes < 1024 else human_size(
        bytes >> 10, units[1:])

def format_integer(integer):
    return locale.format_string('%d', integer, grouping=True)

def human_time(value, units=['seconds', 'minutes', 'hours']):
    return ('%.1f ' % value) + units[0] if value < 60 else human_time(
        value / 60.0, units[1:])

def log_backup_result(backup_result):
    logger.info('%s added', human_size(backup_result['data_added']))
    logger.info('%s files changed',
                format_integer(backup_result['files_changed']))
    logger.info('%s new files', format_integer(backup_result['files_new']))
    logger.info('%s (%s) files processed',
                format_integer(backup_result['total_files_processed']),
                human_size(backup_result['total_bytes_processed']))
    logger.info('Duration: %s', human_time(backup_result['total_duration']))

def init():
    success = False
    # we don't need to init the repo if it already exists
    try:
        if not os.path.isfile(os.path.join(config.REPOSITORY, 'config')):
            restic.init()
        success = True
    except restic.errors.ResticFailedError as e:
        logger.error(f'repository creation failed: {e}')

    return success

def backup():
    success = False

    logger.info('backing up.')

    try:
        res = restic.backup(paths=['.'])
        log_backup_result(res)
        logger.info('backup done.')
    except restic.errors.ResticFailedError as e:
        logger.error(f'backup failed: {e}')
    else:
        success = True

    return success

def forget():
    success = False

    logger.info('forgetting.')
    try:
        restic.forget(
                # if we're not gonna prune nobody will
                prune = True,
                # otherwise restic will never forget because each docker
                # container has a unique hostname
                group_by = 'paths',
                keep_last = config.FORGET_KEEP_LAST,
                keep_hourly = config.FORGET_KEEP_HOURLY,
                keep_daily = config.FORGET_KEEP_DAILY,
                keep_weekly = config.FORGET_KEEP_WEEKLY,
                keep_monthly = config.FORGET_KEEP_MONTHLY,
                keep_yearly = config.FORGET_KEEP_YEARLY)
    except restic.errors.ResticFailedError as e:
        logger.error('forget failed: {e}')
    else:
        logger.info('forgotten.')
        success = True

    return success
