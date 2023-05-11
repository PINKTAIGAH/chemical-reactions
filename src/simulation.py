import numpy as np
from animate import Animate
from algorithms import Algorithms
from observables import Observables


class Simulation(object):

    def __init__(self, N, p,q, D, deltaT, deltaX):
        
        self.N= N
        self.updateFrequency= 10    # in sweeps
        self.algorithms= Algorithms(N, p, q, D, deltaT, deltaX)
        self.observables= Observables()
    
    def generateInitArrays(self):

        self.A= np.random.uniform(low= 0, high= 1/3, size=(self.N, self.N))
        self.B= np.random.uniform(low= 0, high= 1/3, size=(self.N, self.N))
        self.C= np.random.uniform(low= 0, high= 1/3, size=(self.N, self.N))

    def runSimulation(self):

        self.generateInitArrays()
        self.animation= Animate(self.A, self.B, self.C)
        self.epoch= 0
        self.sweeps= 0

        self.timeArray=[]
        self.AFracArray=[]
        self.BFracArray=[]
        self.CFracArray=[]

        while True:
            self.A, self.B, self.C, self.typeField= self.algorithms.updateStep(self.A, self.B, self.C)
            self.epoch+=1
            if self.epoch % (self.N**2) == 0:
                self.sweeps+=1
                print(self.sweeps)
                self.animation.drawImage(self.typeField)
                self.recordSpeciesFraction()

            if self.sweeps== 200:
                np.savetxt('../Data/fraction_data.txt', np.array([self.timeArray, self.AFracArray, self.BFracArray, self.CFracArray]).T)
                break

    def recordSpeciesFraction(self):

        fracA, fracB, fracC= self.observables.findSpeciesFraction(self.typeField)
        self.timeArray.append(self.sweeps)
        self.AFracArray.append(fracA)
        self.BFracArray.append(fracB)
        self.CFracArray.append(fracC)

if __name__ == '__main__':
    simulation= Simulation(50, 0.5, 1, 1, 0.5, 3)
    simulation.runSimulation()




