from __future__ import annotations

import asyncio
import contextlib
import hmac
import secrets

from .protocol import encode_frame, read_frame, relay_proof


class RelayServer:
    def __init__(self, password: str, host: str = "0.0.0.0", port: int = 9876):
        if len(password) < 8:
            raise ValueError("Relay demonstration password must contain at least eight characters")
        self.password = password
        self.host = host
        self.port = port
        self.server: asyncio.AbstractServer | None = None
        self.clients: dict[str, asyncio.StreamWriter] = {}

    async def serve_forever(self) -> None:
        self.server = await asyncio.start_server(self._handle_client, self.host, self.port)
        async with self.server:
            await self.server.serve_forever()

    async def _handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        client_uuid = None
        try:
            hello = await read_frame(reader)
            if hello.get("type") != "hello" or not hello.get("client_uuid"):
                raise ValueError("Expected hello")
            client_uuid = str(hello["client_uuid"])
            challenge = secrets.token_hex(24)
            writer.write(encode_frame({"type": "challenge", "challenge": challenge}))
            await writer.drain()
            auth = await read_frame(reader)
            expected = relay_proof(self.password, challenge, client_uuid)
            if auth.get("type") != "auth" or not hmac.compare_digest(str(auth.get("proof", "")), expected):
                writer.write(encode_frame({"type": "auth_error"}))
                await writer.drain()
                return
            self.clients[client_uuid] = writer
            writer.write(encode_frame({"type": "auth_ok"}))
            await writer.drain()
            while True:
                frame = await read_frame(reader)
                target = frame.get("target_client_uuid")
                if target and target in self.clients:
                    self.clients[target].write(encode_frame(frame))
                    await self.clients[target].drain()
                elif frame["type"] == "ping":
                    writer.write(encode_frame({"type": "pong"}))
                    await writer.drain()
        except (EOFError, ConnectionError, OSError, ValueError):
            pass
        finally:
            if client_uuid and self.clients.get(client_uuid) is writer:
                self.clients.pop(client_uuid, None)
            writer.close()
            with contextlib.suppress(Exception):
                await writer.wait_closed()
