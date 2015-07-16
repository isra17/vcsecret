from vcsecret import VCSecret
from Crypto.PublicKey import RSA
from Crypto import Random
from base64 import b64encode
import argparse, sys

def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-g', '--generate', action='store_true')
    group.add_argument('-e', '--encrypt', action='store')
    group.add_argument('-s', '--generatesecret', action='store', type=int)
    parser.add_argument('-k', '--key', action='store', required=False)

    args = parser.parse_args()
    if args.generate:
        key = RSA.generate(2048)
        pk = b64encode(key.exportKey(format='DER')).decode('utf-8')
        pub = b64encode(key.publickey().exportKey(format='DER')).decode('utf-8')
        print('Public key:\n{}\n'.format(pub))
        print('Private key:\n{}'.format(pk))
    else:
        key = None
        if args.key:
            key = args.key
        else:
            try:
                key = open('.vckey', 'r').read()
            except FileNotFoundError:
                pass
        if (args.encrypt or ars.generatesecret) and not key:
            print('Require --key or .vskey')
            sys.exit(1)

        elif args.encrypt:
            secret = VCSecret(key)
            enc = secret.encrypt(args.encrypt)
            print(enc)
        elif args.generatesecret:
            secret = VCSecret(key)
            secret_value = b64encode(Random.get_random_bytes(args.generatesecret)).decode()
            print('Secret:\n{}\n'.format(secret_value))
            enc = secret.encrypt(secret_value)
            print('Encrypted secret:\n{}\n'.format(enc))
        else:
            parser.print_help()

if __name__ == '__main__':
    main()
