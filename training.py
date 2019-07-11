# training.py
# parameters: 
## category: {description, installation, invocation, citation}
## model_name
# output:
## to console: Classification Report
## to SM2KG/models/model_name: pickled model

#Constants:
categories = ('description', 'installation', 'invocation', 'citation')

import argparse
import random
import pandas as pd
from nltk.corpus import treebank
from sklearn.model_selection import train_test_split

argparser = argparse.ArgumentParser(description=f"Train binary classifier for one of categories: {categories}.")
argparser.add_argument('-c', '--category', choices=categories, required=True, help='category in question')
argv = argparser.parse_args()
selected_category = argv.category
categories_df = {cat : pd.read_csv(f"./data/{cat}.csv") for cat in categories}


# in this case: equal representation from all categories
entries_per_category = min(list(map(lambda df: len(df), categories_df.keys())))
treebank_background = pd.DataFrame(list(map(lambda sent: ' '.join(sent), random.sample(list(treebank.sents()), entries_per_category))), columns=["excerpt"]).assign(description=False)
corpus = pd.concat([categories_df[category].assign(**{selected_category: category == selected_category}) for category in categories_df.keys()])
corpus.dropna(0, inplace=True)
corpus.reset_index(drop=True, inplace=True)
print(corpus)

X, y = corpus.excerpt, corpus[selected_category]
X_train, X_test, y_train, y_test = train_test_split(X, y)

# ## Count Vectorizer and Logistic Regression in Pipeline

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report

def display_accuracy_score(y_test, y_pred_class):
    score = accuracy_score(y_test, y_pred_class)
    print('accuracy score: %s' % '{:.2%}'.format(score))
    return score
def display_null_accuracy(y_test):
    value_counts = pd.value_counts(y_test)
    null_accuracy = max(value_counts) / float(len(y_test))
    print('null accuracy: %s' % '{:.2%}'.format(null_accuracy))
    return null_accuracy

def display_accuracy_difference(y_test, y_pred_class):
    null_accuracy = display_null_accuracy(y_test)
    accuracy_score = display_accuracy_score(y_test, y_pred_class)
    difference = accuracy_score - null_accuracy
    if difference > 0:
        print('model is %s more accurate than null accuracy' % '{:.2%}'.format(difference))
    elif difference < 0:
        print('model is %s less accurate than null accuracy' % '{:.2%}'.format(abs(difference)))
    elif difference == 0:
        print('model is exactly as accurate as null accuracy')
    return null_accuracy, accuracy_score

pipeline = make_pipeline(CountVectorizer(), LogisticRegression())
pipeline.fit(X_train, y_train)

y_pred_class = pipeline.predict(X_test)
y_pred_vals = pipeline.predict_proba(X_test)
#print(y_pred_vals)
#print("X_test: {}, y_pred: {}".format(X_test, y_pred_class))
#results_df = pd.DataFrame({"x_test": X_test, "y_pred": y_pred_vals[:,1], "y_TF_pred": y_pred_class, "y_actual": y_test})
results_df = pd.DataFrame({"x_test": X_test,  "y_TF_pred": y_pred_class, "y_actual": y_test})
print(results_df)
print(confusion_matrix(y_test, y_pred_class))
print('-' * 75 + '\nClassification Report\n')
print(classification_report(y_test, y_pred_class))
display_accuracy_difference(y_test, y_pred_class)