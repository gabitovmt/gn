import json

from cryptography.fernet import Fernet


class CryptoService:

    def __init__(self, key_filename: str):
        with open(key_filename) as f:
            key = f.read().rstrip()
            self.__cipher_suite = Fernet(key)

    def decrypt(self, data):
        return json.loads(self.__cipher_suite.decrypt(data).decode('utf-8'))

    def encrypt(self, data):
        return self.__cipher_suite.encrypt(json.dumps(data).encode('utf-8'))


def load_properties() -> dict[str, str]:
    d = {}
    with open('application.properties') as f:
        for line in f:
            if '=' not in line:
                continue
            key, value = line.rstrip().split('=', maxsplit=1)
            print('->', key, value)
            d[key] = value

    return d


if __name__ == '__main__':
    props = load_properties()
    crypto_service = CryptoService(props['key'])
