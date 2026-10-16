from __future__ import annotations

import asyncio
import contextlib
from collections.abc import Awaitable, Callable

from .protocol import encode_frame, read_frame


FrameHandler = Callable[[dict], Awaitable[None]]


class LanServer:
    def __init__(self, host: str = "0.0.0.0", port: int = 8765, on_frame: FrameHandler | None = None):
        self.host = host
        self.port = port
        self.on_frame = on_frame
        self.server: asyncio.AbstractServer | None = None
        self.clients: set[asyncio.StreamWriter] = set()

    async def start(self) -> None:
        self.server = await asyncio.start_server(self._handle_client, self.host, self.port)

    async def serve_forever(self) -> None:
        if self.server is None:
            await self.start()
        assert self.server is not None
        async with self.server:
            await self.server.serve_forever()

    async def stop(self) -> None:
        if self.server:
            self.server.close()
            await self.server.wait_closed()
        for writer in list(self.clients):
            writer.close()
            with contextlib.suppress(Exception):
                await writer.wait_closed()

    async def broadcast(self, frame: dict, exclude: asyncio.StreamWriter | None = None) -> None:
        data = encode_frame(frame)
        dead = []
        for writer in self.clients:
            if writer is exclude:
                continue
            try:
                writer.write(data)
                await writer.drain()
            except (ConnectionError, OSError):
                dead.append(writer)
        for writer in dead:
            self.clients.discard(writer)

    async def _handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        self.clients.add(writer)
        try:
            while True:
                frame = await read_frame(reader)
                if self.on_frame:
                    await self.on_frame(frame)
                if frame["type"] in {"sync", "ack"}:
                    await self.broadcast(frame, exclude=writer)
                elif frame["type"] == "ping":
                    writer.write(encode_frame({"type": "pong"}))
                    await writer.drain()
        except (EOFError, ConnectionError, OSError, ValueError):
            pass
        finally:
            self.clients.discard(writer)
            writer.close()
            with contextlib.suppress(Exception):
                await writer.wait_closed()
