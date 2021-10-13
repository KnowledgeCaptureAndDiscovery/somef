#!/usr/bin/python
# build_corpus.py

import random
import pandas as pd
from nltk.corpus import treebank

categories = ('description', 'installation', 'invocation', 'citation')


def build_corpora():
    corpora = {}
    for cat in categories:
        corpora[cat] = build_corpus(cat)
    return corpora


def build_corpus(selected_category):
    categories_df = {cat: pd.read_csv(f'./training_corpus/{cat}.csv') for cat in categories}
    negative_sample_size = int(len(categories_df[selected_category]) / 4)
    print(f"Selected Category: {selected_category}")
    for category in categories_df:
        categories_df[category].drop('URL', 1, inplace=True)
        if category != selected_category:
            categories_df[category] = categories_df[category].sample(negative_sample_size)
        categories_df[category] = categories_df[category].assign(**{selected_category: category == selected_category})
        print("{} has {} samples;".format(category, len(categories_df[category])))
        # print(categories_df[category].head())
    treebank_background = pd.DataFrame(
        map(lambda sent: ' '.join(sent), random.sample(list(treebank.sents()), negative_sample_size)),
        columns=["excerpt"]).assign(description=False)
    # print("Treebank has {} samples.".format(len(treebank_background)))
    # print("categories_df")
    corpus = pd.concat(categories_df.values(), ignore_index=True, sort=False)
    corpus.append(treebank_background, ignore_index=True, sort=False)
    corpus.fillna(value='', inplace=True)
    return corpus

