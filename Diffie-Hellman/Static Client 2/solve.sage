from Crypto.Util.number import isPrime, long_to_bytes, getPrime
from pwn import remote
from sympy.ntheory.residue_ntheory import discrete_log
from json import loads, dumps
r = remote("socket.cryptohack.org", 13378)

A_data = loads(r.recvline().split(b":", 1)[1])
B_data = loads(r.recvline().split(b":", 1)[1])
cipher = loads(r.recvline().split(b":", 1)[1])
p = int(A_data["p"], 16)
A = int(A_data["A"],16)

i = 2
smooth_p = 1
while smooth_p < p or not isPrime(smooth_p + 1):
    smooth_p *= i
    i += 1
smooth_p += 1

r.sendline(dumps({
    "g":"0x02",
    "A": hex(A),
    "p": hex(smooth_p)
}).encode())
B = int(r.recvline().decode().split()[13][1:-2],16)

b = discrete_log(smooth_p, B, 2)
shared_secret = pow(A, b, p)

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib

def is_pkcs7_padded(message):
    padding = message[-message[-1]:]
    return all(padding[i] == len(padding) for i in range(0, len(padding)))

def decrypt_flag(shared_secret: int, iv: str, ciphertext: str):
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:16]
    ciphertext = bytes.fromhex(ciphertext)
    iv = bytes.fromhex(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)
    if is_pkcs7_padded(plaintext):
        return unpad(plaintext, 16).decode()
    else:
        return plaintext 

print(decrypt_flag(shared_secret, cipher["iv"], cipher["encrypted"]))
