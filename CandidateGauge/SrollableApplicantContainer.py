from PyQt5.QtWidgets import QVBoxLayout, QScrollArea, QWidget

class ScrollableApplicantContainer(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)

        self.inner_widget = QWidget()
        self.setWidget(self.inner_widget)
        self.inner_layout = QVBoxLayout(self.inner_widget)
