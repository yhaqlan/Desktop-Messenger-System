from __future__ import annotations

import json
from dataclasses import asdict, dataclass


@dataclass(slots=True, frozen=True)
class SyncOperation:
    operation_uuid: str
    operation_type: str
    entity_uuid: str
    owner_user_uuid: str
    payload: dict
    created_at: str

    def to_json(self) -> str:
        return json.dumps(asdict(self), separators=(",", ":"), sort_keys=True)

    @classmethod
    def from_json(cls, raw: str) -> "SyncOperation":
        return cls(**json.loads(raw))
