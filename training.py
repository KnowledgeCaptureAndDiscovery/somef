# training.py
# parameters: 
## category: {description, installation, invocation, citation}
## model_name
# output:
## to console: Classification Report
## to SM2KG/models/`model_name`: pickled model

#Constants:
categories = ('description', 'installation', 'invocation', 'citation')

import argparse
import random
import pandas as pd
from nltk.corpus import treebank
from sklearn.model_selection import train_test_split

argparser = argparse.ArgumentParser(description=f"Train binary classifier for one of categories: {categories}.")
argparser.add_argument('-c', '--category', choices=categories, required=True, help='category in question')
argparser.add_argument('-o', '--output', help='output pickled model')
argv = argparser.parse_args()
selected_category = argv.category
categories_df = {cat : pd.read_csv(f"./data/{cat}.csv") for cat in categories}

negative_sample_size = int(len(categories_df[selected_category]) / 5)
#print("Collecting {} {} samples and 5 * {} negative samples".format(len(categories_df[selected_category]), selected_category, negative_sample_size))
for category in categories_df:
    categories_df[category].drop('URL', 1, inplace=True)
    if category != selected_category:
        categories_df[category] = categories_df[category].sample(negative_sample_size)
    categories_df[category] = categories_df[category].assign(**{selected_category: category == selected_category})
    print("{} has {} samples;".format(category, len(categories_df[category])))
    print(categories_df[category].head())
treebank_background = pd.DataFrame(map(lambda sent: ' '.join(sent), random.sample(list(treebank.sents()), negative_sample_size)), columns=["excerpt"]).assign(description=False)
print("Treebank has {} samples.".format(len(treebank_background)))
print("categories_df")
corpus = pd.concat(categories_df.values(), ignore_index=True)
corpus.append(treebank_background, ignore_index=True)
corpus.dropna(0, inplace=True)
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

if argv.output is not None:
    out_file = argv.output
else:
    out_file = f'models/{selected_category}.sk'
print(f"Saving model to {out_file}")
import pickle
pickle.dump(pipeline, open(out_file, 'wb+'))