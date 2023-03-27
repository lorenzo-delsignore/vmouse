from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMovie
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
from widgets.navbar import Navbar


class TutorialScreen(QWidget):
    def __init__(
        self,
        title,
        description,
        image,
        on_skip_clicked=None,
        on_continue_clicked=None,
        parent=None,
    ):
        super().__init__(parent)

        self.title = title
        self.image = image
        self.description = description
        self.on_skip_clicked = on_skip_clicked
        self.on_continue_clicked = on_continue_clicked

        self.init_ui()

    def init_ui(self):
        # Add Spacer at the top
        vspacer1 = QWidget()
        vspacer1.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        navbar = Navbar(title=self.title, parent=self)

        # Add Description Label
        description_label = QLabel(self.description)
        description_label.setStyleSheet("font-size: 24px; color: #75777B;")
        description_label.setWordWrap(True)

        # Add Animated Image
        image_label = QLabel(self)
        image_gif = QMovie(self.image)
        image_label.setMovie(image_gif)
        image_gif.start()

        image_label.setAlignment(Qt.AlignCenter)

        # Add "Try Now" and "Continue" Buttons
        skip_button = QPushButton("Skip", self)
        skip_button.setCursor(Qt.PointingHandCursor)
        if self.on_skip_clicked is not None:
            skip_button.clicked.connect(self.on_skip_clicked)

        continue_button = QPushButton("Next", self)
        continue_button.setCursor(Qt.PointingHandCursor)
        if self.on_continue_clicked is not None:
            continue_button.clicked.connect(self.on_continue_clicked)

        hlayout2 = QHBoxLayout()
        hlayout2.addWidget(skip_button)
        hlayout2.addWidget(continue_button)

        # Add Layouts and Widgets
        layout = QVBoxLayout()
        # layout.addWidget(vspacer1)
        layout.addWidget(navbar)
        layout.addWidget(description_label)
        layout.addWidget(image_label)
        layout.addLayout(hlayout2)
        layout.setSpacing(20)

        # set stretch factor of middle widget to 1
        layout.setStretchFactor(image_label, 1)

        self.setLayout(layout)

        self.setStyleSheet("background-color: #ffffff;")
        skip_button.setStyleSheet(
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
            }
            """
        )
        continue_button.setStyleSheet(
            """
            QPushButton {
                background-color: #7CB342;
                color: white;
                border-radius: 10px;
                border: none;
                font-size: 16px;
                font-weight: bold;
                padding: 10px 20px;
                margin-top: 20px;
            }

            QPushButton:hover {
                background-color: #558B2F;
            }
            """
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    welcome_widget = TutorialScreen(
        title="Mouse Movement",
        description="You can move the cursor mouse in the camera raising only your index finger in the bounding box displayed in the camera.",
        image="resources/assets/move_mouse.gif",
    )
    welcome_widget.show()
    welcome_widget.showMaximized()
    sys.exit(app.exec_())
