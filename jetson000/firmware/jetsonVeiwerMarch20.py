#!/usr/bin/env python
# -*- coding: utf-8 -*-
import h5py
import pickle
import datetime
from uvctypes import *
import time
import cv2
import numpy as np
try:
  from queue import Queue
except ImportError:
  from Queue import Queue
import platform
import os
import threading
import time
import numpy, scipy.io
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from PIL import Image



directory = "/home/teamlary/mintsData/val/"
# directory = "/home/teamlary/mintsData/valMarch20/"

# Creating a subplot 
ax1 = plt.subplot(2,2,1)
plt.title("Original Image")

ax2 = plt.subplot(2,2,2)
plt.title("Depth Image")

ax3 = plt.subplot(2,2,3)
plt.title("Thermal Image")

ax4 = plt.subplot(2,2,4)
plt.title("Overlay Image")

initial = True
noneCompare = None 
plt.ion()

alpha = .7
beta = (1.0 - alpha)

print("Listing all files")
for filename in sorted(os.listdir(directory)):
    if filename.endswith(".h5"):
        full= directory+filename
        print(full)
        hf = h5py.File(full, 'r')
        left     = cv2.cvtColor(np.array(hf.get('left')), cv2.COLOR_BGR2RGB)
        celcius  = np.array(hf.get('celcius'))
        distance = np.array(hf.get('distance'))
        
   
        cmap = plt.cm.jet
        norm = plt.Normalize(vmin=celcius.min(), vmax=celcius.max())

        # map the normalized data to colors
        # image is now RGBA (512x512x4)
        thermal = cmap(norm(celcius))
        plt.imsave('thermal.png',thermal)

       
        thermal = cv2.cvtColor(cv2.imread('thermal.png'), cv2.COLOR_BGR2RGB)


        overlay = cv2.addWeighted(left,alpha,thermal,beta,0)



        if ((left.size>1) and(distance.size>1)) and (celcius.size>1):
            if(initial):
                im1 = ax1.imshow(left)
                im2 = ax2.imshow(distance,cmap='rainbow')
                im3 = ax3.imshow(celcius,cmap='jet')
                im4 = ax4.imshow(overlay)
                plt.pause(2) 
                # initial = False
            else:
                im1.set_data(left)
                im2.set_data(distance)
                im3.set_data(celcius)
                im4.set_data(overlay)
            
                plt.pause(.01)    

plt.ioff()
plt.show()
plt.close()


