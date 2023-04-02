from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QPushButton,
    QSystemTrayIcon,
    QMenu,
    QMessageBox,
    QHBoxLayout,
    QWidget,
    QStackedLayout,
)
from PyQt5.QtCore import Qt, QSettings, QTimer
from PyQt5.QtGui import QIcon
from widgets.screens import HandTrackingScreen, WelcomeScreen, TutorialScreen
from components import TrayIcon
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # setup tray icon
        self.tray_icon = TrayIcon(self)
        self.tray_icon.show()

        # settings
        self.settings = QSettings("Virtual Mouse", "settings")

        # initialize ui
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setStyleSheet("background: #ffffff;")

        layout = QHBoxLayout(central_widget)

        # layout.addWidget(self.hand_tracking_widget)

        stacked_layout = QStackedLayout()

        # hand tracking screen
        hand_tracking_screen = HandTrackingScreen(
            on_hand_gesture=self.on_hand_gesture,
            on_show_tutorial=lambda: stacked_layout.setCurrentIndex(1),
        )

        stacked_layout.addWidget(hand_tracking_screen)

        # add welcome screen
        self.welcome_screen = WelcomeScreen(
            on_get_started_button_clicked=lambda: stacked_layout.setCurrentIndex(
                stacked_layout.currentIndex() + 1
            )
        )

        stacked_layout.addWidget(self.welcome_screen)

        # add tutorial 1
        self.tutorial_screen = TutorialScreen(
            title="Mouse Movement",
            description="You can move the cursor mouse in the camera raising only your index finger in the bounding box displayed in the camera.",
            image="resources/assets/move_mouse.gif",
            on_continue_clicked=lambda: stacked_layout.setCurrentIndex(
                stacked_layout.currentIndex() + 1
            ),
            on_skip_clicked=lambda: stacked_layout.setCurrentIndex(0),
        )

        stacked_layout.addWidget(self.tutorial_screen)

        # add tutorial 2
        self.tutorial_screen2 = TutorialScreen(
            title="Click Mouse",
            description="You can simulate the click of the mouse in the camera raising only the index finger and middle finger in the bounding box displayed in the camera.\nIn particular you can simulate the following features of the mouse:\nLeft click: you can simulate it by bringing your index and middle fingers closer together and moving them apart \nRight click: you can simulate it by holding your index and middle fingers close together\nDouble click:you can simulate it by bringing your index and middle fingers together and moving them away twice",
            image="resources/assets/mouse_click.gif",
            on_continue_clicked=lambda: stacked_layout.setCurrentIndex(0),
            on_skip_clicked=lambda: stacked_layout.setCurrentIndex(0),
        )

        stacked_layout.addWidget(self.tutorial_screen2)

        # welcome screen
        onboarding = not self.settings.value("onboard", False, bool)
        if onboarding:
            # Set onboard flag to true
            self.settings.setValue("onboard", True)
            stacked_layout.currentIndex(1)

        layout.addLayout(stacked_layout)

        # if onboarding:
        #     self.showMaximized()

        self.showMaximized()
        self.show()

    def on_hand_gesture(self, reason):
        # print("gesture: " + reason)
        self.tray_icon.set_active()

    def show_window(self):
        window_state = self.windowState()

        if window_state & Qt.WindowMinimized:
            self.setWindowState(window_state & ~Qt.WindowMinimized)

        self.show()
        self.activateWindow()

    def changeEvent(self, event):
        # Hide the application window when it is minimized
        if event.type() == event.WindowStateChange:
            if self.isMinimized():
                self.hide()

        super().changeEvent(event)

    def closeEvent(self, event):
        # Hide the window instead of closing it
        self.tray_icon.hide()
        event.accept()
        self.hide()

    def quit(self):
        # Remove the tray icon and exit the application
        self.tray_icon.hide()
        self.close()
        sys.exit()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()

    # print(settings.fileName())
    # window.setGeometry(100, 100, 500, 500)  # Set the window's geometry
    window.setWindowTitle("Vmouse")  # Set the window's title
    window.setWindowIcon(QIcon("resources/assets/logo.png"))

    # # Create a label widget
    # label = QLabel("Hello World", window)
    # label.move(200, 200)

    # # Create a push button widget
    # button = QPushButton("Click Me!", window)
    # button.move(200, 250)

    window.show()  # Show the window
    app.exec_()
