from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QSizePolicy,
)
import sys
from PyQt5.QtWidgets import QApplication


class WelcomeScreen(QWidget):
    def __init__(self, on_get_started_button_clicked=None, parent=None):
        super().__init__(parent)

        self.on_get_started_button_clicked = on_get_started_button_clicked
        self.init_ui()

    def init_ui(self):
        # Add Logo
        logo_label = QLabel(self)
        logo_pixmap = QPixmap("resources/assets/icon.png")

        width = 300
        height = int(logo_pixmap.height() * width / logo_pixmap.width())

        logo_label.setPixmap(logo_pixmap.scaled(width, height))
        logo_label.setAlignment(Qt.AlignCenter)

        # Add Welcome Message
        welcome_label = QLabel("Hey! Welcome", self)
        welcome_label.setAlignment(Qt.AlignCenter)

        # Add Description
        description_label = QLabel(
            "Hand gesture control software that allows you to operate a computer mouse using hand movements and finger gestures.",
            self,
        )
        description_label.setAlignment(Qt.AlignCenter)
        description_label.setWordWrap(True)
        description_label.setFixedWidth(800)

        # Add "Get Started" button
        hlayout = QHBoxLayout()
        hlayout.setContentsMargins(0, 0, 0, 0)

        # space to the left
        hspacer1 = QWidget()
        hspacer1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        hlayout.addWidget(hspacer1)

        vlayout = QVBoxLayout()
        vlayout.addWidget(description_label)

        # add the button
        get_started_button = QPushButton("Get Started", self)
        get_started_button.setCursor(Qt.PointingHandCursor)

        if self.on_get_started_button_clicked is not None:
            get_started_button.clicked.connect(self.on_get_started_button_clicked)

        vlayout.addWidget(get_started_button)
        hlayout.addLayout(vlayout)

        # add space to the right
        hspacer2 = QWidget()
        hspacer2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        hlayout.addWidget(hspacer2)

        # Add a spacer to the top
        vspacer1 = QWidget()
        vspacer1.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        # Add a spacer to the top
        vspacer2 = QWidget()
        vspacer2.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        # Add layout widget
        layout = QVBoxLayout()
        layout.addWidget(vspacer1)
        layout.addWidget(logo_label)
        layout.addWidget(welcome_label)
        # layout.addWidget(description_label)
        layout.addLayout(hlayout)
        layout.addWidget(vspacer2)
        layout.setSpacing(20)

        # Set layout
        self.setLayout(layout)

        # Set background
        self.setStyleSheet("background-color: #ffffff;")

        welcome_label.setStyleSheet(
            """
            margin-top: 40px;
            font-weight: bold;
            font-size: 40px;
            color: black;
            """
        )

        description_label.setStyleSheet(
            """
            font-size: 24px;
            color: #75777B;
            """
        )

        get_started_button.setFixedWidth(800)
        get_started_button.setStyleSheet(
            """
            QPushButton {
                background-color: #F5D565;
                color: black;
                border-radius: 10px;
                border: none;
                font-size: 16px;
                font-weight: bold;
                padding: 10px 20px;
                margin-top: 20px;
            }

            QPushButton:hover {
                background-color: #F58A45;
                cursor: pointer;
            }
            """
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    welcome_widget = WelcomeScreen()
    welcome_widget.show()
    welcome_widget.showMaximized()
    sys.exit(app.exec_())
