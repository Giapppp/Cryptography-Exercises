from Crypto.Util.number import *
from pkcs1 import emsa_pkcs1_v15
BIT_LENGTH = 768

def solve_e(m, s):
    print("log...")
    _m = mod(m, n)
    _s = mod(s, n)
    e = int(log(_m, _s))
    return e

def smooth_prime(size):
    i = 2
    smooth_p = 1
    while smooth_p < size or not isPrime(smooth_p + 1):
        smooth_p *= i
        i += 1
    smooth_p += 1
    return smooth_p


p = smooth_prime(1<<900)
n = p**2

def xor(a, b):
  return [x ^ y for x,y in zip(a, b)]

from pwn import remote
import json
io=remote("socket.cryptohack.org", int(13394))
print(io.recvline())

#get signature
io.sendline(json.dumps({"option":"get_signature"}).encode())
data = json.loads(io.readline())
s = int(data["signature"], 16)

#send n and get suffix
io.sendline(json.dumps({'option':'set_pubkey', 'pubkey':hex(n)}).encode())
data = json.loads(io.readline())
suffix = data["suffix"]

msg1 = "This is a test for a fake signature." + suffix
msg2 = "My name is Giapppp and I own CryptoHack.org" + suffix
msg3 = "Please send all my money to 1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2" + suffix

m1 = bytes_to_long(emsa_pkcs1_v15.encode(msg1.encode(), BIT_LENGTH // 8))
m2 = bytes_to_long(emsa_pkcs1_v15.encode(msg2.encode(), BIT_LENGTH // 8))
m3 = bytes_to_long(emsa_pkcs1_v15.encode(msg3.encode(), BIT_LENGTH // 8))

e1 = solve_e(m1, s)
io.sendline(json.dumps({'option':'claim','msg':msg1, 'e':hex(int(e1)), 'index':int(0)}))
data1 = json.loads(io.readline().decode())

e2 = solve_e(m2, s)
io.sendline(json.dumps({'option':'claim','msg':msg2, 'e':hex(int(e2)), 'index':int(1)}))
data2 = json.loads(io.readline().decode())

e3 = solve_e(m3, s)
io.sendline(json.dumps({'option':'claim','msg':msg3, 'e':hex(int(e3)), 'index':int(2)}))
data3 = json.loads(io.readline().decode())

s1 = bytes.fromhex(data1['secret'])
s2 = bytes.fromhex(data2['secret'])
s3 = bytes.fromhex(data3['secret'])

def xor(a, b):
    return [x^y for x, y in zip(a, b)]

print(''.join([chr(c) for c in xor(xor(s1, s2), s3)]))
             
