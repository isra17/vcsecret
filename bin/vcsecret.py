#!/bin/python3

if __name__ == '__main__':
    import argparse, sys
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-g', '--generate', action='store_true')
    group.add_argument('-e', '--encrypt', action='store')
    parser.add_argument('-k', '--key', action='store', required=False)

    args = parser.parse_args()
    if args.generate:
        key = RSA.generate(2048)
        pk = b64encode(key.exportKey(format='DER')).decode('utf-8')
        pub = b64encode(key.publickey().exportKey(format='DER')).decode('utf-8')
        print('Public key:\n{}\n'.format(pub))
        print('Private key:\n{}'.format(pk))

    elif args.encrypt:
        key = None
        if args.key:
            key = args.key
        else:
            try:
                key = open('.vckey', 'r').read()
            except FileNotFoundError:
                pass

        if not key:
            print('Require --key or .vskey')
            sys.exit(1)

        secret = VCSecret(key)
        enc = secret.encrypt(args.encrypt)
        print('Encrypted value:\n{}'.format(enc))
    else:
        parser.print_help()

