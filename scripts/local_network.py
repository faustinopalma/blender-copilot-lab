"""Defense in depth for this local experiment, not an operating-system sandbox."""

import ipaddress
import sys


def require_loopback(event: str, args: tuple) -> None:
    if event in ("socket.connect", "socket.bind"):
        address = args[1]
        if not isinstance(address, tuple):
            raise PermissionError(f"Non-IP socket denied: {event}")
        host = address[0]
    elif event == "socket.getaddrinfo":
        host = args[0]
    else:
        return
    if isinstance(host, bytes):
        host = host.decode("ascii")
    if host == "localhost":
        return
    try:
        allowed = ipaddress.ip_address(host).is_loopback
    except ValueError:
        allowed = False
    if not allowed:
        raise PermissionError(f"Non-loopback network access denied: {event} {host}")


def install_guard() -> None:
    sys.addaudithook(require_loopback)
