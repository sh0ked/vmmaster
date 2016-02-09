# coding: utf-8
import logging
import logging.handlers
import graypy
import os
import sys

from config import config
from core.utils.network_utils import ping


class StreamToLogger(object):
    """
    Fake file-like stream object that redirects writes to a logger instance.
    """

    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())


def setup_logging(
    logname='', logdir=None, logfile_name='vmmaster.log',
    scrnlog=True, txtlog=True, loglevel=None
):
    if loglevel is None:
        loglevel = logging.getLevelName(config.LOG_LEVEL.upper())

    if logdir:
        logdir = os.path.abspath(logdir)
    else:
        logdir = config.LOG_DIR

    if not os.path.exists(logdir):
        os.mkdir(logdir)

    _log = logging.getLogger(logname)
    _log.setLevel(loglevel)

    if scrnlog:
        log_format = \
            "%(asctime)s - %(levelname)-7s :: %(name)-6s :: %(message)s"
    else:
        log_format = "%(asctime)s - %(levelname)-7s :: %(message)s"

    log_formatter = logging.Formatter(log_format)

    if txtlog:
        txt_handler = logging.handlers.RotatingFileHandler(
            os.path.join(logdir, logfile_name),
            maxBytes=config.LOG_SIZE,
            backupCount=5
        )
        txt_handler.setFormatter(log_formatter)
        _log.addHandler(txt_handler)

    if scrnlog:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_formatter)
        _log.addHandler(console_handler)

    if hasattr(config, 'GRAYLOG'):
        host = config.GRAYLOG[0]
        port = config.GRAYLOG[1]

        if ping(host, port):
            graylog_handler = graypy.GELFHandler(host=host, port=port)
            graylog_handler.setFormatter(log_formatter)
            _log.addHandler(graylog_handler)
        else:
            _log.info('GRAYLOG URL not available')

    stdout_logger = logging.getLogger('STDOUT')
    slout = StreamToLogger(stdout_logger, logging.INFO)
    sys.stdout = slout

    stderr_logger = logging.getLogger('STDERR')
    slerr = StreamToLogger(stderr_logger, logging.ERROR)
    sys.stderr = slerr

    _log.info("Logger initialised.")
    return _log


log = logging.getLogger('LOG')
