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
from textblob import Word
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

#The following are synonym groups which can be used to classify the headers.

citation = [Word("citation").synsets[2], Word("reference").synsets[1], Word("cite").synsets[3]]
run = [Word("run").synsets[9],Word("run").synsets[34],Word("execute").synsets[4]]
install = [Word("installation").synsets[0],Word("install").synsets[0],Word("setup").synsets[1],Word("prepare").synsets[0],Word("preparation").synsets[0],Word("manual").synsets[0],Word("guide").synsets[2],Word("guide").synsets[9]]
download = [Word("download").synsets[0]]
requirement = [Word("requirement").synsets[2],Word("prerequisite").synsets[0],Word("prerequisite").synsets[1],Word("dependency").synsets[0],Word("dependent").synsets[0]]
contact = [Word("contact").synsets[9]]
description = [Word("description").synsets[0],Word("description").synsets[1],Word("introduction").synsets[3],Word("introduction").synsets[6],Word("basics").synsets[0],Word("initiation").synsets[1],Word("start").synsets[0],Word("start").synsets[4],Word("started").synsets[0],Word("started").synsets[1],Word("started").synsets[7],Word("started").synsets[8],Word("overview").synsets[0],Word("summary").synsets[0],Word("summary").synsets[2]]
contributor = [Word("contributor").synsets[0]]
documentation = [Word("documentation").synsets[1]]
license = [Word("license").synsets[3],Word("license").synsets[0]]
usage = [Word("usage").synsets[0],Word("example").synsets[0],Word("example").synsets[5],Word("implement").synsets[1],Word("implementation").synsets[1],Word("demo").synsets[1],Word("tutorial").synsets[0],Word("tutorial").synsets[1]]
update = [Word("updating").synsets[0],Word("updating").synsets[3]]
issues = [Word("issues").synsets[0],Word("errors").synsets[5],Word("problems").synsets[0],Word("problems").synsets[2]]
support = [Word("support").synsets[7],Word("help").synsets[0],Word("help").synsets[9],Word("report").synsets[0],Word("report").synsets[6]]



group = dict()
group.update({"citation":citation})
group.update({"download":download})
group.update({"run":run})
group.update({"installation":install})
group.update({"requirement":requirement})
group.update({"contact":contact})
group.update({"description":description})
group.update({"contributor":contributor})
group.update({"documentation":documentation})
group.update({"license":license})
group.update({"usage":usage})
group.update({"update":update})
group.update({"issues":issues})
group.update({"support":support})


def find_sim(wordlist,wd): #returns the max probability between a word 'wd' and group 'wordlist'
    simvalue = []
    for sense in wordlist: #we iterate over every sense of a given word and match it against our wordlist
        if(wd.path_similarity(sense)!=None): 
            simvalue.append(wd.path_similarity(sense))
    if(len(simvalue)!=0):
        return max(simvalue)
    else:
        return 0
    

def match_group(word_syn,group,threshold): #selects group which best matches with a given word
    currmax = 0
    maxgroup = "" #this is the group that has best been matched with a given header
    simvalues = dict()
    for sense in word_syn: #for a given sense of a word as defined by the specific synset
        similarities = [] #mapping similarity between a synset value and a given group 
        for key, value in group.items(): #value has all the similar words
            path_sim = find_sim(value,sense) #this tells us how well the word has matched to a GROUP, not a specific word within the group
#             print("Similarity to", key, "is:",path_sim)
            if(path_sim>threshold): #we consider only the words that match above our given threshold
                if(path_sim>currmax):
                    maxgroup = key
                    currmax = path_sim

    return maxgroup


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

    # Clean the content
    df['Content'] = df['Content'].str.split("[\n]+", n=1, expand=True)[1]
    df['Header'] = df['Header'].str.replace('#', '')

    # Stemming and remove the stopwords
    df['Token'] = df['Header'].apply(lambda x: stemTitle(x))

    # Extract categories
    df['Tag'] = 'unknown'
    # ##installation
    # install_filter = (df['Token'].str.len() < 40) & (df['Token'].str.contains("instal"))   
    # df.loc[install_filter, ['Tag']] = 'installation'
    # ##description
    # description_filter = (df['Token'].str.len() < 40) & (df['Token'].str.contains("introduct"))
    # df.loc[description_filter, ['Tag']] = 'description'
    # ##citation
    # citation_filter = (df['Token'].str.len() < 20) & (df['Token'].str.contains("refer|citat|public"))
    # df.loc[citation_filter, ['Tag']] = 'citation'
    # ##license
    # license_filter = (df['Token'].str.len() < 40) & (df['Token'].str.contains("licens"))
    # df.loc[license_filter, ['Tag']] = 'license'
    # ##document
    # document_filter = (df['Token'].str.len() < 40) & (df['Token'].str.contains("document"))
    # df.loc[document_filter, ['Tag']] = 'document'
    # ##acknowledge
    # acknowledg_filter = (df['Token'].str.len() < 40) & (df['Token'].str.contains("acknowledg"))
    # df.loc[acknowledg_filter, ['Tag']] = 'acknowledgement'
    # ##prerequisite
    # prereq_filter = (df['Token'].str.len() < 40) & (df['Token'].str.contains("prerequisit|requir|depend"))
    # df.loc[prereq_filter, ['Tag']] = 'prerequisite'
    # ##example
    # example_filter = (df['Token'].str.len() < 60) & (df['Token'].str.contains("exampl|demo"))
    # df.loc[example_filter, ['Tag']] = 'example'
    # # contribution
    # contribute_filter = (df['Token'].str.len() < 40) & (df['Token'].str.contains("contribut"))
    # df.loc[contribute_filter, ['Tag']] = 'contribution'

    cat = pd.DataFrame(columns = ['Content','Tag'])
    for index, row in df.iterrows():
        sent = row['Header'].split(" ")
        for s in sent:
            synn = Word(s).synsets
            if(len(synn)>0):
                bestgroup = match_group(synn,group,0.8)
                if(bestgroup!=""):
                    row['Tag']=bestgroup
                    cat = cat.append({'Content':row['Content'],'Tag':bestgroup}, ignore_index=True)

   
    # cat = df.loc[(isinstance(df['Tag'], (list, tuple)) and df['Tag'][0] != 'unknown'), ['Content', 'Tag']]
    cat['confidence'] = [[1]] * len(cat)
    cat.rename(columns={'Content': 'excerpt'}, inplace=True)
    cat_json = cat.groupby('Tag')['excerpt', 'confidence'].apply(lambda x: x.to_dict('r')).to_dict()

    # strings without tag
    str_list = df[df['Tag'] == 'unknown']['Content'].tolist()

    return cat_json, str_list
