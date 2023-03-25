import cv2
import mediapipe as mp
import math
import numpy as np


class HandDetector:
    def __init__(
        self, mode=False, maxhands=2, modelcomplexity=1, detectioncon=0.5, trackcon=0.5
    ):
        self.mode = mode
        self.maxhands = maxhands
        self.detectioncon = detectioncon
        self.trackcon = trackcon
        self.modelcomplex = modelcomplexity

        self.mphands = mp.solutions.hands
        self.hands = self.mphands.hands(
            self.mode,
            self.maxhands,
            self.modelcomplex,
            self.detectioncon,
            self.trackcon,
        )
        self.mpdraw = mp.solutions.drawing_utils
        self.tipids = [4, 8, 12, 16, 20]

    def findhands(self, img, draw=True):
        imgrgb = cv2.cvtcolor(img, cv2.color_bgr2rgb)
        self.results = self.hands.process(imgrgb)

        if self.results.multi_hand_landmarks:
            for handlms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpdraw.draw_landmarks(
                        img, handlms, self.mphands.hand_connections
                    )

        return img

