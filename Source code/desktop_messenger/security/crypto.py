from __future__ import annotations

import base64
import json
import os

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey, X25519PublicKey
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt


MESSAGE_CONTEXT = b"DesktopMessenger/message/v1"
PRIVATE_KEY_CONTEXT = b"DesktopMessenger/private-key/v1"


def generate_identity_keypair() -> tuple[bytes, bytes]:
    private = X25519PrivateKey.generate()
    private_bytes = private.private_bytes(
        serialization.Encoding.Raw,
        serialization.PrivateFormat.Raw,
        serialization.NoEncryption(),
    )
    public_bytes = private.public_key().public_bytes(
        serialization.Encoding.Raw,
        serialization.PublicFormat.Raw,
    )
    return private_bytes, public_bytes


def derive_message_key(private_key_bytes: bytes, peer_public_key_bytes: bytes, chat_uuid: str) -> bytes:
    private_key = X25519PrivateKey.from_private_bytes(private_key_bytes)
    peer_public_key = X25519PublicKey.from_public_bytes(peer_public_key_bytes)
    shared_secret = private_key.exchange(peer_public_key)
    return HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=MESSAGE_CONTEXT + chat_uuid.encode("utf-8"),
    ).derive(shared_secret)


def encrypt_message(key: bytes, plaintext: str, message_uuid: str) -> tuple[bytes, bytes]:
    if len(key) != 32:
        raise ValueError("AES-256-GCM requires a 32-byte key")
    nonce = os.urandom(12)
    ciphertext = AESGCM(key).encrypt(nonce, plaintext.encode("utf-8"), message_uuid.encode("utf-8"))
    return nonce, ciphertext


def decrypt_message(key: bytes, nonce: bytes, ciphertext: bytes, message_uuid: str) -> str:
    plaintext = AESGCM(key).decrypt(nonce, ciphertext, message_uuid.encode("utf-8"))
    return plaintext.decode("utf-8")


def protect_private_key(password: str, private_key_bytes: bytes) -> str:
    salt = os.urandom(16)
    nonce = os.urandom(12)
    wrapping_key = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1).derive(password.encode("utf-8"))
    ciphertext = AESGCM(wrapping_key).encrypt(nonce, private_key_bytes, PRIVATE_KEY_CONTEXT)
    payload = {
        "version": 1,
        "kdf": "scrypt",
        "cipher": "AES-256-GCM",
        "salt": base64.urlsafe_b64encode(salt).decode("ascii"),
        "nonce": base64.urlsafe_b64encode(nonce).decode("ascii"),
        "ciphertext": base64.urlsafe_b64encode(ciphertext).decode("ascii"),
    }
    return json.dumps(payload, separators=(",", ":"))


def unprotect_private_key(password: str, payload_json: str) -> bytes:
    payload = json.loads(payload_json)
    salt = base64.urlsafe_b64decode(payload["salt"])
    nonce = base64.urlsafe_b64decode(payload["nonce"])
    ciphertext = base64.urlsafe_b64decode(payload["ciphertext"])
    wrapping_key = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1).derive(password.encode("utf-8"))
    return AESGCM(wrapping_key).decrypt(nonce, ciphertext, PRIVATE_KEY_CONTEXT)
