import numpy as np
from animate import Animate

class Simulation(object):

    def __init__(self, N, p,q, D, deltaT, deltaX):
        
        self.N= N
        self.p= p
        self.q= q
        self.D= D
        self.deltaT= deltaT
        self.deltaX= deltaX

    def generateInitArrays(self):

        self.A= np.random.uniform(low= 0, high= 1/3, size=(self.N, self.N))
        self.B= np.random.uniform(low= 0, high= 1/3, size=(self.N, self.N))
        self.C= np.random.uniform(low= 0, high= 1/3, size=(self.N, self.N))

    def runSimulation(self):

        self.generateInitArrays()
