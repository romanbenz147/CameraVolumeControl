import cv2
import os
import time
import mediapipe as mp

from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

volume = cast(interface, POINTER(IAudioEndpointVolume))

current_volume_level = volume.GetMasterVolumeLevelScalar()
volume_step = 0.05

def increase_volume():
    global current_volume_level
    current_volume_level = min(current_volume_level + volume_step, 1.0)
    volume.SetMasterVolumeLevelScalar(current_volume_level, None)

def decrease_volume():
    global current_volume_level
    current_volume_level = max(current_volume_level - volume_step, 0.0)
    volume.SetMasterVolumeLevelScalar(current_volume_level, None)

    
    

def HandTracking():
    cap = cv2.VideoCapture(0)
    pTime = 0

    mpHands = mp.solutions.hands
    hands = mpHands.Hands(static_image_mode=False, max_num_hands=2)
    mpDraw = mp.solutions.drawing_utils

    while True:
        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        result = hands.process(imgRGB)
        
        if result.multi_hand_landmarks:
            number_hands = len(result.multi_hand_landmarks)
            print(number_hands)
            for handLms in result.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    cv2.circle(img, (cx, cy), 3, (255, 0, 255), cv2.FILLED)

                    mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)


        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, f'FPS:{int(fps)}', (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Test", img)

        cv2.waitKey(1)


HandTracking()
