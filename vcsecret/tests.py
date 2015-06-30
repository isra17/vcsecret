from Crypto.PublicKey import RSA
from base64 import b64encode
import unittest
import vcsecret

class TestVCSecret(unittest.TestCase):
    def setUp(self):
        key = RSA.generate(2048)
        self.private_key = b64encode(key.exportKey(format='DER'))
        self.public_key = b64encode(key.publickey().exportKey(format='DER'))

        self.private_secret = vcsecret.VCSecret(self.private_key)
        self.public_secret = vcsecret.VCSecret(self.public_key)

        self.secret = payload = self.public_secret.encrypt('secret')

    def test_encrypt(self):
        payload = self.public_secret.encrypt('test')

        self.assertEqual(4, len(payload.split(':')))
        self.assertTrue(payload.startswith('!!vcsecret:'))

    def test_decrypt(self):
        payload = self.private_secret.decrypt(self.secret)

        self.assertEqual('secret', payload)

    def test_decrypt_obj(self):
        dict_enc = {
                'a': 'not_a_secret',
                'b': self.secret,
                'c': [123, self.secret],
                'd': {'secret': self.secret, 'foo':b'bar'}
            }

        self.private_secret.decrypt_obj(dict_enc)
        self.assertEqual({
            'a': 'not_a_secret',
            'b': 'secret',
            'c': [123, 'secret'],
            'd': {'secret':'secret', 'foo':b'bar'}
            }, dict_enc)

    def test_decrypt_require_private_key(self):
        with self.assertRaises(vcsecret.CannotDecrypt):
            self.public_secret.decrypt(self.secret)

