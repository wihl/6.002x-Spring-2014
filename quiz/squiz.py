import random
import pylab

def sampleQuizzes():
    numTrials = 10000
    numInRange = 0
    for trial in range(numTrials):
        midterm1 = random.randrange(50,81,1)
        midterm2 = random.randrange(60,91,1)
        final    = random.randrange(55,96,1)

        grade = 0.25 * float(midterm1) + 0.25 * float(midterm2) + 0.50 * float(final)
        if grade >= 70 and grade <= 75:
            numInRange += 1

    return numInRange / float(numTrials)


def generateScores(numTrials):
    scores = []
    for trial in range(numTrials):
        midterm1 = random.randrange(50,81,1)
        midterm2 = random.randrange(60,91,1)
        final    = random.randrange(55,96,1)

        grade = 0.25 * float(midterm1) + 0.25 * float(midterm2) + 0.50 * float(final)
        scores.append(grade)

    return scores

def plotQuizzes():
    scores = generateScores(10000)
    pylab.hist(scores,bins=7)
    pylab.title("Distribution of Scores")
    pylab.xlabel("Final Score")
    pylab.ylabel("Number of Trials")
    pylab.show()
    



#for i in range(10):
#    print "trial ",i, sampleQuizzes()

plotQuizzes()

        

