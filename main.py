#Video
import cv2
import time
import mediapipe as mp
from math import hypot
#Audio
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER
import numpy as np 


def VolumeControl(length, volume_interface):
    if volume_interface:
        volMin, volMax, _ = volume_interface.GetVolumeRange()
        vol = max(0.0, min(1.0, length / 100))  
        volume_interface.SetMasterVolumeLevelScalar(vol, None)
        time.sleep(0.3)



def HandTracking(volume_interface):
    cap = cv2.VideoCapture(0)
    pTime = 0

    mpHands = mp.solutions.hands
    hands = mpHands.Hands(static_image_mode=False, max_num_hands=2)
    mpDraw = mp.solutions.drawing_utils

    print("Listening for Input")

    while True:
        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        result = hands.process(imgRGB)

        lmList = []
        
        if result.multi_hand_landmarks:
            number_hands = len(result.multi_hand_landmarks)
            for handLms in result.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([id, cx, cy]) 
                    #cv2.circle(img, (cx, cy), 3, (255, 0, 255), cv2.FILLED)

                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

                if lmList != []:
                    x1, y1 = lmList[4][1], lmList[4][2]
                    x2, y2 = lmList[8][1], lmList[8][2]

                    #cv2.circle(img, (x1, y1), 15, (255, 0, 0), cv2.FILLED)  
                    #cv2.circle(img, (x2, y2), 15, (255, 0, 0), cv2.FILLED)
                    #cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)

                    length1 = hypot(x2 - x1, y2 - y1)
                    VolumeControl(length1, volume)


        cTime = time.time()
        #fps = 1 / (cTime - pTime)
        #pTime = cTime
        #cv2.putText(img, f'FPS:{int(fps)}', (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        #cv2.imshow("Video", img)

        if cv2.waitKey(1) & 0xff == ord("q"):
            break


devices = AudioUtilities.GetSpeakers()
if not devices:
    print("No audio devices found")
else:
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    HandTracking(volume)
