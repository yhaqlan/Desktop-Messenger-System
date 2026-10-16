from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@dataclass(slots=True, frozen=True)
class User:
    user_uuid: str
    username: str
    display_name: str
    public_key: bytes


@dataclass(slots=True, frozen=True)
class Message:
    message_uuid: str
    chat_uuid: str
    sender_user_uuid: str
    ciphertext: bytes
    nonce: bytes
    status: str
    client_created_at: str
