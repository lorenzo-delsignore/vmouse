from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QMovie
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


class Navbar(QWidget):
    def __init__(self, title, parent=None):
        super().__init__(parent=parent)

        self.title = title

        # Add Title and Logo
        logo_label = QLabel(self)
        logo_pixmap = QPixmap("resources/assets/logo.png")
        logo_label.setPixmap(logo_pixmap)
        logo_width = 50
        logo_height = int(logo_pixmap.height() * logo_width / logo_pixmap.width())
        logo_label.setPixmap(logo_pixmap.scaled(logo_width, logo_height))
        logo_label.setAlignment(Qt.AlignLeft)

        title_label = QLabel(self.title)
        title_label.setAlignment(Qt.AlignLeft)
        title_label.setStyleSheet(
            """
            margin-top: 5px; 
            font-size: 30px; 
            margin-left: -10px;
            font-weight: bold;
            color: black;
            """
        )

        hlayout = QHBoxLayout()

        # add logo label to the layout
        hlayout.addWidget(logo_label)

        # add title label to the layout
        hlayout.addWidget(title_label)

        # add stretchable spacer to the right with stretch factor 2
        right_spacer = QWidget()
        right_spacer.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        hlayout.addWidget(right_spacer, 1)

        # set layout margins to 0
        hlayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(hlayout)
