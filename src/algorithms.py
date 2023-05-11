import numpy as np

class Algorithms(object):

    def __init__(self, N, p, q, D, deltaT, deltaX):
        
        self.N= N
        self.p= p
        self.q= q
        self.D= D
        self.deltaT= deltaT
        self.deltaX= deltaX   
    
    def laplacian1D(self, arr: np.ndarray):
           
        return (np.roll(arr, 1, axis=0) + np.roll(arr, -1, axis=0) - 2*arr) / self.deltaX**2
    
    def laplacian2D(self, arr: np.ndarray):
           
        return (np.roll(arr, 1, axis=0) + np.roll(arr, 1, axis=1) + \
        np.roll(arr, -1, axis=0) + np.roll(arr, -1, axis=1) - 4 * arr) / self.deltaX**2
    
    def laplacian3D(self, arr: np.ndarray):
           
        return (np.roll(arr, 1, axis=0) + np.roll(arr, 1, axis=1) +  np.roll(arr, 1, axis=2) +\
        np.roll(arr, -1, axis=0) + np.roll(arr, -1, axis=1) + np.roll(arr, -1, axis=2) - 6 * arr) / self.deltaX**2
    
    def partialX(self, arr: np.ndarray):

        return (np.roll(arr, -1, axis=0) - np.roll(arr, +1, axis=0))/(2*self.deltaX)
   
    def updateA(self, a, b, c):
   
        self.a += self.deltaT * (self.D*self.laplacian2D(a) + self.q*a*(1-a-b-c) - self.p*a*c)
    
    def updateB(self, a, b, c):
   
        self.b +=self.deltaT * (self.D*self.laplacian2D(b) + self.q*b*(1-a-b-c) - self.p*a*b)
        
    def updateC(self, a, b, c):
   
        self.c += self.deltaT * (self.D*self.laplacian2D(c) + self.q*c*(1-a-b-c) - self.p*b*c)
    
    def updateConcentrations(self):

        self.aCurr, self.bCurr, self.cCurr= self.a.copy(), self.b.copy(), self.c.copy()
        self.updateA(self.aCurr, self.bCurr, self.cCurr)
        self.updateB(self.aCurr, self.bCurr, self.cCurr)
        self.updateC(self.aCurr, self.bCurr, self.cCurr)

    def findMaximumConcentration(self):

        self.d= 1- self.a - self.b - self.c
        totalConcenteration= np.dstack((self.a, self.b, self.c, self.d))
        maximumConcentration= np.amax(totalConcenteration, axis=2)
        self.AMask= maximumConcentration==self.a
        self.BMask= maximumConcentration==self.b
        self.CMask= maximumConcentration==self.c
        
    def generateTau(self):

        self.tau= np.zeros((self.N, self.N))
        self.tau[self.AMask]= 1
        self.tau[self.BMask]= 2
        self.tau[self.CMask]= 3
    
    def get_tau_value(self, a_ij, b_ij, c_ij):
        d_ij = 1 - a_ij - b_ij - c_ij
        values = [d_ij, a_ij, b_ij, c_ij]
        # print(values)
        # max_val = max(values)
        idx = values.index(max(values))
        # print(f'Max values is in elelmnet {idx}')
        # print(idx)
        return idx


    def get_field_tau(self):
        tau = np.zeros(shape=(self.N, self.N))
        for row in range(self.N):
            for col in range(self.N):
                tau[row, col] = self.get_tau_value(
                    self.a[row, col],
                    self.b[row, col],
                    self.c[row, col]
                    )
        return tau
    
    
    def updateStep(self, a, b, c):

        self.a= a
        self.b= b
        self.c= c
        self.updateConcentrations()
        # self.findMaximumConcentration()
        # self.generateTau()  
        self.tau= self.get_field_tau()

        return self.a, self.b, self.c, self.tau
        

   