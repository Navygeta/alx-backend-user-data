#!/usr/bin/env python3
"""
Return a salted, hashed password as a byte string.
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Hash and return the password as a byte string."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Validate the provided password against the hashed password."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
