# Windows Release Validation Checklist

- [ ] Build completes with PyInstaller and produces a non-empty distribution.
- [ ] Application launches on a clean Windows machine without a Python installation.
- [ ] First launch creates the SQLite database and required directories.
- [ ] Registration, login, logout, and invalid-password handling work.
- [ ] Two clients discover/connect through the same LAN/hotspot on port 8765.
- [ ] Internet relay is tested with a reachable host on port 9876; loopback is not misrepresented as remote.
- [ ] Pending operations survive restart and retry after reconnect.
- [ ] Duplicate synchronization operations do not duplicate messages.
- [ ] Message ciphertext cannot be decoded without the derived key.
- [ ] Friend request accept/reject and remove behavior synchronize.
- [ ] UI hover, press, focus, status, and empty-state feedback are visible.
- [ ] Antivirus false positives and Windows firewall prompts are documented.
- [ ] Final executable checksum and test machine details are recorded.
