import numpy as np

class Observables(object):

    def findSpeciesFraction(self, typeField):
        
        fracA= np.count_nonzero(typeField==1)/typeField.size
        fracB= np.count_nonzero(typeField==2)/typeField.size
        fracC= np.count_nonzero(typeField==3)/typeField.size

        return fracA, fracB, fracC
    
    def findAbsorbtionTime(self, time):
        
        timeArr= np.array(time)
        meanTime= np.mean(timeArr)
        errMeanTime= np.std(timeArr)/np.sqrt(timeArr.size)

        return meanTime, errMeanTime