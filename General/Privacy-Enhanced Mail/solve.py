from Crypto.PublicKey import RSA

f=open("key.pem", "r")
key=RSA.importKey(f.read())

print(key.d)
