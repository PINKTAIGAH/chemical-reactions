import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

class Animate(object):
#===========================================================
# Animate a simulation that returns an image without tying matplotlib to 
# simulation steps.

    def __init__(self, a, b, c):
    #=======================================================
    # Initialise figure and inital frame of animation

        self.findInitialFrame(a, b, c)
        self.fig= plt.figure()
        self.im= plt.imshow(self.initialFrame, animated=True, cmap= 'gnuplot', vmin=0, vmax= 3)
    
    def drawImage(self, lattice_array):
    #=======================================================
    # Draw frame of the animation

        plt.cla()
        self.im= plt.imshow(lattice_array, animated= True, cmap= 'gnuplot', vmin=0, vmax= 3)
        plt.draw()
        plt.pause(0.0001)

    def findInitialFrame(self, a, b, c):
        
        totalConcenteration= np.dstack((a, b, c, 1-a-b-c))
        maximumConcentration= np.amax(totalConcenteration, axis=2)
        aMask= maximumConcentration==a
        bMask= maximumConcentration==b
        cMask= maximumConcentration==c
        
        self.initialFrame= np.zeros(a.shape)
        self.initialFrame[aMask]= 1
        self.initialFrame[bMask]= 2
        self.initialFrame[cMask]= 3
