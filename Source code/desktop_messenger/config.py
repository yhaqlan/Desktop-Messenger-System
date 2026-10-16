from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .paths import default_database_path


@dataclass(slots=True)
class AppConfig:
    database_path: Path
    lan_host: str = "0.0.0.0"
    lan_port: int = 8765
    relay_host: str = "127.0.0.1"
    relay_port: int = 9876

    @classmethod
    def load(cls, path: Path | None = None) -> "AppConfig":
        if path is None or not path.exists():
            return cls(database_path=default_database_path())
        raw = json.loads(path.read_text(encoding="utf-8"))
        return cls(
            database_path=Path(raw.get("database_path", default_database_path())),
            lan_host=raw.get("lan", {}).get("host", "0.0.0.0"),
            lan_port=int(raw.get("lan", {}).get("port", 8765)),
            relay_host=raw.get("relay", {}).get("host", "127.0.0.1"),
            relay_port=int(raw.get("relay", {}).get("port", 9876)),
        )
