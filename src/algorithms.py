import numpy as np

class Algorithms(object):

    def __init__(self, N, p,q, D, deltaT, deltaX):
        
        self.N= N
        self.p= p
        self.q= q
        self.D= D
        self.deltaT= deltaT
        self.deltaX= deltaX

    def updateA(self):

        up= np.roll(self.oldA, -1, axis=0)
        down= np.roll(self.oldA, +1, axis=0)
        right= np.roll(self.oldA, +1, axis=1)
        left= np.roll(self.oldA, -1, axis=1)
        
        self.A= self.oldA + (self.D*self.deltaT/self.deltaX**2)*(up+down+left+right-4*self.oldA) +\
                        self.q*self.oldA*(1-self.oldA-self.oldB-self.oldC) - self.p*self.oldA*self.oldC

    def updateB(self):

        up= np.roll(self.oldB, -1, axis=0)
        down= np.roll(self.oldB, +1, axis=0)
        right= np.roll(self.oldB, +1, axis=1)
        left= np.roll(self.oldB, -1, axis=1)
        self.B= self.oldB + (self.D*self.deltaT/self.deltaX**2)*(up+down+left+right-4*self.oldB) +\
                        self.q*self.oldB*(1-self.oldA-self.oldB-self.oldC) - self.p*self.oldA*self.oldB  


    def updateC(self):

        up= np.roll(self.oldC, -1, axis=0)
        down= np.roll(self.oldC, +1, axis=0)
        right= np.roll(self.oldC, +1, axis=1)
        left= np.roll(self.oldC, -1, axis=1)
        self.C= self.oldC + (self.D*self.deltaT/self.deltaX**2)*(up+down+left+right-4*self.oldC) +\
                        self.q*self.oldC*(1-self.oldA-self.oldB-self.oldC) - self.p*self.oldC*self.oldB  
   
    def updateConcentrations(self):

        self.updateA()
        self.updateB()
        self.updateC()

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

        self.oldA= A
        self.oldB= B
        self.oldC= C
        self.updateConcentrations()
        self.findMaximumConcentration()
        self.generateTypeField()

        return self.A, self.B, self.C, self.typeField
        

   