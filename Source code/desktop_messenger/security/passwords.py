from __future__ import annotations

import base64
import hashlib
import hmac
import os


N = 2**14
R = 8
P = 1
DKLEN = 32


def hash_password(password: str) -> str:
    if len(password) < 8:
        raise ValueError("Password must contain at least eight characters")
    salt = os.urandom(16)
    digest = hashlib.scrypt(password.encode("utf-8"), salt=salt, n=N, r=R, p=P, dklen=DKLEN)
    return "scrypt${}${}${}${}${}".format(
        N,
        R,
        P,
        base64.urlsafe_b64encode(salt).decode("ascii"),
        base64.urlsafe_b64encode(digest).decode("ascii"),
    )


def verify_password(password: str, encoded: str) -> bool:
    try:
        name, n, r, p, salt_b64, digest_b64 = encoded.split("$")
        if name != "scrypt":
            return False
        salt = base64.urlsafe_b64decode(salt_b64)
        expected = base64.urlsafe_b64decode(digest_b64)
        actual = hashlib.scrypt(
            password.encode("utf-8"), salt=salt, n=int(n), r=int(r), p=int(p), dklen=len(expected)
        )
        return hmac.compare_digest(actual, expected)
    except (ValueError, TypeError):
        return False
