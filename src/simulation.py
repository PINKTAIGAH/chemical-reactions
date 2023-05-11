import numpy as np
from animate import Animate
from algorithms import Algorithms
from observables import Observables


class Simulation(object):

    def __init__(self, N, p,q, D, deltaT, deltaX, nStep):
        
        self.N= N
        self.updateFrequency= 10    # in sweeps
        self.algorithms= Algorithms(N, p, q, D, deltaT, deltaX)
        self.observables= Observables()
    
    def generateInitArrays(self):

        self.A= np.random.default_rng().random(size=(self.N, self.N)) /3
        self.B= np.random.default_rng().random(size=(self.N, self.N)) /3
        self.C= np.random.default_rng().random(size=(self.N, self.N)) /3

    def runSimulationVisualisation(self):

        self.generateInitArrays()
        self.animation= Animate(self.A, self.B, self.C)
        self.epoch= 0
        self.sweeps= 0

        while True:
            self.A, self.B, self.C, self.tau= self.algorithms.updateStep(self.A, self.B, self.C)
            self.epoch+=1
            if self.epoch % 10 == 0:
                self.sweeps+=1
                print(self.epoch)
                self.animation.drawImage(self.tau)

    def runSimulationFractions(self):

        self.generateInitArrays()
        self.epoch= 0
        self.sweeps= 0
        self.timeArray=[]
        self.AFracArray=[]
        self.BFracArray=[]
        self.CFracArray=[]
        self.absorbingState= False

        while not self.absorbingState:
            self.A, self.B, self.C, self.tau= self.algorithms.updateStep(self.A, self.B, self.C)
            self.epoch+=1
            if self.epoch % (10) == 0:
                self.sweeps+=1
                print(self.sweeps)
                self.recordSpeciesFraction()
                self.absorbingState= self.isAbsorbingState()

        np.savetxt('../Data/fraction_data.txt', np.array([self.timeArray, self.AFracArray, self.BFracArray, self.CFracArray]).T)

    def recordSpeciesFraction(self):

        fracA, fracB, fracC= self.observables.findSpeciesFraction(self.tau)
        self.timeArray.append(self.sweeps)
        self.AFracArray.append(fracA)
        self.BFracArray.append(fracB)
        self.CFracArray.append(fracC)

    def isAbsorbingState(self):
        return np.all(self.tau==1) or np.all(self.tau==1) or np.all(self.tau==1)

if __name__ == '__main__':
    simulation= Simulation(50, 0.5, 1, 1, 0.1, 1, 10000)
    simulation.runSimulationVisualisation()




