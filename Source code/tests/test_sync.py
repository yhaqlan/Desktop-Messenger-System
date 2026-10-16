import tempfile
import unittest
import uuid
from pathlib import Path

from desktop_messenger.database import MessengerRepository
from desktop_messenger.domain.models import utc_now
from desktop_messenger.sync import SyncEngine
from desktop_messenger.sync.operations import SyncOperation


class SyncTests(unittest.TestCase):
    def test_operation_is_idempotent(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = MessengerRepository(Path(directory) / "sync.sqlite3")
            alice = repo.create_user("alice", "Alice", "password123")
            operation = SyncOperation(
                operation_uuid=str(uuid.uuid4()),
                operation_type="notification.upsert",
                entity_uuid=str(uuid.uuid4()),
                owner_user_uuid=alice["user_uuid"],
                payload={
                    "notification_uuid": str(uuid.uuid4()),
                    "user_uuid": alice["user_uuid"],
                    "notification_type": "sync",
                    "title": "Synchronized",
                    "body": "Remote operation applied",
                    "created_at": utc_now(),
                },
                created_at=utc_now(),
            )
            engine = SyncEngine(repo)
            self.assertTrue(engine.apply_remote(operation, "peer-1"))
            self.assertFalse(engine.apply_remote(operation, "peer-1"))


if __name__ == "__main__":
    unittest.main()
