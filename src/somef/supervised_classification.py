import logging
import sys
import pickle
import pandas as pd
from .utils import constants
from pathlib import Path
from os import path
from .rolf import preprocessing
from .process_results import Result


def run_category_classification(readme_text: str, threshold: float, results: Result):
    """
    Function which returns the categories, confidence and technique of the given repo
    Parameters
    ----------
    @param readme_text: the pure text of the readme
    @param threshold: the threshold for the confidence
    @param results: the JSON results to attach the resultant categories
    Returns
    -------
    @returns: A Result with the categories incorporated
    """
    df = pd.DataFrame([readme_text], columns=['Text'])
    preprocessing.Preprocessor(df).run()
    text = [df['Text'][0]]
    try:
        for model_file in (Path(__file__).parent / 'rolf/models').iterdir():
            with open(model_file, 'rb') as f:
                model = pickle.load(f)
                cat = model.predict(text).tolist()[0]
                prob = max(model.predict_proba(text).tolist()[0])
                if cat != 'Other' and prob > threshold:
                    results.add_result(constants.CAT_APPLICATION_DOMAIN,
                                       {
                                           constants.PROP_TYPE: constants.STRING,
                                           constants.PROP_VALUE: cat
                                       }, prob, constants.TECHNIQUE_SUPERVISED_CLASSIFICATION)
    except Exception as e:
        logging.error("Error when applying supervised classification " + str(e))
    return results


def classify(scores, threshold, excerpts_headers, header_parents, repository_metadata: Result):
    """
    Function takes scores dictionary and a threshold as input
    Parameters
    ----------
    @param scores: score dictionary passed as input
    @param threshold: threshold to filter predictions (only predictions above threshold are returned)
    @param excerpts_headers: headers to which each excerpt belongs (if any)
    @param header_parents: parent headers of each excerpt
    @param repository_metadata: Result with the results of the repository so far

    Returns
    -------
    @returns Result including predictions and their text excerpts with a confidence above the given threshold.
    """
    logging.info("Checking thresholds for classified excerpts.")
    try:
        source = repository_metadata.results[constants.CAT_README_URL][0]
        source = source[constants.PROP_RESULT][constants.PROP_VALUE]
    except:
        source = "README.md"
    # print(scores)
    for ele in scores.keys():
        excerpt = ""
        confidence = 0
        header = ""
        num_elems = 1  # for calculating an average of confidence (in case multiple values are aggregated).
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
                    confidence = scores[ele]['confidence'][i]
                else:
                    current_header = ""
                    if element in set(excerpts_headers['text']):
                        elem = excerpts_headers.loc[excerpts_headers['text'] == element]
                        ind = elem.index.values[0]
                        current_header = elem.at[ind, 'header']
                    # if both headers are the same, the new data is added
                    if header == current_header:
                        excerpt = excerpt + scores[ele]['excerpt'][i] + ' \n'
                        confidence = confidence + scores[ele]['confidence'][i]
                        num_elems = num_elems + 1
                    # if they are not the same, add a result
                    else:
                        result = {
                            constants.PROP_TYPE: constants.TEXT_EXCERPT,
                            constants.PROP_VALUE: excerpt
                        }
                        if header != "":
                            result[constants.PROP_ORIGINAL_HEADER] = header
                        repository_metadata.add_result(ele, result, confidence / num_elems,
                                                       constants.TECHNIQUE_SUPERVISED_CLASSIFICATION, source)
                        header = current_header
                        num_elems = 1
                        excerpt = scores[ele]['excerpt'][i] + ' \n'
                        confidence = scores[ele]['confidence'][i]
        # if an element hasn't been added, it's added at this point
        if excerpt != "":
            result = {
                constants.PROP_TYPE: constants.TEXT_EXCERPT,
                constants.PROP_VALUE: excerpt
            }
            if header != "":
                result[constants.PROP_ORIGINAL_HEADER] = header
            repository_metadata.add_result(ele, result, confidence / num_elems,
                                           constants.TECHNIQUE_SUPERVISED_CLASSIFICATION,
                                           source)
    logging.info("All excerpts below the threshold have been removed.")
    return repository_metadata


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
    try:
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
                logging.info("Classifying excerpts for the category " + category)
                classifier = pickle.load(open(file_name, 'rb'))
                scores = classifier.predict_proba(text_to_classifier)
                score_dict[category] = {'excerpt': text_to_results, 'confidence': scores[:, 1]}
                print(score_dict)
                # logging.info("Excerpt classification successful category"+ category)
    except Exception as e:
        logging.error("Error while running supervised classifiers on README " + str(e))

    return score_dict
