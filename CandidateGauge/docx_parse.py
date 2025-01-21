import os
import re
import spacy
import PyPDF2
import docx2txt
from typing import Tuple
from openAI import score_resume


# Load the spaCy NLP model
nlp = spacy.load("en_core_web_sm")


class Applicant:
    def __init__(self, first_name, last_name, contact, resume, score):
        self.first_name = first_name
        self.last_name = last_name
        self.contact = contact
        self.resume = resume
        self.score = score

    def __str__(self):
        return f"{self.first_name} {self.last_name}\n{self.contact}"


def extract_text_from_docx(file_path):
    try:
        # Extract text from the DOCX file
        text = docx2txt.process(file_path)
        return text.replace('\t', ' ').replace('\n', ' ')
    except Exception as e:
        print(f'Error extracting text from file {file_path}: {e}')
        return ''


def extract_text_from_pdf(file_path):
    try:
        # Open the PDF file
        with open(file_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfFileReader(f)

            # Extract text from the PDF file
            text = ''
            for i in range(pdf_reader.getNumPages()):
                text += pdf_reader.getPage(i).extractText()

            return text.replace('\t', ' ').replace('\n', ' ')
    except Exception as e:
        print(f'Error extracting text from file {file_path}: {e}')
        return ''


def extract_name(text: str, file_name: str) -> Tuple[str, str]:
    blacklist = ["Servers"]

    # First, check if the name is in the file name
    file_name_no_ext = os.path.splitext(file_name)[0]
    file_name_candidates = file_name_no_ext.split('_')
    for candidate in file_name_candidates:
        if candidate not in blacklist and nlp(candidate)[0].ent_type_ == "PERSON":
            first_name, last_name = candidate, ''
            return first_name, last_name

    doc = nlp(text)
    first_name = last_name = None

    for ent in doc.ents:
        if ent.label_ == "PERSON":
            tokens = ent.text.strip().split()
            if any(token in blacklist for token in tokens):
                continue
            first_name, last_name = tokens[0], tokens[-1]
            break

    if not first_name:
        first_name = 'Unknown'
    if not last_name:
        last_name = 'Unknown'

    return first_name, last_name


def extract_name_from_file_name(file_path: str) -> Tuple[str, str]:
    file_name = os.path.basename(file_path).split('.')[0]
    words = re.findall(r'\b\w+\b', file_name)
    if len(words) >= 2:
        return words[0], words[1]
    return 'Unknown', 'Unknown'


def extract_applicant_info(file_path: str):
    # Extract text from the file
    if file_path.endswith('.docx') or file_path.endswith('.DOCX'):
        text = extract_text_from_docx(file_path)
    elif file_path.endswith('.pdf'):
        text = extract_text_from_pdf(file_path)
    else:
        print(f'Unsupported file type: {file_path}')
        return None

    # Extract the applicant's contact information
    phone_regex = r'(\d{3})[-\.\s]*(\d{3})[-\.\s]*(\d{4})'
    email_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    phone_matches = re.findall(phone_regex, text)
    email_matches = re.findall(email_regex, text)
    contact = ''
    if phone_matches:
        contact += f'Phone: {phone_matches[0][0]}-{phone_matches[0][1]}-{phone_matches[0][2]}\n'
    if email_matches:
        contact += f'Email: {email_matches[0]}'

    # Extract the applicant's name
    first_name, last_name = extract_name(text, os.path.basename(file_path))

    # Check if the first text in the email address is the name
    if email_matches:
        email_name = email_matches[0].split('@')[0].split('.')[0]
        if first_name.lower() in email_name.lower():
            first_name, last_name = first_name, last_name
        else:
            first_name, last_name = email_name.capitalize(), last_name

    # If the name is still unknown, check the file name
    if first_name.lower() == 'unknown' and last_name.lower() == 'unknown':
        first_name, last_name = extract_name_from_file_name(file_path)

    score = "Not Ranked"

    return Applicant(first_name, last_name, contact, text, score)


def process_resumes(resumes_folder: str):
    for root, _, files in os.walk(resumes_folder):
        for file in files:
            if file.startswith('~') or file.startswith('.'):
                continue

            file_path = os.path.join(root, file)
            applicant = extract_applicant_info(file_path)
            if applicant:
                yield applicant
