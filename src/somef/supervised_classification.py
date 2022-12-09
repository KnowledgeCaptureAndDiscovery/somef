import sys
import pickle
import pandas as pd
from .utils import constants
from pathlib import Path
from os import path
from .rolf import preprocessing


def run_category_classification(readme_text: str, threshold: float):
    """
    Function which returns the categories, confidence and technique of the given repo
    Parameters
    ----------
    readme_text: the pure text of the readme
    threshold: the threshold for the confidence

    Returns
    -------
    Returns the list of the results
    """
    df = pd.DataFrame([readme_text], columns=['Text'])
    preprocessing.Preprocessor(df).run()
    text = [df['Text'][0]]
    res = []
    for model_file in (Path(__file__).parent / 'rolf/models').iterdir():
        with open(model_file, 'rb') as f:
            model = pickle.load(f)
            cat = model.predict(text).tolist()[0]
            prob = max(model.predict_proba(text).tolist()[0])
            if cat != 'Other' and prob > threshold:
                res.append({constants.CONFIDENCE: [prob], constants.VALUE: [cat],
                            constants.TECHNIQUE: constants.SUPERVISED_CLASSIFICATION})
    return res


def classify(scores, threshold, excerpts_headers, header_parents):
    """
    Function takes scores dictionary and a threshold as input
    Parameters
    ----------
    scores: score dictionary passed as input
    threshold: threshold to filter predictions (only predictions above threshold are returned)
    excerpts_headers: headers to which each excerpt belongs (if any)
    header_parents: parent headers of each excerpt

    Returns
    -------
    Predictions containing excerpts with a confidence above the given threshold.
    """
    print("Checking Thresholds for Classified Excerpts.")
    predictions = {}
    for ele in scores.keys():
        print("Running for", ele)
        flag = False
        predictions[ele] = []
        excerpt = ""
        confid = []
        header = ""
        for i in range(len(scores[ele]['confidence'])):
            if scores[ele]['confidence'][i] >= threshold:
                element = scores[ele]['excerpt'][i]
                # if excerpt is empty, it means it's the first iteration of the loop
                if excerpt == "":
                    if element in set(excerpts_headers['text']):
                        elem = excerpts_headers.loc[excerpts_headers['text'] == element]
                        ind = elem.index.values[0]
                        header = elem.at[ind, 'header']
                    excerpt = excerpt + scores[ele]['excerpt'][i] + ' \n'
                    confid.append(scores[ele]['confidence'][i])
                else:
                    current_header = ""
                    if element in set(excerpts_headers['text']):
                        elem = excerpts_headers.loc[excerpts_headers['text'] == element]
                        ind = elem.index.values[0]
                        current_header = elem.at[ind, 'header']
                    # if both headers are the same, the new data is added
                    if header == current_header:
                        excerpt = excerpt + scores[ele]['excerpt'][i] + ' \n'
                        confid.append(scores[ele]['confidence'][i])
                    # if they are not the same, a new excerpt is created with the previous data
                    # and stores the new data as part of a new excerpt
                    else:
                        if not header == "":
                            element = remove_unimportant_excerpts(
                                {'excerpt': excerpt, 'confidence': confid, 'originalHeader': header,
                                 'parentHeader': header_parents[header]})
                        else:
                            element = remove_unimportant_excerpts({'excerpt': excerpt, 'confidence': confid})
                        if len(element['confidence']) != 0:
                            predictions[ele].append(element)
                        header = current_header
                        excerpt = scores[ele]['excerpt'][i] + ' \n'
                        confid = [scores[ele]['confidence'][i]]
        # if an element hasn't been added, it's added at this point
        if excerpt != "":
            if not header == "":
                element = remove_unimportant_excerpts(
                    {'excerpt': excerpt, 'confidence': confid, 'originalHeader': header,
                     'parentHeader': header_parents[header]})
            else:
                element = remove_unimportant_excerpts({'excerpt': excerpt, 'confidence': confid})
            if len(element['confidence']) != 0:
                predictions[ele].append(element)
        print("Run completed.")
    print("All excerpts below the given threshold have been removed. \n")
    return predictions


def remove_unimportant_excerpts(excerpt_element):
    """
    Function which removes all excerpt lines which have been classified but contain only one word.
    TO DO: It does not seem to filter lines with one word
    Parameters
    ----------
    excerpt_element: excerpt to process

    Returns
    -------
    Returns the excerpt to be entered into the predictions
    """
    excerpt_info = excerpt_element['excerpt']
    excerpt_confidence = excerpt_element[constants.CONFIDENCE]
    if 'originalHeader' in excerpt_element:
        final_excerpt = {'excerpt': "", 'confidence': [], constants.TECHNIQUE: constants.SUPERVISED_CLASSIFICATION,
                         'originalHeader': ""}
    else:
        final_excerpt = {'excerpt': "", 'confidence': [], constants.TECHNIQUE: constants.SUPERVISED_CLASSIFICATION}
    final_excerpt['excerpt'] += excerpt_info
    final_excerpt['confidence'] = excerpt_confidence
    if 'originalHeader' in excerpt_element:
        final_excerpt['originalHeader'] += excerpt_element['originalHeader']
    if 'parentHeader' in excerpt_element and excerpt_element['parentHeader'] != "":
        final_excerpt['parentHeader'] = excerpt_element['parentHeader']
    return final_excerpt


def run_classifiers(excerpts, file_paths):
    """
    Function takes readme text as input and runs the provided classifiers on it
    Returns the dictionary containing scores for each excerpt.
    Parameters
    ----------
    excerpts: text fragments to process
    file_paths: pickle files of the classifiers

    Returns
    -------
    A score dictionary with the results

    """
    score_dict = {}
    if len(excerpts) > 0:
        text_to_classifier = []
        text_to_results = []
        for key in excerpts.keys():
            text_to_classifier.append(key)
            text_to_results.append(excerpts[key])
        for category in constants.supervised_categories:
            if category not in file_paths.keys():
                sys.exit("Error: Category " + category + " file path not present in config.json")
            file_name = file_paths[category]
            if not path.exists(file_name):
                sys.exit(f"Error: File or Directory {file_name} does not exist")
            print("Classifying excerpts for the category", category)
            classifier = pickle.load(open(file_name, 'rb'))
            scores = classifier.predict_proba(text_to_classifier)
            score_dict[category] = {'excerpt': text_to_results, 'confidence': scores[:, 1]}
            print("Excerpt Classification Successful for the Category", category)
        print("\n")

    return score_dict
