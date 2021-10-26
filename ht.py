
import cv2
import mediapipe as mp
import time

mphands=mp.solutions.hands
hands = mphands.Hands()
mpdraw = mp.solutions.drawing_utils
webcam = cv2.VideoCapture(0)
while True:
    successfull, img=webcam.read()
    imgrgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgrgb)
    #print(results.multi_hand_landmarks)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c=img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                print(id, cx, cy)
                if id == 8:
                    cv2.circle(img, (cx,cy), 10, (221, 56, 230), cv2.FILLED)
            mpdraw.draw_landmarks(img, handLms, mphands.HAND_CONNECTIONS)
    cv2.imshow('Hand Tracking', img)
    key=cv2.waitKey(1)
    if key==81 or key==113:
        break
webcam.release()