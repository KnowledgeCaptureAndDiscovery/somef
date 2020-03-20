## input file: readme files text data
## output file: json files with categories extracted using header analysis; other text data cannot be extracted

import os
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import string
import collections
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

def stemTitle(title):
    porter=PorterStemmer()
    token_words=word_tokenize(title)
    stop_words = set(stopwords.words('english'))
    token_words
    stem_title=[]
    for word in token_words:
        if word not in stop_words:
            stem_title.append(porter.stem(word))
            stem_title.append(" ")
    return "".join(stem_title)


def extract_categories_using_headers(text):
    # Extract header and content
    a = re.findall('\`\`\`[^\`]+\`\`\`', text, flags=re.DOTALL)
    a_sub = [re.sub('#', '#notes:', i) for i in a]
    for i, j in zip(a, a_sub):
        text = text.replace(i, j)
    Header = re.findall('#{1,5} .*', text)
    content = re.split('#{1,5} .*', text)
    Content = [re.sub('#notes', '#', i) for i in content]
    # if len(Header)>0:
    #     Content.pop(0)
    Header.insert(0,"initial page content")
    df = pd.DataFrame(columns=['Header', 'Content'])
    for i, j in zip(Header, Content):
        df = df.append({'Header': i, 'Content': j}, ignore_index=True)

    print(df)
    # Clean the content
    df['Content'] = df['Content'].str.split("[\n]+", n=1, expand=True)[1]
    df['Header'] = df['Header'].str.replace('#', '')

    # Stemming and remove the stopwords
    df['Token'] = df['Header'].apply(lambda x: stemTitle(x))

    # Extract categories
    df['Tag'] = 'unknown'
    ##installation
    install_filter = (df['Token'].str.len() < 40) & (df['Token'].str.contains("instal"))   
    df.loc[install_filter, ['Tag']] = 'installation'
    ##description
    description_filter = (df['Token'].str.len() < 40) & (df['Token'].str.contains("introduct"))
    df.loc[description_filter, ['Tag']] = 'description'
    ##citation
    citation_filter = (df['Token'].str.len() < 20) & (df['Token'].str.contains("refer|citat|public"))
    df.loc[citation_filter, ['Tag']] = 'citation'
    ##license
    license_filter = (df['Token'].str.len() < 40) & (df['Token'].str.contains("licens"))
    df.loc[license_filter, ['Tag']] = 'license'
    ##document
    document_filter = (df['Token'].str.len() < 40) & (df['Token'].str.contains("document"))
    df.loc[document_filter, ['Tag']] = 'document'
    ##acknowledge
    acknowledg_filter = (df['Token'].str.len() < 40) & (df['Token'].str.contains("acknowledg"))
    df.loc[acknowledg_filter, ['Tag']] = 'acknowledgement'
    ##prerequisite
    prereq_filter = (df['Token'].str.len() < 40) & (df['Token'].str.contains("prerequisit|requir|depend"))
    df.loc[prereq_filter, ['Tag']] = 'prerequisite'
    ##example
    example_filter = (df['Token'].str.len() < 60) & (df['Token'].str.contains("exampl|demo"))
    df.loc[example_filter, ['Tag']] = 'example'
    # contribution
    contribute_filter = (df['Token'].str.len() < 40) & (df['Token'].str.contains("contribut"))
    df.loc[contribute_filter, ['Tag']] = 'contribution'
   
    # to json
    cat = df.loc[(df['Tag'] != 'unknown'), ['Content', 'Tag']]
    cat['confidence'] = [[1]] * len(cat)
    cat.rename(columns={'Content': 'excerpt'}, inplace=True)
    cat_json = cat.groupby('Tag')['excerpt', 'confidence'].apply(lambda x: x.to_dict('r')).to_dict()

    # strings without tag
    str_list = df[df['Tag'] == 'unknown']['Content'].tolist()

    return cat_json, str_list
