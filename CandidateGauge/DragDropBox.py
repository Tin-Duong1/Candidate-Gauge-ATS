from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import Qt
import shutil


class DragDropBox(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = []
        for url in event.mimeData().urls():
            file_path = str(url.toLocalFile())
            files.append(file_path)
            try:
                shutil.copy(file_path, "resumes/")  # Assuming you want to save the file in a folder named "resumes" in the same directory as the script
            except Exception as e:
                print(f"Error: {e}")

        # You can use the list of dropped file paths (files) for further processing if needed
        print(files)
