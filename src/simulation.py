import numpy as np
from animate import Animate
from algorithms import Algorithms
from observables import Observables
from scipy.optimize import curve_fit

def func(x, a,b,c):
    return a*np.sin(b*x) +c

class Simulation(object):

    def __init__(self, N, p,q, D, deltaT, deltaX, nStepLimit):
        
        self.N= N
        self.deltaT= deltaT
        self.nStepLimit= nStepLimit
        self.updateFrequency= 10    # in sweeps
        self.algorithms= Algorithms(N, p, q, D, deltaT, deltaX)
        self.observables= Observables()

    def generateInitArrays(self):

        self.A= np.random.default_rng().random(size=(self.N, self.N)) /3
        self.B= np.random.default_rng().random(size=(self.N, self.N)) /3
        self.C= np.random.default_rng().random(size=(self.N, self.N)) /3

    def findSpeciesFraction(self):

        self.fracA, self.fracB, self.fracC= self.observables.findSpeciesFraction(self.tau)
    
    def recordSpeciesFraction(self):

        self.timeArray.append(self.epoch)
        self.AFracArray.append(self.fracA)
        self.BFracArray.append(self.fracB)
        self.CFracArray.append(self.fracC)

    def recordAbsorbtionTime(self):

        self.absorbtionTime.append(self.epoch*self.deltaT)

    def isAbsorbingState(self):
        return np.all(self.tau==1) or np.all(self.tau==1) or np.all(self.tau==1)
    
    def recordOccilationVals(self):

        self.elementArray1.append(self.A[self.element1Index])
        self.elementArray2.append(self.A[self.element2Index])
        self.timeArray.append(self.epoch*self.deltaT)

    def runSimulationVisualisation(self):

        self.generateInitArrays()
        self.animation= Animate(self.A, self.B, self.C)
        self.epoch= 0

        while True:
            self.A, self.B, self.C, self.tau= self.algorithms.updateStep(self.A, self.B, self.C)
            self.epoch+=1
            if self.epoch % 10 == 0:
                print(self.epoch)
                self.animation.drawImage(self.tau)

    def runSimulationFractions(self):

        self.generateInitArrays()
        self.epoch= 0
        self.timeArray=[]
        self.AFracArray=[]
        self.BFracArray=[]
        self.CFracArray=[]
        self.absorbingState= False

        while not self.absorbingState:
            self.A, self.B, self.C, self.tau= self.algorithms.updateStep(self.A, self.B, self.C)
            self.epoch+=1
            if self.epoch % (10) == 0:
                print(self.epoch)
                self.findSpeciesFraction()
                self.recordSpeciesFraction()
                self.absorbingState= self.isAbsorbingState()

        np.savetxt('../Data/fraction_data.txt', np.array([self.timeArray, self.AFracArray, self.BFracArray, self.CFracArray]).T)

    def runSimulationAbsorbsion(self):
        self.epoch= 0
        self.absorbingState= False
        self.absorbtionTime=[]

        while len(self.absorbtionTime) < 10:
            self.generateInitArrays()
            self.absorbingState= False
            print(f'{len(self.absorbtionTime)}/10 dp collected')

            while not self.absorbingState:    
                self.A, self.B, self.C, self.tau= self.algorithms.updateStep(self.A, self.B, self.C)
                self.epoch+=1
  
                if self.epoch % 10 == 0:
                    self.absorbingState= self.isAbsorbingState()

                if self.absorbingState == True:
                    self.recordAbsorbtionTime()
                elif self.epoch % self.nStepLimit==0:
                    self.generateInitArrays()
                    self.epoch=0

        
        mean, err= self.observables.findAbsorbtionTime(self.absorbtionTime)
        print(f'Mean absorbtion time is {mean:.3} +/- {err:.5} seconds')
    
    def runSimulationOccilation(self):

        self.element1Index= (25, 7)
        self.element2Index= (5, 17)
        self.generateInitArrays()
        self.epoch= 0
        self.elementArray1=[]
        self.elementArray2=[]
        self.timeArray=[]

        while True:
            self.A, self.B, self.C, self.tau= self.algorithms.updateStep(self.A, self.B, self.C)
            self.epoch+=1
            print(self.epoch)
            if self.epoch%10 == 0:
                self.recordOccilationVals()

            if self.epoch % self.nStepLimit == 0:
                break
        
        np.savetxt('../Data/occilation_data.txt', np.array([self.timeArray, self.elementArray1, self.elementArray2]).T)
        popt1, _= curve_fit(func, self.timeArray, self.elementArray1, p0=[1, 20, 0.1])
        popt2, _= curve_fit(func, self.timeArray, self.elementArray2, p0=[1, 20, 0.1])
        print(f'The period of occilation on element 1 is {popt1[1]} s')
        print(f'The period of occilation on element 2 is {popt2[1]} s')

if __name__ == '__main__':
    
    # # Part a
    # simulation= Simulation(50, 0.5, 1, 1, 0.1, 1, 10000)
    # simulation.runSimulationVisualisation()

    # # Part b
    # simulation= Simulation(50, 0.5, 1, 1, 0.1, 1, 10000)
    # simulation.runSimulationFractions()

    # # Part c 
    # simulation= Simulation(50, 0.5, 1, 1, 0.1, 1, 10000)
    # simulation.runSimulationAbsorbsion()

    # Part d
    # simulation= Simulation(50, 2.5, 1, 0.5, 0.1, 1, 10000)
    # simulation.runSimulationVisualisation()

    # Part e
    simulation= Simulation(50, 2.5, 1, 0.5, 0.1, 1, 4000)
    simulation.runSimulationOccilation()


