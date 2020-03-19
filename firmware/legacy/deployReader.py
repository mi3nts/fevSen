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


directory = 'threeWayImageDataSets/hdf5ThreeWay/'


leftImagesAll = []
thermalImagesAll = []




for filename in sorted(os.listdir(directory)):
    if filename.endswith(".h5"):
        full= directory+filename
        hf = h5py.File(full, 'r')
        print(hf.keys())
        leftImage = np.array(hf.get('left'))
        celciusImage = np.array(hf.get('celcius'))
        distanceImage = np.array(hf.get('distance'))




        cmap = plt.cm.jet
        norm = plt.Normalize(vmin=celciusImage.min(), vmax=celciusImage.max())

        # map the normalized data to colors
        # image is now RGBA (512x512x4)
        thermal = cmap(norm(celciusImage))
        plt.imsave('thermal.png',thermal)

        left    = cv2.cvtColor(leftImage, cv2.COLOR_BGR2RGB)
        thermal = cv2.cvtColor(cv2.imread('thermal.png'), cv2.COLOR_BGR2RGB)

        alpha = 0.5
        beta = (1.0 - alpha)

        overlay = cv2.addWeighted(leftImage,alpha,thermal,beta,0)
        cv2.imshow('frameLeft',leftImage)
        cv2.imshow('overlay',overlay)
        cv2.imshow('frameThermal' ,cv2.applyColorMap(np.uint8(celciusImage),cv2.COLORMAP_JET))
        cv2.imshow('frameDistance',cv2.applyColorMap(np.uint8(distanceImage),cv2.COLORMAP_RAINBOW))
        cv2.waitKey(500)
        
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #   cv2.destroyAllWindows()
        #   break
  
  
        # distanceImage[distanceImage>1500]=0

        # plt.subplot(221)
        # plt.imshow(cv2.cvtColor(leftImage, cv2.COLOR_BGR2RGB))
        # plt.title("Original Image")
        # plt.subplot(222)
        # plt.imshow(distanceImage,cmap='rainbow')
        # plt.title("Depth Image")
        # cbar1 =  plt.colorbar();
        # cbar1.ax.set_ylabel(r"Distance(cm)", rotation=270,labelpad=20)
        # plt.subplot(223)
        # plt.imshow(overlay)
        # plt.title("Thermal Visual Overlay")
        # plt.subplot(224)
        # plt.imshow(celciusImage,cmap='jet')
        # plt.title("Thermal Image")
        # cbar1 =  plt.colorbar();
        # cbar1.ax.set_ylabel(r"Temperature(C)", rotation=270,labelpad=20)
        # figManager = plt.get_current_fig_manager()
        # figManager.window.showMaximized()
        # plt.show()

        # plt.show(block=False)
        # plt.pause(10)
        # plt.close()
