# DesktopMessengerPythonSyncedLively

A Windows-oriented PySide6 desktop messenger reconstruction with SQLite persistence, stable UUID identifiers, offline queuing, LAN transport on port 8765, a demonstration relay transport on port 9876, and authenticated message encryption.

## Implemented in this reconstructed source

- SQLite schema and repositories for accounts, social relationships, direct chats, messages, receipts, notifications, attachments, settings, pending work, and synchronization metadata.
- Password hashing with `hashlib.scrypt`.
- X25519 shared-secret agreement, HKDF-SHA-256 key derivation, and AES-256-GCM authenticated encryption using `cryptography`.
- Idempotent operation application based on stable operation UUIDs.
- Async newline-framed LAN and relay transports with frame-size limits.
- Relay pre-shared-password challenge/response proof. This demonstration protocol is not a replacement for TLS.
- PySide6 dark user interface with Chats, Friends, Notifications, Network, Profile, Settings, and Logout areas.

## Evidence limits

PySide6 was not installed in the generation environment, so the UI files were syntax-checked but not launched here. Core database, security, synchronization, and protocol tests use Python's standard `unittest` runner and were executed. Use the included Windows build scripts to create and test a native executable on Windows.

## Commands

```text
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python run_desktop_messenger.py
python run_lan_host.py
python run_relay_server.py --password YOUR_DEMO_PASSWORD
```
