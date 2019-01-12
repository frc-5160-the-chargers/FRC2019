import cv2
import time

camera = cv2.VideoCapture(1)

print(camera.get(cv2.CAP_PROP_FPS))

running = False

c = 30
e = -7
s = 100


camera.set(cv2.CAP_PROP_CONTRAST, c)
camera.set(cv2.CAP_PROP_EXPOSURE, e)
camera.set(cv2.CAP_PROP_SATURATION, s)

while running:
    # (ok_flag, img) = camera.read()
    
    # cv2.imshow("CallingCamera View", img)
    
    # x = cv2.waitKey(0) 
    x = 0
    if x == ord(' '):
        running = False

    time.sleep(0.1)

    camera.set(cv2.CAP_PROP_CONTRAST, c)
    camera.set(cv2.CAP_PROP_EXPOSURE, e)
    camera.set(cv2.CAP_PROP_SATURATION, s)
    
#    c -= 1
#    e -= 1
    #s += 0.1
    
    print("Contrast {}, Saturation {}, Exposure {}".format(c, s, e))

cv2.destroyAllWindows()