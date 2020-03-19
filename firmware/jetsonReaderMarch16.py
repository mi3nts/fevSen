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

directory = 'threeWayImageDataSets/hdf5ThreeWayMar17/'

leftImagesAll    = []
rightImagesAll   = []
thermalImagesAll = []

print("Listing all files")
for filename in sorted(os.listdir(directory)):
    
    if filename.endswith(".h5"):
        full= directory+filename
        hf = h5py.File(full, 'r')
        leftImagesAll.append(np.array(hf.get('left')))
        rightImagesAll.append(np.array(hf.get('right')))
        thermalImagesAll.append(np.array(hf.get('thermal')))


print("Showing all file frames without lag")

# Creating a subplot 
ax1 = plt.subplot(2,2,1)
ax2 = plt.subplot(2,2,2)
ax3 = plt.subplot(2,2,3)

initial = True
noneCompare = None 
plt.ion()
# plt.show()



print("Showing all file frames with lag")

for indexIn in range(len(leftImagesAll)-2):
      
    left    = leftImagesAll[indexIn+2]
    right   = rightImagesAll[indexIn+2]
    thermal = thermalImagesAll[indexIn]
        
    if ((left.size>1) and(right.size>1)) and (thermal.size>1):
        if(initial):
            im1 = ax1.imshow(left)
            im2 = ax2.imshow(right)
            im3 = ax3.imshow(thermal)
            initial = False
        else:
            im1.set_data(left)
            im2.set_data(right)
            im3.set_data(thermal)
            plt.pause(1)

plt.ioff()
plt.show()


