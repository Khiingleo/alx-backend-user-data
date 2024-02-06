#!/usr/bin/env python3
""" encrypting passwords"""
import bcrypt


def hash_password(password: str) -> bytes:
    """hashes a password"""

    hashed_password = bcrypt.hashpw(password.encode('utf-8'),
                                    bcrypt.gensalt())
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ determines if hashed and unhashed passwords are same"""
    is_valid = bcrypt.checkpw(password.encode('utf-8'), hashed_password)
    return is_valid
