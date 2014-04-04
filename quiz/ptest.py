def probTest(limit):
    for n in range(1, 200):
        prob = 1./ 6. * (5./6.) ** (n-1)
        if prob < limit:
            return n
    return float('NaN')


print probTest (1e-10)
