# % # ***************************************************************************
# % #   Stereo Vision - Thermal
# % #   ---------------------------------
# % #   Written by: Lakitha Omal Harindha Wijeratne
# % #   - for -
# % #   Mints: Multi-scale Integrated Sensing and Simulation
# % #   ---------------------------------
# % #   Date: April 02nd, 2020
# % #   ---------------------------------
# % #   This module is written for generic implimentation of MINTS projects
# % #   --------------------------------------------------------------------------
# % #   https://github.com/mi3nts
# % #   http://utdmints.info/
# % #  ***************************************************************************
#
#  Step 012: Stereo Thermal Calibration Jetson 001

import cv2
import pickle
import numpy as  np
from matplotlib import pyplot as plt
from scipy.io import loadmat
import datetime
import os,sys,inspect
from os import path
import h5py
import imutils
from mintsJetson import camReader as cr

cr.printMINTS("fevSen")
cr.printLabel("Loading Parametors")
stereoParams  = pickle.load(open("dataFiles/DF_003_stereoParams_Jetson001_2020_04_02_19_05_49.p", "rb"))
thermalParams = pickle.load(open("dataFiles/DF_005_thermalParams_Jetson001_2020_04_02_22_55_59.p", "rb"))
overlayParams = pickle.load(open("dataFiles/DF_011_overlayParams_Jetson001_2020_04_04_19_19_01.p", "rb"))

cr.printLabel("Defining Image Names")
thermalImageName = "exampleImages/jetson001_thermal.h5"
leftImageName    = "exampleImages/jetson001_left.jpg"
rightImageName   = "exampleImages/jetson001_right.jpg"
scalingFactor    = 4

cr.printLabel("Defining Coordinates")
coordsIn = [(1601,964,1630,1002), (1601,964,1630,1002), (1601,964,1630,1002)]

cr.printLabel("Loading Disparity Model")
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

def main():
    cr.printLabel("Visual Validation")
    left, distcanceCM, temperatureC = cr.overlayReturn002(leftImageName,rightImageName,thermalImageName,stereoParams,thermalParams,leftMatcher,overlayParams)
    cr.plotSubplot(left, distcanceCM, temperatureC)

    cr.printLabel("Gaining Results")
    resultsCelius = cr.getCurrentFeverSensorInfoCelcius(leftImageName,rightImageName,thermalImageName,\
                                            stereoParams,thermalParams,overlayParams,\
                                                leftMatcher,scalingFactor,coordsIn)
    resultsFarenheit=cr.getCurrentFeverSensorInfoFarenheit(leftImageName,rightImageName,thermalImageName,\
                                                stereoParams,thermalParams,overlayParams,\
                                                    leftMatcher,scalingFactor,coordsIn)

    cr.printLabel("Printing Results in CM & Celcius:")
    print(resultsCelius)

    cr.printLabel("Printing Results in CM & Farenheit:")
    print(resultsFarenheit)

    cr.printLabel("MINTS done")
    cr.printMINTS("fevSen")
    
if __name__ == '__main__':
  main()
