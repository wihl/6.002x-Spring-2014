import random
import pylab
import numpy as np

# Global Variables
MAXRABBITPOP = 1000
CURRENTRABBITPOP = 500
CURRENTFOXPOP = 30

def rabbitGrowth():
    """ 
    rabbitGrowth is called once at the beginning of each time step.

    It makes use of the global variables: CURRENTRABBITPOP and MAXRABBITPOP.

    The global variable CURRENTRABBITPOP is modified by this procedure.

    For each rabbit, based on the probabilities in the problem set write-up, 
      a new rabbit may be born.
    Nothing is returned.
    """
    # you need this line for modifying global variables
    global CURRENTRABBITPOP

    p = 1.0 - float((CURRENTRABBITPOP / float(MAXRABBITPOP)))
    if random.random() < p:
        CURRENTRABBITPOP += 1
        if CURRENTRABBITPOP > MAXRABBITPOP:
            CURRENTRABBITPOP = MAXRABBITPOP
            
def foxGrowth():
    """ 
    foxGrowth is called once at the end of each time step.

    It makes use of the global variables: CURRENTFOXPOP and CURRENTRABBITPOP,
        and both may be modified by this procedure.

    Each fox, based on the probabilities in the problem statement, may eat 
      one rabbit (but only if there are more than 10 rabbits).

    If it eats a rabbit, then with a 1/3 prob it gives birth to a new fox.

    If it does not eat a rabbit, then with a 1/10 prob it dies.

    Nothing is returned.
    """
    # you need these lines for modifying global variables
    global CURRENTRABBITPOP
    global CURRENTFOXPOP
    p = CURRENTRABBITPOP / float(MAXRABBITPOP)
    if random.random() < p :
        # eat the rabbit
        CURRENTRABBITPOP -= 1
        if random.random() > (2/3):
               CURRENTFOXPOP += 1
    else:
        if random.random() < 0.1:
               if CURRENTFOXPOP > 10:
                   CURRENTFOXPOP -= 1
    
            
def runSimulation(numSteps):
    """
    Runs the simulation for `numSteps` time steps.

    Returns a tuple of two lists: (rabbit_populations, fox_populations)
      where rabbit_populations is a record of the rabbit population at the 
      END of each time step, and fox_populations is a record of the fox population
      at the END of each time step.

    Both lists should be `numSteps` items long.
    """

    rabbit_populations = []
    fox_populations = []


    for i in xrange(numSteps):
        rabbitGrowth()
        foxGrowth()
        rabbit_populations.append(CURRENTRABBITPOP)
        fox_populations.append(CURRENTFOXPOP)

    return (rabbit_populations, fox_populations)


CURRENTRABBITPOP = 10
MAXRABBITPOP = 100
CURRENTFOXPOP = 20

rabbitGrowth()
print CURRENTRABBITPOP
rabbitGrowth()
print CURRENTRABBITPOP

(rabbits, foxes) =  runSimulation(200)

#rabbitPopulationOverTime = np.array(rabbits)

#coeff = np.polyfit(range(len(rabbitPopulationOverTime)), rabbitPopulationOverTime, 2)

#pylab.plot(np.polyval(coeff, range(len(rabbitPopulationOverTime))))
print len(rabbits), len(foxes)
pylab.plot(range(200), rabbits, range(200), foxes)
pylab.show()
