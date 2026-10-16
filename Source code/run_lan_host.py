import argparse
import asyncio

from desktop_messenger.network.lan_server import LanServer


async def run(host: str, port: int):
    server = LanServer(host, port)
    print(f"Desktop Messenger LAN server listening on {host}:{port}")
    await server.serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    asyncio.run(run(args.host, args.port))
