# coding: utf-8

from mock import Mock, patch
from core.config import setup_config, config
from tests.unit.helpers import server_is_up, server_is_down, \
    BaseTestCase, DatabaseMock


class TestServerDoesntShutdown(BaseTestCase):
    def setUp(self):
        setup_config('data/config.py')
        config.NO_SHUTDOWN_WITH_SESSIONS = True

        self.address = ("localhost", 9001)

        with patch(
            'core.connection.Virsh', Mock(),
        ), patch(
            'core.network.Network', Mock()
        ), patch(
            'core.db.Database', DatabaseMock()
        ), patch(
            'core.sessions.SessionWorker', Mock()
        ):
            from vmmaster.server import VMMasterServer
            from nose.twistedtools import threaded_reactor
            reactor, _reactor_thread = threaded_reactor()
            self.vmmaster = VMMasterServer(reactor, self.address[1])
            server_is_up(self.address)

        self.desired_caps = {
            'desiredCapabilities': {
                'platform': self.vmmaster.app.pool.platforms.platforms.keys()[0]
            }
        }

        self.ctx = self.vmmaster.app.app_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()

    def test_server_doesnt_shutdown_with_active_sessions(self):
        """
        - delete server with active session
        Expected: server wait for end active sessions

        - session is succeed
        Expected: server is down
        """
        with patch('core.db.Database', DatabaseMock()):
            self.vmmaster.app.sessions.kill_all()
            from core.sessions import Session
            session = Session()
            session.closed = False

        self.vmmaster.reactor.fireSystemEvent('shutdown')

        with self.assertRaises(RuntimeError):
            server_is_down(self.address, wait=0.1)

        self.assertFalse(session.closed)

        with patch('core.db.Database', DatabaseMock()):
            session.succeed()

        server_is_down(self.address)
