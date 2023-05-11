import numpy as np

class Simulation(object):

    def __init__(self, N, p,q, D, deltaT, deltaX):
        
        self.N= N
        self.p= p
        self.q= q
        self.D= D
        self.deltaT= deltaT
        self.deltaX= deltaX

    def generateInitArray(self):

        self.array= np.random.uniform(low= 0, hifh= 1/3, size=(self.N, self.N))