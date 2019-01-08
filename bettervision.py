# Import the camera server
from cscore import CameraServer

# Import OpenCV and NumPy
import cv2 as cv
import numpy as np

def main():
    cs = CameraServer.getInstance()
    cs.enableLogging()
    
    # Capture from the first USB Camera on the system
    camera = cs.startAutomaticCapture()
    camera.setResolution(320, 240)

    # Get a CvSink. This will capture images from the camera
    cvSink = cs.getVideo()

    # (optional) Setup a CvSource. This will send images back to the Dashboard
    outputStream = cs.putVideo("Name", 320, 240)

    # Allocating new images is very expensive, always try to preallocate
    img = np.zeros(shape=(240, 320, 3), dtype=np.uint8)
  
    while True:
        # Tell the CvSink to grab a frame from the camera and put it
        # in the source image.  If there is an error notify the output.
        time, img = cvSink.grabFrame(img)
        if time == 0:
            # Send the output the error.
            outputStream.notifyError(cvSink.getError());
            # skip the rest of the current iteration
            continue
        img2, contours, hierarchy = cv.findContours(img,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            cv.drawContours(img, [contour], 0, (255, 0, 255), 3)
            contourArea = cv.contourArea(contour)
            #minArea and maxArea filters for contours
            if contourArea < minArea or contourArea > maxArea:
                continue

            #The last test we will cover is solidity. 
            #That is, the ratio between the contour area and the bounding rectangle area. 
            #This is useful to determine the “rectangle-ness” of the contour. 
            #The more closely the bounding rectangle fits the contours, the closer this ratio will be to 1.
            x,y,w,h = cv.boundingRect(contour)
            ratio = cv.contourArea(contour)/(w*h)

            moments = cv.moments(contour)
            centerX = int(moments['m10']/moments['m00'])
            centerY = int(moments['m01']/moments['m00'])


        # (optional) send some image back to the dashboard
        outputStream.putFrame(img)