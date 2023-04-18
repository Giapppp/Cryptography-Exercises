from pwn import *
from Cryptodome.Util import number
import json
import base64
import codecs

r = remote('socket.cryptohack.org', 13377, level = 'debug')

def json_recv():
    line = r.recvline()
    return json.loads(line.decode())

def json_send(hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request)

def solvePuzzle(received):
    if received["type"] == "hex":
        result = str(bytes.fromhex(received["encoded"]))[2:-1]
    elif received["type"] == "base64":
        result = str(base64.b64decode(received["encoded"]))[2:-1]
    elif received["type"] == "rot13":
        result = codecs.encode(received["encoded"], 'rot_13')
    elif received["type"] == "bigint":
        result = str(number.long_to_bytes(int(received["encoded"], 16)))[2:-1]      
    elif received["type"] == "utf-8":
        result = ''.join(map(str, [chr(num) for num in received["encoded"]]))
        
    to_send = {"decoded": result}
    json_send(to_send)

for i in range(101):
    solvePuzzle(json_recv())
