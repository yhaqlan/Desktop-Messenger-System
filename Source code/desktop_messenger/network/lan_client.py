from __future__ import annotations

import asyncio
import contextlib

from .protocol import encode_frame, read_frame


class LanClient:
    def __init__(self, host: str, port: int = 8765):
        self.host = host
        self.port = port
        self.reader: asyncio.StreamReader | None = None
        self.writer: asyncio.StreamWriter | None = None

    async def connect(self) -> None:
        self.reader, self.writer = await asyncio.open_connection(self.host, self.port)

    async def send(self, frame: dict) -> None:
        if self.writer is None:
            raise RuntimeError("LAN client is not connected")
        self.writer.write(encode_frame(frame))
        await self.writer.drain()

    async def receive(self) -> dict:
        if self.reader is None:
            raise RuntimeError("LAN client is not connected")
        return await read_frame(self.reader)

    async def close(self) -> None:
        if self.writer:
            self.writer.close()
            with contextlib.suppress(Exception):
                await self.writer.wait_closed()
        self.reader = None
        self.writer = None
