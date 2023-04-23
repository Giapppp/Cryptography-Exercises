from pwn import remote
import json
from math import prod
from gmpy2 import iroot
from Crypto.Util.number import long_to_bytes

io = remote("socket.cryptohack.org", 13386)
io.recvline()
e = 11
n = -1
flags = []
while len(flags) < 2:
    io.sendline('{"option": "get_flag"}')
    flag = json.loads(io.recvline())
    n = flag["modulus"]
    flags.append([flag["encrypted_flag"], *flag["padding"]])

def gcd(a, b): 
    return a.monic() if b == 0 else gcd(b, a % b)

def franklinreiter(C1, C2, e, N, aa, bb):
    P.<X> = Zmod(N)[]
    g1 = (aa[0]*X + bb[0])^e - C1
    g2 = (aa[1]*X + bb[1])^e - C2
    result = N - gcd(g1, g2).coefficients()[0]
    return long_to_bytes(result)

c1, c2 = tuple(flags)
print(franklinreiter(c1[0], c2[0], e, n, (c1[1], c2[1]), (c1[2], c2[2])))
