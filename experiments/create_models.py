import random
import pandas as pd
import pickle
import nltk
import numpy as np
import shutil
nltk.download('treebank')
from nltk.corpus import treebank
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import BernoulliNB
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import Perceptron
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from xgboost.sklearn import XGBClassifier
from sklearn.metrics import make_scorer, accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split, cross_val_score, cross_validate, StratifiedKFold
from sklearn.pipeline import make_pipeline
from setup_corpus import build_corpora

categories = ('citation', 'description', 'installation', 'invocation')
description_df = pd.read_csv('./training_corpus/description.csv')
installation_df = pd.read_csv('./training_corpus/installation.csv')
invocation_df = pd.read_csv('./training_corpus/invocation.csv')
citation_df = pd.read_csv('./training_corpus/citation.csv')
corpora = build_corpora()
scoring = {'accuracy' : make_scorer(accuracy_score),
           'precision' : make_scorer(precision_score),
           'recall' : make_scorer(recall_score),
           'f1_score' : make_scorer(f1_score)}
pipelines = {
    'cvbb': make_pipeline(CountVectorizer(), BernoulliNB()),
    'cvlr': make_pipeline(CountVectorizer(), LogisticRegression(solver='liblinear')),
    'cvnb': make_pipeline(CountVectorizer(), MultinomialNB()),
    'tfada': make_pipeline(TfidfVectorizer(), AdaBoostClassifier()),  #(max_depth=3, random_state=0))
    'tfdtc': make_pipeline(CountVectorizer(), DecisionTreeClassifier()),
    'tflr': make_pipeline(TfidfVectorizer(), LogisticRegression(solver='liblinear')),
    'tfnb': make_pipeline(TfidfVectorizer(), MultinomialNB()),
    'tfper': make_pipeline(TfidfVectorizer(), Perceptron(tol=1e-3, random_state=0)),
    'tfrfc': make_pipeline(TfidfVectorizer(), RandomForestClassifier()),  #(max_depth=3, random_state=0))
    'tfsgd': make_pipeline(TfidfVectorizer(), SGDClassifier(loss='log')),
    'tfxgb': make_pipeline(TfidfVectorizer(), XGBClassifier(use_label_encoder=False,eval_metric="logloss"))
}
evaluation_names = ('cvlr', 'tflr', 'tfnb', 'cvnb', 'cvbb', 'tfsgd', 'tfxgb', 'tfper', 'tfrfc', 'tfdtc', 'tfada')
evaluation_text = {
    'cvbb': '"sklearnpipeline(CountVectorizer, BernoulliBayes)", -,Allen,',
    'cvlr': '"sklearnpipeline(CountVectorizer, LogisticRegression)", - ,Allen,',
    'cvnb': '"sklearnpipeline(CountVectorizer, NaiveBayes)", -,Allen,',
    'tfada': '"sklearnpipeline(TFIDFVectorizer, AdaBoostClassifier)", -,Allen,',
    'tfdtc': '"sklearnpipeline(TFIDFVectorizer, DecisionTreeClassifier)", -,Allen,',
    'tflr': '"sklearnpipeline(TFIDFVectorizer, LogisticRegression)", - ,Allen,',
    'tfnb': '"sklearnpipeline(TFIDFVectorizer, NaiveBayes)", - ,Allen,',
    'tfper': '"sklearnpipeline(TFIDFVectorizer, Perceptron)", -,Allen,',
    'tfrfc': '"sklearnpipeline(TFIDFVectorizer, RandomForestClassifier)", -,Allen,',
    'tfsgd': '"sklearnpipeline(TFIDFVectorizer, StochasticGradientDescent)",loss = \'log\',Allen,',
    'tfxgb': '"sklearnpipeline(TFIDFVectorizer, XGBClassifier)", -,Allen,'
}

def evaluate_category(corpora,category):
    dec = 3
    cv = StratifiedKFold(n_splits = 5, shuffle=True)
    file_content = "sklearn Primitive - Citation,Hyperparameters,Input Data Used,Accuracy,Precision,Recall,F-measure,Pickle ID"
    limit =  0.0
    file_to_copy = ""
    for name in evaluation_text:
        X = corpora[category].excerpt
        Y = corpora[category][category]
        #print(X)
        for e in X:
            print(e)
        #Y = Y.astype(int)
        x_train, x_test, y_train, y_test = train_test_split(X, Y, stratify=Y, test_size=0.2)
        pipeline = pipelines[name]
        pipeline.fit(x_train, y_train)
        title = "./trained_models/" + category[:3] + name + ".p"
        print(title)
        pickle.dump(pipeline, open(title, 'wb+'))
        scores = cross_validate(pipeline, X, Y, cv=cv, scoring=scoring)
        file_content = file_content + "\n" + evaluation_text[name] + np.format_float_positional(np.around(scores["test_accuracy"].mean(), decimals=dec)) + "," + np.format_float_positional(np.around(scores["test_precision"].mean(), decimals=dec)) + "," + np.format_float_positional(np.around(scores["test_recall"].mean(), decimals=dec)) + "," + np.format_float_positional(np.around(scores["test_f1_score"].mean(), decimals=dec)) + "," + category[:3] + name + ".p"
        if np.around(scores["test_f1_score"].mean(), decimals=dec) > limit:
            limit = np.around(scores["test_f1_score"].mean(), decimals=dec)
            file_to_copy = "./trained_models/" + category[:3] + name + ".p"

    category_title = "./ranking/" + category + "_classifier.csv"
    f = open(category_title, 'w')
    f.write(file_content)
    shutil.copy(file_to_copy,"../src/somef/models/"+category+".p")


if __name__ == '__main__':
    print("Number of description entries: {}".format(len(description_df)))
    description_df.head()
    print("Number of installation entries: {}".format(len(installation_df)))
    installation_df.head()
    print("Number of invocation entries: {}".format(len(invocation_df)))
    invocation_df.head()
    print("Number of citation entries: {}".format(len(citation_df)))
    citation_df.head()
    for category in categories:
        print()
        print("###### Creating " + category + " model ######")
        evaluate_category(corpora, category)


