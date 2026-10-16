import tempfile
import unittest
from pathlib import Path

from desktop_messenger.database import MessengerRepository


class DatabaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.repo = MessengerRepository(Path(self.temp.name) / "test.sqlite3")

    def tearDown(self):
        self.temp.cleanup()

    def test_create_and_authenticate_user(self):
        user = self.repo.create_user("alice", "Alice", "password123")
        self.assertEqual(user["username"], "alice")
        self.assertIsNotNone(self.repo.authenticate("ALICE", "password123"))
        self.assertIsNone(self.repo.authenticate("alice", "bad password"))

    def test_friendship_and_stable_direct_chat(self):
        alice = self.repo.create_user("alice", "Alice", "password123")
        bob = self.repo.create_user("bob", "Bob", "password123")
        request_uuid = self.repo.send_friend_request(alice["user_uuid"], bob["user_uuid"])
        self.repo.respond_to_friend_request(request_uuid, bob["user_uuid"], True)
        self.assertEqual(len(self.repo.list_friends(alice["user_uuid"])), 1)
        first = self.repo.ensure_direct_chat(alice["user_uuid"], bob["user_uuid"])
        second = self.repo.ensure_direct_chat(bob["user_uuid"], alice["user_uuid"])
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
