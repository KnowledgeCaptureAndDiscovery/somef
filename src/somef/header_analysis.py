## Main function: header_analysis(text)
## input file: readme files text data
## output file: json files with categories extracted using header analysis; other text data cannot be extracted
import re
import string

import numpy as np
import pandas as pd
from textblob import Word

from . import parser_somef

pd.options.mode.chained_assignment = None  # default='warn'

# Define wordnet groups
group = dict()

#Word("citation").synsets[2] -> Includes ack, which is not the right sense
citation = [Word("citation").synsets[3],Word("reference").synsets[1], Word("cite").synsets[3]]
group.update({"citation": citation})

ack = [Word("acknowledgement").synsets[0]]
group.update({"acknowledgement": ack})

run = [Word("run").synsets[9], Word("run").synsets[34], Word("execute").synsets[4]]
group.update({"run": run})

install = [Word("installation").synsets[0], Word("install").synsets[0], Word("setup").synsets[1],
           Word("prepare").synsets[0], Word("preparation").synsets[0], Word("manual").synsets[0],
           Word("guide").synsets[2], Word("guide").synsets[9]]
group.update({"installation": install})

download = [Word("download").synsets[0]]
group.update({"download": download})

requirement = [Word("requirement").synsets[2], Word("prerequisite").synsets[0], Word("prerequisite").synsets[1],
               Word("dependency").synsets[0], Word("dependent").synsets[0]]
group.update({"requirement": requirement})

contact = [Word("contact").synsets[9]]
group.update({"contact": contact})

description = [Word("description").synsets[0], Word("description").synsets[1],
               Word("introduction").synsets[3], Word("introduction").synsets[6],
               Word("basics").synsets[0],
               Word("initiation").synsets[1],
#               Word("overview").synsets[0],
               Word("summary").synsets[0], Word("summary").synsets[2]]
group.update({"description": description})

contributor = [Word("contributor").synsets[0]]
group.update({"contributor": contributor})

documentation = [Word("documentation").synsets[1]]
group.update({"documentation": documentation})

license = [Word("license").synsets[3], Word("license").synsets[0]]
group.update({"license": license})

usage = [Word("usage").synsets[0], Word("example").synsets[0], Word("example").synsets[5],
         #Word("implement").synsets[1],Word("implementation").synsets[1],
         Word("demo").synsets[1], Word("tutorial").synsets[0],
         Word("tutorial").synsets[1],
         Word("start").synsets[0], Word("start").synsets[4], Word("started").synsets[0],
         Word("started").synsets[1], Word("started").synsets[7], Word("started").synsets[8]]
group.update({"usage": usage})

#update = [Word("updating").synsets[0], Word("updating").synsets[3]]
#group.update({"update": update})

# Needs to be revisited
#Word("issues").synsets[0],
faq = [Word("errors").synsets[5], Word("problems").synsets[0],
          Word("problems").synsets[2], Word("faq").synsets[0]]
group.update({"faq": faq})

support = [Word("support").synsets[7], Word("help").synsets[0], Word("help").synsets[9], Word("report").synsets[0],
           Word("report").synsets[6]]
group.update({"support": support})


def extract_bash_code(text):
    splitted = text.split("```")
    output = []
    if (len(splitted)>=3):
        for index, value in enumerate(splitted):
            if index%2 == 1:
                output.append(splitted[index])
    return output


def extract_header_content(text):  # extract the header and content of text to dataframe
    print('Extracting headers and content.')
    header = []
    headers = parser_somef.extract_headers(text)
    for key in headers.keys():
        if headers[key]:
            header.append(key)
    content = parser_somef.extract_content_per_header(text, headers)
    parent_headers = parser_somef.extract_headers_parents(text)
    # into dataframe
    df = pd.DataFrame(columns=['Header', 'Content', 'ParentHeader'])
    for i, j in zip(header, content):
        df = df.append({'Header': i, 'Content': j, 'ParentHeader': parent_headers[i]}, ignore_index=True)
    df['Content'].replace('', np.nan, inplace=True)
    df.dropna(subset=['Content'], inplace=True)
    return df


def find_sim(wordlist, wd):
    """
    Function that returns the max probability between a word and subgroup
    Parameters
    ----------
    wordlist
    wd

    Returns
    -------

    """
    sim_value = []
    for sense in wordlist:
        if (wd.path_similarity(sense) != None):
            sim_value.append(wd.path_similarity(sense))
    if (len(sim_value) != 0):
        return max(sim_value)
    else:
        return 0


def match_group(word_syn, group, threshold):  # match a word with a subgroup
    currmax = 0
    maxgroup = ""
    simvalues = dict()
    for sense in word_syn:  # for a given sense of a word
        similarities = []
        for key, value in group.items():  # value has all the similar words
            path_sim = find_sim(value, sense)
            # print("Similarity is:",path_sim)
            if (path_sim > threshold):  # then append to the list
                if (path_sim > currmax):
                    maxgroup = key
                    currmax = path_sim
    return maxgroup


def label_header(header):  # label the header with a subgroup
    # remove punctuation
    header_clean = header.translate(str.maketrans('', '', string.punctuation))
    sentence = header_clean.strip().split(" ")
    label = []
    for s in sentence:
        synn = Word(s).synsets
        if (len(synn) > 0):
            bestgroup = match_group(synn, group, 0.8)
            if (bestgroup != "" and bestgroup not in label):
                label.append(bestgroup)
    return label

def label_parent_headers(parentHeaders):  # label the header with a subgroup
    header = ""
    for value in parentHeaders:
        header += value + " "
    # remove punctuation
    header_clean = header.translate(str.maketrans('', '', string.punctuation))
    sentence = header_clean.strip().split(" ")
    label = []
    for s in sentence:
        synn = Word(s).synsets
        if (len(synn) > 0):
            bestgroup = match_group(synn, group, 0.8)
            if (bestgroup != "" and bestgroup not in label):
                label.append(bestgroup)
    return label


def clean_html(text):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', text)
    return cleantext


def extract_categories_using_headers(text):  # main function
    #remove call to clean_html to solve GitHub issues 139 and 89
    #text = clean_html(text)
    data = extract_header_content(text)
    print('Labeling headers.')
    if data.empty:
        print("File to analyze has no headers")
        return {}, [text]
    data['Group'] = data['Header'].apply(lambda row: label_header(row))
    data['GroupParent'] = data['ParentHeader'].apply(lambda row: label_parent_headers(row))
    for i in data.index:
        if len(data['Group'][i]) == 0 and len(data['GroupParent'][i]) > 0:
            data.at[i, 'Group'] = data['GroupParent'][i]
    data = data.drop(columns=['GroupParent'])
    if len(data['Group'].iloc[0]) == 0:
        data['Group'].iloc[0] = ['unknown']
    groups = data.apply(lambda x: pd.Series(x['Group']), axis=1).stack().reset_index(level=1, drop=True)

    groups.name = 'Group'
    data = data.drop('Group', axis=1).join(groups)
    if data['Group'].iloc[0] == 'unknown':
        data['Group'].iloc[0] = np.NaN

    # to json
    group = data.loc[(data['Group'] != 'None') & pd.notna(data['Group'])]
    #group = group.reindex(columns=['Content', 'Group'])
    group['confidence'] = [[1]] * len(group)
    group.rename(columns={'Content': 'excerpt'}, inplace=True)
    group.rename(columns={'Header': 'originalHeader'}, inplace=True)
    group.rename(columns={'ParentHeader': 'parentHeader'}, inplace=True)
    group['technique'] = 'Header extraction'
    #group['original header'] = 'NaN'
    group_json = group.groupby('Group').apply(lambda x: x.to_dict('r')).to_dict()
    for key in group_json.keys():
        for ind in range(len(group_json[key])):
            del group_json[key][ind]['Group']

    # for key in group_json.keys():
    #     for ind in range(len(group_json[key])):
    #         print(group_json[key][ind]['excerpt'])

    print('Converting to json files.')

    # strings without tag (they will be classified)
    str_list = data.loc[data['Group'].isna(), ['Content']].values.squeeze().tolist()
    if type(str_list) != list:
        str_list = [str_list]

    # remove empty field parentHeader
    for key in group_json.keys():
        elements = group_json[key]
        new_elements = []
        for element in elements:
            if element['parentHeader'] == "":
                del element['parentHeader']
            new_elements.append(element)
        group_json[key] = new_elements

    return group_json, str_list
