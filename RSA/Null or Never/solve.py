from tqdm import tqdm
from Crypto.Util.number import *

def iroot(k, n):
    u, s = n, n+1
    while u < s:
        s = u
        t = (k-1) * s + n // pow(s, k-1)
        u = t // k
    return s
# We don't know the padding length so we store all possible values t in a table
table = []
for k in range(0, 8 * 100, 8):
    y = pow(1 << k, e, n)
    y = inverse(y, n)
    table.append((c * y) % n)
	
for t in tqdm(table):
    for i in range(300):
        z = t + i * n
        x = iroot(e, z)
        x = long_to_bytes(x)
        if b'crypto' in x:
            print(x)
            break
    else:
        continue
    break
