primes = []
for i in range(851, 999):
  if is_prime(i):
    primes.append(i)

x = var('x')
for p in primes:
  print(p, solve_mod([ 588*x == 665, 665*x == 216, 216*x == 113 ], p))
