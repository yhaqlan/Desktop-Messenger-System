from __future__ import annotations

import asyncio
import contextlib

from .protocol import encode_frame, read_frame, relay_proof


class RelayClient:
    def __init__(self, client_uuid: str, password: str, host: str, port: int = 9876):
        self.client_uuid = client_uuid
        self.password = password
        self.host = host
        self.port = port
        self.reader: asyncio.StreamReader | None = None
        self.writer: asyncio.StreamWriter | None = None

    async def connect(self) -> None:
        self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
        self.writer.write(encode_frame({"type": "hello", "client_uuid": self.client_uuid}))
        await self.writer.drain()
        challenge = await read_frame(self.reader)
        if challenge.get("type") != "challenge":
            raise RuntimeError("Relay did not issue a challenge")
        proof = relay_proof(self.password, challenge["challenge"], self.client_uuid)
        self.writer.write(encode_frame({"type": "auth", "proof": proof}))
        await self.writer.drain()
        result = await read_frame(self.reader)
        if result.get("type") != "auth_ok":
            raise PermissionError("Relay authentication failed")

    async def send(self, frame: dict) -> None:
        if self.writer is None:
            raise RuntimeError("Relay client is not connected")
        self.writer.write(encode_frame(frame))
        await self.writer.drain()

    async def receive(self) -> dict:
        if self.reader is None:
            raise RuntimeError("Relay client is not connected")
        return await read_frame(self.reader)

    async def close(self) -> None:
        if self.writer:
            self.writer.close()
            with contextlib.suppress(Exception):
                await self.writer.wait_closed()
        self.reader = None
        self.writer = None
