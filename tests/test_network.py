from voiddrop.network import detect_network_address
import ipaddress


def test_detect_network_address_returns_local_ipv4():
    result = detect_network_address()
    pieces = result.ip.split(".")
    assert len(pieces) == 4
    assert all(piece.isdigit() and 0 <= int(piece) <= 255 for piece in pieces)
    assert not result.ip.startswith("127.")
    assert ipaddress.ip_address(result.ip).is_private
