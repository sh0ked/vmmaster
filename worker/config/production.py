import os
import logging
import logging.config
import logging.handlers
from core.logger import setup_logging

log = logging.getLogger(__name__)

STATIC_FOLDERS = 'worker/static'

RABBITMQ_USER = 'n.ustinov'
RABBITMQ_PASSWORD = 'Paicae6u'
RABBITMQ_HOST = 'mq1.prod.test'
PARALLEL_PROCESSES = 1

# database
DATABASE = "postgresql://vmmaster:vmmaster@localhost/vmmaster_db"

# screenshots
SCREENSHOTS_DIR = os.sep.join(["/var/www/screenshots"])
SCREENSHOTS_DAYS = 7

# logging
LOG_TYPE = "plain"
LOG_LEVEL = "DEBUG"
LOGGING = setup_logging(log_type=LOG_TYPE, log_level=LOG_LEVEL)

# kvm
USE_KVM = False
KVM_MAX_VM_COUNT = 20
KVM_PRELOADED = {}

# PLATFORM = "ubuntu-14.04-x64-logging"

# openstack
USE_OPENSTACK = True
OPENSTACK_MAX_VM_COUNT = 2
OPENSTACK_PRELOADED = {}

OPENSTACK_AUTH_URL = "http://openstack-cd.n1.test"
OPENSTACK_PORT = 5000
OPENSTACK_CLIENT_VERSION = "v2.0"
OPENSTACK_USERNAME = "n.ustinov"
OPENSTACK_PASSWORD = "sho3Pping2gis"
OPENSTACK_TENANT_NAME = "QA Automation"
OPENSTACK_TENANT_ID = "2524a2791a5e4b2fa3d26ab87cbf8e09"
OPENSTACK_ZONE_FOR_VM_CREATE = "nova"
OPENSTACK_PLATFORM_NAME_PREFIX = "origin-"
OPENSTACK_PING_RETRY_COUNT = 3
OPENSTACK_DEFAULT_FLAVOR = "m1.small"
OPENASTACK_VM_META_DATA = {
    "admin_pass": "testPassw0rd.",
}

VM_CHECK = False
VM_CHECK_FREQUENCY = 1800
VM_CREATE_CHECK_PAUSE = 5
VM_CREATE_CHECK_ATTEMPTS = 1000
PRELOADER_FREQUENCY = 3
PING_TIMEOUT = 15

# selenium
SELENIUM_PORT = 4455
VMMASTER_AGENT_PORT = 9000
