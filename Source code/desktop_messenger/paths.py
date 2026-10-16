from __future__ import annotations

import os
from pathlib import Path


APP_NAME = "DesktopMessenger"


def application_data_dir() -> Path:
    if os.name == "nt":
        base = Path(os.environ.get("LOCALAPPDATA", Path.home()))
    else:
        base = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
    path = base / APP_NAME
    path.mkdir(parents=True, exist_ok=True)
    return path


def default_database_path() -> Path:
    return application_data_dir() / "desktop_messenger.sqlite3"


def attachment_dir() -> Path:
    path = application_data_dir() / "attachments"
    path.mkdir(parents=True, exist_ok=True)
    return path
