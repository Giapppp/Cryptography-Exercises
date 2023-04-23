P = 2
N = 50
E = 31337

def binary2bytes(s):
    return int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='big')

def read_matrix(m):
    l = []
    for y in range(50):
        for x in m:
            l.append(str(x[y]))
    plaintext = ("".join(l))
    return binary2bytes(plaintext[:2480])

def load_matrix(fname):
    data = open(fname, 'r').read().strip()
    rows = [list(map(int, row)) for row in data.splitlines()]
    return Matrix(GF(P), rows)

c = load_matrix("flag.enc")
c = c ** pow(E, -1, c.multiplicative_order())
print(read_matrix(c))
