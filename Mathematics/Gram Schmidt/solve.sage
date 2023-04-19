v = [vector([4,1,3,-1]), vector([2,1,-3,4]), vector([1,0,-2,7]), vector([6, 2, 9, -5])]
u = []


for x in v:
    for e in u:
        x -= (x.dot_product(e) / e.dot_product(e))*e
    u.append(x)


print(round(u[3][1], 5))
