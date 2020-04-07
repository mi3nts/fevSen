

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
#  Step 000: Stereo Thermal Calibration

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

cr.printLabel("User Defined Variables")
stereoParams  = pickle.load(open("dataFiles/DF_003_stereoParams_Jetson001_2020_04_02_19_05_49.p", "rb"))
thermalParams = pickle.load(open("dataFiles/DF_005_thermalParams_Jetson001_2020_04_02_22_55_59.p", "rb"))
overlayParams = pickle.load(open("dataFiles/DF_011_overlayParams_Jetson001_2020_04_04_19_19_01.p", "rb"))

cutOffs       = overlayParams['cutOffs']
homographyAll = overlayParams['homographyAll']
fitA          = overlayParams['fitA']
fitB          = overlayParams['fitB']

# print(overlayParams)
# resizeWidth   = 648
#
# directory = "/home/teamlary/mintsData/"
#
# readName1 = directory + "stereoThermal/2020_04_05_22_35_50_746254_stereoThermal.h5"
# readName2 = directory + "stereoThermal/2020_04_05_22_35_51_758923_stereoThermal.h5"
# readName3 = directory + "stereoThermal/2020_04_05_22_35_53_110790_stereoThermal.h5"
# readName4 = directory + "stereoThermal/2020_04_05_22_35_53_907504_stereoThermal.h5"
# readName5 = directory + "stereoThermal/2020_04_05_22_35_53_907504_stereoThermal.h5"
#
# cr.printLabel("Loading Disparity Model")
#
# windowSize = 15                    # wsize default 3; 5; 7 for SGBM reduced size image; 15 for SGBM full size image (1300px and above); 5 Works nicely
# maxDisparity = 64
# leftMatcher = cv2.StereoSGBM_create(
#     minDisparity=0,
#     numDisparities=maxDisparity,             # max_disp has to be dividable by 16 f. E. HH 192, 256
#     blockSize=5,
#     P1=8 * 3 * windowSize ** 2,    # wsize default 3; 5; 7 for SGBM reduced size image; 15 for SGBM full size image (1300px and above); 5 Works nicely
#     P2=32 * 3 * windowSize ** 2,
#     disp12MaxDiff=1,
#     uniquenessRatio=15,
#     speckleWindowSize=0,
#     speckleRange=2,
#     preFilterCap=63,
#     mode=cv2.STEREO_SGBM_MODE_SGBM_3WAY
# )
# alpha = .5
# beta = (1.0 - alpha)
#
# def main():
#     cr.printLabel("Loading 3 Way Image ")
#     now = datetime.datetime.now()
#     valid,left,right,thermal = hdf5Reader(readName1)
#     leftScaled,rightScaled             = scaleStereo(left,right,resizeWidth)
#     # distanceImageF, finalCelciusImageF = overlayReturn001(leftScaled,rightScaled,thermal,stereoParams,thermalParams,leftMatcher,overlayParams)
#
#     now = datetime.datetime.now()
#     distanceCM               = getDistanceImage(leftScaled,rightScaled,stereoParams,leftMatcher,fitA,fitB)
#     celcius                  = getCelciusUndistorted(thermal,thermalParams)
#     distanceCMF              = getReverseMapping(distanceCM,stereoParams)
#     shape        = leftScaled.shape
#     celciusMasks = np.zeros((shape[0], shape[1],len(homographyAll)),dtype=np.bool)
#
#     now = datetime.datetime.now()
#     for indexIn in range(len(homographyAll)):
#         celciusMasks[:,:,indexIn]= (cutOffs[indexIn][0]<=distanceCM )&\
#                                                     (distanceCM <cutOffs[indexIn][1])
#
#     celciusImages = np.zeros((shape[0], shape[1],len(homographyAll)),dtype=np.uint16)
#     print(datetime.datetime.now()-now)
#
#     now = datetime.datetime.now()
#     for indexIn in range(len(homographyAll)):
#         celciusImages[:,:,indexIn]     = cv2.warpPerspective(celcius,\
#                                                                 homographyAll[indexIn],\
#                                                                 (shape[1], shape[0]))
#     celciusImagesFinal = np.zeros((shape[0], shape[1],len(homographyAll)),dtype=np.uint16)
#     print(datetime.datetime.now()-now)
#
#     now = datetime.datetime.now()
#     for indexIn in range(len(homographyAll)):
#         celciusImagesFinal[:,:,indexIn] = np.multiply(celciusMasks[:,:,indexIn],celciusImages[:,:,indexIn])
#     print(datetime.datetime.now()-now)
#
#     now = datetime.datetime.now()
#     np.sum(celciusImagesFinal,axis = 2)
#     print(datetime.datetime.now()-now)
#
#
#     plt.subplot(221)
#     plt.imshow(np.sum(celciusImagesFinal,axis = 2))
#     # plt.subplot(222)
#     # plt.imshow(cv2.cvtColor(rightScaled, cv2.COLOR_BGR2RGB))
#     # plt.subplot(223)
#     # plt.imshow(ktoc(cv2.resize(thermal[:,:], (640, 480))),cmap='jet')
#     plt.suptitle("All")
#     plt.show()
#     #
#     #
#     #
#     #
#     #
#     # print(datetime.datetime.now()-now)
#     # celcius = finalCelciusImageF
#     # cmap = plt.cm.jet
#     # norm = plt.Normalize(vmin=celcius.min(), vmax=celcius.max())
#     #
#     #     # map the normalized data to colors
#     #     # image is now RGBA (512x512x4)
#     # thermal = cmap(norm(celcius))
#     # plt.imsave('thermal.png',thermal)
#     #
#     #
#     # thermal = cv2.cvtColor(cv2.imread('thermal.png'), cv2.COLOR_BGR2RGB)
#     #
#     #
#     # overlay = cv2.addWeighted(leftScaled,alpha,thermal,beta,0)
# #
#     # # plt.figure()
#     # plt.subplot(221)
#     # plt.imshow(cv2.cvtColor(leftScaled, cv2.COLOR_BGR2RGB))
#     # plt.subplot(222)
#     # plt.imshow(distanceImageF,cmap='rainbow')
#     # plt.subplot(223)
#     # plt.imshow(finalCelciusImageF,cmap='jet')
#     # plt.subplot(224)
#     # plt.imshow(overlay)
#     # plt.suptitle("All")
#     # plt.show()
#
#     # print("Going in to the loop")
#     # while(True):
#     #     try:
#     #         raw1Valid,left1,right1,thermal   = hdf5Reader(rawName1)
#     #
#     #         if (raw1Valid and raw2Valid):
#     #             if ((left.size>1) and(right.size>1)) and (thermal.size>1):
#     #                 print(dateTime1)
#     #                 distance, celcius = overlayReturn(left,right,thermal)
#     #                 hdf5Saver(valName,left,celcius,distance)
#     #                 # SYNC CODE GOES HERE
#     #
#     #     except:
#     #         print("An exception occurred")
#     #         time.sleep(1)
#
#
#
#
# def scaleStereo(left,right,widthIn):
#     return imutils.resize(left,width=widthIn),imutils.resize(right,width=widthIn);
#
#
#
# def getRectifiedStereo(leftImage,rightImage,stereoParams):
#
#     frameLeftRect    = cv2.remap(leftImage ,stereoParams['mapXLeft'],\
#                                                             stereoParams['mapYLeft'],\
#                                                                         cv2.INTER_CUBIC)
#     frameRightRect   = cv2.remap(rightImage,stereoParams['mapXRight'],\
#                                                                     stereoParams['mapYRight'],
#                                                                         cv2.INTER_CUBIC)
#
#     return frameLeftRect,frameRightRect;
#
#
# def getDistanceImage(leftImage,rightImage,stereoParams,leftMatcher,fitA,fitB):
#     frameLeftRect,frameRightRect = getRectifiedStereo(leftImage,rightImage,stereoParams)
#     distanceImageRaw             = leftMatcher.compute(frameLeftRect,frameRightRect)
#
#     return fitA*(distanceImageRaw**fitB);
#
# def getCelciusUndistorted(thermal,thermalParams):
#     frameCelciusRect = cv2.undistort(\
#                                         ktoc(cv2.resize(thermal[:,:], (640, 480))),\
#                                         thermalParams['mtxThermal'],\
#                                         thermalParams['distThermal']
#                                         , None,\
#                                         thermalParams['newcameramtx']\
#                                         )
#
#     return frameCelciusRect;
#
# # def getDistanceMasks(distanceImage,cutOffs,numOfHomographies):
# #     np.zeros((8,8) dtype=np.bool)
# #     for indexIn in range(numOfHomographies):
# #         maskCelclius.append(cutOffs[indexIn][0]<=distanceImage)&\
# #                                                     (distanceImage<cutOffs[indexIn][1])
#
#
#
#
#
#
#
#
# def hdf5Reader(fileName):
#     if (path.exists(fileName)):
#         print("File: "+ fileName +" Exists")
#         hf      = h5py.File(fileName, 'r')
#         print(hf.keys())
#         left    = np.array(hf.get('left'))
#         right   = np.array(hf.get('right'))
#         thermal = np.array(hf.get('thermal'))
#         print(thermal)
#         hf.close()
#         return True,left,right,thermal;
#     else:
#         # print("Path:" + fileName +  " Doesnt Exist")
#         return False,[],[],[];
#
# def hdf5Saver(fileName,left,celcius,distance):
#     hf = h5py.File(fileName, 'w')
#     hf.create_dataset('left'    , data=left)
#     hf.create_dataset('celcius' , data=celcius)
#     hf.create_dataset('distance', data=distance)
#     hf.close()
#
#
# def getImagePathTailHdf5Mod(dateTime,labelIn):
#     mod = round(dateTime.microsecond/200000)
#     pathTail = labelIn+"/"+\
#     str(dateTime.year).zfill(4) + \
#     "_" +str(dateTime.month).zfill(2) + \
#     "_" +str(dateTime.day).zfill(2)+ \
#     "_" +str(dateTime.hour).zfill(2) + \
#     "_" +str(dateTime.minute).zfill(2)+ \
#     "_" +str(dateTime.second).zfill(2)+ \
#     "_" +str((mod-1)*20).zfill(2)+ \
#     "_"+labelIn+".h5"
#
#     return pathTail;
#
# def getImagePathTailHdf5Mod2(dateTime,labelIn):
#
#     pathTail = labelIn+"/"+\
#     str(dateTime.year).zfill(4) + \
#     "_" +str(dateTime.month).zfill(2) + \
#     "_" +str(dateTime.day).zfill(2)+ \
#     "_" +str(dateTime.hour).zfill(2) + \
#     "_" +str(dateTime.minute).zfill(2)+ \
#     "_" +str(dateTime.second).zfill(2)+ \
#     "_" +str(dateTime.microsecond).zfill(6)[0]+ \
#     "_"+labelIn+".h5"
#
#     return pathTail;
#
# def ktoc(val):
#     return (val - 27315) / 100.0
#
# def getThermalOverlay(distanceCM,thermalCelcius,numOfHomographies):
#     finalCelciusImage     = np.zeros((480, 640))
#
#     for indexIn in range(numOfHomographies):
#         maskCelclius          = (cutOffs[indexIn][0]<=distanceImage)&\
#                                                     (distanceImage<cutOffs[indexIn][1])
#
#         celciusImage          = cv2.warpPerspective(frameCelciusRect,\
#                                                                 homographyAll[indexIn],\
#                                                                 (cols,rows))
#         maskedCelciusImage    = np.multiply(maskCelclius,celciusImage)
#         finalCelciusImage = finalCelciusImage + maskedCelciusImage
#
#
# #
#
#
# def getReverseMapping(imageIn,stereoParams):
#     return cv2.remap(imageIn ,stereoParams['mapXLeftReverse'],\
#                                                             stereoParams['mapYLeftReverse'],\
#                                                                     cv2.INTER_CUBIC);
#
#
#
# print("Overlay Function")
# def overlayReturn001(leftImage,rightImage,thermal,stereoParams,thermalParams,leftMatcher,overlayParams):
#
#     thermalData   = cv2.resize(thermal[:,:], (640, 480))
#     thermalCelcius = ktoc(thermalData)
#
#     frameLeftRect    = cv2.remap(leftImage ,stereoParams['mapXLeft'],\
#                                                             stereoParams['mapYLeft'],\
#                                                                         cv2.INTER_CUBIC)
#     frameRightRect   = cv2.remap(rightImage,stereoParams['mapXRight'],\
#                                                                     stereoParams['mapYRight'],
#                                                                         cv2.INTER_CUBIC)
#
#     frameCelciusRect = cv2.undistort(\
#                                         thermalCelcius,\
#                                         thermalParams['mtxThermal'],\
#                                         thermalParams['distThermal']
#                                         , None,\
#                                         thermalParams['newcameramtx']\
#                                         )
#
#     disparityPre     = leftMatcher.compute(frameLeftRect,frameRightRect)
#     distanceImage    = overlayParams['fitA']*(disparityPre**overlayParams['fitB'])
#
#
#
#
#     rows,cols,ch = frameLeftRect.shape
#     finalCelciusImage     = np.zeros((rows,cols))
#
#     for indexIn in range(len(homographyAll)):
#         maskCelclius          = (cutOffs[indexIn][0]<=distanceImage)&\
#                                                     (distanceImage<cutOffs[indexIn][1])
#
#         celciusImage          = cv2.warpPerspective(frameCelciusRect,\
#                                                                 homographyAll[indexIn],\
#                                                                 (cols,rows))
#         maskedCelciusImage    = np.multiply(maskCelclius,celciusImage)
#         finalCelciusImage     = finalCelciusImage + maskedCelciusImage
#
#     distanceImageF = cv2.remap(distanceImage ,stereoParams['mapXLeftReverse'],\
#                                                         stereoParams['mapYLeftReverse'],\
#                                                                 cv2.INTER_CUBIC)
#     finalCelciusImageF = cv2.remap(finalCelciusImage ,stereoParams['mapXLeftReverse'],\
#                                                     stereoParams['mapYLeftReverse'],\
#                                                             cv2.INTER_CUBIC)
#
#     return distanceImageF, finalCelciusImageF;
#
#
#
#
#
#
#
# print("Overlay Function")
# def overlayReturn(leftImage,rightImage,thermal):
#     thermalData   = cv2.resize(thermal[:,:], (640, 480))
#     thermalCelcius = ktoc(thermalData)
#
#     frameLeftRect    = cv2.remap(leftImage ,stereoParams['mapXLeft'],\
#                                                             stereoParams['mapYLeft'],\
#                                                                         cv2.INTER_CUBIC)
#     frameRightRect   = cv2.remap(rightImage,stereoParams['mapXRight'],\
#                                                                     stereoParams['mapYRight'],
#                                                                         cv2.INTER_CUBIC)
#
#     frameCelciusRect = cv2.undistort(\
#                                         thermalCelcius,\
#                                         thermalParams['mtxThermal'],\
#                                         thermalParams['distThermal']
#                                         , None,\
#                                         thermalParams['newcameramtx']\
#                                         )
#
#     disparityPre     = leftMatcher.compute(frameLeftRect,frameRightRect)
#     distanceImage    = 30590*(disparityPre**-0.9453)
#
#
#     finalCelciusImage     = np.zeros((480, 640))
#
#     rows,cols,ch = frameLeftRect.shape
#
#     for indexIn in range(len(homographyAll)):
#         maskCelclius          = (cutOffs[indexIn]<=distanceImage)&\
#                                                     (distanceImage<cutOffs[indexIn+1])
#
#         celciusImage          = cv2.warpPerspective(frameCelciusRect,\
#                                                                 homographyAll[indexIn],\
#                                                                 (cols,rows))
#         maskedCelciusImage    = np.multiply(maskCelclius,celciusImage)
#         finalCelciusImage = finalCelciusImage + maskedCelciusImage
#
#     distanceImageF = cv2.remap(distanceImage ,stereoParams['mapXLeftReverse'],\
#                                                         stereoParams['mapYLeftReverse'],\
#                                                                 cv2.INTER_CUBIC)
#     finalCelciusImageF = cv2.remap(finalCelciusImage ,stereoParams['mapXLeftReverse'],\
#                                                     stereoParams['mapYLeftReverse'],\
#                                                             cv2.INTER_CUBIC)
#
#     return distanceImageF, finalCelciusImageF;
#
# if __name__ == '__main__':
#   main()
