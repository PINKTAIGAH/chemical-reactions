import numpy as np

class Algorithms(object):

    def __init__(self, N, p,q, D, deltaT, deltaX):
        
        self.N= N
        self.p= p
        self.q= q
        self.D= D
        self.deltaT= deltaT
        self.deltaX= deltaX
 
    def makeArrayCopy(self):
        self.oldA= np.copy(self.A)
        self.oldB= np.copy(self.B)
        self.oldC= np.copy(self.C)  

    def findNeighbiourElements(self, array):

        up= np.roll(array, -1, axis=0)
        down= np.roll(array, +1, axis=0)
        right= np.roll(array, +1, axis=1)
        left= np.roll(array, -1, axis=1)

        return up, down, left, right

    def updateA(self):

        self.AUp, self.ADown, self.ALeft, self.ARight= self.findNeighbiourElements(self.oldA)
        self.A= self.oldA + (self.D*self.deltaT/self.deltaX**2)*(self.AUp+self.ADown+self.ALeft+self.ARight-4*self.oldA) +\
                        self.q*self.oldA*(1-self.oldA-self.oldB-self.oldC) - self.p*self.oldA*self.oldC

    def updateB(self):

        self.BUp, self.BDown, self.BLeft, self.BRight= self.findNeighbiourElements(self.oldB)
        self.B= self.oldB + (self.D*self.deltaT/self.deltaX**2)*(self.BUp+self.BDown+self.BLeft+self.BRight-4*self.oldB) +\
                        self.q*self.oldB*(1-self.oldA-self.oldB-self.oldC) - self.p*self.oldA*self.oldB  

    def updateC(self):

        self.CUp, self.CDown, self.CLeft, self.CRight= self.findNeighbiourElements(self.oldC)
        self.C= self.oldC + (self.D*self.deltaT/self.deltaX**2)*(self.CUp+self.CDown+self.CLeft+self.CRight-4*self.oldC) +\
                        self.q*self.oldC*(1-self.oldA-self.oldB-self.oldC) - self.p*self.oldC*self.oldB  
 
    def findMaximumConcentration(self):

        totalConcenteration= np.dstack((self.A, self.B, self.C, 1-self.A-self.B-self.C))
        maximumConcentration= np.amax(totalConcenteration, axis=2)
        self.AMask= maximumConcentration==self.A
        self.BMask= maximumConcentration==self.B
        self.CMask= maximumConcentration==self.C
        
    def generateTypeField(self):

        self.typeField= np.zeros((self.N, self.N))
        self.typeField[self.AMask]= 1
        self.typeField[self.BMask]= 2
        self.typeField[self.CMask]= 3
    
    def updateStep(self, A, B, C):

        self.A= A
        self.B= B
        self.C= C
        self.makeArrayCopy()
        self.findMaximumConcentration()
        self.generateTypeField()

        return self.A, self.B, self.C, self.typeField
        

   