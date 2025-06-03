"""import cv2
import numpy as np
import pyvirtualcam

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

cap = cv2.VideoCapture(0)

with pyvirtualcam.Camera(width=640, height=480, fps=120) as virtual_cam:
    print("Virtual camera started!")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            #frame[y:y + h, x:x + w] = (0, 0, 0)
            frame[y:y+h, x:x+w] = cv2.blur(frame[y:y+h, x:x+w], (50, 50))


        virtual_cam.send(frame)

        cv2.imshow("Virtual Camera", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()"""
"""import cv2
import numpy as np
import pyvirtualcam

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

smiley = cv2.imread("vopros.png", cv2.IMREAD_UNCHANGED)

if smiley.shape[2] == 3:
    smiley = cv2.cvtColor(smiley, cv2.COLOR_BGR2BGRA)
    smiley[:, :, 3] = 255

def overlay_smiley(frame, x, y, w, h):
    smiley_resized = cv2.resize(smiley, (w, h))

    for c in range(0, 3):
        frame[y:y+h, x:x+w, c] = smiley_resized[:, :, c] * (smiley_resized[:, :, 3] / 255.0) + \
                                  frame[y:y+h, x:x+w, c] * (1.0 - smiley_resized[:, :, 3] / 255.0)

cap = cv2.VideoCapture(0)

with pyvirtualcam.Camera(width=640, height=480, fps=20) as virtual_cam:
    print("Virtual camera started!")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            overlay_smiley(frame, x, y, w, h)

        virtual_cam.send(frame)

        cv2.imshow("Virtual Camera", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()"""
import cv2
import numpy as np
import pyvirtualcam

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

smiley = cv2.imread("vopros.png", cv2.IMREAD_UNCHANGED)

if smiley.shape[2] == 3:
    smiley = cv2.cvtColor(smiley, cv2.COLOR_BGR2BGRA)
    smiley[:, :, 3] = 255

def overlay_smiley(frame, x, y, w, h):
    smiley_resized = cv2.resize(smiley, (w, h))

    for c in range(0, 3):        frame[y:y+h, x:x+w, c] = smiley_resized[:, :, c] * (smiley_resized[:, :, 3] / 255.0) + \
                                  frame[y:y+h, x:x+w, c] * (1.0 - smiley_resized[:, :, 3] / 255.0)

cap = cv2.VideoCapture(0)

with pyvirtualcam.Camera(width=640, height=480, fps=20) as virtual_cam:
    print("Virtual camera started!")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            overlay_smiley(frame, x, y, w, h)

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        virtual_cam.send(frame_rgb)

        cv2.imshow("Virtual Camera", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
