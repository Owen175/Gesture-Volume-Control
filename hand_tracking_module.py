import cv2
import time
import mediapipe as mp
import pyautogui
import mouse

#def moveMouse(screen_width, screen_height, lm):
#    mouse.move(lm.x*screen_width, lm.y*screen_height)

class handDetector:
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.fingerPos = None

        self.mpHands = mp.solutions.hands
        self.hands = mp.solutions.hands.Hands(static_image_mode=self.mode, max_num_hands=self.maxHands, min_detection_confidence=self.detectionCon, min_tracking_confidence=self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True, finger=8):
        img = cv2.flip(img, 1)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)


        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                self.mpHands.HAND_CONNECTIONS)
            self.fingerPos = handLms.landmark[finger]
        return img


    def findPosition(self, img, handNo=0, draw=True, indexes=[], numberPoints=False):
        lmList = []
        indexPosList = []
        h, w, c = img.shape
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for index in indexes:
                indexPosList.append([myHand.landmark[index].x*w, myHand.landmark[index].y*h])
            for id, lm in enumerate(myHand.landmark):
                cx, cy = int(lm.x*w), int(lm.y*h)
                lmList.append([id,cx,cy])
                if numberPoints:
                    cv2.putText(img, f'{str(id)}', (cx, cy),
                            cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 3)
                if draw:
                    cv2.circle(img,(cx, cy), 15, (255,0,255), cv2.FILLED)
        if indexes:
            return lmList, indexPosList
        return lmList



def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    #success, img = cap.read()
    index = 8
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=False)
        if len(lmList) > index:
            print(lmList[index])

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime


        cv2.putText(img, str(int(fps)), (10,70),
                cv2.FONT_HERSHEY_PLAIN,3,(0,0,0),3)

        cv2.imshow('Image', img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
