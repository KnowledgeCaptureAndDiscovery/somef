import random
import pandas as pd
import pickle
import nltk
import numpy as np
import shutil
nltk.download('treebank')
from nltk.corpus import treebank
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
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

def evaluate_category(corpora,pipeline,category):
    dec = 3
    cv = StratifiedKFold(n_splits = 5, shuffle=True)
    file_content = "sklearn Primitive - Citation,Hyperparameters,Input Data Used,Accuracy,Precision,Recall,F-measure,Pickle ID"
    limit =  0.0
    file_to_copy = ""
    for name in evaluation_names:
        X = corpora[category].excerpt
        Y = corpora[category][category]
        x_train, x_test, y_train, y_test = train_test_split(X, Y, stratify=Y, test_size=0.2)
        pipeline.fit(x_train, y_train)
        title = "./trained_models/" + category[:3] + name + ".p"
        print(title)
        pickle.dump(pipeline, open(title, 'wb+'))
        scores = cross_validate(pipeline, X, Y, cv=cv, scoring=scoring)
        file_content = file_content + "\n" + evaluation_text[name] + np.format_float_positional(np.around(scores["test_accuracy"].mean(), decimals=dec)) + "," + np.format_float_positional(np.around(scores["test_precision"].mean(), decimals=dec)) + "," + np.format_float_positional(np.around(scores["test_recall"].mean(), decimals=dec)) + "," + np.format_float_positional(np.around(scores["test_f1_score"].mean(), decimals=dec)) + "," + category[:3] + name + ".p"
        if (np.around(scores["test_f1_score"].mean(), decimals=dec) > limit):
            limit = np.around(scores["test_f1_score"].mean(), decimals=dec)
            file_to_copy = "./trained_models/" + category[:3] + name + ".p"

    category_title = "./ranking/" + category + "_classifier.csv"
    f = open(category_title, 'w')
    f.write(file_content)
    shutil.copy(file_to_copy,"../src/somef/models/"+category+".p")


if __name__ == '__main__':
    print("Number of description entries: {}".format(len(description_df)))
    print("Number of installation entries: {}".format(len(installation_df)))
    print("Number of invocation entries: {}".format(len(invocation_df)))
    print("Number of citation entries: {}".format(len(citation_df)))
    description_df.head()
    pipeline = make_pipeline(CountVectorizer(), LogisticRegression(solver='liblinear'))
    for category in categories:
        print()
        print("###### Creating " + category + " model ######")
        evaluate_category(corpora, pipeline, category)


