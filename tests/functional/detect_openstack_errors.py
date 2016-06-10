# coding: utf-8

import os
import unittest
import subprocess

from StringIO import StringIO

from os import setsid, killpg
from signal import SIGTERM
from netifaces import ifaddresses, AF_INET
from ConfigParser import RawConfigParser


class TestCaseWithMicroApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = os.path.dirname(os.path.realpath(__file__))
        cls.p = subprocess.Popen(["gunicorn",
                                  "--log-level=warning",
                                  "-w 2",
                                  "-b 0.0.0.0:5000",
                                  "tests.functional.app.views:app"
                                  ], preexec_fn=setsid)
        config = RawConfigParser()
        config.read("%s/tests/config" % path)
        try:
            this_machine_ip = \
                ifaddresses('eth0').setdefault(AF_INET)[0]["addr"]
        except ValueError:
            this_machine_ip = \
                ifaddresses('wlan0').setdefault(AF_INET)[0]["addr"]
        config.set("Network", "addr", "http://%s:5000" % this_machine_ip)
        with open('%s/tests/config' % path, 'wb') as configfile:
            config.write(configfile)

    @classmethod
    def tearDownClass(cls):
        killpg(cls.p.pid, SIGTERM)

    def setUp(self):
        self.loader = unittest.TestLoader()
        self.runner = unittest.TextTestRunner(stream=StringIO())
        self.stream = StringIO()

    def test_positive_case(self):
        from tests.test_normal import TestPositiveCase
        suite = self.loader.loadTestsFromTestCase(TestPositiveCase)
        result = self.runner.run(suite)
        self.assertEqual(2, result.testsRun, result.errors)
        self.assertEqual(1, len(result.errors), result.errors)
        self.assertEqual(0, len(result.failures), result.failures)
        self.assertEqual("test_error", result.errors[0][0]._testMethodName)
