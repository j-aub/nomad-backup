import logging
import nomad
import os
import requests_unixsocket
import time

from nomad_backup import config

logger = logging.getLogger(__name__)
# use requests_unixsocket
# if we're running under nomad use the socket by default
nomad = nomad.Nomad(session=requests_unixsocket.Session(),
                    address=("http+unix://%2Fsecrets%2Fapi.sock" if not
                             os.getenv("NOMAD_ADDR") and
                        os.getenv("NOMAD_SECRETS_DIR") else
                        os.getenv("NOMAD_ADDR")))

# https://developer.hashicorp.com/nomad/api-docs/jobs
# pending, running, dead
def job_status():
    return nomad.jobs[config.JOB]['Status']

# stop_job must be called before start_job to ensure the job dict is
# created!
def stop_job():
    success = False

    # when a job is deleted there's no guarantee that it'll be evailable from
    # nomad since at any time gc could happen. So we obtain the job dict before
    # ever deleting the job.
    global job
    job = nomad.job[config.JOB]

    logger.info('stopping job.')
    if job_status() == 'running':
        nomad.job.deregister_job(config.JOB)

    # job kill timeout is 30s so we'll sleep
    # 1,2,4,8,16 giving 31 seconds
    t = 1
    while t <= 16 and job_status() == 'running':
        logger.info('job is still running. Sleeping.')
        time.sleep(t)
        t = t*2

    # TODO: in theory the job could've gotten cleaned up right before we
    # check the status
    final_status = job_status()
    if not final_status == 'dead':
        logger.error(f'failed to stop the job! job status is {final_status}')
    else:
        logger.info('job has stopped.')
        success = True

    return success

# We don't care if starting the job went well. All that matters is that the
# backup was done properly
def start_job():
    logger.info('starting job.')
    nomad.job.register_job(config.JOB, {'Job': job})
