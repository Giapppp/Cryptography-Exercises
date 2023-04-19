PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103]
ct = 1350995397927355657956786955603012410260017344805998076702828160316695004588429433
M = Matrix(ZZ, len(PRIMES)+1, len(PRIMES)+2)
M[0,0], M[0,1] = c, 1
for i in range(len(PRIMES)):
    M[i+1,0] = round(2^256*sqrt(PRIMES[i]))
    M[i+1,i+2] = 1
Mred = M.LLL()
flag = ''
for c in Mred[0][2:]:
    flag += chr(-c)
print(flag)
