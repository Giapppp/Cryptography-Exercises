from pwn import remote
from json import loads, dumps
from sympy.ntheory import discrete_log
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib


def is_pkcs7_padded(message):
    padding = message[-message[-1] :]
    return all(padding[i] == len(padding) for i in range(0, len(padding)))


def decrypt_flag(shared_secret: int, iv: str, ciphertext: str):
    # Derive AES key from shared secret
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode("ascii"))
    key = sha1.digest()[:16]
    # Decrypt flag
    ciphertext = bytes.fromhex(ciphertext)
    iv = bytes.fromhex(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)
    if is_pkcs7_padded(plaintext):
        return unpad(plaintext, 16).decode("ascii")
    else:
        return plaintext.decode("ascii")


(io := remote("socket.cryptohack.org", 13373)).recvuntil(b": ")

alice = loads(io.recvline().decode())
io.recvline()
io.recvuntil(b": ")
encrypted = loads(io.recvline().decode())

io.recvuntil(b": ")
# g must be coprime with composite p
io.sendline(dumps({"p": hex(p := 1 << 1536), "g": hex(g := 3), "A": hex(1)}))
io.recvuntil(b": ")
B = int(loads(io.recvline().decode())["B"], 16)
io.close()
assert B == pow(g, b := discrete_log(p, B, g), p)
print(
    decrypt_flag(
        pow(int(alice["A"], 16), b, int(alice["p"], 16)),
        encrypted["iv"],
        encrypted["encrypted"],
    )
)
