# Problem Set 3: Simulating the Spread of Disease and Virus Population Dynamics 

import numpy
import random
import pylab

''' 
Begin helper code
'''

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """

'''
End helper code
'''

#
# PROBLEM 2
#
class SimpleVirus(object):

    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):
        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).
        """
        self.maxBirthProb = maxBirthProb
        self.clearProb    = clearProb

    def getMaxBirthProb(self):
        """
        Returns the max birth probability.
        """
        return self.maxBirthProb

    def getClearProb(self):
        """
        Returns the clear probability.
        """
        return self.clearProb

    def doesClear(self):
        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step. 
        returns: True with probability self.getClearProb and otherwise returns
        False.
        """
        return random.random() < self.clearProb

    
    def reproduce(self, popDensity):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient and
        TreatedPatient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).         

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.         
        
        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
        """
        if random.random() < self.maxBirthProb * (1 - popDensity):
            return SimpleVirus(self.maxBirthProb, self.clearProb)
        else:
            raise NoChildException



class Patient(object):
    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """    

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the maximum virus population for this patient (an integer)
        """
        self.viruses = viruses
        self.maxPop  = maxPop
        self.totalPop = len(viruses)
        self.populationDensity = 0.0

    def getViruses(self):
        """
        Returns the viruses in this Patient.
        """
        return self.viruses


    def getMaxPop(self):
        """
        Returns the max population.
        """
        return self.maxPop


    def getTotalPop(self):
        """
        Gets the size of the current total virus population. 
        returns: The total virus population (an integer)
        """
        return self.totalPop



    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:
        
        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.   
        
        - The current population density is calculated. This population density
          value is used until the next call to update() 
        
        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.                    

        returns: The total virus population at the end of the update (an
        integer)
        """
        virus_copy = self.viruses[:]
        virusThatDied = []
        newVirus      = []
        for virus in virus_copy:
            if virus.doesClear():
                self.viruses.remove(virus)
            else:
                try:
                    newVirus.append(virus.reproduce(self.populationDensity))
                    #print "a new virus is born"
                except NoChildException:
                    pass

        self.viruses.extend(newVirus)
        self.totalPop = len(self.viruses)
        self.populationDensity = self.totalPop / float(self.maxPop)
        return self.totalPop



#
# PROBLEM 3
#
def simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb,
                          numTrials):
    """
    Run the simulation and plot the graph for problem 3 (no drugs are used,
    viruses do not have any drug resistance).    
    For each of numTrials trial, instantiates a patient, runs a simulation
    for 300 timesteps, and plots the average virus population size as a
    function of time.

    numViruses: number of SimpleVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: Maximum clearance probability (a float between 0-1)
    numTrials: number of simulation runs to execute (an integer)
    """
    numSteps = 300
    virusPop = [0] * numSteps

    for trial in xrange(numTrials):
        viruses = []
        for i in xrange(numViruses):
            viruses.append(SimpleVirus(maxBirthProb, clearProb))
            patient = Patient(viruses, maxPop)
        for i in xrange(numSteps):
            virusPop[i] += patient.update()

    for i in xrange(numSteps):
        virusPop[i] = virusPop[i] / float(numTrials)

    pylab.plot(virusPop, label="population")
    pylab.title("Simulation without drugs")
    pylab.xlabel("time")
    pylab.ylabel("population")
    pylab.legend(loc = 1)
    pylab.show()

#
# PROBLEM 4
#
class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """   

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        """
        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)       

        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'srinol':False}, means that this virus
        particle is resistant to neither guttagonol nor srinol.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.
        """
        SimpleVirus.__init__(self, maxBirthProb,clearProb)
        self.resistances = resistances
        self.mutProb = mutProb


    def getResistances(self):
        """
        Returns the resistances for this virus.
        """
        return self.resistances

    def getMutProb(self):
        """
        Returns the mutation probability for this virus.
        """
        return self.getMutProb

    def isResistantTo(self, drug):
        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in TreatedPatient to determine how many virus
        particles have resistance to a drug.       

        drug: The drug (a string)

        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        if drug in self.resistances:
            return self.resistances[drug]
        else:
            return False


    def reproduce(self, popDensity, activeDrugs):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the TreatedPatient class.

        A virus particle will only reproduce if it is resistant to ALL the drugs
        in the activeDrugs list. For example, if there are 2 drugs in the
        activeDrugs list, and the virus particle is resistant to 1 or no drugs,
        then it will NOT reproduce.

        Hence, if the virus is resistant to all drugs
        in activeDrugs, then the virus reproduces with probability:      

        self.maxBirthProb * (1 - popDensity).                       

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). The offspring virus
        will have the same maxBirthProb, clearProb, and mutProb as the parent.

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.       

        For example, if a virus particle is resistant to guttagonol but not
        srinol, and self.mutProb is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90%
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        srinol and a 90% chance that the offspring will not be resistant to
        srinol.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population       

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings).

        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """
        # step 1 check resistances
        for r in activeDrugs:
            if not self.resistances[r]:
                raise NoChildException
                return None #defensive

        # step 2 decide to reproduce
        if random.random() < self.maxBirthProb * (1 - popDensity):
            # step 3 apply mutations
            childResistances = {}
            for r in self.resistances:
                pb = random.random()
                if self.resistances[r]:
                    if pb < (1 - self.mutProb):
                        childResistances[r] = self.resistances[r]
                    else:
                        childResistances[r] = not self.resistances[r]
                else:
                    if pb < (1 - self.mutProb):
                        childResistances[r] = self.resistances[r]
                    else:
                        childResistances[r] = not self.resistances[r]

            child =  ResistantVirus(self.maxBirthProb, self.clearProb,
                                  childResistances, self.mutProb)
        else:
            raise NoChildException


        return child

            

class TreatedPatient(Patient):
    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).              

        viruses: The list representing the virus population (a list of
        virus instances)

        maxPop: The  maximum virus population for this patient (an integer)
        """
        Patient.__init__(self, viruses, maxPop)
        self.prescriptions = []
        self.populationDensity = 0.0

    def addPrescription(self, newDrug):
        """
        Administer a drug to this patient. After a prescription is added, the
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: The list of drugs being administered to a patient is updated
        """
        if newDrug not in self.prescriptions:
            self.prescriptions.append(newDrug)


    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.

        returns: The list of drug names (strings) being administered to this
        patient.
        """
        return self.prescriptions


    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in
        drugResist.       

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'srinol'])

        returns: The population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        popCount = 0
        lenDrugResist = len(drugResist)
        for virus in self.viruses:
            resistCount = 0
            for drug in drugResist:
                if virus.isResistantTo(drug):
                    resistCount += 1
            if resistCount == lenDrugResist:
                popCount += 1

        return popCount


    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:

        - Determine whether each virus particle survives and update the list of
          virus particles accordingly

        - The current population density is calculated. This population density
          value is used until the next call to update().

        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.
          The list of drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces.

        returns: The total virus population at the end of the update (an
        integer)
        """
        virus_copy = self.viruses[:]
        virusThatDied = []
        newVirus      = []
        for virus in virus_copy:
            if virus.doesClear():
                self.viruses.remove(virus)
            else:
                # if the virus has resistance to all prescriptions, it is allowed to reproduce
                resistSet = set(virus.getResistances())
                if resistSet.issubset(set(self.prescriptions)):
                    try:
                        newVirus.append(virus.reproduce(self.populationDensity,self.prescriptions))
                        #print "a new virus is born"
                    except NoChildException:
                        pass

        self.viruses.extend(newVirus)
        self.totalPop = len(self.viruses)
        self.populationDensity = self.totalPop / float(self.maxPop)
        return self.totalPop




#
# PROBLEM 5
#
def simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances,
                       mutProb, numTrials, delayTime=150, showPlot = True):
    """
    Runs simulations and plots graphs for problem 5.

    For each of numTrials trials, instantiates a patient, runs a simulation for
    150 timesteps, adds guttagonol, and runs the simulation for an additional
    150 timesteps.  At the end plots the average virus population size
    (for both the total virus population and the guttagonol-resistant virus
    population) as a function of time.

    numViruses: number of ResistantVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: maximum clearance probability (a float between 0-1)
    resistances: a dictionary of drugs that each ResistantVirus is resistant to
                 (e.g., {'guttagonol': False})
    mutProb: mutation probability for each ResistantVirus particle
             (a float between 0-1). 
    numTrials: number of simulation runs to execute (an integer)
    
    """
    numSteps = delayTime + 150
    virusPopNoDrug   = [0] * numSteps
    virusPopWithDrug = [0] * numSteps

    for trial in xrange(numTrials):
        viruses = []
        for i in xrange(numViruses):
            viruses.append(ResistantVirus(maxBirthProb, clearProb, resistances, mutProb))

        patient = TreatedPatient(viruses, maxPop)
        for i in xrange(numSteps):
            if i == delayTime:
                patient.addPrescription('guttagonol')
            totalPop = patient.update()
            virusPopNoDrug[i] += totalPop
            virusPopWithDrug[i] += patient.getResistPop(['guttagonol'])


    for i in xrange(numSteps):
        virusPopNoDrug[i] = virusPopNoDrug[i] / float(numTrials)
        virusPopWithDrug[i] = virusPopWithDrug[i] / float(numTrials)

    if showPlot == True:
        #pylab.plot(virusPopNoDrug, label="no drug")
        pylab.plot(virusPopWithDrug, label="with drug")
        #print virusPopNoDrug
        pylab.title("Simulation with drugs")
        pylab.xlabel("time")
        pylab.ylabel("population")
        pylab.legend(loc = 1)
        pylab.show()
    return virusPopWithDrug


#random.seed(0)
'''

print "Virus testing"
v1 = SimpleVirus(1.0, 0.0) #never cleared and always reproduces
print v1.doesClear(), " should be False" 
print type(v1.reproduce(0)), "should be virus type"

v1 = SimpleVirus(0.0, 0.0) #never cleared, never produces
print v1.doesClear(), " should be true"
try:
    print type(v1.reproduce(0)), "exception should be thrown"
except NoChildException as e:
    print "correctly raised exception"
v1 = SimpleVirus(1.0, 1.0) #always clears, always reproduces
print v1.doesClear(), " should be false"
print type(v1.reproduce(0)), "should be virus type"

print "\n\nPatient Testing"

virus = SimpleVirus(1.0, 0.0)
patient = Patient([virus], 100)
print "Updating the patient for 100 trials..."
#patient.update implemented incorrectly
print patient.getTotalPop(), "should be 100"

simulationWithoutDrug(100, 1000, 0.1, 0.05, 1)

# Part 4

rv= ResistantVirus(1.0, 0.0, {"drug2": True}, 1.0)

try:
    child = rv.reproduce(0,[])
    print rv.getResistances()
    print child.getResistances()
except NoChildException as e:
    print "no child virus"

virus = ResistantVirus(1.0, 1.0, {}, 0.0)
patient = TreatedPatient([virus], 100)
virus1 = ResistantVirus(1.0, 0.0, {"drug1": True}, 0.0)
patient = TreatedPatient([virus1], 100)
for i in xrange(100):
    r  = patient.update()

'''

# Problem 5
#simulationWithDrug(100, 1000, 0.1, 0.05, {'guttagonol': False}, 0.005, 100)

