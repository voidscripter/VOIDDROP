"""Command line entry point."""

import argparse
from pathlib import Path
import sys

import uvicorn

from . import __version__
from .config import Config
from .network import detect_network_address
from .server import create_app


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(prog="voiddrop", description="Share files privately on your local network.")
    result.add_argument("--host", default="0.0.0.0", help="interface to bind (default: 0.0.0.0)")
    result.add_argument("--port", type=int, default=8080, help="port to listen on (default: 8080)")
    result.add_argument("--directory", type=Path, default=Path.home() / "VOIDDROP", help="shared folder")
    result.add_argument("--pin", help="optional 4–12 digit access PIN")
    result.add_argument("--version", action="version", version=f"VOIDDROP {__version__}")
    return result


def main() -> None:
    args = parser().parse_args()
    try:
        config = Config(host=args.host, port=args.port, directory=args.directory, pin=args.pin)
    except (ValueError, OSError) as exc:
        parser().error(str(exc))
    try:
        address = detect_network_address()
        network_ip = address.ip
        interface = address.interface
    except OSError as exc:
        network_ip = None
        interface = "unavailable"
        print(f"Network address unavailable: {exc}", file=sys.stderr)
    local_url = f"http://localhost:{config.port}"
    print("\nVOIDDROP\n\n● Server starting\n\nLocal:\n" + local_url)
    if network_ip:
        print(f"\nNetwork:\nhttp://{network_ip}:{config.port}\n\nInterface: {interface}\nIP: {network_ip}\nPort: {config.port}")
    else:
        print(f"\nNetwork:\nUnavailable\n\nInterface: {interface}\nPort: {config.port}")
    print("\nPress CTRL+C to stop\n")
    app = create_app(config, network_ip)
    try:
        uvicorn.run(app, host=config.host, port=config.port, log_level="warning")
    except KeyboardInterrupt:
        pass
    finally:
        print("\nVOIDDROP stopped.")


if __name__ == "__main__":
    main()
