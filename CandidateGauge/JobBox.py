from PyQt5.QtWidgets import QHBoxLayout, QFrame, QLabel
from PyQt5.QtCore import Qt, pyqtSignal

from PyQt5.QtWidgets import QHBoxLayout, QLabel


class JobBox(QFrame):
    clicked = pyqtSignal()

    def __init__(self, job, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setObjectName('job_box')
        self.setFrameStyle(QFrame.NoFrame)  # remove the border
        self.setContentsMargins(0, 0, 0, 0)  # remove any spacing around the edge
        self.setStyleSheet('background-color: #3F3F3F; border-radius: 5px; padding: 4px;')
        self.job = job

        job_title_label = QLabel(job['title'])
        job_title_label.setObjectName('job_title_label')
        job_title_label.setStyleSheet('font-weight: bold; color: white')
        job_title_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        job_box_layout = QHBoxLayout(self)
        job_box_layout.addWidget(job_title_label)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()    

    def show_job_data(self, job):
        self.parent().parent().parent().show_job_data(job)