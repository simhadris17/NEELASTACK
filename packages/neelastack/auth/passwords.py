

from argon2 import PasswordHasher
from argon2.exceptions import (
    InvalidHashError,
    VerificationError,
    VerifyMismatchError,
)

pwd = PasswordHasher()


def hash_password(value: str) -> str:
    return pwd.hash(value)


def verify_password(value: str, password_hash: str) -> bool:
    try:
        return pwd.verify(password_hash, value)
    except (InvalidHashError, VerifyMismatchError, VerificationError):
        return False