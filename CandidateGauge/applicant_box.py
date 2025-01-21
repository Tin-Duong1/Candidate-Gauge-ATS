from PyQt5.QtWidgets import QHBoxLayout, QFrame, QLabel
from PyQt5.QtCore import Qt, pyqtSignal

from PyQt5.QtWidgets import QHBoxLayout, QLabel

class ApplicantBox(QFrame):
    clicked = pyqtSignal()

    def __init__(self, applicant, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setObjectName('applicant_box')
        self.setFrameStyle(QFrame.NoFrame)
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet('background-color: #3F3F3F; border-radius: 5px; padding: 4px;')
        self.applicant = applicant

        applicant_name_label = QLabel(f"{applicant.first_name} {applicant.last_name}")
        applicant_name_label.setObjectName('applicant_name_label')
        applicant_name_label.setStyleSheet('font-weight: bold; color: white')
        applicant_name_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        applicant_score = QLabel(f"{applicant.score}")
        applicant_score.setObjectName('applicant_score')
        applicant_score.setStyleSheet('font-weight: bold; color: white')
        applicant_score.setAlignment(Qt.AlignTop | Qt.AlignRight)


        

        applicant_box_layout = QHBoxLayout(self)
        applicant_box_layout.addWidget(applicant_name_label)
        applicant_box_layout.addWidget(applicant_score)



    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()

    def show_applicant_data(self):
        self.parent().parent().parent().show_applicant_data(self.applicant)
