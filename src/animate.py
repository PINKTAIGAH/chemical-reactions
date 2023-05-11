import matplotlib.pyplot as plt
import matplotlib
import numpy as np

class Animate(object):
#===========================================================
# Animate a simulation that returns an image without tying matplotlib to 
# simulation steps.

    def __init__(self, A, B, C):
    #=======================================================
    # Initialise figure and inital frame of animation
    
        self.findInitialFrame(A, B, C)
        self.fig= plt.figure()
        self.im= plt.imshow(self.initialFrame, animated=True, cmap= 'magma')
        plt.colorbar()
    
    def drawImage(self, lattice_array):
    #=======================================================
    # Draw frame of the animation

        plt.cla()
        self.im= plt.imshow(lattice_array, animated= True, cmap= 'magma')
        plt.draw()
        plt.pause(0.0001)

    def findInitialFrame(self, A, B, C):
        
        totalConcenteration= np.dstack((A, B, C, 1-A-B-C))
        maximumConcentration= np.amax(totalConcenteration, axis=2)
        AMask= maximumConcentration==A
        BMask= maximumConcentration==B
        CMask= maximumConcentration==C
        
        self.initialFrame= np.zeros(A.shape)
        self.initialFrame[AMask]= 1
        self.initialFrame[BMask]= 2
        self.initialFrame[CMask]= 3
