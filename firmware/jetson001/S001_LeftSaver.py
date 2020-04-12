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

directory = "/home/pyimagesearch/mintsData/jetson001/"
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
leftCamIndex   = cr.getLeftWebCamIndex(myCmd)[1]
print("Left Camera Index: {}".format(leftCamIndex))


cr.printLabel("Initiating Visual Cameras with Maximum Resolution")
capLeft  =  cr.openWebCamMPGJ(leftCamIndex, width, height,frameRate)

cr.printLabel("Creating Sub Directories")
cr.folderCheck(directory+"left")

cr.printLabel("Visual Camera Check")

if not capLeft.isOpened() :
        print('Left Camera Stream Not opened')
        exit(0)
else:
    print("Left Camera Stream Open")

cr.printLabel("Entering Main function")

def main():

    try:
        for n in range(10):
            print("Check: " + str(n+1))
            retLeft, frameLeft     = capLeft.read()
            if not retLeft:
                print('Empty Left frame')
        cr.printLabel("Entering While Loop")

        while True:
            try:
                dateTime          = datetime.datetime.now()

                retLeft, left     = capLeft.read()
  
                if not retLeft:
                    print('Empty Left frame')
                else: 
                    if (imageSave):
                        imageName   = directory + cr.getImagePathTail(dateTime,'left')
                        cv2.imwrite(imageName,left)
                        print("Saving: {}".format(imageName))
                        
                    if(display):
                        cv2.imshow('Left Frame' , imutils.resize(left, width=640))
                    
                if cv2.waitKey(1)&0xFF == ord('q'):
                    capLeft.release()
                    break
            except KeyboardInterrupt:             
                capLeft.release()
                print()
                print("Exiting While Loop:")
                break
            except:
                
                print("Unexpected error in Loop:")
        
        capLeft.release()
        cr.printLabel("MINTS done")
    except:
        capLeft.release()
        print("Unexpected error:")
        raise


    cr.printMINTS("fevSen")


if __name__ == '__main__':
  main()
