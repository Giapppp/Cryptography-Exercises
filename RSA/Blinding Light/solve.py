from pwn import *
from Crypto.Util.number import bytes_to_long
from json import loads
io = remote("socket.cryptohack.org", 13376)

io.recvline()
io.sendline(b'{"option":"get_pubkey"}')
x=loads(io.recvline().strip().decode())
n,e=int(x["N"],16),int(x["e"],16)

m = bytes_to_long(b"admin=True") 

m2 = (2**e*m) % n

io.sendline(b'{"option":"sign","msg":"'+hex(m2)[2:].encode()+b'"}')
s2=int(loads(io.recvline().strip().decode())["signature"],16)

s = s2*pow(2,-1,n)%n
io.sendline(b'{"option":"verify","msg":"'+hex(m)[2:].encode()+b'","signature":"'+hex(s)[2:].encode() +b'"}')
print(loads(io.recvline().strip().decode())["response"])
