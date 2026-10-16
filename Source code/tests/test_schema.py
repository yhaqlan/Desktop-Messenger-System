import tempfile
import unittest
from pathlib import Path

from desktop_messenger.database.connection import Database


EXPECTED_TABLES = {
    "users", "devices", "sessions", "friend_requests", "friendships", "chats",
    "chat_members", "messages", "message_receipts", "attachments", "notifications",
    "settings", "peer_connections", "pending_operations", "applied_operations",
    "sync_state", "sync_log",
}


class SchemaTests(unittest.TestCase):
    def test_expected_tables_and_foreign_keys(self):
        with tempfile.TemporaryDirectory() as directory:
            db = Database(Path(directory) / "schema.sqlite3")
            db.initialize()
            with db.connect() as conn:
                names = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'")}
                self.assertTrue(EXPECTED_TABLES.issubset(names))
                self.assertEqual(conn.execute("PRAGMA foreign_keys").fetchone()[0], 1)


if __name__ == "__main__":
    unittest.main()
