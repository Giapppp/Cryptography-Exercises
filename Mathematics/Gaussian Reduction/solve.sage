t = vector(ZZ, [846835985, 9834798552]) # for "taller"
s = vector(ZZ, [87502093, 123094980]) # for "shorter"
while True:
    if t.norm() < s.norm():
        t, s = s, t # obviously should swap if this is the case
    p = round(t.dot_product(s)/s.dot_product(s)) # projecting the taller vector onto the shorter & round to the spanned lattice
    if p == 0:
        break
    t -= p*s
print(t.dot_product(s))
