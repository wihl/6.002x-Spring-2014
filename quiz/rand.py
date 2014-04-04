import random as random
randomList1 = []
randomList2 = []
for i in range(1000):
    randomList1.append(int(random.random() * 2))

for i in range(1000):
    randomList2.append(random.choice((0,1)))

dist = [0,0]
for i in randomList1:
    dist[i] += 1

print dist

dist = [0,0]
for i in randomList2:
    dist[i] += 1

print dist
