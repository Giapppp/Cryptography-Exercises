enc_flag = "0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104"
unhex_flag = [n for n in bytes.fromhex(enc_flag)]
secret = (ord(c) for c in "crypto{")
key = [(n ^ c) for n, c in zip(secret, unhex_flag)] + [ord("y")] 
print("".join(chr(c) for c in [unhex_flag[i] ^ key[i % len(key)] for i in range(len(unhex_flag))]))
