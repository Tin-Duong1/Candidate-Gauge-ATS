from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, pyqtSignal

from PyQt5.QtWidgets import QLabel

class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()