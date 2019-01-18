import cv2

def Setup(camera : cv2.VideoCapture):
    '''Automatically set up the camera feed to use the proper contrast exposure and saturation'''
    contrast = 30
    exposure = -7
    saturation = 100

    camera.set(cv2.CAP_PROP_CONTRAST, contrast)
    camera.set(cv2.CAP_PROP_EXPOSURE, exposure)
    camera.set(cv2.CAP_PROP_SATURATION, saturation)