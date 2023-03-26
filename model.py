import cv2
import mediapipe as mp
import math
import numpy as np


class HandDetector:
    def __init__(
        self, mode=False, max_hands=2, modelcomplexity=1, detectioncon=0.5, trackcon=0.5
    ):
        self.mode = mode
        self.max_hands = max_hands
        self.detectioncon = detectioncon
        self.trackcon = trackcon
        self.modelcomplex = modelcomplexity

        self.mphands = mp.solutions.hands
        self.hands = self.mphands.Hands(
            self.mode,
            self.max_hands,
            self.modelcomplex,
            self.detectioncon,
            self.trackcon,
        )
        self.mpdraw = mp.solutions.drawing_utils
        self.tipids = [4, 8, 12, 16, 20]

    def find_hands(self, img, draw=True):
        imgrgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgrgb)

        if self.results.multi_hand_landmarks:
            for handlms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpdraw.draw_landmarks(
                        img, handlms, self.mphands.HAND_CONNECTIONS
                    )

        return img

    def find_position(self, img, handno=0, draw=True):
        xlist = []
        ylist = []
        bbox = []
        self.lmlist = []
        if self.results.multi_hand_landmarks:
            myhand = self.results.multi_hand_landmarks[handno]
            for id, lm in enumerate(myhand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                xlist.append(cx)
                ylist.append(cy)
                self.lmlist.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

            xmin, xmax = min(xlist), max(xlist)
            ymin, ymax = min(ylist), max(ylist)
            bbox = xmin, ymin, xmax, ymax

            if draw:
                cv2.rectangle(
                    img, (xmin - 20, ymin - 20), (xmax + 20, ymax + 20), (0, 255, 0), 2
                )

        return self.lmlist, bbox

