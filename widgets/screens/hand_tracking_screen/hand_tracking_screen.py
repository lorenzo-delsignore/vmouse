from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QStackedWidget,
    QGroupBox,
    QAction,
    QMenuBar,
    QSizePolicy,
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QImage, QPixmap
import numpy as np
import time
import pyautogui
import cv2
import model as htm
from hand_gesture_module import HandGestureModule
import widgets.screens.hand_tracking_screen.styles as styles
from widgets.navbar import Navbar


class HandTrackingScreen(QWidget):
    def __init__(self, on_hand_gesture=None, on_show_tutorial=None):
        super().__init__()
        self.setWindowTitle("Hand Tracking")
        self.setGeometry(100, 100, 800, 600)

        # Setup GUI
        self.image_label = QLabel(self)
        self.image_label.setMinimumSize(640, 480)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet(styles.image_label)

        # Create menu bar
        menu_bar = QMenuBar()
        menu_bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        menu_bar.setStyleSheet("color: #000000;")
        help_menu = menu_bar.addMenu("Help")

        # Add "Show Tutorial" action to the "Help" menu
        tutorial_action = QAction("Show Tutorial", self)

        tutorial_action.triggered.connect(on_show_tutorial)
        help_menu.addAction(tutorial_action)

        self.start_button = QPushButton("Start Tracking", self)
        self.start_button.clicked.connect(self.toggle_tracking)
        self.start_button.setStyleSheet(styles.start_button)
        self.start_button.setCursor(Qt.PointingHandCursor)

        self.quit_button = QPushButton("Quit", self)
        self.quit_button.clicked.connect(self.quit)
        self.quit_button.setStyleSheet(styles.quit_button)
        self.quit_button.setCursor(Qt.PointingHandCursor)

        # Set up layouts
        hbox = QHBoxLayout()
        hbox.addWidget(self.start_button)
        hbox.addWidget(self.quit_button)

        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)
        vbox.addLayout(hbox)

        group_box = QGroupBox("Hand Tracking")
        group_box.setLayout(vbox)

        main_layout = QVBoxLayout()
        main_layout.addWidget(menu_bar)
        main_layout.addWidget(Navbar(title="Vmouse"))
        main_layout.addWidget(group_box)

        # set stretch factor
        main_layout.setStretchFactor(group_box, 1)

        self.setLayout(main_layout)

        # Set up variables for hand tracking
        self.wCam, self.hCam = 640, 480
        self.wScr, self.hScr = pyautogui.size()

        self.gesture_handler = HandGestureModule(
            wScr=self.wScr,
            hScr=self.hScr,
            width=self.wCam,
            height=self.hCam,
            frame_reduction=90,
            on_mouse_move=self.move_mouse,
            on_mouse_click=self.mouse_click,
        )

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_image)
        self.timer.start(1)

        self.on_hand_gesture = on_hand_gesture
        self.handle_user_gesture = False

    def start_tracking(self):
        self.window().hide()
        self.handle_user_gesture = True
        self.start_button.setText("Stop Tracking")
        self.start_button.setStyleSheet(styles.quit_button)

    def stop_tracking(self):
        self.handle_user_gesture = False
        self.start_button.setText("Start Tracking")
        self.start_button.setStyleSheet(styles.start_button)

    def toggle_tracking(self):
        if self.handle_user_gesture:
            self.stop_tracking()
        else:
            self.start_tracking()

    def quit(self):
        self.update_gui_timer.stop()
        self.gesture_handler.release()
        cv2.destroyAllWindows()
        self.close()

    def move_mouse(self, clocX, clocY):
        if not self.handle_user_gesture:
            return

        pyautogui.moveTo(self.wScr - clocX, clocY, duration=0)
        if not self.on_hand_gesture is None:
            self.on_hand_gesture(reason="move_mouse")

    def mouse_click(self, reason):
        if not self.handle_user_gesture:
            return

        if reason == "left_click":
            pyautogui.click()
        elif reason == "right_click":
            pyautogui.rightClick()

        if not self.on_hand_gesture is None:
            self.on_hand_gesture(reason=reason)

    def update_image(self):
        frame = self.gesture_handler.get_frame()

        # display frame on image label
        height, width, channel = frame.shape
        bytes_per_line = 3 * width
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        q_image = QImage(
            img_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888
        )
        pixmap = QPixmap.fromImage(q_image)
        self.image_label.setPixmap(pixmap)
