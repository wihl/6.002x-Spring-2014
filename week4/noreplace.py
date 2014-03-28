import random

def noReplacementSimulation(numTrials):
    '''
    Runs numTrials trials of a Monte Carlo simulation
    of drawing 3 balls out of a bucket containing
    3 red and 3 green balls. Balls are not replaced once
    drawn. Returns the a decimal - the fraction of times 3 
    balls of the same color were drawn.
    '''
    # Your code here
    allMatch = 0
    for trial in xrange(numTrials):
        bucket = ['r','r','r','g','g','g']
        # pick the first ball
        ball1 = random.choice(bucket)
        bucket.remove(ball1)
        ball2 = random.choice(bucket)
        bucket.remove(ball2)
        ball3 = random.choice(bucket)
        bucket.remove(ball3)
        if ball1 == ball2 and ball1 == ball3:
            allMatch += 1

    return allMatch / float(numTrials)



print noReplacementSimulation(100000)
