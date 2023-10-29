import sys
import logging
import subprocess
import urllib3

from nomad_backup import config
from nomad_backup import nomad

logger = logging.getLogger(__name__)

def configure_logging():
    # https://urllib3.readthedocs.io/en/1.26.x/advanced-usage.html#ssl-warnings
    # properly log the python-nomad ssl error
    logging.captureWarnings(True)
    root_logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s %(name)-15s %(levelname)-4s: %(message)s',
        '%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)

def run_hook():
    success = False

    try:
        subprocess.run([config.HOOK_PATH], check=True)
    except OSError as e:
        # this exception can be caused by a number of things so we'll print
        # the exception itself for easier debugging
        logger.error(f'Could not execute hook: {e}')
    except PermissionError:
        logger.error('Insufficient permissions to execute hook.')
    except FileNotFoundError:
        logger.error('The hook file does not exist.')
    except subprocess.CalledProcessError as e:
        logger.error(f'The hook failed with exit code {e.returncode}.')
    else:
        logger.info(f'The hook ran successfully.')
        success = True

    return success

def main():
    # supress python-nomad warning about untrusted ca
    # python-nomad has no way to add a cacert so there's no way to get rid
    # of the error properly
    urllib3.disable_warnings()

    configure_logging()

    # printing the config
    logger.info(f'JOB = {config.JOB}')
    logger.info(f'REPOSITORY = {config.REPOSITORY}')
    logger.info(f'BACKUP_PATH = {config.BACKUP_PATH}')
    logger.info(f'MUST_RUN = {config.MUST_RUN}')
    logger.info(f'STOP_JOB = {config.STOP_JOB}')
    logger.info(f'HOOK = {config.HOOK}')
    logger.info(f'HOOK_PATH = {config.HOOK_PATH if config.HOOK_PATH else ""}')
    logger.info(f'FORGET = {config.FORGET}')
    logger.info(f'FORGET_PRUNE = {config.FORGET_PRUNE}')
    logger.info(f'FORGET_KEEP_LAST = {config.FORGET_KEEP_LAST}')
    logger.info(f'FORGET_KEEP_HOURLY = {config.FORGET_KEEP_HOURLY}')
    logger.info(f'FORGET_KEEP_DAILY = {config.FORGET_KEEP_DAILY}')
    logger.info(f'FORGET_KEEP_WEEKLY = {config.FORGET_KEEP_WEEKLY}')
    logger.info(f'FORGET_KEEP_MONTHLY = {config.FORGET_KEEP_MONTHLY}')
    logger.info(f'FORGET_KEEP_YEARLY = {config.FORGET_KEEP_YEARLY}')

    # if a job is pending it means any moment it could start up so we'll be
    # cautious
    initially_running = nomad.job_status() == 'running' or
    nomad.job_status() == 'pending'

    if config.MUST_RUN and not initially_running:
        logger.error('job is not initially running when it should be.')
        sys.exit(1)

    if config.HOOK:
        logger.info('Running hook.')

        # doesn't make sense to go on if hook failed
        if not run_hook():
            sys.exit(1)

    if config.STOP_JOB and initially_running:
        if not nomad.stop_job():
            sys.exit(1)

    if config.STOP_JOB and initially_running:
        nomad.start_job()

'''
if not backup.backup():
    logger.error('failed to backup.')
    sys.exit(1)

if config.FORGET:
    if not backup.forget():
        logger.error('failed to clean snapshots.')
        sys.exit(1)
'''
