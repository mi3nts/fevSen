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

print("Loading Overlay Parametors")

# Loading Parametors
stereoParams  = pickle.load(open("stereoParams_Feb_25_2020.p", "rb"))
thermalParams = pickle.load(open("thermalParams_Feb_12_2020.p", "rb"))
overlayParams = pickle.load(open("overlayParams_Feb_20_2020.p", "rb"))

cutOffs       = overlayParams['cutOffs ']
homographyAll = overlayParams['homographyAll']

print("Loading Disparity Model")

a = 30590
b = -0.9453

windowSize = 15                    # wsize default 3; 5; 7 for SGBM reduced size image; 15 for SGBM full size image (1300px and above); 5 Works nicely
maxDisparity = 64
leftMatcher = cv2.StereoSGBM_create(
    minDisparity=0,
    numDisparities=maxDisparity,             # max_disp has to be dividable by 16 f. E. HH 192, 256
    blockSize=5,
    P1=8 * 3 * windowSize ** 2,    # wsize default 3; 5; 7 for SGBM reduced size image; 15 for SGBM full size image (1300px and above); 5 Works nicely
    P2=32 * 3 * windowSize ** 2,
    disp12MaxDiff=1,
    uniquenessRatio=15,
    speckleWindowSize=0,
    speckleRange=2,
    preFilterCap=63,
    mode=cv2.STEREO_SGBM_MODE_SGBM_3WAY
)

print("Loading Directory")

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
ax4 = plt.subplot(2,2,4)

initial = True
noneCompare = None 
plt.ion()
# plt.show()


def ktoc(val):
  return (val - 27315) / 100.0

print("Overlay Function")

def overlayReturn(leftImage,rightImage,thermal):
  t1= datetime.datetime.now()
  thermalData   = cv2.resize(thermal[:,:], (640, 480))
  thermalKelvin = thermalData
  thermalCelcius = ktoc(thermalData)

  frameLeftRect    = cv2.remap(leftImage ,stereoParams['mapXLeft'],\
                                                         stereoParams['mapYLeft'],\
                                                                    cv2.INTER_CUBIC)
  frameRightRect   = cv2.remap(rightImage,stereoParams['mapXRight'],\
                                                                stereoParams['mapYRight'],
                                                                    cv2.INTER_CUBIC)

  frameCelciusRect = cv2.undistort(\
                                    thermalCelcius,\
                                    thermalParams['mtxThermal'],\
                                    thermalParams['distThermal']
                                    , None,\
                                    thermalParams['newcameramtx']\
                                    )
             
  disparityPre     = leftMatcher.compute(frameLeftRect,frameRightRect)
  distanceImage    = 30590*(disparityPre**-0.9453)
  
  maskCelcliusAll       = []
  celciusImageAll       = []
  maskedCelciusImageAll = []
  finalCelciusImage     = np.zeros((480, 640))

  rows,cols,ch = frameLeftRect.shape

  for indexIn in range(len(homographyAll)):
    maskCelclius          = (cutOffs[indexIn]<=distanceImage)&\
                                                (distanceImage<cutOffs[indexIn+1])
    # maskCelcliusAll.append(maskCelclius)
    celciusImage          = cv2.warpPerspective(frameCelciusRect,\
                                                             homographyAll[indexIn],\
                                                             (cols,rows))
    # celciusImageAll.append(celciusImage)
    maskedCelciusImage    = np.multiply(maskCelclius,celciusImage)
    # maskedCelciusImageAll.append(maskedCelciusImage)
    finalCelciusImage = finalCelciusImage + maskedCelciusImage

  distanceImageF = cv2.remap(distanceImage ,stereoParams['mapXLeftReverse'],\
                                                    stereoParams['mapYLeftReverse'],\
                                                            cv2.INTER_CUBIC)
  finalCelciusImageF = cv2.remap(finalCelciusImage ,stereoParams['mapXLeftReverse'],\
                                                stereoParams['mapYLeftReverse'],\
                                                        cv2.INTER_CUBIC)
  print(datetime.datetime.now()-t1)
  return distanceImageF, finalCelciusImageF;

print("Reading for a live implimentation")












# print("Showing all file frames with lag")

# for indexIn in range(len(leftImagesAll)-2):
      
#     left    = leftImagesAll[indexIn+2]
#     right   = rightImagesAll[indexIn+2]
#     thermal = thermalImagesAll[indexIn]
#     distanceF, celciusF = overlayReturn(left,right,thermal)
#     print(indexIn)
#     # if ((left.size>1) and(right.size>1)) and (thermal.size>1):
#     #     if(initial):
#     #       distanceF, celciusF = overlayReturn(left,right,thermal)
#     #       im1 = ax1.imshow(left)
#     #       im2 = ax2.imshow(right)
#     #       im3 = ax3.imshow(distanceF)
#     #       im4 = ax4.imshow(celciusF)
#     #       initial = False
#     #     else:
#     #       distanceF, celciusF = overlayReturn(left,right,thermal)
#     #       im1 = ax1.imshow(left)
#     #       im2 = ax2.imshow(right)
#     #       im3 = ax3.imshow(distanceF)
#     #       im4 = ax4.imshow(celciusF)
#     #       plt.pause(.01)

# plt.ioff()
# plt.show()



