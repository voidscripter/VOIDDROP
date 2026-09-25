# VOIDDROP

> **Fast. Local. Private.**

VOIDDROP is a lightweight and privacy-focused local file-sharing tool that lets you transfer files directly between devices on the same network.

No cloud storage.
No accounts.
No external file-hosting service.

Run VOIDDROP on your computer, open the generated network address from another device, and start transferring files through a simple web interface.

---

## ✨ Features

* 🚀 Fast local file transfers
* 🔒 Local-network focused
* 📱 Phone ↔ PC transfers
* 💻 PC ↔ PC transfers
* 📂 Multiple file uploads
* 🖱️ Drag-and-drop support
* 📊 Real-time transfer progress
* ⚡ Transfer speed information
* 📱 QR code connection
* 🔑 Optional PIN protection
* 🗂️ Dedicated shared directory
* 🛡️ Path traversal protection
* 💾 Streaming downloads/uploads
* 🌐 Responsive web interface
* 🐧 Linux-first
* 🔓 Open-source source code

---

# 🧠 How VOIDDROP Works

VOIDDROP turns your computer into a temporary local file server.

When you run:

```bash
voiddrop
```

VOIDDROP starts a local web server.

For example:

```text
Local:
http://localhost:8080

Network:
http://192.168.1.15:8080
```

Your computer can then be accessed by another device connected to the same network.

For example:

```text
PC
 │
 │ Local Network
 │
 ├── 📱 Phone
 ├── 💻 Laptop
 └── 🖥️ Another PC
```

The other device simply opens the network address in its browser.

---

# 📱 Example

Imagine you have a screenshot on your phone and want it on your PC.

Normally you might:

```text
Phone
 ↓
WhatsApp / Telegram / Cloud
 ↓
PC
```

With VOIDDROP:

```text
Phone
   ↓
Local Network
   ↓
PC running VOIDDROP
```

The file stays within your local network instead of being uploaded to a cloud service.

---

# 📦 Installation

## Requirements

You need:

* Python 3
* pip
* A local network connection
* A modern web browser

Linux is the primary supported platform.

---

## Clone the Repository

```bash
git clone https://github.com/voidscripter/VOIDDROP.git
cd VOIDDROP
```

---

## Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Linux/Fish:

```fish
source .venv/bin/activate.fish
```

For Bash/Zsh:

```bash
source .venv/bin/activate
```

---

## Install VOIDDROP

Install the project in editable mode:

```bash
pip install -e .
```

After installation, the `voiddrop` command should be available.

Check:

```bash
voiddrop --help
```

---

# 🚀 Running VOIDDROP

Start the server:

```bash
voiddrop
```

You should see something similar to:

```text
VOIDDROP

● Server running

Local:
http://localhost:8080

Network:
http://192.168.1.15:8080

Shared directory:
~/VOIDDROP

Press CTRL+C to stop
```

Open the **Network** address from another device connected to the same network.

---

# 🌐 Host & Port

You can specify the port:

```bash
voiddrop --port 9000
```

Example:

```text
http://192.168.1.15:9000
```

You can also specify the host:

```bash
voiddrop --host 0.0.0.0
```

This allows VOIDDROP to listen on available network interfaces.

---

# 📁 Shared Directory

VOIDDROP does not expose your entire filesystem.

Instead, it uses a dedicated shared directory:

```text
~/VOIDDROP
```

Only files inside this directory are available through the application.

Example:

```text
~/VOIDDROP/
├── image.png
├── project.zip
├── video.mp4
└── document.pdf
```

This helps prevent accidental access to unrelated files on your system.

You can also specify another directory:

```bash
voiddrop --directory ~/Shared
```

---

# 📤 Uploading Files

The web interface supports file uploads.

You can:

* Click the upload area.
* Select files.
* Drag files into the browser.
* Upload multiple files.

During an upload, VOIDDROP can display information such as:

```text
example.zip

642 MB / 842 MB

76%

Speed: 42.3 MB/s
```

Transfer information is based on the actual transfer rather than simulated values.

---

# 📥 Downloading Files

Files available in the shared directory appear in the web interface.

Example:

```text
Files

project.zip
842 MB

[ Download ] [ Delete ]
```

Downloads are streamed instead of unnecessarily loading the entire file into memory.

This makes the application more suitable for larger files.

---

# 📱 QR Code

VOIDDROP can provide a QR code containing the actual local network address.

Example:

```text
Scan to connect

[ QR CODE ]

http://192.168.1.15:8080
```

Scan the QR code with your phone and the browser can open the VOIDDROP interface.

This avoids manually typing the IP address.

---

# 🔑 PIN Protection

VOIDDROP can optionally require a PIN.

Example:

```bash
voiddrop --pin 4821
```

When PIN protection is enabled, users must authenticate before accessing the file-sharing interface.

The PIN should not be exposed in unnecessary logs or stored insecurely.

---

# 🔒 Security

VOIDDROP is designed with local file-sharing security in mind.

### Path Traversal Protection

User-provided filenames are never trusted directly.

Requests such as:

```text
../../etc/passwd
```

must not allow access outside the configured shared directory.

### Restricted File Access

VOIDDROP only serves files inside the configured shared directory.

It does not intentionally expose:

```text
/etc
/home/other-user
/root
```

or other unrelated filesystem locations.

### No Arbitrary Command Execution

The web interface does not provide a terminal or arbitrary command execution feature.

### No Cloud Upload

Normal VOIDDROP transfers do not require uploading files to an external cloud service.

---

# 🌐 Network Model

VOIDDROP is designed for local networks.

Example:

```text
                 Router
                   │
          ┌────────┴────────┐
          │                 │
        PC                 Phone
   VOIDDROP Server        Browser
          │                 │
          └──── Local ──────┘
                Network
```

Both devices need to be able to communicate with the computer running VOIDDROP.

Depending on your network configuration, firewall rules may affect connectivity.

---

# 🖥️ Web Interface

The interface is designed to work on both desktop and mobile screens.

![VOIDDROP Screenshot](sreenshot%20you%20dont%20need%20it/swash-2026-09-25_18%3A28%3A41.png) 

The main interface provides:

### Upload Area

Drag and drop files or select them manually.

### File List

See files currently available in the shared directory.

### Transfer Information

View transfer progress and useful status information.

### File Actions

Download or delete files from the shared directory.


### File List

See files currently available in the shared directory.

### Transfer Information

View transfer progress and useful status information.

### File Actions

Download or delete files from the shared directory.

---

# ⚙️ CLI Options

Display help:

```bash
voiddrop --help
```

Display version:

```bash
voiddrop --version
```

Change port:

```bash
voiddrop --port 9000
```

Change host:

```bash
voiddrop --host 0.0.0.0
```

Change shared directory:

```bash
voiddrop --directory ~/Shared
```

Enable PIN protection:

```bash
voiddrop --pin 1234
```

Combine options:

```bash
voiddrop \
  --host 0.0.0.0 \
  --port 9000 \
  --directory ~/Shared \
  --pin 1234
```

---

# 🧪 Testing

Run the test suite:

```bash
pytest
```

Tests cover important parts of the application such as:

* File handling
* Path security
* Configuration
* Shared directory behavior
* Network functionality

The project should be tested before publishing changes.

---

# 🏗️ Project Structure

```text
VOIDDROP/
│
├── src/
│   └── voiddrop/
│       ├── __init__.py
│       ├── main.py
│       ├── server.py
│       ├── config.py
│       ├── network.py
│       ├── security.py
│       ├── files.py
│       ├── transfers.py
│       └── qr.py
│
├── web/
│   ├── index.html
│   ├── style.css
│   └── app.js
│
├── tests/
│   ├── test_files.py
│   ├── test_security.py
│   └── test_network.py
│
├── README.md
├── CONTRIBUTING.md
├── LICENSE
├── requirements.txt
├── pyproject.toml
└── .gitignore
```

---

# 🧩 Architecture

VOIDDROP is divided into several components.

### `main.py`

Responsible for starting the application and handling CLI arguments.

### `server.py`

Responsible for the web server and HTTP routes.

### `config.py`

Handles application configuration such as:

* Host
* Port
* Shared directory
* PIN settings

### `network.py`

Handles local network detection and network-related information.

### `security.py`

Handles security-related functionality such as:

* PIN authentication
* Path validation
* Safe file access

### `files.py`

Handles:

* File listing
* File validation
* File deletion
* Shared directory management

### `transfers.py`

Handles file transfer functionality and transfer-related information.

### `qr.py`

Generates the QR code for the detected network address.

### `web/`

Contains the browser interface.

---

# 🔓 Open Source

VOIDDROP is fully open-source.

The source code is available in this repository so anyone can:

* Read the code
* Learn from the project
* Modify the software
* Report bugs
* Suggest improvements
* Submit pull requests
* Build their own version

---

# 🤝 Contributing

Contributions are welcome.

Before making changes:

```bash
git clone https://github.com/voidscripter/VOIDDROP.git
cd VOIDDROP
```

Create a development environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -e .
```

Run tests:

```bash
pytest
```

Please keep contributions:

* Simple
* Secure
* Readable
* Tested
* Focused

See `CONTRIBUTING.md` for more information.

---

# 🐛 Reporting Bugs

If you find a problem, create a GitHub Issue.

Include:

* Operating system
* Python version
* VOIDDROP version
* Command used
* Error message
* Steps to reproduce the issue

Never include:

* Passwords
* PINs
* Private keys
* Tokens
* Sensitive personal information

---

# 🛣️ Roadmap

Possible future improvements include:

* 📱 Better mobile interface
* 📦 Improved large-file handling
* 🔐 Stronger authentication options
* 📊 Better transfer statistics
* 🖥️ Desktop application
* 🪟 Windows support
* 🍎 macOS support
* 🔄 Resume interrupted transfers
* 👥 Multiple-device management
* 🎨 More UI customization

The roadmap may change as the project develops.

---

# ⚠️ Limitations

VOIDDROP is primarily designed for devices that can communicate over the same local network.

Network isolation, firewall settings, VPNs, guest Wi-Fi networks, or router configuration may prevent devices from connecting.

VOIDDROP does not replace a cloud-storage service for remote file sharing over the internet.

---

# 📜 License

VOIDDROP is released under the license included in this repository.

See:

```text
LICENSE
```

for the complete license terms.

---

# 👤 Author

**VoidScripter**

GitHub:

https://github.com/voidscripter

---

# ⭐ Support

If you find VOIDDROP useful, consider giving the repository a ⭐ on GitHub.

Bug reports, suggestions, and contributions are welcome.

---

<div align="center">

**VOIDDROP**

*Move files. Keep them local.*

</div>
