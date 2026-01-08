import logging
import re
import string

import numpy as np
import pandas as pd
from textblob import Word

from .process_results import Result
from .parser import mardown_parser
from .utils import constants
from typing import Dict, Iterable, List, Tuple
from functools import lru_cache
pd.options.mode.chained_assignment = None  # default='warn'


SIMILARITY_THRESHOLD = 0.8


# Define wordnet groups
group = dict()

# Word("citation").synsets[2] -> Includes ack, which is not the right sense
citation = [Word("citation").synsets[3], Word("reference").synsets[1], Word("cite").synsets[3]]
group.update({constants.CAT_CITATION: citation})

ack = [Word("acknowledgement").synsets[0]]
group.update({constants.CAT_ACKNOWLEDGEMENT: ack})

run = [Word("run").synsets[9], Word("run").synsets[34], Word("execute").synsets[4]]
group.update({constants.CAT_RUN: run})

install = [Word("installation").synsets[0], Word("install").synsets[0], Word("setup").synsets[1],
           Word("prepare").synsets[0], Word("preparation").synsets[0], Word("manual").synsets[0],
           Word("guide").synsets[2], Word("guide").synsets[9]]
group.update({constants.CAT_INSTALLATION: install})

download = [Word("download").synsets[0]]
group.update({constants.CAT_DOWNLOAD: download})

requirement = [Word("requirement").synsets[2], Word("prerequisite").synsets[0], Word("prerequisite").synsets[1],
               Word("dependency").synsets[0], Word("dependent").synsets[0]]
group.update({constants.CAT_REQUIREMENTS: requirement})

contact = [Word("contact").synsets[9]]
group.update({constants.CAT_CONTACT: contact})

description = [Word("description").synsets[0], Word("description").synsets[1],
               Word("introduction").synsets[3], Word("introduction").synsets[6],
               Word("basics").synsets[0],
               Word("initiation").synsets[1],
               #               Word("overview").synsets[0],
               Word("summary").synsets[0], Word("summary").synsets[2]]
group.update({constants.CAT_DESCRIPTION: description})

contributor = [Word("contributor").synsets[0]]
group.update({constants.CAT_CONTRIBUTORS: contributor})

contributing = [Word("contributing").synsets[1]]
group.update({constants.CAT_CONTRIBUTING_GUIDELINES: contributing})

documentation = [Word("documentation").synsets[1]]
group.update({constants.CAT_DOCUMENTATION: documentation})

license = [Word("license").synsets[3], Word("license").synsets[0]]
group.update({constants.CAT_LICENSE: license})

usage = [Word("usage").synsets[0], Word("example").synsets[0], Word("example").synsets[5],
         # Word("implement").synsets[1],Word("implementation").synsets[1],
         Word("demo").synsets[1], Word("tutorial").synsets[0],
         Word("tutorial").synsets[1],
         Word("start").synsets[0], Word("start").synsets[4], Word("started").synsets[0],
         Word("started").synsets[1], Word("started").synsets[7], Word("started").synsets[8]]
group.update({constants.CAT_USAGE: usage})

# update = [Word("updating").synsets[0], Word("updating").synsets[3]]
# group.update({"update": update})

# Needs to be revisited
# Word("issues").synsets[0],
faq = [Word("errors").synsets[5], Word("problems").synsets[0],
       Word("problems").synsets[2], Word("faq").synsets[0]]
group.update({constants.CAT_FAQ: faq})

support = [Word("support").synsets[7], Word("help").synsets[0], Word("help").synsets[9], Word("report").synsets[0],
           Word("report").synsets[6]]
group.update({constants.CAT_SUPPORT: support})

@lru_cache(maxsize=4096)
def get_synsets(word: str):
    """Cached access to WordNet synsets."""
    return Word(word).synsets


@lru_cache(maxsize=16384)
def path_similarity_cached(sense1, sense2) -> float:
    """Cached path similarity lookup."""
    sim = sense1.path_similarity(sense2)
    return sim if sim is not None else 0.0

# def extract_bash_code(text):
#     """Function to detect code blocks"""
#     split = text.split("```")
#     output = []
#     if len(split) >= 3:
#         for index, value in enumerate(split):
#             if index % 2 == 1:
#                 output.append(split[index])
#     return output
def extract_bash_code(text: str) -> List[str]:
    blocks = text.split("```")
    return [blocks[i] for i in range(1, len(blocks), 2)]

# def extract_header_content(text):
#     """Function designed to extract headers and contents of text and place it in a dataframe"""
#     header = []
#     headers = mardown_parser.extract_headers(text)
#     for key in headers.keys():
#         if headers[key]:
#             header.append(key)
#     content, none_header_content = mardown_parser.extract_content_per_header(text, headers)
#     parent_headers = mardown_parser.extract_headers_parents(text)
#     # into dataframe
#     df = pd.DataFrame(columns=['Header', 'Content', 'ParentHeader'])
#     dfs = [pd.DataFrame({'Header': [i], 'Content': [j], 'ParentHeader': [parent_headers.get(i, None)]}) for i, j in
#            zip(header, content)]
#     df = pd.concat(dfs, ignore_index=True)
#     # for i, j in zip(header, content):
#     #     df = df.append({'Header': i, 'Content': j, 'ParentHeader': parent_headers[i]}, ignore_index=True)
#     # df['Content'].replace('', np.nan, inplace=True)
#     df['Content'] = df['Content'].replace('', np.nan)

#     df.dropna(subset=['Content'], inplace=True)
#     return df, none_header_content
def extract_header_content(text: str) -> Tuple[pd.DataFrame, str | None]:
    headers = mardown_parser.extract_headers(text)
    header_list = [h for h, v in headers.items() if v]

    content, none_header_content = mardown_parser.extract_content_per_header(text, headers)
    parents = mardown_parser.extract_headers_parents(text)

    min_len = min(len(header_list), len(content)) 
    header_list = header_list[:min_len] 
    content = content[:min_len]
    
    df = pd.DataFrame({
        'Header': header_list,
        'Content': content,
        'ParentHeader': [parents.get(h) for h in header_list],
    })

    # df['Content'].replace('', np.nan, inplace=True)
    df['Content'] = df['Content'].replace('', np.nan)
    df.dropna(subset=['Content'], inplace=True)

    return df, none_header_content


def find_sim(wordlist, wd):
    """
    Function that returns the max probability between a word and subgroup
    Parameters
    ----------
    wordlist: word group
    wd: input word

    Returns
    -------
    Maximum probability between word and a category
    """
    sim_value = []
    for sense in wordlist:
        if wd.path_similarity(sense) is not None:
            sim_value.append(wd.path_similarity(sense))
    if len(sim_value) != 0:
        return max(sim_value)
    else:
        return 0


# def match_group(word_syn, group, threshold):
#     """Function designed to match a word with a subgroup"""
#     currmax = 0
#     maxgroup = ""
#     simvalues = dict()
#     for sense in word_syn:  # for a given sense of a word
#         similarities = []
#         for key, value in group.items():  # value has all the similar words
#             path_sim = find_sim(value, sense)
#             # print("Similarity is:",path_sim)
#             if path_sim > threshold:  # then append to the list
#                 if path_sim > currmax:
#                     maxgroup = key
#                     currmax = path_sim
#     return maxgroup


def label_header(header):
    """Function designed to label a header with a subgroup"""
    # remove punctuation
    header_clean = header.translate(str.maketrans('', '', string.punctuation))
    sentence = header_clean.strip().split(" ")
    label = []
    for s in sentence:
        synn = Word(s).synsets 
        if len(synn) > 0:
            # bestgroup = match_group(synn, group, 0.8)
            bestgroup = match_group(synn)
            if bestgroup != "" and bestgroup not in label:
                label.append(bestgroup) 
    return label


def label_parent_headers(parentHeaders):
    """label the header with a subgroup"""
    header = ""
    for value in parentHeaders:
        header += value + " "
    # remove punctuation
    header_clean = header.translate(str.maketrans('', '', string.punctuation))
    sentence = header_clean.strip().split(" ")
    label = []
    for s in sentence:
        synn = Word(s).synsets
        if len(synn) > 0:
            # bestgroup = match_group(synn, group, 0.8)
            bestgroup = match_group(synn)
            if bestgroup != "" and bestgroup not in label:
                label.append(bestgroup)
    return label


def clean_html(text):
    """Cleaner function"""
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', text)
    return cleantext


def max_similarity(word_synsets, group_synsets) -> float:
    return max(
        (path_similarity_cached(ws, gs) for ws in word_synsets for gs in group_synsets),
        default=0.0,
    )


WORDNET_GROUPS: Dict[str, List] | None = None


def get_groups() -> Dict[str, List]:
    global WORDNET_GROUPS
    if WORDNET_GROUPS is None:
        WORDNET_GROUPS = build_wordnet_groups()
    return WORDNET_GROUPS

def match_group(word_synsets) -> str:
    best_group = ""
    best_score = 0.0

    for key, synsets in get_groups().items():
        score = max_similarity(word_synsets, synsets)
        if score > SIMILARITY_THRESHOLD and score > best_score:
            best_score = score
            best_group = key

    return best_group


# def tokenize_header(text: str) -> Iterable[str]:
#     clean = text.translate(str.maketrans('', '', string.punctuation))
#     return clean.strip().split()
def tokenize_header(text) -> Iterable[str]: 
    # if list transform to string
    if isinstance(text, list): 
        text = " ".join(map(str, text)) 
    elif text is None: 
        text = "" 
    clean = text.translate(str.maketrans('', '', string.punctuation)) 
    return clean.strip().split()

def label_text(text: str) -> List[str]:
    labels: List[str] = []
    for token in tokenize_header(text):
        synsets = get_synsets(token)
        if synsets:
            grp = match_group(synsets)
            if grp and grp not in labels:
                labels.append(grp)
    return labels
# def extract_categories(repo_data, repository_metadata: Result):
#     """
#     Function that adds category information extracted using header information
#     Parameters
#     ----------
#     @param repo_data: data to use the header analysis
#     @param repository_metadata: Result object with the results found so far in the repo

#     Returns
#     -------
#     @return Result with the information added.
#     """
#     logging.info("Extracting information using headers")
#     if repo_data is None or repo_data == "" or len(repo_data) == 0:
#         return repository_metadata, []
#     try:
#         data, none_header_content = extract_header_content(repo_data)
#         logging.info('Labeling headers.')
#         if data.empty:
#             logging.warning("File to analyze has no headers")
#             return repository_metadata, [repo_data]
#         data['Group'] = data['Header'].apply(lambda row: label_header(row))
#         data['GroupParent'] = data['ParentHeader'].apply(lambda row: label_parent_headers(row))
#         for i in data.index:
#             if len(data['Group'][i]) == 0 and len(data['GroupParent'][i]) > 0:
#                 data.at[i, 'Group'] = data['GroupParent'][i]
#         data = data.drop(columns=['GroupParent'])
#         if len(data['Group'].iloc[0]) == 0:
#             # data['Group'].iloc[0] = ['unknown']
#             data.loc[0, 'Group'] = ['unknown']
#         groups = data.apply(lambda x: pd.Series(x['Group']), axis=1).stack().reset_index(level=1, drop=True)

#         groups.name = 'Group'
#         data = data.drop('Group', axis=1).join(groups)
#         if data['Group'].iloc[0] == 'unknown':
#             # data['Group'].iloc[0] = np.NaN
#             data.loc[0, 'Group'] = np.nan

#         # to json
#         group = data.loc[(data['Group'] != 'None') & pd.notna(data['Group'])]
#         group.rename(columns={'Content': constants.PROP_VALUE}, inplace=True)
#         group.rename(columns={'Header': constants.PROP_ORIGINAL_HEADER}, inplace=True)
#         group.rename(columns={'ParentHeader': constants.PROP_PARENT_HEADER}, inplace=True)
#         for index, row in group.iterrows():
#             source = ""
#             if constants.CAT_README_URL in repository_metadata.results.keys():
#                 source = repository_metadata.results[constants.CAT_README_URL][0]
#                 source = source[constants.PROP_RESULT][constants.PROP_VALUE]
#             parent_header = ""
#             if row[constants.PROP_PARENT_HEADER] != "":
#                 parent_header = row.loc[constants.PROP_PARENT_HEADER]
#             result = {
#                 constants.PROP_VALUE: row.loc[constants.PROP_VALUE],
#                 constants.PROP_TYPE: constants.TEXT_EXCERPT,
#                 constants.PROP_ORIGINAL_HEADER: row.loc[constants.PROP_ORIGINAL_HEADER]
#             }
#             if parent_header != "" and len(parent_header) > 0:
#                 result[constants.PROP_PARENT_HEADER] = parent_header
#             if source != "":
#                 repository_metadata.add_result(row.Group, result, 1, constants.TECHNIQUE_HEADER_ANALYSIS, source)
#             else:
#                 repository_metadata.add_result(row.Group, result, 1, constants.TECHNIQUE_HEADER_ANALYSIS)

#         # strings without tag (they will be classified)
#         string_list = data.loc[data['Group'].isna(), ['Content']].values.squeeze().tolist()
#         if type(string_list) != list:
#             string_list = [string_list]
#         if none_header_content is not None and none_header_content != "":
#             string_list.append(none_header_content.strip())
#         logging.info("Header information extracted.")
#         return repository_metadata, string_list
#     except Exception as e:
#         logging.error("Error while extracting headers: ", str(e))
#         return repository_metadata, [repo_data]

def extract_categories(repo_data: str, repository_metadata: Result) -> Tuple[Result, List[str]]:
    logging.info("Extracting information using headers")

    if not repo_data:
        return repository_metadata, []

    try:
        df, none_header_content = extract_header_content(repo_data)

        if df.empty:
            logging.warning("File to analyze has no headers")
            return repository_metadata, [repo_data]

        df['Group'] = df['Header'].map(label_text)
        df['ParentGroup'] = df['ParentHeader'].fillna('').map(label_text)

        df.loc[df['Group'].str.len() == 0, 'Group'] = df['ParentGroup']
        df.drop(columns=['ParentGroup'], inplace=True)

        if not df.iloc[0]['Group']:
            df.loc[df.index[0], 'Group'] = ['unknown']

        df = df.explode('Group')
        df.loc[df['Group'] == 'unknown', 'Group'] = np.nan

        valid = df[df['Group'].notna()].copy()
        valid.rename(columns={
            'Content': constants.PROP_VALUE,
            'Header': constants.PROP_ORIGINAL_HEADER,
            'ParentHeader': constants.PROP_PARENT_HEADER,
        }, inplace=True)

        source = None
        if constants.CAT_README_URL in repository_metadata.results:
            source = repository_metadata.results[constants.CAT_README_URL][0]
            source = source[constants.PROP_RESULT][constants.PROP_VALUE]

        logging.info("Extracting information using headers - iterating over valid entries")
        logging.info("Valid rows: %s", len(valid))

        for _, row in valid.iterrows():
            result = {
                constants.PROP_VALUE: row[constants.PROP_VALUE],
                constants.PROP_TYPE: constants.TEXT_EXCERPT,
                constants.PROP_ORIGINAL_HEADER: row[constants.PROP_ORIGINAL_HEADER],
            }

            if row[constants.PROP_PARENT_HEADER]:
                result[constants.PROP_PARENT_HEADER] = row[constants.PROP_PARENT_HEADER]

            repository_metadata.add_result(
                row['Group'],
                result,
                1,
                constants.TECHNIQUE_HEADER_ANALYSIS,
                source,
            )

        leftovers = df[df['Group'].isna()]['Content'].tolist()
        if none_header_content:
            leftovers.append(none_header_content.strip())

        return repository_metadata, leftovers

    except Exception:
        logging.exception("Error while extracting headers")
        return repository_metadata, [repo_data]
    

def build_wordnet_groups() -> Dict[str, List]:
    """Build WordNet groups lazily."""
    g: Dict[str, List] = {}

    g[constants.CAT_CITATION] = [
        Word("citation").synsets[3],
        Word("reference").synsets[1],
        Word("cite").synsets[3],
    ]

    g[constants.CAT_ACKNOWLEDGEMENT] = [Word("acknowledgement").synsets[0]]

    g[constants.CAT_RUN] = [
        Word("run").synsets[9],
        Word("run").synsets[34],
        Word("execute").synsets[4],
    ]

    g[constants.CAT_INSTALLATION] = [
        Word("installation").synsets[0],
        Word("install").synsets[0],
        Word("setup").synsets[1],
        Word("prepare").synsets[0],
        Word("preparation").synsets[0],
        Word("manual").synsets[0],
        Word("guide").synsets[2],
        Word("guide").synsets[9],
    ]

    g[constants.CAT_DOWNLOAD] = [Word("download").synsets[0]]

    g[constants.CAT_REQUIREMENTS] = [
        Word("requirement").synsets[2],
        Word("prerequisite").synsets[0],
        Word("prerequisite").synsets[1],
        Word("dependency").synsets[0],
        Word("dependent").synsets[0],
    ]

    g[constants.CAT_CONTACT] = [Word("contact").synsets[9]]

    g[constants.CAT_DESCRIPTION] = [
        Word("description").synsets[0],
        Word("description").synsets[1],
        Word("introduction").synsets[3],
        Word("introduction").synsets[6],
        Word("basics").synsets[0],
        Word("initiation").synsets[1],
        Word("summary").synsets[0],
        Word("summary").synsets[2],
    ]

    g[constants.CAT_CONTRIBUTORS] = [Word("contributor").synsets[0]]
    g[constants.CAT_CONTRIBUTING_GUIDELINES] = [Word("contributing").synsets[1]]
    g[constants.CAT_DOCUMENTATION] = [Word("documentation").synsets[1]]
    g[constants.CAT_LICENSE] = [Word("license").synsets[3], Word("license").synsets[0]]

    g[constants.CAT_USAGE] = [
        Word("usage").synsets[0],
        Word("example").synsets[0],
        Word("example").synsets[5],
        Word("demo").synsets[1],
        Word("tutorial").synsets[0],
        Word("tutorial").synsets[1],
        Word("start").synsets[0],
        Word("start").synsets[4],
        Word("started").synsets[0],
        Word("started").synsets[1],
        Word("started").synsets[7],
        Word("started").synsets[8],
    ]

    g[constants.CAT_FAQ] = [
        Word("errors").synsets[5],
        Word("problems").synsets[0],
        Word("problems").synsets[2],
        Word("faq").synsets[0],
    ]

    g[constants.CAT_SUPPORT] = [
        Word("support").synsets[7],
        Word("help").synsets[0],
        Word("help").synsets[9],
        Word("report").synsets[0],
        Word("report").synsets[6],
    ]

    return g
