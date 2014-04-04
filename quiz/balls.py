import random
import pylab

balls = []
for i in range(1000):
    balls.append(random.choice((0,1)))

# 0 is white, 1 is black


def lv(balls):
    n = 1
    while (balls[random.randrange(0,len(balls))] == 1):
        n += 1
    return n


def mc(balls, k):
    n = 1
    pos = random.randrange(0,len(balls))
    while (balls[pos] == 1 and n <= (k+1)):
        print pos, balls[pos], n
        n += 1
        pos += 1
        if pos >= len(balls):
            pos = 0
    if n >= k:
        return 0
    return n



histogram = [ 0 for i in range(1,1000)]  # intialize the list to be all zeros

for i in range(1000):
    result = mc(balls,10)
    histogram[ result ] += 1

pylab.plot( histogram )
pylab.xlim([0,10])
pylab.show()
#print "lv:", lv(balls)
#print "mc:", mc(balls, 1)

