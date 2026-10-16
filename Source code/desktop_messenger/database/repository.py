from __future__ import annotations

import json
import uuid
from pathlib import Path

from ..domain.models import utc_now
from ..security.crypto import generate_identity_keypair, protect_private_key
from ..security.passwords import hash_password, verify_password
from .connection import Database


class MessengerRepository:
    def __init__(self, database_path: Path):
        self.db = Database(database_path)
        self.db.initialize()

    def create_user(self, username: str, display_name: str, password: str, email: str | None = None):
        username = username.strip()
        display_name = display_name.strip()
        if not username or not display_name:
            raise ValueError("Username and display name are required")
        private_key, public_key = generate_identity_keypair()
        now = utc_now()
        user_uuid = str(uuid.uuid4())
        with self.db.transaction() as conn:
            conn.execute(
                """INSERT INTO users(
                       user_uuid, username, display_name, email, password_hash,
                       public_key, protected_private_key, created_at, updated_at
                   ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    user_uuid,
                    username,
                    display_name,
                    email.strip() if email else None,
                    hash_password(password),
                    public_key,
                    protect_private_key(password, private_key),
                    now,
                    now,
                ),
            )
        return self.get_user(user_uuid)

    def get_user(self, user_uuid: str):
        with self.db.connect() as conn:
            return conn.execute("SELECT * FROM users WHERE user_uuid = ? AND deleted_at IS NULL", (user_uuid,)).fetchone()

    def find_user(self, username: str):
        with self.db.connect() as conn:
            return conn.execute(
                "SELECT * FROM users WHERE username = ? COLLATE NOCASE AND deleted_at IS NULL", (username.strip(),)
            ).fetchone()

    def authenticate(self, username: str, password: str):
        row = self.find_user(username)
        return row if row is not None and verify_password(password, row["password_hash"]) else None

    def search_users(self, query: str, exclude_user_uuid: str, limit: int = 20):
        pattern = f"%{query.strip()}%"
        with self.db.connect() as conn:
            return conn.execute(
                """SELECT user_uuid, username, display_name, public_key
                   FROM users
                   WHERE deleted_at IS NULL AND user_uuid <> ?
                     AND (username LIKE ? COLLATE NOCASE OR display_name LIKE ? COLLATE NOCASE)
                   ORDER BY display_name LIMIT ?""",
                (exclude_user_uuid, pattern, pattern, limit),
            ).fetchall()

    def send_friend_request(self, sender_uuid: str, receiver_uuid: str) -> str:
        if sender_uuid == receiver_uuid:
            raise ValueError("Cannot send a friend request to the same account")
        request_uuid = str(uuid.uuid4())
        now = utc_now()
        with self.db.transaction() as conn:
            conn.execute(
                """INSERT INTO friend_requests(
                       request_uuid, sender_user_uuid, receiver_user_uuid, status, created_at, updated_at
                   ) VALUES (?, ?, ?, 'pending', ?, ?)""",
                (request_uuid, sender_uuid, receiver_uuid, now, now),
            )
        return request_uuid

    def respond_to_friend_request(self, request_uuid: str, receiver_uuid: str, accept: bool) -> str | None:
        now = utc_now()
        with self.db.transaction() as conn:
            row = conn.execute(
                "SELECT * FROM friend_requests WHERE request_uuid = ? AND receiver_user_uuid = ? AND status = 'pending'",
                (request_uuid, receiver_uuid),
            ).fetchone()
            if row is None:
                raise ValueError("Pending friend request not found")
            status = "accepted" if accept else "rejected"
            conn.execute("UPDATE friend_requests SET status = ?, updated_at = ? WHERE request_uuid = ?", (status, now, request_uuid))
            if not accept:
                return None
            low, high = sorted((row["sender_user_uuid"], row["receiver_user_uuid"]))
            friendship_uuid = str(uuid.uuid5(uuid.NAMESPACE_URL, f"desktop-messenger:friendship:{low}:{high}"))
            conn.execute(
                """INSERT INTO friendships(friendship_uuid, user_low_uuid, user_high_uuid, status, created_at, updated_at)
                   VALUES (?, ?, ?, 'active', ?, ?)
                   ON CONFLICT(user_low_uuid, user_high_uuid)
                   DO UPDATE SET status = 'active', updated_at = excluded.updated_at""",
                (friendship_uuid, low, high, now, now),
            )
            return friendship_uuid

    def list_friends(self, user_uuid: str):
        with self.db.connect() as conn:
            return conn.execute(
                """SELECT u.user_uuid, u.username, u.display_name, u.public_key
                   FROM friendships f
                   JOIN users u ON u.user_uuid = CASE
                     WHEN f.user_low_uuid = ? THEN f.user_high_uuid ELSE f.user_low_uuid END
                   WHERE f.status = 'active' AND (f.user_low_uuid = ? OR f.user_high_uuid = ?)
                   ORDER BY u.display_name""",
                (user_uuid, user_uuid, user_uuid),
            ).fetchall()

    def ensure_direct_chat(self, first_user_uuid: str, second_user_uuid: str) -> str:
        low, high = sorted((first_user_uuid, second_user_uuid))
        chat_uuid = str(uuid.uuid5(uuid.NAMESPACE_URL, f"desktop-messenger:direct-chat:{low}:{high}"))
        now = utc_now()
        with self.db.transaction() as conn:
            conn.execute(
                """INSERT OR IGNORE INTO chats(chat_uuid, chat_type, created_by_uuid, created_at, updated_at)
                   VALUES (?, 'direct', ?, ?, ?)""",
                (chat_uuid, first_user_uuid, now, now),
            )
            for member in (first_user_uuid, second_user_uuid):
                conn.execute(
                    "INSERT OR IGNORE INTO chat_members(chat_uuid, user_uuid, role, joined_at) VALUES (?, ?, 'member', ?)",
                    (chat_uuid, member, now),
                )
        return chat_uuid

    def store_message(
        self,
        message_uuid: str,
        chat_uuid: str,
        sender_user_uuid: str,
        nonce: bytes,
        ciphertext: bytes,
        status: str = "pending",
        created_at: str | None = None,
    ) -> None:
        with self.db.transaction() as conn:
            conn.execute(
                """INSERT OR IGNORE INTO messages(
                       message_uuid, chat_uuid, sender_user_uuid, ciphertext, nonce, status, client_created_at
                   ) VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (message_uuid, chat_uuid, sender_user_uuid, ciphertext, nonce, status, created_at or utc_now()),
            )

    def list_chat_messages(self, chat_uuid: str, limit: int = 100):
        with self.db.connect() as conn:
            return conn.execute(
                "SELECT * FROM messages WHERE chat_uuid = ? ORDER BY client_created_at DESC LIMIT ?",
                (chat_uuid, limit),
            ).fetchall()

    def queue_operation(self, owner_uuid: str, operation_type: str, entity_uuid: str, payload: dict) -> str:
        operation_uuid = str(uuid.uuid4())
        now = utc_now()
        with self.db.transaction() as conn:
            conn.execute(
                """INSERT INTO pending_operations(
                       operation_uuid, owner_user_uuid, operation_type, entity_uuid,
                       payload_json, status, created_at, updated_at
                   ) VALUES (?, ?, ?, ?, ?, 'pending', ?, ?)""",
                (operation_uuid, owner_uuid, operation_type, entity_uuid, json.dumps(payload, separators=(",", ":")), now, now),
            )
        return operation_uuid

    def pending_operations(self, limit: int = 100):
        with self.db.connect() as conn:
            return conn.execute(
                "SELECT * FROM pending_operations WHERE status IN ('pending', 'failed') ORDER BY created_at LIMIT ?", (limit,)
            ).fetchall()
