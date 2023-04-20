import requests
import json
from binascii import hexlify,unhexlify
from pwn import *

url = "http://aes.cryptohack.org/lazy_cbc"
def encrypt(url,plaintext):
	url +="/encrypt/"+hexlify(plaintext.encode()).decode()+"/"
	return json.loads(requests.get(url).text)

def receive(url,ciphertext):
	url +="/receive/"+ciphertext+"/"
	return json.loads(requests.get(url).text)

def get_flag(url,key):
	url +="/get_flag/"+key+"/"
	return json.loads(requests.get(url).text)['plaintext']

plaintext ='a'*48
ciphertext = encrypt(url,plaintext)['ciphertext']
plaintext  = receive(url,ciphertext[:32]+'0'*32+ciphertext[:32])['error'].split(':')[1].strip()
key = xor(unhexlify(plaintext[:32]).decode(),bytes.fromhex(plaintext[64:]))
print(unhexlify(get_flag(url,key.hex())).decode())
