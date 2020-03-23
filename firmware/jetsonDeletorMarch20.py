#!/usr/bin/env python
# -*- coding: utf-8 -*-
import h5py
# import pickle
import datetime
# from uvctypes import *
import time
import cv2
import numpy as np
# try:
#   from queue import Queue
# except ImportError:
#   from Queue import Queue
# import platform
import os
# import threading
import time
# import numpy, scipy.io
# from matplotlib import pyplot as plt
# from matplotlib.animation import FuncAnimation
# from PIL import Image



directoryRaw = "/home/teamlary/mintsData/raw/"
directoryVal = "/home/teamlary/mintsData/val/"

lag = datetime.timedelta(minutes=-10)

dateTime = datetime.datetime.now()
cutOffDateTime = dateTime + lag

print("Cut Off Time:")
print(cutOffDateTime)



def main():
  deletor(directoryRaw)
  deletor(directoryVal)

      
def deletor(directory):
  print()
  print("Cleaning "+ directory)
  for filename in sorted(os.listdir(directory)):
      # Check if its an HDF5 file
      try:
        if filename.endswith(".h5"):
            dateTimeSplit = filename.split('_')
            fileDateTime = datetime.datetime(int(dateTimeSplit[0]),int(dateTimeSplit[1]),int(dateTimeSplit[2]),\
                                              int(dateTimeSplit[3]),int(dateTimeSplit[4]),int(dateTimeSplit[5]))
            if(cutOffDateTime>fileDateTime):
              os.remove(directory+filename)
              print(directory+filename+" removed")

      except OSError as e:
        print ("Error: %s - %s." % (e.filename, e.strerror))




if __name__ == '__main__':
  main()