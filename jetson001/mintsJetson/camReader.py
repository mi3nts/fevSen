# ***************************************************************************
#   camReader
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


import cv2
import os
import numpy as np
from imutils.video import WebcamVideoStream
import imutils
import math
from scipy.io import loadmat
# def py_frame_callback(frame, userptr):

#   array_pointer = cast(frame.contents.data, POINTER(c_uint16 * (frame.contents.width * frame.contents.height)))
#   data = np.frombuffer(
#     array_pointer.contents, dtype=np.dtype(np.uint16)
#   ).reshape(
#     frame.contents.height, frame.contents.width
#   ) # no copy

#   # data = np.fromiter(
#   #   frame.contents.data, dtype=np.dtype(np.uint8), count=frame.contents.data_bytes
#   # ).reshape(
#   #   frame.contents.height, frame.contents.width, 2
#   # ) # copy

#   if frame.contents.data_bytes != (2 * frame.contents.width * frame.contents.height):
#     return

#   if not q.full():
#     q.put(data)

# # PTR_PY_FRAME_CALLBACK = CFUNCTYPE(None, POINTER(uvc_frame), c_void_p)(py_frame_callback)

def ktof(val):
  return (1.8 * ktoc(val) + 32.0)

def ktoc(val):
  return (val - 27315) / 100.0

def raw_to_8bit(data):
  cv2.normalize(data, data, 0, 65535, cv2.NORM_MINMAX)
  np.right_shift(data, 8, data)
  return cv2.cvtColor(np.uint8(data), cv2.COLOR_GRAY2RGB)

def display_temperature(img, val_k, loc, color):
  val = ktoc(val_k)
  cv2.putText(img,"{0:.1f} degC".format(val), loc, cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2)
  x, y = loc
  cv2.line(img, (x - 2, y), (x + 2, y), color, 1)
  cv2.line(img, (x, y - 2), (x, y + 2), color, 1)

def getLeftWebCamIndex(myCmd):
    lines = myCmd.splitlines()
    for num, name in enumerate(lines, start=1):
        if "2.2" in name:
            camString =  int(lines[num].strip().replace("/dev/video",""))
            return  True ,camString;

    return False , "xxx";


def getRightWebCamIndex(myCmd):
    lines = myCmd.splitlines()
    for num, name in enumerate(lines, start=1):
        if "2.4" in name:
            camString =  int(lines[num].strip().replace("/dev/video",""))
            return True, camString;

    return False, "xxx";


def takeWebCamImage(indexIn):
    capture = cv2.VideoCapture(indexIn)
    # capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('Y', 'U', 'Y', 'V'))
    # capture.set(cv::CAP_PROP_FOURCC, cv::VideoWriter::fourcc('M', 'J', 'P', 'G'));
    time.sleep(0.1)
    ret0, out_image = capture.read()
    # print(out_image.shape)
    # time.sleep(1)
    # out_image = cv2.cvtColor(out_image , cv2.COLOR_HSV2BGR)

    # cv2.imshow('frame',out_image)
    # cv2.waitKey(0)


    capture.release()
    return ret0,out_image;


def getImagePathTail(dateTime,labelIn):
    pathTail = labelIn+"/"+\
    str(dateTime.year).zfill(4) + \
    "_" +str(dateTime.month).zfill(2) + \
    "_" +str(dateTime.day).zfill(2)+ \
    "_" +str(dateTime.hour).zfill(2) + \
    "_" +str(dateTime.minute).zfill(2)+ \
    "_" +str(dateTime.second).zfill(2)+ \
    "_" +str(dateTime.microsecond).zfill(6)+ \
    "_"+labelIn+".jpg"
    # print(pathTail)
    return pathTail;

def getImagePathTailMat(dateTime,labelIn):
    pathTail = labelIn+"/"+\
    str(dateTime.year).zfill(4) + \
    "_" +str(dateTime.month).zfill(2) + \
    "_" +str(dateTime.day).zfill(2)+ \
    "_" +str(dateTime.hour).zfill(2) + \
    "_" +str(dateTime.minute).zfill(2)+ \
    "_" +str(dateTime.second).zfill(2)+ \
    "_"+labelIn+".mat"

    return pathTail;

def getImagePathTailHdf5(dateTime,labelIn):

    pathTail = labelIn+"/"+\
    str(dateTime.year).zfill(4) + \
    "_" +str(dateTime.month).zfill(2) + \
    "_" +str(dateTime.day).zfill(2)+ \
    "_" +str(dateTime.hour).zfill(2) + \
    "_" +str(dateTime.minute).zfill(2)+ \
    "_" +str(dateTime.second).zfill(2)+ \
    "_" +str(dateTime.microsecond).zfill(2)+ \
    "_"+labelIn+".h5"

    return pathTail;


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

def saveWebCamImage(capture,imageName):
    ret,image  = capture.read()
    print(image)
    print(imageName)
    cv2.imwrite(imageName,image)

def grab_frame(cap):
    ret,frame = cap.read()
    return cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)


def openWebCamMPGJ(dev, width, height,framerate):
    gst = ('v4l2src device=/dev/video{} do-timestamp=true ! \
         image/jpeg, width={}, height={}, framerate={}/1 \
           ! jpegparse ! jpegdec ! videoconvert ! appsink ').format(dev, width, height,framerate)

    return cv2.VideoCapture(gst, cv2.CAP_GSTREAMER)



def openUSBCam(dev, width, height):
    # We want to set width and height here, otherwise we could just do:
    #     return cv2.VideoCapture(dev)
    gst_str = ('v4l2src device=/dev/video{} ! '
               'video/x-raw, width=(int){}, height=(int){} ! '
               'videoconvert ! appsink').format(dev, width, height)
    return cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)

def openUSBCamVS(dev, width, height):
    # We want to set width and height here, otherwise we could just do:
    #     return cv2.VideoCapture(dev)
    gst_str = ('v4l2src device=/dev/video{} ! '
               'video/x-raw, width=(int){}, height=(int){} ! '
               'videoconvert ! appsink').format(dev, width, height)
    return WebcamVideoStream(gst_str, cv2.CAP_GSTREAMER).start()


def getImagePathTailHdf5Mod2(dateTime,labelIn):

    pathTail = labelIn+"/"+\
    str(dateTime.year).zfill(4) + \
    "_" +str(dateTime.month).zfill(2) + \
    "_" +str(dateTime.day).zfill(2)+ \
    "_" +str(dateTime.hour).zfill(2) + \
    "_" +str(dateTime.minute).zfill(2)+ \
    "_" +str(dateTime.second).zfill(2)+ \
    "_" +str(dateTime.microsecond).zfill(6)[0]+ \
    "_"+labelIn+".h5"

    return pathTail;

def folderCheck(outputPath):
    exists = os.path.isdir(outputPath)
    if not exists:
        print("Creating Directory '{}'".format(outputPath))
        os.makedirs(outputPath)
    else:
        print("Directory '{}' exists".format(outputPath))

    return exists

def thermalRawConvert(thermalData):
  return raw_to_8bit(cv2.resize(thermalData[:,:], (640, 480)))



def mat2PyGetImageCornersStereo(leftImagePoints,rightImagePoints,objp,\
                                    horizontalInnerCorners,verticalInnerCorners):
    printLabel("Reading Corner Points from Stereo Visual Cameras")
    objPoints         = []  # 3d point in real world space
    leftImageCorners  = []
    rightImageCorners = []
    leftFileNames     =  []
    rightFileNames    = []


    for imageIndex in range(len(leftImagePoints[0][0])):
       leftImageCurrentCorners  = []
       rightImageCurrentCorners = []
       objPoints.append(objp)

       for cornerIndex in range(len(leftImagePoints)):

           leftXCordCurrent= np.float32(leftImagePoints[cornerIndex][0][imageIndex])
           leftYCordCurrent= np.float32(leftImagePoints[cornerIndex][1][imageIndex])
           leftImageCurrentCorners.append([[leftXCordCurrent,leftYCordCurrent]])

           rightXCordCurrent = np.float32(rightImagePoints[cornerIndex][0][imageIndex])
           rightYCordCurrent = np.float32(rightImagePoints[cornerIndex][1][imageIndex])
           rightImageCurrentCorners.append([[rightXCordCurrent,rightYCordCurrent]])

       leftImageCorners.append(leftImageCurrentCorners)
       rightImageCorners.append(rightImageCurrentCorners)

    leftCorners = np.array(leftImageCorners)
    rightCorners = np.array(rightImageCorners)


    printLabel("Rearranging Corners of Stereo Cameras to Suit Python Deployments")

    leftCornersArranged  = leftCorners
    rightCornersArranged = rightCorners

    for imageIndex in range(len(leftImagePoints[0][0])):
       currentLeftCornerPoints = leftCorners[imageIndex]
       for cornerIndex in range(len(leftImagePoints)):
           arrangedIndex = horizontalInnerCorners*((cornerIndex)%verticalInnerCorners)\
                               + math.floor(cornerIndex/verticalInnerCorners)
           leftCornersArranged[imageIndex][arrangedIndex]  = \
                                           leftImageCorners[imageIndex][cornerIndex]
           rightCornersArranged[imageIndex][arrangedIndex] = \
                                           rightImageCorners[imageIndex][cornerIndex]
    return leftCornersArranged,rightCornersArranged, objPoints;




def mat2PyGetImageCornersStereoScaled(leftImagePoints,rightImagePoints,\
                                    horizontalInnerCorners,verticalInnerCorners,\
                                    scaleFactor):
    objp        = np.zeros((horizontalInnerCorners*verticalInnerCorners, 3), np.float32)
    objp[:, :2] = np.mgrid[0:horizontalInnerCorners, 0:verticalInnerCorners].T.reshape(-1, 2)

    printLabel("Reading Corner Points from Stereo Visual Cameras")
    objPoints         = []  # 3d point in real world space
    leftImageCorners  = []
    rightImageCorners = []
    leftFileNames     =  []
    rightFileNames    = []

    for imageIndex in range(len(leftImagePoints[0][0])):
       leftImageCurrentCorners  = []
       rightImageCurrentCorners = []
       objPoints.append(objp)

       for cornerIndex in range(len(leftImagePoints)):

           leftXCordCurrent= np.float32(leftImagePoints[cornerIndex][0][imageIndex])
           leftYCordCurrent= np.float32(leftImagePoints[cornerIndex][1][imageIndex])
           leftImageCurrentCorners.append([[leftXCordCurrent,leftYCordCurrent]])

           rightXCordCurrent = np.float32(rightImagePoints[cornerIndex][0][imageIndex])
           rightYCordCurrent = np.float32(rightImagePoints[cornerIndex][1][imageIndex])
           rightImageCurrentCorners.append([[rightXCordCurrent,rightYCordCurrent]])

       leftImageCorners.append(leftImageCurrentCorners)
       rightImageCorners.append(rightImageCurrentCorners)

    leftCorners = np.array(leftImageCorners)
    rightCorners = np.array(rightImageCorners)


    printLabel("Rearranging Corners of Stereo Cameras to Suit Python Deployments")
    leftCornersArranged  = leftCorners
    rightCornersArranged = rightCorners

    for imageIndex in range(len(leftImagePoints[0][0])):
       currentLeftCornerPoints = leftCorners[imageIndex]
       for cornerIndex in range(len(leftImagePoints)):
           arrangedIndex = horizontalInnerCorners*((cornerIndex)%verticalInnerCorners)\
                               + math.floor(cornerIndex/verticalInnerCorners)
           leftCornersArranged[imageIndex][arrangedIndex]  = \
                                           leftImageCorners[imageIndex][cornerIndex]
           rightCornersArranged[imageIndex][arrangedIndex] = \
                                           rightImageCorners[imageIndex][cornerIndex]


    print("Scaling to Match Higher Resolution")
    return leftCornersArranged*scaleFactor,rightCornersArranged*scaleFactor, objPoints;



def mat2PyGetStereoFileNames(imageFileNamesLeft,imageFileNamesRight):
    leftFileNames  =  []
    rightFileNames  =  []
    for leftImageFileName,rightImageFileName in zip(imageFileNamesLeft[0],imageFileNamesRight[0]):
       leftFileNames.append(leftImageFileName[0])
       rightFileNames.append(rightImageFileName[0])

    return leftFileNames,rightFileNames;



def replaceNames(imageFileNames,replace,replaceWith):
    fileNames  =  []

    for fileName in imageFileNames:
       fileNames.append(fileName.replace(replace,replaceWith))

    return fileNames;



def mat2PyGetStereoMapping(horizontalSquares,verticalSquares,fileName,display,displayTime):
    horizontalInnerCorners = horizontalSquares-1
    verticalInnerCorners   = verticalSquares-1

    printLabel("Loading Stereo Vision Parametors From Matlab")
    leftAndRightParametors = loadmat(fileName)
    allImagePoints         = leftAndRightParametors['imagePoints']
    leftImagePoints        = leftAndRightParametors['leftImagePoints']
    rightImagePoints       = leftAndRightParametors['rightImagePoints']
    imageFileNamesLeft     = leftAndRightParametors['imageFileNames1']
    imageFileNamesRight    = leftAndRightParametors['imageFileNames2']




    printLabel("Defining 3D Object Points")
    objp        = np.zeros((horizontalInnerCorners*verticalInnerCorners, 3), np.float32)
    objp[:, :2] = np.mgrid[0:horizontalInnerCorners, 0:verticalInnerCorners].T.reshape(-1, 2)

    # Arrays to store object points and image points from all the images.
    printLabel("Defining World Points and Image Points")
    objPoints      = []  # 3d point in real world space


    printLabel("Gaining Corner Points from the Matlab Deployment")
    leftCorners,rightCorners, objPoints = mat2PyGetImageCornersStereo(\
                                                            leftImagePoints,\
                                                            rightImagePoints,\
                                                            objp,\
                                                            horizontalInnerCorners,\
                                                            verticalInnerCorners\
                                                            )


    printLabel("Gaining Stereo File Names from the Matlab Deployment")
    leftFileNames,rightFileNames = mat2PyGetStereoFileNames(imageFileNamesLeft,imageFileNamesRight)


    printLabel("Verification of Stereo Corners")
    displayCornerPointsStereo(leftCorners,rightCorners,leftFileNames,rightFileNames,\
                                            horizontalInnerCorners,verticalInnerCorners,\
                                            display,displayTime)

    printLabel("Gaining Image Size")
    imgSize = getImageSize(leftFileNames[0])

    printLabel("Calibrating Individual Cameras")
    retLeft, mtxLeft, distLeft, rvecsLeft, tvecsLeft      = cv2.calibrateCamera(\
                                                           objPoints, leftCorners, imgSize, None, None)
    print("Left Camera Calibrated")
    retRight, mtxRight, distRight, rvecsRight, tvecsRight = cv2.calibrateCamera(\
                                                           objPoints, rightCorners, imgSize, None, None)
    print("Right Camera Calibrated")


    printLabel("Calibrating Stereo Cameras")
    flags = 0
    flags |= cv2.CALIB_FIX_INTRINSIC
    # flags |= cv2.CALIB_FIX_PRINCIPAL_POINT
    flags |= cv2.CALIB_USE_INTRINSIC_GUESS
    flags |= cv2.CALIB_FIX_FOCAL_LENGTH
    # flags |= cv2.CALIB_FIX_ASPECT_RATIO
    flags |= cv2.CALIB_ZERO_TANGENT_DIST
    # flags |= cv2.CALIB_RATIONAL_MODEL
    # flags |= cv2.CALIB_SAME_FOCAL_LENGTH
    # flags |= cv2.CALIB_FIX_K3
    # flags |= cv2.CALIB_FIX_K4
    # flags |= cv2.CALIB_FIX_K5

    stereocalib_criteria = (cv2.TERM_CRITERIA_MAX_ITER +
                                    cv2.TERM_CRITERIA_EPS, 100, 1e-5)
    ret, M1, d1, M2, d2, R, T, E, F = cv2.stereoCalibrate(
                                            objPoints, \
                                            leftCorners,rightCorners,\
                                            mtxLeft, distLeft, \
                                            mtxLeft, distLeft, \
                                            imgSize,\
                                            criteria=stereocalib_criteria, flags=flags)

    printLabel("Starting Stereo Calibration ")
    R1, R2, P1, P2, Q, _, _        = cv2.stereoRectify(\
                                         mtxLeft, distLeft, \
                                            mtxLeft, distLeft, \
                                                imgSize,\
                                                    R,\
                                                        T, \
                                                            alpha=1)

    print("Stereo Calibration done")

    printLabel("Gaining Stereo Mapping")
    mapXLeft, mapYLeft = cv2.initUndistortRectifyMap(mtxLeft, \
                                                distLeft,\
                                                R1,\
                                                P1,\
                                                imgSize,
                                                cv2.CV_32F)
    mapXRight, mapYRight = cv2.initUndistortRectifyMap(mtxLeft, \
                                                distLeft,\
                                                R2,\
                                                P2,\
                                                imgSize,
                                                cv2.CV_32F)

    return leftFileNames,rightFileNames,mapXLeft,mapYLeft,mapXRight, mapYRight,\
                M1, d1, M2, d2, R1, R2, P1, P2, R, T, E, F, Q ;






def displayCornerPointsStereo(leftCorners,rightCorners,leftFileNames,rightFileNames,\
                                            horizontalInnerCorners,verticalInnerCorners,
                                                display,delayTimeMillis):
    subpix_criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.01)

    for leftCornersCurrent,leftFileNamesCurrent,rightCornersCurrent,rightFileNamesCurrent in \
                   zip(leftCorners,leftFileNames,rightCorners,rightFileNames):

       imgLeft  = cv2.imread(leftFileNamesCurrent)
       imgRight = cv2.imread(rightFileNamesCurrent)

       grayLeft   = cv2.cvtColor(imgLeft, cv2.COLOR_BGR2GRAY)
       grayRight   = cv2.cvtColor(imgRight, cv2.COLOR_BGR2GRAY)

       cv2.cornerSubPix(grayLeft, leftCornersCurrent, (3, 3), (-1, -1), subpix_criteria)
       cv2.drawChessboardCorners(imgLeft, (horizontalInnerCorners,verticalInnerCorners),\
               leftCornersCurrent, True)


       cv2.cornerSubPix(grayRight, rightCornersCurrent, (3, 3), (-1, -1), subpix_criteria)
       cv2.drawChessboardCorners(imgRight, (horizontalInnerCorners,verticalInnerCorners),\
               rightCornersCurrent, True)
       if(display):
           cv2.imshow("Left", imgLeft)
           cv2.imshow("Right", imgRight)
           cv2.waitKey(delayTimeMillis)

    cv2.destroyAllWindows()


def displayCornerPointsStereoScaled(leftCorners,rightCorners,leftFileNames,rightFileNames,\
                                            horizontalInnerCorners,verticalInnerCorners,
                                                delayTimeMillis,widthIn):
    subpix_criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.01)

    for leftCornersCurrent,leftFileNamesCurrent,rightCornersCurrent,rightFileNamesCurrent in \
                   zip(leftCorners,leftFileNames,rightCorners,rightFileNames):

       imgLeft  = cv2.imread(leftFileNamesCurrent)
       imgRight = cv2.imread(rightFileNamesCurrent)

       grayLeft   = cv2.cvtColor(imgLeft, cv2.COLOR_BGR2GRAY)
       grayRight   = cv2.cvtColor(imgRight, cv2.COLOR_BGR2GRAY)

       cv2.cornerSubPix(grayLeft, leftCornersCurrent, (3, 3), (-1, -1), subpix_criteria)
       cv2.drawChessboardCorners(imgLeft, (horizontalInnerCorners,verticalInnerCorners),\
               leftCornersCurrent, True)

       cv2.cornerSubPix(grayRight, rightCornersCurrent, (3, 3), (-1, -1), subpix_criteria)
       cv2.drawChessboardCorners(imgRight, (horizontalInnerCorners,verticalInnerCorners),\
                      rightCornersCurrent, True)

       cv2.imshow("Left", imutils.resize(imgLeft, width=widthIn))
       cv2.imshow("Right", imutils.resize(imgLeft, width=widthIn))
       cv2.waitKey(delayTimeMillis)

    cv2.destroyAllWindows()



def getImageSize(fileName):
    print("Gaining Image Size for '{}'".format(fileName))
    img  = cv2.imread(fileName)
    print("Image Width: {}, Image Height: {}".format(img.shape[1], img.shape[0]))
    return (img.shape[1], img.shape[0]);




def getStereoRectificationMaps(leftCorners,rightCorners,objPoints,imgSize):

    printLabel("Left Camera Calibrating")
    retLeft, mtxLeft, distLeft, rvecsLeft, tvecsLeft      = cv2.calibrateCamera(\
                                                           objPoints, leftCorners, imgSize, None, None)
    print("Left Camera Calibrated")

    printLabel("Right Camera Calibrating")
    retRight, mtxRight, distRight, rvecsRight, tvecsRight = cv2.calibrateCamera(\
                                                           objPoints, rightCorners, imgSize, None, None)
    print("Right Camera Calibrated")

    printLabel("Starting Stereo Calibration")

    flags = 0
    flags |= cv2.CALIB_FIX_INTRINSIC
    # flags |= cv2.CALIB_FIX_PRINCIPAL_POINT
    flags |= cv2.CALIB_USE_INTRINSIC_GUESS
    flags |= cv2.CALIB_FIX_FOCAL_LENGTH
    # flags |= cv2.CALIB_FIX_ASPECT_RATIO
    flags |= cv2.CALIB_ZERO_TANGENT_DIST
    # flags |= cv2.CALIB_RATIONAL_MODEL
    # flags |= cv2.CALIB_SAME_FOCAL_LENGTH
    # flags |= cv2.CALIB_FIX_K3
    # flags |= cv2.CALIB_FIX_K4
    # flags |= cv2.CALIB_FIX_K5

    stereocalib_criteria = (cv2.TERM_CRITERIA_MAX_ITER +
                                    cv2.TERM_CRITERIA_EPS, 100, 1e-5)
    ret, M1, d1, M2, d2, R, T, E, F = cv2.stereoCalibrate(
                                            objPoints, \
                                            leftCorners,rightCorners,\
                                            mtxLeft, distLeft, \
                                            mtxLeft, distLeft, \
                                            imgSize,\
                                            criteria=stereocalib_criteria, flags=flags)

    print("Stereo Calibration Done")

    printLabel("Gaining Rectification Parametors")
    R1, R2, P1, P2, Q, _, _        = cv2.stereoRectify(\
                                         mtxLeft, distLeft, \
                                            mtxLeft, distLeft, \
                                                imgSize,\
                                                    R,\
                                                        T, \
                                                            alpha=1)


    printLabel("Gaining Stereo Maps")
    mapXLeft, mapYLeft = cv2.initUndistortRectifyMap(mtxLeft, \
                                                distLeft,\
                                                R1,\
                                                P1,\
                                                imgSize,
                                                cv2.CV_32F)
    mapXRight, mapYRight = cv2.initUndistortRectifyMap(mtxLeft, \
                                                distLeft,\
                                                R2,\
                                                P2,\
                                                imgSize,
                                                cv2.CV_32F)

    return mapXLeft,mapYLeft,mapXRight,mapYRight;

def stereoTestMap(leftFile,rightFile,mapXLeft,mapYLeft,mapXRight,mapYRight,displayTime):
    printLabel("Displaying Test Image Mappings on '{}' and '{}'".format(leftFile,rightFile))
    imLeft          = cv2.imread(leftFile)
    imRight         = cv2.imread(rightFile)
    imLeftRemapped  = cv2.remap(imLeft,mapXLeft,mapYLeft,cv2.INTER_CUBIC)
    imRightRemapped = cv2.remap(imRight,mapXRight,mapYRight,cv2.INTER_CUBIC)

    cv2.imshow(leftFile+" remapped",imLeftRemapped)
    cv2.imshow(rightFile+" remapped",imRightRemapped)
    cv2.waitKey(displayTime)
    cv2.destroyAllWindows()
    return imLeftRemapped,imRightRemapped;


def getReverseMapping(mapX, mapY):
    assert(mapX.shape == mapY.shape)
    rows = mapX.shape[0]
    cols = mapX.shape[1]
    mX = np.ones(mapX.shape, dtype=mapX.dtype) * -1
    mY = np.ones(mapY.shape, dtype=mapY.dtype) * -1
    for i in range(rows):
        for j in range(cols):

            i_ = round(mapY[i, j])
            j_ = round(mapX[i, j])

            if 0 <= i_ < rows and 0 <= j_ < cols:
                mX[int(i_), int(j_)] = j
                mY[int(i_), int(j_)] = i
    return mX, mY

def stereoReverseTestMap(imLeftRemapped,imRightRemapped,\
                            mapXLeftReverse,mapYLeftReverse,\
                                mapXRightReverse,mapYRightReverse,\
                            displayTime):
    imLeftRemappedReverse  = cv2.remap(imLeftRemapped,mapXLeftReverse,mapYLeftReverse,cv2.INTER_CUBIC)
    imRightRemappedReverse = cv2.remap(imRightRemapped,mapXRightReverse,mapYRightReverse,cv2.INTER_CUBIC)

    cv2.imshow("Left Image Reversed"  ,imLeftRemappedReverse)
    cv2.imshow("Right Image Reversed" ,imRightRemappedReverse)
    cv2.waitKey(displayTime)
    cv2.destroyAllWindows()

# Thermal Camera Calibration
def mat2PyGetImageCornersThermal(thermalImagePoints,\
                                        horizontalInnerCorners,\
                                            verticalInnerCorners):

    printLabel("Reading Corner Points from Stereo Visualthe Thermal Camera")

    objp        = np.zeros((horizontalInnerCorners*verticalInnerCorners, 3), np.float32)
    objp[:, :2] = np.mgrid[0:horizontalInnerCorners, 0:verticalInnerCorners].T.reshape(-1, 2)


    objPoints         = []  # 3D point in real world space
    imgPointsthermal  = []  # 2D points in image plane.

    # Organizing Corner Points
    thermalImageCorners  = []

    for imageIndex in range(len(thermalImagePoints[0][0])):
        thermalImageCurrentCorners  = []
        objPoints.append(objp)

        for cornerIndex in range(len(thermalImagePoints)):

            thermalXCordCurrent= np.float32(thermalImagePoints[cornerIndex][0][imageIndex])
            thermalYCordCurrent= np.float32(thermalImagePoints[cornerIndex][1][imageIndex])
            thermalImageCurrentCorners.append([[thermalXCordCurrent,thermalYCordCurrent]])

        thermalImageCorners.append(thermalImageCurrentCorners)

    thermalCorners = np.array(thermalImageCorners)

    print("Rearanging Corners")
    thermalCornersArranged  = thermalCorners

    for imageIndex in range(len(thermalImagePoints[0][0])):

        for cornerIndex in range(len(thermalImagePoints)):

            arrangedIndex = horizontalInnerCorners*((cornerIndex)%verticalInnerCorners)\
                                + math.floor(cornerIndex/verticalInnerCorners)

            thermalCornersArranged[imageIndex][arrangedIndex]  = \
                                            thermalImageCorners[imageIndex][cornerIndex]

    return thermalCornersArranged,objPoints;



def mat2PyGetThermalFileNames(imageFileNames):
    fileNames  =  []
    for imageFileName in imageFileNames[0]:
        fileNames.append(imageFileName[0])
    return fileNames;


def displayCornerPointsThermal(thermalCorners,thermalFileNames,\
                                            horizontalInnerCorners,verticalInnerCorners,
                                                display,displayTime):
    subpix_criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.01)

    for thermalCornersCurrent,thermalFileNamesCurrent in \
            zip(thermalCorners,thermalFileNames):

        imgthermal    = cv2.imread(thermalFileNamesCurrent)
        graythermal   = cv2.cvtColor(imgthermal, cv2.COLOR_BGR2GRAY)

        cv2.cornerSubPix(graythermal, thermalCornersCurrent, (3, 3), (-1, -1), subpix_criteria)
        cv2.drawChessboardCorners(imgthermal, (horizontalInnerCorners,verticalInnerCorners),\
                    thermalCornersCurrent, True)
        if(display):
            cv2.imshow("Thermal", imgthermal)
            cv2.waitKey(displayTime)

    cv2.destroyAllWindows()







def mat2PyGetThermalMapping(horizontalSquares,\
                                    verticalSquares,\
                                        loadName,\
                                            display,delayTimeMillis):

    horizontalInnerCorners = horizontalSquares-1
    verticalInnerCorners   = verticalSquares-1

    thermalParametors = loadmat(loadName)

    printLabel("Loading Thermal Parametors From Matlab")

    thermalImagePoints        = thermalParametors['imagePoints']
    imageFileNamesThermal     = thermalParametors['imageFileNames']


    # Arrays to store object points and image points from all the images.
    # Organizing the file names
    printLabel("Gaining Corner Points from the Matlab Deployment")
    thermalCorners,objPoints =  mat2PyGetImageCornersThermal(thermalImagePoints,\
                                            horizontalInnerCorners,\
                                                verticalInnerCorners)



    printLabel("Gaining Thermal File Names from the Matlab Deployment")
    thermalFileNames = mat2PyGetThermalFileNames(imageFileNamesThermal)


    # Verification of Corner Points
    print("Verification of Thermal Corner Points")
    displayCornerPointsThermal(thermalCorners,thermalFileNames,\
                                                horizontalInnerCorners,verticalInnerCorners,
                                                    display,delayTimeMillis)

    printLabel("Gaining Image Size")
    imgSize = getImageSize(thermalFileNames[0])


    printLabel("Calibrating Thermal Camera")
    retThermal, mtxThermal, distThermal, rvecsThermal, tvecsThermal  = cv2.calibrateCamera(\
                                                            objPoints, thermalCorners, imgSize, None, None)
    print("Thermal Camera Calibrated")

    printLabel("Optimizing Thermal Camera Matrix")
    newCameraMtx, _    = cv2.getOptimalNewCameraMatrix(mtxThermal,distThermal, imgSize, 1)

    imThermal          = cv2.imread(thermalFileNames[0])
    newcameramtx, _    = cv2.getOptimalNewCameraMatrix(mtxThermal,distThermal, imgSize, 1)
    undistortedThermal = cv2.undistort(imThermal , mtxThermal,distThermal, None, newcameramtx)


    return thermalFileNames, thermalCorners,\
                mtxThermal, distThermal, rvecsThermal, tvecsThermal, \
                    newCameraMtx;


def thermalTestUndistort(imageFile,mtxThermal,distThermal,newcameramtx,displayTime):
    printLabel("Displaying Undistorted Image for '{}'".format(imageFile))
    imThermal          = cv2.imread(imageFile)
    undistortedThermal = cv2.undistort(imThermal, mtxThermal,distThermal, None, newcameramtx)
    cv2.imshow(imageFile+ " Original",imThermal)
    cv2.imshow(imageFile+ " Undistorted",undistortedThermal)
    cv2.waitKey(displayTime)
    cv2.destroyAllWindows()



def saveRectifiedForMatStereo(leftFileNames,rightFileNames,stereoParams):
    for leftFileNamesCurrent,rightFileNamesCurrent in \
                   zip(leftFileNames,rightFileNames):

        imLeft  = cv2.imread(leftFileNamesCurrent)
        imRight = cv2.imread(rightFileNamesCurrent)

        imLeftRemapped =cv2.remap(imLeft,stereoParams['mapXLeft'],\
                                            stereoParams['mapYLeft'],\
                                                cv2.INTER_CUBIC)

        imRightRemapped=cv2.remap(imRight,stereoParams['mapXRight'],\
                                            stereoParams['mapYRight'],
                                                cv2.INTER_CUBIC)

        newLeft  = leftFileNamesCurrent.replace("Resized", "ResizedRectified")
        newRight = rightFileNamesCurrent.replace("Resized", "ResizedRectified")

        print("Writing Rectified Left  Image of '{}' as '{}'".format(leftFileNamesCurrent,newRight))
        cv2.imwrite(newLeft,    imLeftRemapped);
        print("Writing Rectified Right Image of '{}' as '{}'".format(rightFileNamesCurrent,newRight))
        cv2.imwrite(newRight,   imRightRemapped);


def saveUndistortedForMatThermal(thermalFileNames,thermalParams):
    for thermalFileNamesCurrent in thermalFileNames:

        imThermal  = cv2.imread(thermalFileNamesCurrent)

        imThermalRemapped = cv2.undistort(\
                                    imThermal,\
                                    thermalParams['mtxThermal'],\
                                    thermalParams['distThermal']
                                    , None,\
                                    thermalParams['newcameramtx']\
                                    )

        newThermal  = thermalFileNamesCurrent.replace("thermal", "thermaUndistorted")

        print("Writing Rectified Thermal  Image of '{}' as '{}'".format(thermalFileNamesCurrent,newThermal))
        # cv2.imwrite(newThermal,    imThermalRemapped);


def getReplacedFileNames(leftFileNames,replace,replaceWith):
    thermalFileNames = []
    for leftFileName in leftFileNames:
        thermalFileNames.append(leftFileName.replace(replace,replaceWith))
    return thermalFileNames;

def getHomogrpahyParams(cornersLeft,cornersThermal):
    homographyAll = []
    for leftCornerNow,thermalCornerNow,homographyIndex in zip (cornersLeft,cornersThermal,range(len(cornersLeft))):
        homographyAll.append(cv2.findHomography(thermalCornerNow,\
                                                                    leftCornerNow,\
                                                                      cv2.RANSAC, 4)[0])
    return homographyAll;

def displayOverlayImages(fileNamesLeft,fileNamesThermal,\
                            homographyAll,displayTime):

    for currentImageIndex in range(len(fileNamesLeft)):
        print("Overlaying {} on {}".format(fileNamesThermal[currentImageIndex],\
                                                fileNamesLeft[currentImageIndex]))
        imLeft    = cv2.imread(fileNamesLeft[currentImageIndex])
        imThermal = cv2.imread(fileNamesThermal[currentImageIndex])
        rows,cols,ch = imLeft.shape
        thermalOverlay   = cv2.warpPerspective(imThermal,\
                                homographyAll[currentImageIndex],(cols,rows))
        alpha = 0.2
        beta = (1.0 - alpha)

        mergedHomographyLocal = cv2.addWeighted(imLeft,alpha,thermalOverlay, beta, 0.0)
        cv2.imshow("Left" ,imLeft )
        cv2.imshow("Thermal" ,imThermal)
        cv2.imshow("Homography" , mergedHomographyLocal)
        cv2.waitKey(displayTime)
    cv2.destroyAllWindows()

def getDistanceParamsMat2Py(loadName2,numOfHomographies):
    distanceParamsMat            = loadmat(loadName2)
    fitA                         = distanceParamsMat['a'][0][0]
    fitB                         = distanceParamsMat['b'][0][0]
    cutOffsPre                   = distanceParamsMat['cutOffs'][0]
    distancesCM                  = distanceParamsMat['actualDistances'][0]
    cutOffs = []
    for indexIn in range(numOfHomographies-1):
        cutOffs.append([cutOffsPre[indexIn],cutOffsPre[indexIn+1]])
    cutOffs.append([cutOffsPre[indexIn+1],np.inf])
    return fitA, fitB, cutOffs, distancesCM.tolist();


def mat2PyGetCornerPointsMono(imagePoints,\
                                fileNamesIn,\
                                    horizontalSquares,\
                                        verticalSquares):

    horizontalInnerCorners = horizontalSquares-1
    verticalInnerCorners   = verticalSquares-1

    print("Organizing Corner Points")
    imageCorners  = []
    fileNames  =  []


    for imageIndex in range(len(imagePoints[0][0])):
        imageCurrentCorners  = []

        for cornerIndex in range(len(imagePoints)):

            XCordCurrent= np.float32(imagePoints[cornerIndex][0][imageIndex])
            YCordCurrent= np.float32(imagePoints[cornerIndex][1][imageIndex])
            imageCurrentCorners.append([[XCordCurrent,YCordCurrent]])

        imageCorners.append(imageCurrentCorners)

    corners = np.array(imageCorners)

    print("Rearanging Corners for Python")
    cornersArranged  = corners

    for imageIndex in range(len(imagePoints[0][0])):

        for cornerIndex in range(len(imagePoints)):

            arrangedIndex = horizontalInnerCorners*((cornerIndex)%verticalInnerCorners)\
                                + math.floor(cornerIndex/verticalInnerCorners)

            cornersArranged[imageIndex][arrangedIndex]  = \
                                            imageCorners[imageIndex][cornerIndex]

    # Organizing the file names
    print("Organizing File Names")
    for imageFileName in fileNamesIn[0]:
        fileNames.append(imageFileName[0])

    return cornersArranged,fileNames;

def printLabel(inputString):
    print(" ")
    print("------------------------------------------")
    print(inputString)

def printMINTS(inputString):
    print(" ")
    print("============== MINTS {} ==============".format(inputString))
    print(" ")
