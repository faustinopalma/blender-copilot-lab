import unittest

from local_network import require_loopback


class LocalNetworkTests(unittest.TestCase):
    def test_loopback_connections(self):
        for host in ("localhost", "127.0.0.1", "::1"):
            require_loopback("socket.connect", (object(), (host, 9876)))

    def test_loopback_listener(self):
        require_loopback("socket.bind", (object(), ("127.0.0.1", 9876)))

    def test_external_connections_denied(self):
        for host in ("example.com", "8.8.8.8", "192.168.1.2"):
            with self.assertRaises(PermissionError):
                require_loopback("socket.connect", (object(), (host, 443)))

    def test_external_dns_denied(self):
        with self.assertRaises(PermissionError):
            require_loopback("socket.getaddrinfo", ("example.com", 443))

    def test_wildcard_listener_denied(self):
        for host in ("0.0.0.0", "::", ""):
            with self.assertRaises(PermissionError):
                require_loopback("socket.bind", (object(), (host, 9876)))

    def test_non_ip_connection_denied(self):
        with self.assertRaises(PermissionError):
            require_loopback("socket.connect", (object(), "some-pipe"))

    def test_bytes_localhost(self):
        require_loopback("socket.getaddrinfo", (b"localhost", 9876))

    def test_unrelated_events_ignored(self):
        require_loopback("open", ("file.txt", "r"))


if __name__ == "__main__":
    unittest.main()
