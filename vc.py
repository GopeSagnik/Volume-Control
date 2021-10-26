
import cv2
import time
import numpy as np
import math
import HandTrackingMod as htm
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


wcam, hcam = 1080, 720



devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange=volume.GetVolumeRange()

vol=0
volbar=50
volper=100

minvol = volRange[0]
maxvol= volRange[1]

webcam = cv2.VideoCapture(0)
webcam.set(3, wcam)
webcam.set(4, hcam)

detector = htm.handDetector(maxHands=1)
while True:
    success, img = webcam.read()   
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList)!=0:
        #print(lmList[4], lmList[8])

        x1, y1= lmList[4][1],lmList[4][2]
        x2, y2 =lmList[8][1], lmList[8][2]
        cx, cy=(x1+x2)//2, (y1+y2)//2
        cv2.circle(img, (x1, y1), 10, (255,0,255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255,0,255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2,y2), (255,0,255),2)
        cv2.circle(img, (cx,cy),8, (255,0,255), cv2.FILLED)
        length = math.hypot(x2-x1, y2-y1)
        print(length) 
        # hand range is 17 - 105
        #vol raneg is -45 - 0
        vol = np.interp(length, [17, 105], [minvol, maxvol])
        volbar = np.interp(length, [17, 105], [400, 150])
        volper = np.interp(length, [17,105], [0,100])
        #print(vol)
        volume.SetMasterVolumeLevel(vol, None)

        if length<21:
            cv2.circle(img, (cx,cy),8, (255,0,0), cv2.FILLED)

    cv2.rectangle(img, (50,150), (85,400), (0,255,0),3)
    cv2.rectangle(img, (50,int(volbar)), (85,400), (0,255,0),cv2.FILLED)
    cv2.putText(img, f'{int(volper)}%', (40,450), cv2.FONT_ITALIC, 1, (255,0,255), 3)
    
    cv2.imshow('Volume Control by Hand... press \'q\' to close', img)
    key=cv2.waitKey(1)
    if key==81 or key==113:
        break
webcam.release()
