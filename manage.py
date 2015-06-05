from flask import Flask

from twisted.internet import reactor
from flask.ext.script import Manager

from vmmaster.core.config import setup_config, config
from vmmaster.core.utils.init import home_dir, useradd
from vmmaster.core.logger import log
from vmmaster.core import db
from vmmaster.core.logger import setup_logging

try:
    setup_config('%s/config.py' % home_dir())
    db.database = db.Database(config.DATABASE)
except AttributeError:
    config = None
    db.database = None

from vmmaster.server import VMMasterServer
from vmmaster.core.utils.utils import change_user_vmmaster

app = Flask(__name__)
manager = Manager(app)


def activate_logger():
    setup_logging(config.LOG_DIR)


def main():
    VMMasterServer(reactor, config.PORT).run()


@manager.command
def runserver():
    """
    Run server
    """
    activate_logger()
    main()


@manager.command
def cleanup():
    """
    Run cleanup
    """
    from vmmaster import cleanup
    cleanup.run()


@manager.command
def init():
    """
    Initialize application
    """
    activate_logger()
    log.info('Initialize application')
    useradd()
    change_user_vmmaster()
    exit(0)


@manager.command
def migrations():
    """
    Database migrations
    """
    from migrations import migrations
    migrations.run(config.DATABASE)


@manager.command
def version():
    """
    Show application version
    """
    import versioneer

    versioneer.VCS = 'git'
    versioneer.versionfile_source = 'vmmaster/_version.py'
    versioneer.versionfile_build = 'vmmaster/_version.py'
    versioneer.tag_prefix = ''  # tags are like 0.1.0
    versioneer.parentdir_prefix = 'vmmaster-'  # dirname like 'myproject-0.1.0'

    print 'Version: %s' % versioneer.get_version()


if __name__ == '__main__':
    manager.run()
