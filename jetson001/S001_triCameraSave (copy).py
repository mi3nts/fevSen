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


cr.printMINTS("fevSen")

cr.printLabel("Logging Inputs")

highResolution = True
imageSave      = True
display        = True

directory = "/home/pyimagesearch/mintsData/jetson001/"
width     = 2592
height    = 1944
frameRate = 15

# For Low Resolution
if not highResolution:
    width     = 640
    height    = 480
    frameRate = 30

cr.printLabel("Assigning Queues:")
qThermal  = Queue(maxsize = 5)

print("High Resolution: {}, Image Saving: {}, Display: {}".format(highResolution,imageSave,display))


cr.printLabel("Script Parametors:")
print("High Resolution: {}, Image Saving: {}, Display: {}".format(highResolution,imageSave,display))

cr.printLabel("Local Directory: {} Assigned".format(directory))

cr.printLabel("Visual Camera Parametors:")
print("Height: {}, Width: {}, Frame Rate: {}".format(height,width,frameRate))

cr.printLabel("Gaining Camera Indexes")
myCmd = os.popen('v4l2-ctl --list-devices').read()
leftCamIndex   = cr.getLeftWebCamIndex(myCmd)[1]
rightCamIndex  = cr.getRightWebCamIndex(myCmd)[1]
print("Left Camera Index: {}".format(leftCamIndex))
print("Right Camera Index: {}".format(rightCamIndex))

cr.printLabel("Initiating Visual Cameras with Maximum Resolution")
capLeft  =  cr.openWebCamMPGJ(leftCamIndex, width, height,frameRate)
capRight =  cr.openWebCamMPGJ(rightCamIndex, width, height,frameRate)

cr.printLabel("Creating Sub Directories")
cr.folderCheck(directory+"left")
cr.folderCheck(directory+"right")
cr.folderCheck(directory+"thermal")

cr.printLabel("Initiating Thermal Buffer")
BUF_SIZE = 2
q = Queue(BUF_SIZE)

cr.printLabel("Visual Camera Check")

if not capLeft.isOpened() :
        print('Left Camera Stream Not opened')
        exit(0)
else:
    print("Left Camera Stream Open")

if not capRight.isOpened()  :
        print('Right Camera Stream Not Open')
        exit(0)
else:
    print("Right Camera Stream Open")

cr.printLabel("Entering Main function")

def main():

    cr.printLabel("Initiating Thermal Camera")
    ctx  = POINTER(uvc_context)()
    dev  = POINTER(uvc_device)()
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

            cr.printLabel("Thermal Camera Initiated")
            cr.printLabel("Thermal Camera Properties:")
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

            try:
                startTime = time.time()
                cr.printLabel("Initiating Checks")
                for n in range(10):
                    print("Check: " + str(n+1))
                    q.get(True, 500)
                    retLeft, frameLeft     = capLeft.read()
                    retRight,frameRight    = capRight.read()
                    if not retLeft:
                        print('Empty Left frame')
                    if not retRight:
                        print('Empty Right frame')

                cr.printLabel("Entering While Loop")
                while True:
                    dateTime          = datetime.datetime.now()
                    thermalData       = q.get(True, 500)
                    retLeft, left     = capLeft.read()
                    retRight,right    = capRight.read()

                    if not retLeft:
                        print('Empty Left frame')
                    if not retRight:
                        print('Empty Right frame')

                    qThermal.put(cr.thermalRawConvert(thermalData))

                    if(qThermal.full()):
                        print(dateTime)
                        thermal = qThermal.get()
                        if(imageSave):
                            leftImageName      = directory + cr.getImagePathTail(dateTime,'left')
                            rightImageName     = directory + cr.getImagePathTail(dateTime,'right')
                            thermalImageName   = directory + cr.getImagePathTail(dateTime,'thermal')

                            cv2.imwrite(leftImageName,left )
                            cv2.imwrite(rightImageName,right)
                            cv2.imwrite(thermalImageName,thermal)

                        if(display):
                            cv2.imshow('Left Frame' , imutils.resize(left, width=640))
                            cv2.imshow('Right Frame', imutils.resize(right, width=640))
                            cv2.imshow('Thermal Frame', imutils.resize(thermal, width=640))
                    else:
                        print("Thermal Queue not full")
                        print("Thermal Queue Size: {}".format(qThermal.qsize()))
                    #



                    if cv2.waitKey(1)&0xFF == ord('q'):
                        break

            finally:
                libuvc.uvc_stop_streaming(devh)


            capLeft.release()
            capRight.release()
            cv2.destroyAllWindows()
            cr.printLabel("MINTS done")

        finally:
            libuvc.uvc_unref_device(dev)
    finally:
        libuvc.uvc_exit(ctx)




    cr.printMINTS("fevSen")



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


if __name__ == '__main__':
  main()
