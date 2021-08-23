import hashlib
import base64


def build_hmac_1(text: str, salt: str, algorithm: str = 'blake2b', encoding: str = 'utf-8') -> str:
    hash_object = hashlib.new(algorithm)
    hash_object.update((text + salt).encode(encoding))
    raw_digest = hash_object.digest()
    return base64.b64encode(raw_digest).decode(encoding)


def build_hmac_2(text: str, salt: str, algorithm: str = 'blake2b', encoding: str = 'utf-8') -> str:
    hash_object = hashlib.new(algorithm)
    hash_object.update((text + salt).encode(encoding))
    result = hash_object.hexdigest()
    raw = int(result, base=16)
    raw = raw.to_bytes(length=(raw.bit_length() + 7) // 8, byteorder='big')
    return base64.b64encode(raw).decode(encoding)


if __name__ == '__main__':
    example_password = 'aaaaaac'
    result_1 = build_hmac_1(example_password, 'b')
    result_2 = build_hmac_2(example_password, 'b')

    print(result_1)
    print(result_2)
    print(result_1 == result_2)
