import hashlib
import base64
import random
import string
import json

default_algorithm = 'blake2b'
default_encoding = 'utf-8'
default_char_space = string.ascii_lowercase + string.ascii_uppercase + string.digits


def build_text_hash(text: str, algorithm: str = default_algorithm, encoding: str = default_encoding) -> str:
    hash_object = hashlib.new(algorithm)
    hash_object.update(text.encode(encoding))
    raw_digest = hash_object.digest()
    return base64.b64encode(raw_digest).decode(encoding)


def build_json_hash(data: dict, salt: str = None, algorithm: str = default_algorithm, encoding: str = default_encoding):
    to_hash = dict(data)
    if salt:
        to_hash['salt'] = salt
    json_str = json.dumps(to_hash, sort_keys=True, separators=(',', ':'))
    return build_text_hash(json_str, algorithm=algorithm, encoding=encoding)


def build_salt(size: int = 16, char_space: str = default_char_space) -> str:
    return ''.join(random.choice(char_space) for _ in range(size))
