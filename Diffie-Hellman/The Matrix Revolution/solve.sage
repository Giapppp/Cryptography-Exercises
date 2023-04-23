from Crypto.Cipher import AES
from Crypto.Hash import SHA256

import json

P = 2
N = 150

def load_matrix(fname):
    data = open(fname, 'r').read().strip()
    rows = [list(map(int, row)) for row in data.splitlines()]
    return Matrix(GF(P), rows)

def ff_discrete_log(poly1, poly2, d):
    K = GF(2^d)
    R.<xd> = PolynomialRing(K)

    poly1 = poly1(xd)
    root1 = poly1.roots()[0][0]

    poly2 = poly2(xd)
    root2 = poly2.roots()[0][0]

    pari_g = pari(root1)
    pari_a = pari(root2)
    ans = int(pari_a.fflog(pari_g))
    
    assert root1^ans == root2
    return ans

G = load_matrix('generator.txt')
A = load_matrix('alice.pub')
B = load_matrix('bob.pub')

def get_alice_priv():
    g61, g89 = factor(G.charpoly())
    a61, a89 = factor(A.charpoly())

    P61 = 2^61 - 1
    P89 = 2^89 - 1

    log61 = int(ff_discrete_log(g61[0], a61[0], 61))
    log89 = int(ff_discrete_log(g89[0], a89[0], 89))

    poss61 = [int(log61 * pow(2, i, P61)) for i in range(61)]
    poss89 = [int(log89 * pow(2, i, P89)) for i in range(89)]

    for p61 in poss61:
        for p89 in poss89:
            poss_alice = crt([p61, p89], [P61, P89])
            if is_prime(poss_alice) and G^poss_alice == A:
                print("Found:", poss_alice)
                return poss_alice

A_priv = get_alice_priv()
shared_secret = B^A_priv

KEY_LENGTH = 128
def derive_aes_key(M):
    mat_str = ''.join(str(x) for row in M for x in row)
    return SHA256.new(data=mat_str.encode()).digest()[:KEY_LENGTH]

key = derive_aes_key(shared_secret)
flag_data = json.load(open('flag.enc', 'r'))

cipher = AES.new(key, AES.MODE_CBC, bytes.fromhex(flag_data['iv']))
plaintext = cipher.decrypt(bytes.fromhex(flag_data['ciphertext']))
print(plaintext)
