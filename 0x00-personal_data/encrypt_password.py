#!/usr/bin/env python3
"""Module with a python script"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Function that hashes the password"""
    encoded = password.encode()
    hashed = bcrypt.hashpw(encoded, bcrypt.gensalt())

    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Function that validates the password"""
    valid = False
    encoded = password.encode()
    if bcrypt.checkpw(encoded, hashed_password):
        valid = True
    return valid
