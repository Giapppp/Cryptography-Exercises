import requests

url_base = 'http://aes.cryptohack.org/triple_des'
weak_key = '0101010101010101FEFEFEFEFEFEFEFE'

def hack():
  response = requests.get(url="%s/encrypt_flag/%s" % (url_base, weak_key)).json()
  ciphertext = response['ciphertext']
  
  response = requests.get(url="%s/encrypt/%s/%s" % (url_base, weak_key, ciphertext)).json()
  plaintext = bytes.fromhex(response['ciphertext']).decode()
  return plaintext

if __name__ == '__main__':
  flag = hack()
  print(flag)
