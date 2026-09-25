# VOIDDROP

Transfer files between devices on the same local network. VOIDDROP serves a small web interface from your computer; files are stored in a dedicated local folder and never sent to a cloud service.

## Screenshot

![VOIDDROP Screenshot](sreenshot%20you%20dont%20need%20it/swash-2026-09-25_18%3A28%3A41.png)

## Features

- Local web interface for desktop and mobile browsers
- Multi-file uploads with browser progress, live speed, and completion state
- Streaming uploads and downloads for large files
- List, download, and delete shared files
- Optional PIN gate
- QR code generated for the detected local network address
- Files confined to a dedicated shared directory
- No account, cloud storage, analytics, or public-IP lookup

## Demo

Run `voiddrop` on the computer holding the files, then open the printed **Network** URL from another device on the same Wi-Fi or wired LAN. Choose files or drop them onto the upload area. They appear in the Files list when the transfer completes.

## Installation

Python 3.10 or newer is required. From a checkout:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
voiddrop
```

The default shared directory is `~/VOIDDROP`; it is created when the application starts. Uvicorn, FastAPI, and qrcode (with Pillow for PNG output) are installed as project dependencies.

## Usage

```bash
voiddrop
voiddrop --port 9000 --directory ~/Shared
voiddrop --host 0.0.0.0 --port 8080 --pin 4821
```

Use the network URL printed at startup on other devices on the LAN. The local URL is for the host computer. Press `Ctrl+C` to stop. A PIN, when enabled, is checked in memory and is not printed or written to disk.

## CLI options

| Option | Purpose |
| --- | --- |
| `--host HOST` | Bind address (default `0.0.0.0`) |
| `--port PORT` | Listening port from 1 to 65535 (default `8080`) |
| `--directory PATH` | Shared folder (default `~/VOIDDROP`) |
| `--pin DIGITS` | Require a 4–12 digit PIN |
| `--help` | Show command help |
| `--version` | Show version |

## Security

VOIDDROP shares only the configured directory. Upload names are reduced to safe basenames; downloads and deletes resolve within the shared directory and reject symlinks. Uploads first go to an unpredictable hidden temporary file and are published only after the request completes. A conflicting filename is rejected rather than overwritten.

The PIN protects the interface and transfer endpoints with an HTTP-only, SameSite cookie. The service uses plain HTTP, so the PIN and file contents are not encrypted on the LAN; use VOIDDROP only on a trusted network. Binding to `0.0.0.0` makes the server reachable on every active interface, subject to your firewall.

## How file sharing works

The host runs a local HTTP server. A second device connects directly to its private LAN address and streams the selected file to the host. The host writes it to the shared folder. Downloads stream from that folder back to the client. No external server is involved. Network address discovery uses a local UDP routing decision and does not send application data to the probe address.

## Project structure

```text
src/voiddrop/   CLI, configuration, network discovery, security and API
web/            HTML, CSS and vanilla JavaScript
tests/          File, configuration, network and API tests
```

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Testing

```bash
pytest
```

Tests cover configuration validation, path handling, file listing/deletion, PIN authorization, transfer endpoints, and local address detection.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Please keep transfers local, preserve the shared-directory boundary, and add tests for security-sensitive behavior.

## License

MIT. See [LICENSE](LICENSE).
