from PyQt5.QtWidgets import QApplication, QTextEdit, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QFrame, QPushButton, QLabel, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QIcon
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox
from openAI import score_resume

from JobBox import JobBox
from ClickableLabel import ClickableLabel
from NewJobDialog import NewJobDialog
from DragDropBox import DragDropBox
from docx_parse import process_resumes
from applicant_box import ApplicantBox
from SrollableApplicantContainer import ScrollableApplicantContainer


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.applicants = []
        # Window properties
        self.setWindowTitle('AI Resume Analyzer')
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumWidth(500)
        self.displayrun = 0

        # Set the application icon
        self.setWindowIcon(QIcon('icon_image.png'))

        # Set Fusion style and customize color palette
        QApplication.setStyle("Fusion")
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, QColor(25, 25, 25))
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Highlight, QColor(142, 45, 197).lighter())
        palette.setColor(QPalette.HighlightedText, Qt.black)
        self.setPalette(palette)

        # Data structure to store the job information
        self.jobs = []

        # Main layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Content area and sidebar layout (now nested inside another QHBoxLayout)
        content_and_sidebar_layout = QHBoxLayout()
        content_and_sidebar_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addLayout(content_and_sidebar_layout)

        # Sidebar
        sidebar = QFrame()
        sidebar.setFrameShape(QFrame.StyledPanel)
        sidebar.setFixedWidth(100)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)

        create_job_button = QPushButton('J')
        create_job_button.setFixedSize(80, 80)
        create_job_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        create_job_button.clicked.connect(self.show_jobs)
        create_job_button.setCursor(Qt.PointingHandCursor)

        view_candidates_button = QPushButton('A')
        view_candidates_button.setFixedSize(80, 80)
        view_candidates_button.setSizePolicy(
            QSizePolicy.Fixed, QSizePolicy.Fixed)
        view_candidates_button.clicked.connect(self.show_applicants)
        view_candidates_button.setCursor(Qt.PointingHandCursor)

        sidebar_layout.addSpacing(10)
        sidebar_layout.addWidget(create_job_button)
        sidebar_layout.addWidget(view_candidates_button)

        # Add an exit icon to the bottom of the sidebar
        exit_button = QPushButton()
        # Assuming you have an exit icon image named 'exit_icon.png'
        exit_button.setIcon(QIcon('exit_icon.png'))
        exit_button.setFixedSize(40, 40)
        exit_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # Connect the button to the close_application slot
        exit_button.clicked.connect(self.close_application)
        exit_button.setCursor(Qt.PointingHandCursor)

        sidebar_layout.addStretch(1)
        sidebar_layout.addSpacing(10)
        sidebar_layout.addWidget(exit_button, alignment=Qt.AlignCenter)

        # Content area
        content_area = QFrame()
        content_area.setFrameShape(QFrame.StyledPanel)

        # Add content layout with a new QVBoxLayout
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(0, 25, 0, 0)
        content_area.setAcceptDrops(True)

        # New horizontal box within the content layout
        top_horizontal_box = QHBoxLayout()
        # Align the content of the horizontal box to the top
        top_horizontal_box.setAlignment(Qt.AlignTop)
        # Set the spacing between the widgets to 0
        top_horizontal_box.setSpacing(0)

        # Create a QLabel with the text "Add Job:"
        self.add_job_text = QLabel("Add Job ")
        # Set the text color to white
        self.add_job_text.setStyleSheet('color: white; font-weight: bold')
        self.add_job_text.setMaximumWidth(120)
        self.add_job_text.setAlignment(Qt.AlignLeft)
        # Add the QLabel to the top_horizontal_box
        top_horizontal_box.addWidget(self.add_job_text)

        self.plus_icon = ClickableLabel()  # Create a ClickableLabel for the icon
        # Assuming you have an icon image named 'icon_above_box1.png'
        self.plus_icon.setPixmap(QIcon('plus_icon.png').pixmap(16, 16))
        # Add the icon QLabel to the left content box layout
        top_horizontal_box.addWidget(self.plus_icon, alignment=Qt.AlignLeft)
        # Connect the icon_label to the show_new_job_dialog slot
        self.plus_icon.clicked.connect(self.show_new_job_dialog)
        self.plus_icon.setCursor(Qt.PointingHandCursor)

        self.displayApp_button = QPushButton('Display Applicants')
        self.displayApp_button.setFixedSize(150, 35)
        self.displayApp_button.setSizePolicy(
            QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.displayApp_button.clicked.connect(self.on_process_icon_clicked)
        self.displayApp_button.setCursor(Qt.PointingHandCursor)
        top_horizontal_box.addWidget(
            self.displayApp_button, alignment=Qt.AlignLeft)

        # Create a QLabel with the text "Add Job:"
        self.jobSel_text = QLabel("Select Job:")
        # Set the text color to white
        self.jobSel_text.setStyleSheet('color: white; font-weight: bold;')
        self.jobSel_text.setMaximumWidth(110)
        self.jobSel_text.setAlignment(Qt.AlignLeft)
        # Add the QLabel to the top_horizontal_box
        top_horizontal_box.addWidget(self.jobSel_text)

        self.job_combobox = QComboBox()
        self.job_combobox.setFixedSize(200, 35)
        self.job_combobox.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        top_horizontal_box.addWidget(self.job_combobox, alignment=Qt.AlignLeft)

        self.sortPush_button = QPushButton('Sort')
        self.sortPush_button.setFixedSize(60, 35)
        self.sortPush_button.setSizePolicy(
            QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.sortPush_button.setCursor(Qt.PointingHandCursor)
        top_horizontal_box.addWidget(
            self.sortPush_button, alignment=Qt.AlignLeft)

        # Add the box layout to the content layout
        content_layout.addLayout(top_horizontal_box, stretch=0)

        # Add two boxes to the content area (inside a QHBoxLayout)

        box_layout = QHBoxLayout()
        box_layout.setSpacing(20)

        self.box1 = QFrame()
        self.box1.setFixedWidth(200)
        self.box1_layout = QVBoxLayout(self.box1)
        self.box1_layout.setSpacing(10)
        self.box1_layout.setAlignment(Qt.AlignTop)
        self.box1.setFrameShape(QFrame.StyledPanel)
        content_area.setFrameShape(QFrame.NoFrame)  # Update this line
        sidebar.setFrameShape(QFrame.NoFrame)

        self.box2 = QFrame()
        self.box2.setFixedWidth(450)
        self.box2_layout = QVBoxLayout(self.box2)
        self.box2.setFrameShape(QFrame.StyledPanel)

        box_layout.addWidget(self.box1)
        box_layout.addWidget(self.box2)

        self.box3 = DragDropBox()
        self.box3.setFrameShape(QFrame.StyledPanel)
        self.box3_layout = QVBoxLayout(self.box3)
        self.box3_dragText = QLabel(
            "Drag in applicant resume files and select Display Applicants")
        self.box3_dragText.setAlignment(Qt.AlignCenter)
        self.box3_layout.addWidget(self.box3_dragText)
        self.box3_layout.setAlignment(Qt.AlignTop)

        # Initially hidden
        self.box3.hide()
        self.job_combobox.hide()
        self.jobSel_text.hide()
        self.sortPush_button.hide()
        self.displayApp_button.hide()
        box_layout.addWidget(self.box3)

        # Add the box layout to the content layout
        content_layout.addLayout(box_layout, stretch=1)

        # Add sidebar and content area to the main layout
        content_and_sidebar_layout.addWidget(sidebar)
        content_and_sidebar_layout.addWidget(content_area)

    def add_job_box(self, job):
        # Create the job box widget
        job_box = JobBox(job, parent=self)

        # Add the job box widget to the content layout
        self.box1_layout.addWidget(job_box)

        # Connect the clicked signal of the job box to the display_job_data slot using a lambda function
        job_box.clicked.connect(lambda: self.show_job_data(job))

        # Add the job title to the QComboBox
        self.job_combobox.addItem(job['title'])

    def show_new_job_dialog(self):
        # Create an instance of the NewJobDialog and show it as a modal dialog
        dialog = NewJobDialog(parent=self, palette=self.palette())
        if dialog.exec_():
            # Get the job data from the dialog
            job_title = dialog.job_title_input.text()
            required_skills = dialog.required_skills_input.text()
            preferred_skills = dialog.preferred_skills_input.text()
            min_experience = dialog.min_experience_input.text()
            preferred_experience = dialog.preferred_experience_input.text()
            education_level = dialog.education_level_input.text()
            certifications = dialog.certifications_input.text()
            industry_knowledge = dialog.industry_knowledge_input.text()
            soft_skills = dialog.soft_skills_input.text()
            keywords = dialog.keywords_input.text()

            # Store the job data
            job = {
                'title': job_title,
                'reqskills': required_skills,
                'prefskills': preferred_skills,
                'minexperience': min_experience,
                'prefexperience': preferred_experience,
                'edulevel': education_level,
                'certs': certifications,
                'knowledge': industry_knowledge,
                'sskills': soft_skills,
                'kw': keywords
            }
            self.jobs.append(job)

            # Add the job box widget to the content layout
            self.add_job_box(job)

    def show_job_data(self, job):
        # Clear the contents of box2
        for i in reversed(range(self.box2_layout.count())):
            widgetToRemove = self.box2_layout.itemAt(i).widget()
            self.box2_layout.removeWidget(widgetToRemove)
            widgetToRemove.setParent(None)

        # Add the job data to box2
        job_data = QTextEdit()  # Change this line to use QTextEdit instead of QPlainTextEdit
        job_data.setReadOnly(True)

        # Create a mapping from short keys to full titles
        titles = {
            'title': 'Job Title',
            'reqskills': 'Required Skills',
            'prefskills': 'Preferred Skills',
            'minexperience': 'Minimum Experience (Years)',
            'prefexperience': 'Preferred Experience (Years)',
            'edulevel': 'Education Level',
            'certs': 'Certifications/licenses',
            'knowledge': 'Industry/Domain Knowledge',
            'sskills': 'Soft Skills',
            'kw': 'Additional Keywords'
        }

        formatted_text = ''
        for key, value in job.items():
            formatted_text += f'<b>{titles[key]}:</b><br>{value}<br><br>'

        # This method is available in QTextEdit
        job_data.setHtml(formatted_text)
        self.box2_layout.addWidget(job_data)

    def show_applicants(self):
        # Hide box1 box2 and add jobs
        self.box1.hide()
        self.box2.hide()
        self.plus_icon.hide()
        self.add_job_text.hide()

        # Show box3 and process resumes
        self.displayApp_button.show()
        self.box3.show()
        self.job_combobox.show()
        self.jobSel_text.show()
        self.sortPush_button.show()

    def show_jobs(self):
        # Hide box3 and process resumes
        self.box3.hide()
        self.displayApp_button.hide()
        self.jobSel_text.hide()

        # Show box1 and box2
        self.box1.show()
        self.box2.show()
        self.plus_icon.show()
        self.add_job_text.show()
        self.job_combobox.hide()
        self.sortPush_button.hide()

    def close_application(self):
        self.close()

    def on_process_icon_clicked(self):
        self.jobSel_text.show()
        resumes_folder = "resumes"
        self.box3_dragText.hide()
        applicants_generator = process_resumes(resumes_folder)
        self.applicants = list(applicants_generator)
        self.display_applicants(self.applicants)

        # Update the connection line to use the class attribute
        self.sortPush_button.clicked.connect(
            lambda: self.on_sortPush_click(self.applicants))

    def display_applicants(self, applicants):
        # Create the scrollable container
        scrollable_container = ScrollableApplicantContainer()

        for applicant in applicants:
            applicant_box = ApplicantBox(applicant)
            scrollable_container.inner_layout.addWidget(applicant_box)
            applicant_box.clicked.connect(applicant_box.show_applicant_data)

        scrollable_container.inner_layout.addStretch()

        # Clear the contents of box3
        for i in reversed(range(self.box3_layout.count())):
            widgetToRemove = self.box3_layout.itemAt(i).widget()
            self.box3_layout.removeWidget(widgetToRemove)
            widgetToRemove.setParent(None)

        # Add the scrollable container to box3_layout
        self.box3_layout.addWidget(scrollable_container)

    def on_sortPush_click(self, applicants):
        # Get the selected job title from the combo box
        selected_job_title = self.job_combobox.currentText()

        # Get the job data from the jobs list using the selected job title
        selected_job = self.get_job_by_title(selected_job_title)

        if not selected_job:
            # If the selected job is not found, show a message and return
            print("Selected job not found.")
            return

        # Score and sort the applicants based on the selected job
        for i, applicant in enumerate(applicants):
            score, sentiment_label, sentiment_score = score_resume(
                applicant.resume, selected_job)
            applicants[i].score = (score, sentiment_score)

        sorted_applicants = sorted(
            applicants, key=lambda x: x.score, reverse=True)

        # Clear the current applicants displayed and re-display the sorted applicants
        self.display_applicants([applicant for applicant in sorted_applicants])

    def get_job_by_title(self, title):
        for job in self.jobs:
            if job['title'] == title:
                return job
        return None
