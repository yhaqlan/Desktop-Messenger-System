from __future__ import annotations

import asyncio
import hashlib
import hmac
import json
from typing import Any


MAX_FRAME_BYTES = 2 * 1024 * 1024
ALLOWED_TYPES = {"hello", "challenge", "auth", "auth_ok", "auth_error", "sync", "ack", "ping", "pong"}


def encode_frame(frame: dict[str, Any]) -> bytes:
    frame_type = frame.get("type")
    if frame_type not in ALLOWED_TYPES:
        raise ValueError(f"Unsupported frame type: {frame_type!r}")
    encoded = json.dumps(frame, separators=(",", ":"), ensure_ascii=False).encode("utf-8") + b"\n"
    if len(encoded) > MAX_FRAME_BYTES:
        raise ValueError("Frame exceeds the maximum allowed size")
    return encoded


async def read_frame(reader: asyncio.StreamReader) -> dict[str, Any]:
    raw = await reader.readline()
    if not raw:
        raise EOFError("Connection closed")
    if len(raw) > MAX_FRAME_BYTES:
        raise ValueError("Frame exceeds the maximum allowed size")
    frame = json.loads(raw.decode("utf-8"))
    if not isinstance(frame, dict) or frame.get("type") not in ALLOWED_TYPES:
        raise ValueError("Invalid protocol frame")
    return frame


def relay_proof(password: str, challenge: str, client_uuid: str) -> str:
    message = f"{challenge}|{client_uuid}".encode("utf-8")
    return hmac.new(password.encode("utf-8"), message, hashlib.sha256).hexdigest()
