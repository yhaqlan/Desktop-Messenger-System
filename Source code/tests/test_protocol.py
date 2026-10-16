import json
import unittest

from desktop_messenger.network.protocol import encode_frame, relay_proof


class ProtocolTests(unittest.TestCase):
    def test_frame_encoding(self):
        encoded = encode_frame({"type": "ping"})
        self.assertTrue(encoded.endswith(b"\n"))
        self.assertEqual(json.loads(encoded), {"type": "ping"})

    def test_relay_proof_is_deterministic_and_bound_to_client(self):
        first = relay_proof("password123", "challenge", "client-a")
        second = relay_proof("password123", "challenge", "client-a")
        other = relay_proof("password123", "challenge", "client-b")
        self.assertEqual(first, second)
        self.assertNotEqual(first, other)


if __name__ == "__main__":
    unittest.main()
