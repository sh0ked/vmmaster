# coding: utf-8

import os
import time

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from vmmaster.core.config import config, setup_config
from vmmaster.core.db import Session
from vmmaster.core.utils.utils import change_user_vmmaster
from vmmaster.core.utils.init import home_dir
from vmmaster.core.logger import setup_logging, log

setup_config('%s/config.py' % home_dir())
setup_logging(logdir=config.LOG_DIR, logfile_name='vmmaster_cleanup.log')


engine = create_engine(config.DATABASE)
session_factory = sessionmaker(bind=engine)


def transaction(func):
    def wrapper(*args, **kwargs):
        db_session = session_factory()
        try:
            return func(db_session=db_session, *args, **kwargs)
        except:
            db_session.rollback()
            raise
        finally:
            db_session.close()
    return wrapper


def old():
    d = time.time() - 60 * 60 * 24 * config.SCREENSHOTS_DAYS
    return d


@transaction
def old_sessions(db_session=None):
    return db_session.query(Session).filter(Session.time < old()).all()


def delete_files(session=None):
    from shutil import rmtree
    from errno import ENOENT

    if session:
        session_dir = os.path.join(config.SCREENSHOTS_DIR, str(session.id))
        try:
            rmtree(session_dir)
        except OSError as os_error:
            # Ignore 'No such file or directory' error
            if os_error.errno != ENOENT:
                log.info('Unable to delete %s (%s)' %
                         (str(session_dir), os_error.strerror))


@transaction
def delete_session_data(sessions=None, db_session=None):
    from datetime import datetime, timedelta
    sessions_count = len(sessions)

    log.info("Got %s sessions. " % str(sessions_count))
    if sessions_count:
        first_id = sessions[0].id
        last_id = sessions[-1].id
        checkpoint = datetime.now()
        time_step = timedelta(days=0, seconds=10)

        log.info("Done: %s%% (0 / %d)" % ('0.0'.rjust(5), sessions_count))
        for num, session in enumerate(sessions):
            delta = datetime.now() - checkpoint
            # Show deletion progress each 10 seconds
            if delta > time_step or num == sessions_count - 1:
                percentage = str(
                    round((num + 1)/float(sessions_count) * 100, 1))
                log.info("Done: %s%% (%d / %d)" %
                         (percentage.rjust(5), num + 1, sessions_count))
                checkpoint = datetime.now()
            delete_files(session)
            db_session.delete(session)
            db_session.commit()
        log.info("Total: %s sessions (%d:%d) have been deleted.\n" % (
            str(sessions_count), first_id, last_id))
    else:
        log.info("Nothing to delete.\n")


def run():
    log.info('Running cleanup...')
    change_user_vmmaster()
    outdated_sessions = old_sessions()
    delete_session_data(outdated_sessions)
