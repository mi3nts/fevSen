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

imageSave      = True
display        = False

directory = "/home/pyimagesearch/mintsData/jetson001/"


cr.printLabel("Local Directory: {} Assigned".format(directory))


cr.printLabel("Creating Sub Directories")
cr.folderCheck(directory+"thermal")

cr.printLabel("Initiating Thermal Buffer")
BUF_SIZE = 2
q = Queue(BUF_SIZE)


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
                cr.printLabel("Initiating Checks")
                for n in range(10):
                    print("Check: " + str(n+1))
                    q.get(True, 500)

                cr.printLabel("Entering While Loop")
                while True:
                    dateTime          = datetime.datetime.now()
                    thermal           = q.get(True, 500)
     
                  
                    if(imageSave):
                        imageName   = directory + cr.getImagePathTailHdf5(dateTime,'thermal')
                        print("Saving: {}".format(imageName))
                        hf = h5py.File(imageName, 'w')
                        hf.create_dataset('thermal', data=thermal)
                        hf.close()


                    if(display):
                        cv2.imshow('Thermal', cr.thermalRawConvert(thermal))

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
