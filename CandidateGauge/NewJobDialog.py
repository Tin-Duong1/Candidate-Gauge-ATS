from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QDialog
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, QLabel, QPushButton


class NewJobDialog(QDialog):
    def __init__(self, parent=None, palette=None):
        super().__init__(parent)
        if palette:
            self.setPalette(palette)
        self.setWindowTitle('New Job')
        self.setGeometry(100, 100, 600, 400)

        main_layout = QVBoxLayout(self)

        form_layout = QFormLayout()
        main_layout.addLayout(form_layout)

        # Add input fields
        self.job_title_input = QLineEdit()
        self.job_title_input.setPlaceholderText("Software Engineer, Data Analyst, etc.")
        form_layout.addRow(QLabel("Job Title/Position"), self.job_title_input)

        self.required_skills_input = QLineEdit()
        self.required_skills_input.setPlaceholderText("Python, Java, SQL, etc.")
        form_layout.addRow(QLabel("Required Skills"), self.required_skills_input)

        self.preferred_skills_input = QLineEdit()
        self.preferred_skills_input.setPlaceholderText("Project Management, Agile, etc.")
        form_layout.addRow(QLabel("Preferred Skills"), self.preferred_skills_input)

        self.min_experience_input = QLineEdit()
        self.min_experience_input.setPlaceholderText("2, 5, 10, etc.")
        form_layout.addRow(QLabel("Minimum Experience (Years)"), self.min_experience_input)

        self.preferred_experience_input = QLineEdit()
        self.preferred_experience_input.setPlaceholderText("3, 7, 12, etc.")
        form_layout.addRow(QLabel("Preferred Experience (Years)"), self.preferred_experience_input)

        self.education_level_input = QLineEdit()
        self.education_level_input.setPlaceholderText("High School Diploma, Bachelor's Degree, etc.")
        form_layout.addRow(QLabel("Education Level"), self.education_level_input)

        self.certifications_input = QLineEdit()
        self.certifications_input.setPlaceholderText("PMP, CPA, etc.")
        form_layout.addRow(QLabel("Certifications/licenses"), self.certifications_input)

        self.industry_knowledge_input = QLineEdit()
        self.industry_knowledge_input.setPlaceholderText("Healthcare, Finance, etc.")
        form_layout.addRow(QLabel("Industry/Domain Knowledge"), self.industry_knowledge_input)

        self.soft_skills_input = QLineEdit()
        self.soft_skills_input.setPlaceholderText("Communication, Teamwork, etc.")
        form_layout.addRow(QLabel("Soft Skills"), self.soft_skills_input)

        self.keywords_input = QLineEdit()
        self.keywords_input.setPlaceholderText("Machine Learning, Big Data, etc.")
        form_layout.addRow(QLabel("Additional Keywords"), self.keywords_input)

        # Add buttons
        buttons_layout = QHBoxLayout()

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_button)

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.accept)
        buttons_layout.addWidget(save_button)

        main_layout.addLayout(buttons_layout)