from Crypto.PublicKey import RSA

with open("bruce_rsa.pub", "rb") as f:
    rsa_key = RSA.import_key(f.read())
    
    print(rsa_key.n)
