
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import LabelEncoder
from nltk.corpus import stopwords
from sklearn.svm import SVC
from collections import defaultdict
from sklearn.metrics import precision_score, recall_score
import nlpaug.augmenter.word as naw
from fairlearn.metrics import demographic_parity_difference, equalized_odds_difference, demographic_parity_ratio, false_negative_rate



def model(X_train, y_train):
    # Initialize the SVC classifier
    clf = SVC(kernel='linear', C=1.0)

    # Fit the classifier to the transformed training data
    clf.fit(X_train, y_train)
    return clf

def predict(clf, X_test):
    return clf.predict(X_test)
    
def score(y_test, y_pred):
    # Compute precision and recall
    precision = precision_score(y_test, y_pred, average='weighted')
    recall = recall_score(y_test, y_pred, average='weighted')

    # Print the results
    print('Precision:', precision)
    print('Recall:', recall)

def augment_df(df):
    # Create a list of unique categories
    categories = df['Category'].unique().tolist()

    # Create an augmenter object
    aug = naw.SynonymAug(aug_src='wordnet', lang='eng')

    # Augment each resume in the dataset for each category
    augmented_data = []
    for category in categories:
        category_data = df[df['Category'] == category]
        for resume in category_data['Resume'].values:
            augmented_resume = aug.augment(resume)[0]
            if resume != augmented_resume:
                print("Different")
            augmented_data.append((category, augmented_resume))

    # Convert the augmented data to a DataFrame
    augmented_df = pd.DataFrame(augmented_data, columns=['Category', 'Resume'])
    return augmented_df


def get_most_common_words(X, feature_names):
    word_count = X.sum(axis=0)
    word_count_df = pd.DataFrame({'word': feature_names, 'count': word_count.tolist()[0]})
    word_count_df = word_count_df.sort_values('count', ascending=False).reset_index(drop=True)
    print(word_count_df)


def get_labels_stats(df):
    categories = df['Category'].value_counts().reset_index()
    print(categories)


def get_fairness_score(mapping, y_test, y_pred, X_test):
    print("Fairness test:")
    # Calculate the equalized odds difference on the test set
    hash = defaultdict(int)
    for category, label in mapping.items():
        hash[category] = np.count_nonzero(y_pred == label)
    dp_diff = demographic_parity_difference(y_test, y_pred, sensitive_features=X_test.index)

    # eod = equalized_odds_difference(y_test, y_pred, sensitive_features=df['Category'].unique())
    print('disparity difference: ', hash, hash['Data Science'])


def count_frequent_words_top_10_cat():
    # load the data
    df = pd.read_csv('resume_dataset.csv')

    # create a CountVectorizer object
    vectorizer = CountVectorizer(stop_words='english')

    # compute word frequencies for each category
    for category in df['Category'].unique():
        # get all resumes in this category
        category_data = df[df['Category'] == category]
        
        # fit the vectorizer to the resumes in this category
        X = vectorizer.fit_transform(category_data['Resume'])
        
        # compute the sum of word frequencies for each word
        word_freq = X.sum(axis=0)
        
        # get the feature names (i.e. the words)
        feature_names = vectorizer.get_feature_names()
        
        # sort the words by frequency
        sorted_word_freq = sorted(zip(feature_names, word_freq.tolist()[0]), key=lambda x: x[1], reverse=True)
        
        # print the top 10 words for this category
        print(f"Category: {category}")
        for word, freq in sorted_word_freq[:10]:
            print(f"\t{word}: {freq}")

def get_model():
    df= pd.read_csv('./ml/UpdatedResumeDataSet.csv',index_col=None,)
    # df = augment_df(df)
    stop_words = set(stopwords.words('english'))
    vectorizer = CountVectorizer(stop_words=stop_words)
    encoder = LabelEncoder()

    print("Get most common categories:")
    get_labels_stats(df)

    # get the feature names
    shuffled_df = df.sample(frac=1)
    print(df)
    X = vectorizer.fit_transform(shuffled_df.Resume.values)
    y = encoder.fit_transform(shuffled_df.Category.values)
    mapp = {y_val: cat_val for y_val, cat_val in zip(y, shuffled_df.Category.values)}
    mapping = dict(zip(encoder.classes_, range(len(encoder.classes_))))
    feature_names = vectorizer.get_feature_names_out()
    
    print("Get most common words:")
    get_most_common_words(X, feature_names)
   
    print("Get the model.")
    # print the tokenized resume content

    print("Initial test:")
    for percent in np.linspace(0.5, 0.9, 10):
        print("-"*5)
        print("Percent train is", percent)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1 - percent)
        clf = model(X_train, y_train)
        y_pred = predict(clf, X_test)
        score(y_test, y_pred)
        # assuming y_true and y_pred are your true and predicted labels, respectively
        cm = confusion_matrix(y_test, y_pred)
        # plot the confusion matrix as an image
        plt.imshow(cm, cmap='binary')

        # add labels for the x and y axes
        plt.xlabel('Predicted')
        plt.ylabel('True')
        # add a colorbar to show the scale of the values
        plt.colorbar()
        # add the values of the confusion matrix to the image
        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                plt.text(i, j, cm[i, j], ha='center', va='center')
                if i != j and cm[i, j] > 0:
                    print("True: {}, pred: {}, number of false positives: {}".format(mapp[i], mapp[j],cm[i, j]))

        x1 = sorted(mapp.keys())
        x2 = [mapp[xi] for xi in x1]

        plt.yticks(x1, x2)
        print("-"*5)
    # show the image
    # plt.show()

    get_fairness_score(mapping, y_test, y_pred, X_test)

    return clf,feature_names, X_train, X_test, y_train, y_test


