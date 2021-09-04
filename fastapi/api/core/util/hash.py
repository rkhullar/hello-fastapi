import base64
import hashlib
import json
import random
import string
from dataclasses import dataclass


@dataclass
class HashFactory:
    algorithm: str = 'blake2b'
    encoding: str = 'utf-8'
    char_space: str = string.ascii_lowercase + string.ascii_uppercase + string.digits

    def hash_text(self, text: str) -> str:
        hash_object = hashlib.new(self.algorithm)
        hash_object.update(text.encode(self.encoding))
        raw_digest = hash_object.digest()
        return base64.b64encode(raw_digest).decode(self.encoding)

    def hash_data(self, data: dict = None, salt: str = None, **extra):
        to_hash = dict()
        to_hash.update(data or dict())
        to_hash.update(extra)
        if salt:
            to_hash['salt'] = salt
        json_str = json.dumps(to_hash, sort_keys=True, separators=(',', ':'))
        return self.hash_text(json_str)

    def build_salt(self, size: int = 16) -> str:
        return ''.join(random.choice(self.char_space) for _ in range(size))
