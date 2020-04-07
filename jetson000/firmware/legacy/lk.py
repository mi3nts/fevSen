import numpy as np
import cv2
import time


    

# cap1 = cv2.VideoCapture(3)
# cap1.set(3, 640)
# cap1.set(4, 480)

# time.sleep(2)
# cap2 = cv2.VideoCapture(4)
# cap1.set(3, 640)
# cap1.set(4, 480)


def open_cam_usb(dev, width, height):
    # We want to set width and height here, otherwise we could just do:
    #     return cv2.VideoCapture(dev)
    gst_str = ('v4l2src device=/dev/video{} ! '
               'video/x-raw, width=(int){}, height=(int){} ! '
               'videoconvert ! appsink').format(dev, width, height)
    return cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)

cap1 = open_cam_usb(3,640,480)
cap2 = open_cam_usb(4,640,480)

while(True):
    # Capture frame-by-frame
    # try:
        ret, frame1 = cap1.read()
        ret, frame2 = cap2.read()

        # Our operations on the frame come here
        
        # Display the resulting frame
        cv2.imshow('frame1',frame1)
        cv2.imshow('frame2',frame2)

        # cv2.imwrite('lk1.png', frame1)
        # cv2.imwrite('lk2.png', frame2)
    # except:
    #     print("SOS")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()