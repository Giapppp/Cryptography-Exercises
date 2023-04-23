from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

import json
import codecs
import hashlib

def is_pkcs7_padded(message):
    padding = message[-message[-1]:]
    return all(padding[i] == len(padding) for i in range(0, len(padding)))


def decrypt_flag(shared_secret: int, iv: str, ciphertext: str):
    # Derive AES key from shared secret
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:16]
    # Decrypt flag
    ciphertext = bytes.fromhex(ciphertext)
    iv = bytes.fromhex(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)

    if is_pkcs7_padded(plaintext):
        return unpad(plaintext, 16).decode('ascii')
    else:
        return plaintext.decode('ascii')


alice = {"p": "0xde26ab651b92a129", "g": "0x2", "A": "0x9bf1d8558e7b6768"}
bob = {"B": "0x97e38f7cb7602367"}
flag = {"iv": "427517171ebdc1eb2676462b29c82cab", "encrypted_flag": "a515316381f3af3b965172c99c8a717d5972f2965fb0929245ce42874c15b1b0"}

R = GF(alice["p"])
g = R(alice["g"])
A = R(alice["A"])
B = R(bob["B"])

n = discrete_log(A, g)
print(n)

shared = B**n

print(decrypt_flag(shared, flag["iv"], flag["encrypted_flag"]))
