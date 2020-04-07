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
from os import path
from numba import jit

print("Defining Functions")

def hdf5Reader(fileName):
    if (path.exists(fileName)):
        # print("File: "+ fileName +" Exists")
        hf      = h5py.File(fileName, 'r')
        left    = np.array(hf.get('left'))
        right   = np.array(hf.get('right'))
        thermal = np.array(hf.get('thermal'))
        hf.close()
        return True,left,right,thermal;
    else:
        # print("Path:" + fileName +  " Doesnt Exist")
        return False,[],[],[];




def getImagePathTailHdf5Mod(dateTime,labelIn):
    mod = round(dateTime.microsecond/200000)
    pathTail = labelIn+"/"+\
    str(dateTime.year).zfill(4) + \
    "_" +str(dateTime.month).zfill(2) + \
    "_" +str(dateTime.day).zfill(2)+ \
    "_" +str(dateTime.hour).zfill(2) + \
    "_" +str(dateTime.minute).zfill(2)+ \
    "_" +str(dateTime.second).zfill(2)+ \
    "_" +str((mod-1)*20).zfill(2)+ \
    "_"+labelIn+".h5"
   
    return pathTail;


def ktoc(val):
  return (val - 27315) / 100.0



print("Overlay Function")

def overlayReturn(leftImage,rightImage,thermal):
  thermalData   = cv2.resize(thermal[:,:], (640, 480))
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
  

  finalCelciusImage     = np.zeros((480, 640))

  rows,cols,ch = frameLeftRect.shape



  for indexIn in range(len(homographyAll)):
    maskCelclius          = (cutOffs[indexIn]<=distanceImage)&\
                                                (distanceImage<cutOffs[indexIn+1])

    celciusImage          = cv2.warpPerspective(frameCelciusRect,\
                                                             homographyAll[indexIn],\
                                                             (cols,rows))
    maskedCelciusImage    = np.multiply(maskCelclius,celciusImage)
    finalCelciusImage = finalCelciusImage + maskedCelciusImage

  distanceImageF = cv2.remap(distanceImage ,stereoParams['mapXLeftReverse'],\
                                                    stereoParams['mapYLeftReverse'],\
                                                            cv2.INTER_CUBIC)
  finalCelciusImageF = cv2.remap(finalCelciusImage ,stereoParams['mapXLeftReverse'],\
                                                stereoParams['mapYLeftReverse'],\
                                                        cv2.INTER_CUBIC)
  return distanceImageF, finalCelciusImageF;



print("Gain Rectified Celcius Images")

def getCelciusImages(frameCelciusRect,cols,rows):
    celciusImagesAll = []
    for indexIn in range(len(homographyAll)):
        celciusImagesAll.append(cv2.warpPerspective(frameCelciusRect,\
                                                                homographyAll[indexIn],\
                                                                         (cols,rows)))
    return celciusImagesAll;


def overlayReturnMinimal(leftImage,rightImage,thermal):
  thermalData   = cv2.resize(thermal[:,:], (640, 480))
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
  
  rows,cols,ch = frameLeftRect.shape
  
  celciusImagesAll = getCelciusImages(frameCelciusRect,cols,rows)

  distanceImage, finalCelciusImage = overlayLoop(disparityPre, frameLeftRect, celciusImagesAll)

  distanceImageF = cv2.remap(distanceImage ,stereoParams['mapXLeftReverse'],\
                                                    stereoParams['mapYLeftReverse'],\
                                                            cv2.INTER_CUBIC)
  finalCelciusImageF = cv2.remap(finalCelciusImage ,stereoParams['mapXLeftReverse'],\
                                                stereoParams['mapYLeftReverse'],\
                                                        cv2.INTER_CUBIC)
  return distanceImageF, finalCelciusImageF;





@jit(nopython=True)
def overlayLoop(disparityPre, frameLeftRect, celciusImagesAll):

  distanceImage    = 30590*(disparityPre**-0.9453)
  

  finalCelciusImage     = np.zeros((480, 640))

  rows,cols,ch = frameLeftRect.shape

  for indexIn in range(len(homographyAll)):
    maskCelclius          = (cutOffs[indexIn]<=distanceImage)&\
                                                (distanceImage<cutOffs[indexIn+1])
                                                

    celciusImage          = celciusImagesAll[indexIn]
    maskedCelciusImage    = np.multiply(maskCelclius,celciusImage)
    finalCelciusImage     = finalCelciusImage + maskedCelciusImage

  return distanceImage, finalCelciusImage;



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
directory = "/home/teamlary/mintsData/"

print("defining Lag Intervals")
lag = datetime.timedelta(seconds=-1) 
add = datetime.timedelta(seconds=.2) 


print("Going in to the loop")

while(True):
    currentTime = datetime.datetime.now()
    dateTime1  = currentTime + lag
    dateTime2  = dateTime1 + add
    dateTime3  = dateTime2 + add
    rawName1     = directory + getImagePathTailHdf5Mod(dateTime1,'raw')
    # rawName2     = directory + getImagePathTailHdf5Mod(dateTime2,'raw')
    rawName3     = directory + getImagePathTailHdf5Mod(dateTime3,'raw')
    valName     = directory + getImagePathTailHdf5Mod(dateTime1,'val')
    

    # print("Loading hdf5 files for the relavent data points")
    raw1Valid,left,right,thermal1  = hdf5Reader(rawName1)
    # raw2Valid,left2,right2,thermal2  = hdf5Reader(rawName2)
    raw3Valid,left3,right3,thermal  = hdf5Reader(rawName3)

    if (raw1Valid and raw3Valid):
        if ((left.size>1) and(right.size>1)) and (thermal.size>1):
            t1= datetime.datetime.now()
            distanceF, celciusF = overlayReturnMinimal(left,right,thermal)
            print(datetime.datetime.now()-t1)
            # if(initial):
            #     distanceF, celciusF = overlayReturn(left,right,thermal)
            #     im1 = ax1.imshow(left)
            #     im2 = ax2.imshow(right)
            #     im3 = ax3.imshow(distanceF)
            #     im4 = ax4.imshow(celciusF)
            #     initial = False
            # else:
            #     distanceF, celciusF = overlayReturn(left,right,thermal)
            #     im1 = ax1.imshow(left)
            #     im2 = ax2.imshow(right)
            #     im3 = ax3.imshow(distanceF)
            #     im4 = ax4.imshow(celciusF)
            #     plt.pause(.001)

