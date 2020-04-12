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



def py_frame_callback(frame, userptr):

  array_pointer = cast(frame.contents.data, POINTER(c_uint16 * (frame.contents.width * frame.contents.height)))
  data = np.frombuffer(
    array_pointer.contents, dtype=np.dtype(np.uint16)
  ).reshape(
    frame.contents.height, frame.contents.width
  ) # no copy

  # data = np.fromiter(
  #   frame.contents.data, dtype=np.dtype(np.uint8), count=frame.contents.data_bytes
  # ).reshape(
  #   frame.contents.height, frame.contents.width, 2
  # ) # copy

  if frame.contents.data_bytes != (2 * frame.contents.width * frame.contents.height):
    return

  if not q.full():
    q.put(data)

PTR_PY_FRAME_CALLBACK = CFUNCTYPE(None, POINTER(uvc_frame), c_void_p)(py_frame_callback)

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
        if "2.3" in name:
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
    "_" +str(dateTime.microsecond).zfill(6)+ \
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

def update(i):


    dateTime = datetime.datetime.now()
    thermalCelcius=[]
    leftImage=[]
    rightImage = []

    thermalDataPre = q.get(True, 500)
    retLeft, leftImage = capLeft.read()
    retRight, rightImage = capRight.read()

    thermalData   = cv2.resize(thermalDataPre[:,:], (640, 480))
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

            #
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
        maskCelcliusAll.append(maskCelclius)
        celciusImage          = cv2.warpPerspective(frameCelciusRect,\
                                                                 homographyAll[indexIn],\
                                                                  (cols,rows))
        celciusImageAll.append(celciusImage)
        maskedCelciusImage    = np.multiply(maskCelclius,celciusImage)
        maskedCelciusImageAll.append(maskedCelciusImage)
        finalCelciusImage = finalCelciusImage + maskedCelciusImage

    distanceImageF = cv2.remap(distanceImage ,stereoParams['mapXLeftReverse'],\
                                            stereoParams['mapYLeftReverse'],\
                                                    cv2.INTER_CUBIC)
    finalCelciusImageF = cv2.remap(finalCelciusImage ,stereoParams['mapXLeftReverse'],\
                                        stereoParams['mapYLeftReverse'],\
                                                cv2.INTER_CUBIC)


    threeWayImageName     = "threeWayImageDataSets/"+ getImagePathTailHdf5(dateTime,'hdf5ThreeWay')

    im1.set_data(cv2.cvtColor(leftImage, cv2.COLOR_BGR2RGB))
    im2.set_data(cv2.cvtColor(rightImage, cv2.COLOR_BGR2RGB))
    im3.set_data(distanceImageF)
    im4.set_data(finalCelciusImageF *7)

    # hf = h5py.File(threeWayImageName, 'w')
    #
    # hf.create_dataset('left' , data=leftImage)
    # hf.create_dataset('celcius', data=finalCelciusImageF)
    # hf.create_dataset('distance', data=distanceImageF)
    # hf.close()



myCmd = os.popen('v4l2-ctl --list-devices').read()

leftCamIndex  = getLeftWebCamIndex(myCmd)[1]
rightCamIndex  = getRightWebCamIndex(myCmd)[1]



#Initiate the two cameras
capLeft       = cv2.VideoCapture(0)
capRight      = cv2.VideoCapture(2)


BUF_SIZE = 2
q = Queue(BUF_SIZE)




# cv2.destroyAllWindows()

ax1 = plt.subplot(2,2,1)
plt.title("Left Image")

ax2 = plt.subplot(2,2,2)
plt.title("Right Image")

ax3 = plt.subplot(2,2,3)
plt.title("Depth Image")

ax4 =plt.subplot(2,2,4)
plt.title("Thermal Image")

#create two image plots
im1 = ax1.imshow(grab_frame(capLeft))
im2 = ax2.imshow(grab_frame(capRight))
im3 = ax3.imshow(grab_frame(capLeft))
im4 = ax4.imshow(grab_frame(capRight))

# Loading Parametors
stereoParams  = pickle.load(open("stereoParams_Feb_25_2020.p", "rb"))
thermalParams = pickle.load(open("thermalParams_Feb_12_2020.p", "rb"))
overlayParams = pickle.load(open("overlayParams_Feb_20_2020.p", "rb"))

cutOffs       = overlayParams['cutOffs ']
homographyAll = overlayParams['homographyAll']

print("Loading Disparity Parametors ")

a = 30590
b= -0.9453

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
  ctx = POINTER(uvc_context)()
  dev = POINTER(uvc_device)()
  devh = POINTER(uvc_device_handle)()
  ctrl = uvc_stream_ctrl()

  res = libuvc.uvc_init(byref(ctx), 0)
  if res < 0:
    print("uvc_init error")
    exit(1)

  try:
    res = libuvc.uvc_find_device(ctx, byref(dev), PT_USB_VID, PT_USB_PID, 0)
    if res < 0:
      print("uvc_find_device error")
      exit(1)

    try:
      res = libuvc.uvc_open(dev, byref(devh))
      if res < 0:
        print("uvc_open error")
        exit(1)

      print("device opened!")

      print_device_info(devh)
      print_device_formats(devh)

      frame_formats = uvc_get_frame_formats_by_guid(devh, VS_FMT_GUID_Y16)
      if len(frame_formats) == 0:
        print("device does not support Y16")
        exit(1)

      libuvc.uvc_get_stream_ctrl_format_size(devh, byref(ctrl), UVC_FRAME_FORMAT_Y16,
        frame_formats[0].wWidth, frame_formats[0].wHeight, int(1e7 / frame_formats[0].dwDefaultFrameInterval)
      )

      res = libuvc.uvc_start_streaming(devh, byref(ctrl), PTR_PY_FRAME_CALLBACK, None, 0)
      if res <0:
        print("uvc_start_streaming failed: {0}".format(res))
        exit(1)


      myCmd = os.popen('v4l2-ctl --list-devices').read()

      leftCamIndex  = getLeftWebCamIndex(myCmd)[1]
      rightCamIndex  = getRightWebCamIndex(myCmd)[1]

      try:
        startTime = time.time()
        # your code
        ani = FuncAnimation(plt.gcf(), update, interval=300)
        plt.show()
        capLeft.release()
        capRight.release()

        cv2.destroyAllWindows()
      finally:
        libuvc.uvc_stop_streaming(devh)

      print("done")
    finally:
      libuvc.uvc_unref_device(dev)
  finally:
    libuvc.uvc_exit(ctx)

if __name__ == '__main__':
  main()
