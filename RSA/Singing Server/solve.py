from pwn import *
import json

r = remote("socket.cryptohack.org", 13374)
r.recvline()
r.sendline(json.dumps({"option": "get_secret"}))
secret = json.loads(r.recvline())["secret"]
r.sendline(json.dumps({"option": "sign", "msg": secret})) 
print(bytes.fromhex(json.loads(r.recvline())["signature"][2:])) 
