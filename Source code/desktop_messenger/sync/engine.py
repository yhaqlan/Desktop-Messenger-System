from __future__ import annotations

import base64
import json

from ..domain.models import utc_now
from .operations import SyncOperation


class SyncEngine:
    def __init__(self, repository):
        self.repository = repository

    def export_pending(self, limit: int = 100) -> list[SyncOperation]:
        operations = []
        for row in self.repository.pending_operations(limit):
            operations.append(
                SyncOperation(
                    operation_uuid=row["operation_uuid"],
                    operation_type=row["operation_type"],
                    entity_uuid=row["entity_uuid"],
                    owner_user_uuid=row["owner_user_uuid"],
                    payload=json.loads(row["payload_json"]),
                    created_at=row["created_at"],
                )
            )
        return operations

    def acknowledge(self, operation_uuid: str) -> None:
        with self.repository.db.transaction() as conn:
            conn.execute(
                "UPDATE pending_operations SET status = 'completed', updated_at = ? WHERE operation_uuid = ?",
                (utc_now(), operation_uuid),
            )

    def apply_remote(self, operation: SyncOperation, source_peer_uuid: str | None = None) -> bool:
        now = utc_now()
        with self.repository.db.transaction() as conn:
            if conn.execute(
                "SELECT 1 FROM applied_operations WHERE operation_uuid = ?", (operation.operation_uuid,)
            ).fetchone():
                return False

            payload = operation.payload
            if operation.operation_type == "message.upsert":
                conn.execute(
                    """INSERT OR IGNORE INTO messages(
                           message_uuid, chat_uuid, sender_user_uuid, ciphertext, nonce, status, client_created_at
                       ) VALUES (?, ?, ?, ?, ?, 'sent', ?)""",
                    (
                        payload["message_uuid"],
                        payload["chat_uuid"],
                        payload["sender_user_uuid"],
                        base64.b64decode(payload["ciphertext"]),
                        base64.b64decode(payload["nonce"]),
                        payload.get("client_created_at", operation.created_at),
                    ),
                )
            elif operation.operation_type == "friend_request.upsert":
                conn.execute(
                    """INSERT INTO friend_requests(
                           request_uuid, sender_user_uuid, receiver_user_uuid, status, created_at, updated_at
                       ) VALUES (?, ?, ?, ?, ?, ?)
                       ON CONFLICT(request_uuid) DO UPDATE SET
                         status = excluded.status,
                         updated_at = excluded.updated_at
                       WHERE excluded.updated_at > friend_requests.updated_at""",
                    (
                        payload["request_uuid"],
                        payload["sender_user_uuid"],
                        payload["receiver_user_uuid"],
                        payload["status"],
                        payload["created_at"],
                        payload["updated_at"],
                    ),
                )
            elif operation.operation_type == "notification.upsert":
                conn.execute(
                    """INSERT OR IGNORE INTO notifications(
                           notification_uuid, user_uuid, actor_user_uuid, notification_type,
                           related_entity_uuid, title, body, is_read, created_at
                       ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        payload["notification_uuid"],
                        payload["user_uuid"],
                        payload.get("actor_user_uuid"),
                        payload["notification_type"],
                        payload.get("related_entity_uuid"),
                        payload["title"],
                        payload["body"],
                        int(payload.get("is_read", 0)),
                        payload["created_at"],
                    ),
                )
            else:
                raise ValueError(f"Unsupported synchronization operation: {operation.operation_type}")

            conn.execute(
                "INSERT INTO applied_operations(operation_uuid, source_peer_uuid, applied_at) VALUES (?, ?, ?)",
                (operation.operation_uuid, source_peer_uuid, now),
            )
        return True
