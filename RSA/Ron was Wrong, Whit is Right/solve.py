from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from math import gcd

def getN(n):
    with open(str(n)+'.pem') as f:
        key = RSA.importKey(f.read())
    return key.n, key.e

N, e = getN(21)

for i in range(1, 50):
    Ni, _ = getN(i)
    if 1 < gcd(N, Ni) < N:
        p = gcd(N, Ni)
        q = N//p
        phi = (p-1)*(q-1)
        d = pow(e, -1, phi)
        pvt = RSA.construct((N, e, d))
        break

cipher = PKCS1_OAEP.new(pvt)

with open('21.ciphertext') as f:
    enc_flag = bytes.fromhex(f.read())

flag = cipher.decrypt(enc_flag)
print(flag)
