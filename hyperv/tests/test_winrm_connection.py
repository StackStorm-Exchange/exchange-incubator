import unittest
import winrm

from lib.winrm_connection import WinRmConnection


class TestWinRmConnection(unittest.TestCase):

    def setUp(self):
        super(TestWinRmConnection, self).setUp()

    def test_init(self):
        hostname = 'hostname'
        port = 1234
        transport = 'tport'
        username = 'username'
        password = 'password'
        url = 'https://{}:{}/wsman'.format(hostname, port)
        server_cert_validation = 'ignore'
        connection = WinRmConnection(hostname, port, transport, username, password)
        self.assertIsInstance(connection.session, winrm.Session)
        self.assertEqual(connection.session.url, url)
        self.assertEqual(connection.session.protocol.username, username)
        self.assertEqual(connection.session.protocol.password, password)
        self.assertEqual(connection.session.protocol.server_cert_validation,
                         server_cert_validation)
        self.assertEqual(connection.session.protocol.transport.endpoint, url)
        self.assertEqual(connection.session.protocol.transport.auth_method, transport)
        self.assertEqual(connection.session.protocol.transport.username, username)
        self.assertEqual(connection.session.protocol.transport.password, password)
        self.assertEqual(connection.session.protocol.transport.server_cert_validation,
                         server_cert_validation)
