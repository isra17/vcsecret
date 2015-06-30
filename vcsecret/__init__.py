from base64 import b64encode, b64decode
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.PublicKey import RSA

# Because people are still using python 2 *boo*
def to_bytes(ints):
    return bytes(bytearray(ints))

def to_byte(c):
    return ord(c) if isinstance(c, str) else c

def _pkcs7_pad(payload):
    length = 16 - (len(payload) % 16)
    return payload + to_bytes([length]*length)

def _pkcs7_unpad(payload):
    return payload[:-to_byte(payload[-1])]

class CannotDecrypt(Exception):
    pass

class VCSecret:
    def __init__(self, key):
        self.key = RSA.importKey(b64decode(key))

    def encrypt(self, value):
        value_key = Random.get_random_bytes(16)
        value_iv = Random.get_random_bytes(16)
        value_cipher = AES.new(value_key, AES.MODE_CBC, value_iv)
        value_enc = value_cipher.encrypt(_pkcs7_pad(value.encode()))

        key_cipher = PKCS1_OAEP.new(self.key)
        key_enc = key_cipher.encrypt(value_key)

        return '!!vcsecret:{}:{}:{}'.format( \
                b64encode(key_enc).decode('utf-8'), \
                b64encode(value_iv).decode('utf-8'), \
                b64encode(value_enc).decode('utf-8'))

    def decrypt(self, payload):
        if not self.key.has_private():
            raise CannotDecrypt()

        (prefix, key_enc, value_iv, value_enc) = payload.split(':')
        if prefix != '!!vcsecret':
            raise InvalidSecretError('Secret "{}" should start with !!vcsecret, are you sure this secret is encrypted?'.format(payload))

        key_enc = b64decode(key_enc)
        value_iv = b64decode(value_iv)
        value_enc = b64decode(value_enc)

        key_cipher = PKCS1_OAEP.new(self.key)
        value_key = key_cipher.decrypt(key_enc)

        value_cipher = AES.new(value_key, AES.MODE_CBC, value_iv)
        value = _pkcs7_unpad(value_cipher.decrypt(value_enc))

        return value.decode('utf-8')

    def decrypt_obj(self, o):
        if isinstance(o, str) and o.startswith('!!vcsecret:'):
            return self.decrypt(o)
        elif isinstance(o, list):
            for i,v in enumerate(o):
                o[i] = self.decrypt_obj(v)
        elif isinstance(o, dict):
            for k,v in iter(o.items()):
                o[k] = self.decrypt_obj(v)
        return o

