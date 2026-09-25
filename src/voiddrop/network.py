"""Local IPv4 address discovery without contacting an external service."""

from dataclasses import dataclass
import ipaddress
import socket
import struct


@dataclass(frozen=True)
class NetworkAddress:
    interface: str
    ip: str


def detect_network_address() -> NetworkAddress:
    """Ask the local routing table which source address reaches a private DNS IP."""
    probe = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        probe.connect(("192.0.2.1", 9))
        ip = probe.getsockname()[0]
        if ip.startswith("127.") or ip == "0.0.0.0":
            raise OSError("No active local network interface was found")
        if not ipaddress.ip_address(ip).is_private:
            raise OSError("No private local network address was found")
        interface = "unknown"
        try:
            import fcntl
            lookup = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                for _, name in socket.if_nameindex():
                    request = struct.pack("256s", name.encode("ascii")[:15])
                    try:
                        result = fcntl.ioctl(lookup.fileno(), 0x8915, request)
                        if socket.inet_ntoa(result[20:24]) == ip:
                            interface = name
                            break
                    except OSError:
                        continue
            finally:
                lookup.close()
        except (OSError, ImportError, ValueError):
            pass
        return NetworkAddress(interface, ip)
    finally:
        probe.close()
