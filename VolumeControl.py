import hand_tracking_module as htm
import cv2
import time
import math
import pycaw
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np


pTime = 0
cTime = 0
cap = cv2.VideoCapture(0)
detector = htm.handDetector()
#success, img = cap.read()
index = 8

distance = 50.0

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
minVol = volume.GetVolumeRange()[0]
maxVol = volume.GetVolumeRange()[1]

while True:
    success, img = cap.read()
    img = detector.findHands(img, draw=False)
    lmList, indexPosList = detector.findPosition(img, draw=False, indexes=[4,8])

    if indexPosList:
        xDistance = indexPosList[0][0] - indexPosList[1][0]
        yDistance = indexPosList[0][1] - indexPosList[1][1]

        distance = math.sqrt(xDistance**2 + yDistance**2)

    vol = np.interp(distance, [10,120], [minVol, maxVol])
    #print(distance)
    volume.SetMasterVolumeLevel(vol, None)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime


    cv2.putText(img, str(int(fps)), (10,70),
            cv2.FONT_HERSHEY_PLAIN,3,(0,0,0),3)

    cv2.imshow('Image', img)
    cv2.waitKey(1)