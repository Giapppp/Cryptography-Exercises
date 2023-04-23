import json
from pwn import *
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
from Crypto.Util.number import inverse

def is_pkcs7_padded(message):
  padding = message[-message[-1]:]
  return all(padding[i] == len(padding) for i in range(0, len(padding)))


con = remote('socket.cryptohack.org',13380)
con.recvuntil(b'Intercepted from Alice: ')
alice = json.loads(con.recvline())
p_hex, g_hex, A_hex = alice['p'],alice['g'],alice['A']
con.recvuntil(b'Intercepted from Bob: ')
B_hex = json.loads(con.recvline())['B']
con.recvuntil(b'Intercepted from Alice: ')
data = json.loads(con.recvline())

iv_hex, encrypted_hex = data['iv'], data['encrypted']

p = int(p_hex, 16)
g = int(g_hex, 16)
A = int(A_hex, 16)
B = int(B_hex, 16)
i = inverse(g, p)
A_secret = (A*i)%p
shared_secret = (B*A_secret)%p
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

print(decrypt_flag(shared_secret,iv_hex, encrypted_hex))
