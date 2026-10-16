from __future__ import annotations

from dataclasses import dataclass

from .crypto import unprotect_private_key


@dataclass(slots=True)
class UnlockedIdentity:
    user_uuid: str
    private_key: bytes
    public_key: bytes


def unlock_identity(user_row, password: str) -> UnlockedIdentity:
    return UnlockedIdentity(
        user_uuid=user_row["user_uuid"],
        private_key=unprotect_private_key(password, user_row["protected_private_key"]),
        public_key=user_row["public_key"],
    )
