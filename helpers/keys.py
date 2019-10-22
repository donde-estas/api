"""This module contains every key helper needed inside the API."""


import os
import string
from secrets import choice
import bcrypt


LOG_ROUNDS = os.environ.get("LOG_ROUNDS") or 12
KEY_LENGTH = os.environ.get("KEY_LENGTH") or 16
ALPHABET = string.ascii_letters + string.digits


def generate_random_key():
    """
    Generates a random alphanumeric key of length :KEY_LENGTH
    with at least one lowercase character, one uppercase character and
    at least 4 digits.
    """
    # Based on the secrets module documentation
    while True:
        key = ''.join(choice(ALPHABET) for _ in range(int(KEY_LENGTH)))
        if (any(c.islower() for c in key) and any(
                c.isupper() for c in key) and sum(
                    c.isdigit() for c in key) >= 4):
            return key


def generate_key_digest(plain_key):
    """Digests a key using :LOG_ROUNDS log rounds."""
    return bcrypt.hashpw(
        plain_key.encode('utf-8'), bcrypt.gensalt(int(LOG_ROUNDS))
    )


def check_key(plain_key, key_digest):
    """Checks if :plain_key is the key to :key_digest"""
    return bcrypt.checkpw(plain_key, key_digest)
