from __future__ import annotations

import base64
import uuid

from ..security.crypto import derive_message_key, encrypt_message


class AccountService:
    def __init__(self, repository):
        self.repository = repository

    def register(self, username: str, display_name: str, password: str, email: str | None = None):
        return self.repository.create_user(username, display_name, password, email)

    def login(self, username: str, password: str):
        return self.repository.authenticate(username, password)


class MessagingService:
    def __init__(self, repository):
        self.repository = repository

    def create_encrypted_message(
        self,
        sender_uuid: str,
        receiver_uuid: str,
        sender_private_key: bytes,
        receiver_public_key: bytes,
        plaintext: str,
    ) -> tuple[str, str]:
        if not plaintext.strip():
            raise ValueError("Message cannot be empty")
        chat_uuid = self.repository.ensure_direct_chat(sender_uuid, receiver_uuid)
        message_uuid = str(uuid.uuid4())
        message_key = derive_message_key(sender_private_key, receiver_public_key, chat_uuid)
        nonce, ciphertext = encrypt_message(message_key, plaintext, message_uuid)
        self.repository.store_message(message_uuid, chat_uuid, sender_uuid, nonce, ciphertext)
        self.repository.queue_operation(
            sender_uuid,
            "message.upsert",
            message_uuid,
            {
                "message_uuid": message_uuid,
                "chat_uuid": chat_uuid,
                "sender_user_uuid": sender_uuid,
                "nonce": base64.b64encode(nonce).decode("ascii"),
                "ciphertext": base64.b64encode(ciphertext).decode("ascii"),
            },
        )
        return chat_uuid, message_uuid
