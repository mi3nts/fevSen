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


directory = 'threeWayImageDataSets/hdf5ThreeWay2/'

leftImagesAll    = []
rightImagesAll   = []
thermalImagesAll = []


print("Saving all images")

for filename in sorted(os.listdir(directory)):
    if filename.endswith(".h5"):
        full= directory+filename
        hf = h5py.File(full, 'r')
        leftImagesAll.append(np.array(hf.get('left')))
        rightImagesAll.append(np.array(hf.get('right')))
        thermalImagesAll.append(np.array(hf.get('thermal')))


for lk in leftImagesAll:
  plt.subplot(221)
  plt.imshow(cv2.cvtColor(leftImagesAll[0], cv2.COLOR_BGR2RGB))
  plt.title("Left Image")
  # plt.subplot(222)
  # plt.imshow(cv2.cvtColor(rightImage, cv2.COLOR_BGR2RGB))
  # plt.title("Right Image")
  # plt.subplot(223)
  # plt.imshow(distanceImageF,cmap='rainbow')
  # plt.title("Depth Image")
  # plt.imshow(finalCelciusImageF,cmap='jet')
  # plt.title("Thermal Image")
  # cbar1 =  plt.colorbar();
  # cbar1.ax.set_ylabel(r"Temperature(C)", rotation=270,labelpad=20)
  # figManager = plt.get_current_fig_manager()
              # figManager.window.showMaximized()
  plt.show(block=False)
  plt.pause(5)
  plt.close()





# plt.show(block=False)
        # plt.pause(10)
        # plt.close()

    #   cv2.imshow('overlay',overlay)
    #     cv2.imshow('frameThermal' ,cv2.applyColorMap(np.uint8(celciusImage),cv2.COLORMAP_JET))
    #     cv2.imshow('frameDistance',cv2.applyColorMap(np.uint8(distanceImage),cv2.COLORMAP_RAINBOW))

        # thermalCelcius = ktoc(thermalData)
        
        # frameLeftRect    = cv2.remap(leftImage ,stereoParams['mapXLeft'],\
        #                                                  stereoParams['mapYLeft'],\
        #                                                             cv2.INTER_CUBIC)
        # frameRightRect   = cv2.remap(rightImage,stereoParams['mapXRight'],\
        #                                                         stereoParams['mapYRight'],
        #                                                             cv2.INTER_CUBIC)
        # frameCelciusRect = cv2.undistort(\
        #                                     thermalCelcius,\
        #                                     thermalParams['mtxThermal'],\
        #                                     thermalParams['distThermal']
        #                                     , None,\
        #                                     thermalParams['newcameramtx']\
        #                                     )

             
        # disparityPre     = leftMatcher.compute(frameLeftRect,frameRightRect)
        # distanceImage    = 30590*(disparityPre**-0.9453)

        # maskCelcliusAll       = []
        # celciusImageAll       = []
        # maskedCelciusImageAll = []
        # finalCelciusImage     = np.zeros((480, 640))

        # rows,cols,ch = frameLeftRect.shape

        # for indexIn in range(len(homographyAll)):
        #     maskCelclius          = (cutOffs[indexIn]<=distanceImage)&\
        #                                         (distanceImage<cutOffs[indexIn+1])
        #     maskCelcliusAll.append(maskCelclius)
        #     celciusImage          = cv2.warpPerspective(frameCelciusRect,\
        #                                                                 homographyAll[indexIn],\
        #                                                                   (cols,rows))
        #     celciusImageAll.append(celciusImage)
        #     maskedCelciusImage    = np.multiply(maskCelclius,celciusImage)
        #     maskedCelciusImageAll.append(maskedCelciusImage)
        #     finalCelciusImage = finalCelciusImage + maskedCelciusImage

        # distanceImageF = cv2.remap(distanceImage ,stereoParams['mapXLeftReverse'],\
        #                                             stereoParams['mapYLeftReverse'],\
        #                                                     cv2.INTER_CUBIC)
        # finalCelciusImageF = cv2.remap(finalCelciusImage ,stereoParams['mapXLeftReverse'],\
        #                                         stereoParams['mapYLeftReverse'],\
        #                                                 cv2.INTER_CUBIC)
