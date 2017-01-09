import hashlib
import random


def generate_confirmation_token(email_address):
    salt = hashlib.sha1(str(random.random()).encode('ascii')).hexdigest()[:5]
    email_salt = email_address
    return str(hashlib.sha1(str(salt + email_salt).encode('ascii')).hexdigest())