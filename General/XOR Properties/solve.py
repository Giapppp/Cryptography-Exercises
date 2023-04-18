from pwn import xor

k1 = 'a6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313'
k1k2 = '37dcb292030faa90d07eec17e3b1c6d8daf94c35d4c9191a5e1e'
k2k3 = 'c1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1'
enc = '04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf'

k2 = xor(bytes.fromhex(k1), bytes.fromhex(k1k2)).hex()
k3 = xor(bytes.fromhex(k2), bytes.fromhex(k2k3)).hex()
flag = xor(bytes.fromhex(enc), bytes.fromhex(k1), bytes.fromhex(k2), bytes.fromhex(k3))
print(flag.decode())
