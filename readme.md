# VCSecret

This Python utility and library is used to keep your secret value on Version Control Software. The secret value are encrypted with a public key so everyone can write them. However, the private key is required to decrypt those values. The private key should be stored only on the server running the app.

## Installation

Tested with Python 2.7 and Python 3.4.

Install with pip: `pip install vcsecret`

## Encrypt Secrets

First, to generate a key pair run `vcsecret.py -g`. This should give you a result similar to:
```
Public key:
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAhlze8zfvl48cVYzMTdFwaxPa2TxWbLO6fUwCtCQZ7dfm7wS+LdTLR7TTKTyJiTzfnMHZwbn1UHEqCmgQ0fQ4f1uMU+Oh1RYh3X8nnstkKJ1lyxrmEhvdzO4Vq2O6UtvF7fvV2hyAWdDlPKEXvEvxeYSHtvxEAGT3NcypVDAggG30Khhy2r9W0bKmyB+FPZWCA/zIXp/TEJ+fQeKXfxsEssDKXRnju6dcnD+NqNBAA5OZu9X4GLNR6pxGaEObwfwhhG1tBPUfHMkH5klApb0V6yEyw/y6y2IadJkbKumeT+oKfQ9sFRkeyyRRoaqGYKxqbT9pYUQYsAJN3VBEE7MWCwIDAQAB

Private key:
MIIEowIBAAKCAQEAhlze8zfvl48cVYzMTdFwaxPa2TxWbLO6fUwCtCQZ7dfm7wS+LdTLR7TTKTyJiTzfnMHZwbn1UHEqCmgQ0fQ4f1uMU+Oh1RYh3X8nnstkKJ1lyxrmEhvdzO4Vq2O6UtvF7fvV2hyAWdDlPKEXvEvxeYSHtvxEAGT3NcypVDAggG30Khhy2r9W0bKmyB+FPZWCA/zIXp/TEJ+fQeKXfxsEssDKXRnju6dcnD+NqNBAA5OZu9X4GLNR6pxGaEObwfwhhG1tBPUfHMkH5klApb0V6yEyw/y6y2IadJkbKumeT+oKfQ9sFRkeyyRRoaqGYKxqbT9pYUQYsAJN3VBEE7MWCw...
```

You can write the public key to .vckey at the root of your repository. This will be used to encrypt new value by everyone. Keep the private key in a safe location.

To encrypt a new value, run `vcsecret.py -e 'SecretPassword'`. This should output something similar in the terminal:
```
!!vcsecret:WczC5C59ZULLEoVz6W/SHf1rDYlCBlpEHNo90ty1L7mbstSfwA3/9VK9KTgoU/lu+fl95O1kQNbErFtrnGmjHDmkHBZfdXfsy/CrbIHTZ0L8Z2lEbvI8y5pxekZmitKz7Es6dmLxQcPmQxQb7cBfivewq9Km3apske02rBow5F+AaJ1oJ7Jm+OzqwuNqHqq3IFQkB/4iT4DL67AkwRMcbYDCP30D7fx6KckuQcF2+J6ysenwpCWH83sB0Efw1G87gwzkw6rNA6PqeWxNXVd0qL28+I6PE9MN4b8cmAsLGjM0w02HmBic80f7U00Ju0HjsC9TxUG9o/6QiE2rz0jIig==:WNhFPpqcEJyIyOgPJxp3UQ==:RJZTU8gm5I88GozGEzcX8Q==
```

This is the encrypted value to keep in your configuration files.

## Decrypt Secrets

First, you need to get the private key and create a `VCSecret` instance. The private key can be stored either in a non-versionned file or in a environnement variable.

```python
key = os.environ['VCSECRET_KEY']
secret = vcsecret.VCSecret(key)
```

You can then either decrypt one key at a time:
```python
'SecretPassword' == secret.decrypt(config.password)
```

Or decrypt a dictionnary, looking for value starting with `!!vcsecret:`:
```python
config = {
    'foo':'bar',
    'password': '!!vcsecret:...' # value generated from "vcsecret -e 'SecretPassword'"
  }
secret.decrypt_dict(config)
config.password == 'SecretPassword'
```

That's it, no need to keep and manage dozens of secrets in environnement variables on your production server anymore!
