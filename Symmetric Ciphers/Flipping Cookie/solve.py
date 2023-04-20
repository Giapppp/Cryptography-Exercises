from urllib.request import urlopen
import json

url = 'https://aes.cryptohack.org/flipping_cookie/'

def get_cookie():
    result = urlopen(url + 'get_cookie/')
    data = json.loads(result.read())
    b = bytes.fromhex(data['cookie'])
    return (b[:16], b[16:])

def check_admin(iv, cookie):
    result = urlopen(url + 'check_admin/' + cookie.hex() + '/' + iv.hex() + '/')
    return json.loads(result.read())


(iv, cookie) = get_cookie()

plaintext = b"admin=False;expi"
target    = b"admin=True;;expi"

new_iv = bytes([x ^ y ^ z for (x, y, z) in zip(iv, plaintext, target)])

check = check_admin(new_iv, cookie)
if (check['flag']):
    print(check['flag'])
else:
    print("Flag not found", check)
