# import docx
# import re
from model import get_model
import pandas as pd
from nltk import download
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

# download('stopwords')

# # Extract text from docx file
# document = docx.Document('./Resumes/Akhil.profile.docx')
# text = '\n'.join([paragraph.text for paragraph in document.paragraphs])

# # Preprocess text
# text = text.lower()
# text = re.sub(r'\d+', '', text)
# text = re.sub(r'[^\w\s]', '', text)
# stop_words = set(stopwords.words('english'))
# text = ' '.join([word for word in text.split() if word not in stop_words])

# get the model 
clf, feature_names, X_train, X_test, y_train, y_test = get_model()


# Plan to preprocess the data and get everything out for the UI
