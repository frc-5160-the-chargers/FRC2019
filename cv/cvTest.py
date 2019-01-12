import grip
import camSetup
import cv2

camera = cv2.VideoCapture(1)

camSetup.Setup(camera)

gripPipeline = grip.GripPipeline()

while True:
    ret, frame = camera.read()

    contours = gripPipeline.process(frame)
    cv2.drawContours(frame, contours, 0, (0, 255, 0), 3)

    cv2.imshow("test", frame)
    if not ret:
        break
    k = cv2.waitKey(1)

    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        contours = gripPipeline.process(frame)
        print(len(contours))


cv2.destroyAllWindows()

camera.release()