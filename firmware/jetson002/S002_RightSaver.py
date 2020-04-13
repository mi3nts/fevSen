# ***************************************************************************
#   mintsFevSen
#   ---------------------------------
#   Written by: Lakitha Omal Harindha Wijeratne
#   - for -
#   Mints: Multi-scale Integrated Sensing and Simulation
#      &
#   algolook.com
#   ---------------------------------
#   Date: March 29 th, 2019
#   ---------------------------------
#   This module is written for generic implimentation of MINTS projects
#   --------------------------------------------------------------------------
#   https://github.com/mi3nts
#   http://utdmints.info/
#
#  ***************************************************************************


import datetime
from uvctypes import *
import time
import cv2
import numpy as np
try:
  from queue import Queue
except ImportError:
  from Queue import Queue
import os
# import threading
import time
import imutils
import numpy, scipy.io
from imutils.video import WebcamVideoStream

from mintsJetson import camReader as cr

import h5py

cr.printMINTS("fevSen")

cr.printLabel("Logging Inputs")

highResolution = True
imageSave      = True
display        = False

directory = "/home/pyimagesearch/mintsData/jetson002/"
width     = 2592
height    = 1944
frameRate = 15

# For Low Resolution
if not highResolution:
    width     = 640
    height    = 480
    frameRate = 30


cr.printLabel("Script Parametors:")
print("High Resolution: {}, Image Saving: {}, Display: {}".format(highResolution,imageSave,display))

cr.printLabel("Local Directory: {} Assigned".format(directory))

cr.printLabel("Visual Camera Parametors:")
print("Height: {}, Width: {}, Frame Rate: {}".format(height,width,frameRate))

cr.printLabel("Gaining Camera Indexes")
myCmd = os.popen('v4l2-ctl --list-devices').read()
rightCamIndex   = cr.getRightWebCamIndex(myCmd)[1]
print("Right Camera Index: {}".format(rightCamIndex))


cr.printLabel("Initiating Visual Cameras with Maximum Resolution")
capRight  =  cr.openWebCamMPGJ(rightCamIndex, width, height,frameRate)

cr.printLabel("Creating Sub Directories")
cr.folderCheck(directory+"right")

cr.printLabel("Visual Camera Check")

if not capRight.isOpened() :
        print('Right Camera Stream Not opened')
        exit(0)
else:
    print("Right Camera Stream Open")

cr.printLabel("Entering Main function")

def main():

    try:
        for n in range(10):
            print("Check: " + str(n+1))
            retRight, frameRight     = capRight.read()
            if not retRight:
                print('Empty Right frame')
        cr.printLabel("Entering While Loop")

        while True:
            try:
                dateTime          = datetime.datetime.now()

                retRight, right     = capRight.read()
                print(dateTime)
                if not retRight:
                    print('Empty Right frame')
                else:
                    if (imageSave):
                        imageName   = directory + cr.getImagePathTail(dateTime,'right')
                        cv2.imwrite(imageName,right)
                        print("Saving: {}".format(imageName))


                    if(display):
                        cv2.imshow('Right Frame' , imutils.resize(right, width=640))

                if cv2.waitKey(1)&0xFF == ord('q'):
                    capRight.release()
                    break
            except KeyboardInterrupt:
                capRight.release()
                print()
                print("Exiting While Loop:")
                break
            except:

                print("Unexpected error in Loop:"+EOFError)

        capRight.release()
        cr.printLabel("MINTS done")
    except:
        capRight.release()
        print("Unexpected error:")
        raise


    cr.printMINTS("fevSen")


if __name__ == '__main__':
  main()
