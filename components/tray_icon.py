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
)
from PyQt5.QtCore import Qt, QSettings, QTimer
from PyQt5.QtGui import QIcon


class TrayIcon:
    def __init__(self, window):
        self.window = window

        self.menu = QMenu(window)
        self.menu.addAction("Open", window.show_window)
        self.menu.addAction("Exit", window.quit)

        self.tray_icon = QSystemTrayIcon(window)
        self.tray_icon.setToolTip("My Application")
        self.tray_icon.activated.connect(self.on_tray_icon_activated)

        # Add the context menu to the system tray icon
        self.tray_icon.setContextMenu(self.menu)
        self.set_default_icon()

        self.timer = QTimer()
        self.timer.setInterval(300)
        self.timer.timeout.connect(self.set_default_icon)

    def on_tray_icon_activated(self, reason):
        # Show the application window when the tray icon is double-clicked
        if reason == QSystemTrayIcon.Trigger:
            self.window.show_window()

    def set_default_icon(self):
        self.tray_icon.setIcon(QIcon("resources/tray_icon/default.png"))

    def set_active_icon(self):
        self.tray_icon.setIcon(QIcon("resources/tray_icon/active.png"))

    def set_active(self):
        self.set_active_icon()
        self.timer.stop()
        self.timer.start()

    def show(self):
        # Show the system tray icon
        self.tray_icon.show()

    def hide(self):
        # Hide the system tray icon
        self.tray_icon.hide()
