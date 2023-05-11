import numpy as np
from animate import Animate
from algorithms import Algorithms
import time

class Simulation(object):

    def __init__(self, N, p,q, D, deltaT, deltaX):
        
        self.N= N
        self.updateFrequency= 10    # in sweeps
        self.animation= Animate()
        self.algorithms= Algorithms(N, p, q, D, deltaT, deltaX)

    def generateInitArrays(self):

        self.A= np.random.uniform(low= 0, high= 1/3, size=(self.N, self.N))
        self.B= np.random.uniform(low= 0, high= 1/3, size=(self.N, self.N))
        self.C= np.random.uniform(low= 0, high= 1/3, size=(self.N, self.N))
        print(self.B)

    def runSimulation(self):

        self.generateInitArrays()
        self.epoch= 0
        self.sweeps= 0
        
        while True:
            self.A, self.B, self.C, self.typeField= self.algorithms.updateStep(self.A, self.B, self.C)
            self.epoch+=1
            if self.epoch % (self.N**2) == 0:
                self.sweeps+=1
                # print(self.sweeps)
                self.animation.drawImage(self.typeField)


if __name__ == '__main__':
    simulation= Simulation(50, 0.5, 1,1,0.1,1)
    simulation.runSimulation()




