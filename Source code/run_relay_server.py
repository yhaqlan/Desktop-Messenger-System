import argparse
import asyncio

from desktop_messenger.network.relay_server import RelayServer


async def run(host: str, port: int, password: str):
    print(f"Desktop Messenger demonstration relay listening on {host}:{port}")
    print("Use TLS or a trusted tunnel before exposing a relay to the public Internet.")
    await RelayServer(password=password, host=host, port=port).serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=9876)
    parser.add_argument("--password", required=True)
    args = parser.parse_args()
    asyncio.run(run(args.host, args.port, args.password))
