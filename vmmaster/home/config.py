import os


class Config(object):
    BASEDIR = os.path.dirname(os.path.realpath(__file__))
    PORT = 9000
    DATABASE = "sqlite:///" + BASEDIR + "/vmmaster.db"

    CLONES_DIR = BASEDIR + "/clones"
    ORIGINS_DIR = BASEDIR + "/origins"
    SESSION_DIR = BASEDIR + "/session"
    LOG_DIR = BASEDIR + "/log"
    SCREENSHOTS_DIR = BASEDIR + "/screenshots"

    # clones related stuff
    MAX_CLONE_COUNT = 2
    CLONE_TIMEOUT = 360
    PING_TIMEOUT = 180

    # additional logging
    # GRAYLOG = ('logserver', 12201)

    # selenium
    SELENIUM_PORT = "4455"
