from Crypto.Cipher import AES 
import hashlib 
import requests

def blocks(ct,blocksize = 16):   
    return [ct[i:i+blocksize] for i in range(0,len(ct),blocksize)] 
                                                                     
with open("/usr/share/dict/words") as f: 
    words = [w.strip() for w in f.readlines()] 
                                                                     
enc_flag = requests.get('http://aes.cryptohack.org/passwords_as_keys/encrypt_flag/')       
data = enc_flag.json()
ct = blocks(bytes.fromhex(data["ciphertext"]))
         
for i in words: 
    key = hashlib.md5(i.encode()).digest()
    cipher = AES.new(key,AES.MODE_ECB) 
    msg  = cipher.decrypt(ct[0]) 
    if msg[0:6] == b"crypto" : 
        k = i
        x = msg
key = hashlib.md5(k.encode()).digest() 
cipher = AES.new(key,AES.MODE_ECB) 
msg  = x + cipher.decrypt(ct[1]) 
 
print(msg)   
