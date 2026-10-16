import unittest

from desktop_messenger.security.crypto import (
    decrypt_message,
    derive_message_key,
    encrypt_message,
    generate_identity_keypair,
    protect_private_key,
    unprotect_private_key,
)
from desktop_messenger.security.passwords import hash_password, verify_password


class CryptoTests(unittest.TestCase):
    def test_password_hash_roundtrip(self):
        encoded = hash_password("correct horse battery staple")
        self.assertTrue(verify_password("correct horse battery staple", encoded))
        self.assertFalse(verify_password("wrong password", encoded))

    def test_shared_key_and_message_roundtrip(self):
        private_a, public_a = generate_identity_keypair()
        private_b, public_b = generate_identity_keypair()
        key_a = derive_message_key(private_a, public_b, "chat-1")
        key_b = derive_message_key(private_b, public_a, "chat-1")
        self.assertEqual(key_a, key_b)
        nonce, ciphertext = encrypt_message(key_a, "hello", "message-1")
        self.assertEqual(decrypt_message(key_b, nonce, ciphertext, "message-1"), "hello")

    def test_private_key_protection(self):
        private_key, _ = generate_identity_keypair()
        wrapped = protect_private_key("safe password", private_key)
        self.assertEqual(unprotect_private_key("safe password", wrapped), private_key)


if __name__ == "__main__":
    unittest.main()
