import cv2
import time
import numpy as np
import model as htm


class HandGestureModule:
    def __init__(
        self,
        width,
        height,
        wScr,
        hScr,
        smoothening=3,
        frame_reduction=60,
        on_mouse_move=None,
        on_mouse_click=None,
    ):
        self.video_capture = cv2.VideoCapture(0)
        self.video_capture.set(3, width)
        self.video_capture.set(4, height)

        self.detector = htm.HandDetector(max_hands=1)

        self.wScr = wScr
        self.hScr = hScr
        self.width = width
        self.height = height
        self.smoothening = smoothening
        self.frame_reduction = frame_reduction

        self.on_mouse_move = on_mouse_move
        self.on_mouse_click = on_mouse_click

        self.pTime = 0
        self.plocX, self.plocY = 0, 0
        self.clocX, self.clocY = 0, 0

        self.click_before = False
        self.right_click = False
        self.start_time = None

    def release(self):
        self.video_capture.release()

    def move_mouse(self):
        if not self.on_mouse_move is None:
            self.on_mouse_move(self.clocX, self.clocY)

    def mouse_click(self, reason):
        if not self.on_mouse_click is None:
            self.on_mouse_click(reason)

    def is_moving_mouse(self, fingers):
        # Index Finger : Moving Mode
        return fingers[1] == 1 and fingers[2] == 0

    def is_clicking_mouse(self, fingers):
        # 8. Both Index and middle fingers are up : Clicking Mode
        return fingers[1] == 1 and fingers[2] == 1

    def get_frame(self):
        # Find hand landmarks
        success, img = self.video_capture.read()
        img = self.detector.find_hands(img)
        lmList, bbox = self.detector.find_position(img)

        # Get the tip of the index and middle fingers
        if len(lmList) != 0:
            x1, y1 = lmList[8][1:]
            x2, y2 = lmList[12][1:]

        # Check which fingers are up
        fingers = self.detector.fingers_up()

        # Draw rectangle
        cv2.rectangle(
            img,
            (self.frame_reduction, self.frame_reduction),
            (self.width - self.frame_reduction, self.height - self.frame_reduction),
            (255, 0, 255),
            2,
        )

        if self.is_moving_mouse(fingers):
            # Convert Coordinates
            x3 = np.interp(
                x1,
                (self.frame_reduction, self.width - self.frame_reduction),
                (0, self.wScr),
            )

            y3 = np.interp(
                y1,
                (self.frame_reduction, self.height - self.frame_reduction),
                (0, self.hScr),
            )
            # 6. Smoothen Values
            self.clocX = self.plocX + (x3 - self.plocX) / self.smoothening
            self.clocY = self.plocY + (y3 - self.plocY) / self.smoothening

            # 7. Move Mouse
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            self.plocX, self.plocY = self.clocX, self.clocY

            self.move_mouse()

        if self.is_clicking_mouse(fingers):
            # 9. Find distance between fingers
            length, img, lineInfo = self.detector.find_distance(8, 12, img)

            # 10. Click mouse if distance short
            if length < 30:  # 40
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)

                # start timer
                if not self.right_click:
                    if self.start_time is None:
                        self.start_time = time.time()
                    else:
                        elapsed_time = time.time() - self.start_time

                        if elapsed_time > 0.35:
                            self.mouse_click("right_click")
                            self.right_click = True
                            self.start_time = None

                if not self.click_before:
                    self.click_before = True
                    self.mouse_click("left_click")

            else:
                self.click_before = False
                self.right_click = False
                self.start_time = None

        else:
            self.click_before = False
            self.right_click = False
            self.start_time = None

        # 11. Frame Rate
        cTime = time.time()
        fps = 1 / (cTime - self.pTime)
        self.pTime = cTime
        cv2.putText(
            img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3
        )

        return img
