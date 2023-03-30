import os
import hashlib

WAIT_DURATION = 30


def create_salt():
    return os.urandom(16)


def set(val, salt):
    key = hashlib.pbkdf2_hmac(
        'sha256',
        repr(val).encode('utf-8'),
        salt,
        100000,
        dklen=16
        )
    return key


def evaluate(save_pswd, test_pswd, save_salt):
    return test_pswd[0] == save_pswd[0]



