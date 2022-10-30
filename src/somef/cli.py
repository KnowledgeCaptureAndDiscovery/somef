import argparse
import json
import pickle
import sys
import validators
from os import path
from pathlib import Path
from dateutil import parser as date_parser

from .data_to_graph import DataGraph
from . import header_analysis

from . import parser_somef, regular_expressions, process_repository, markdown_utils, constants, configuration

from .rolf import preprocessing
import pandas as pd



def restricted_float(x):
    x = float(x)
    if x < 0.0 or x > 1.0:
        raise argparse.ArgumentTypeError(f"{x} not in range [0.0, 1.0]")
    return x


def remove_bibtex(string_list):
    """
        Function that takes the string list and removes all bibtex blocks of it
        Parameters
        ----------
        string_list: A list of strings to process

        Returns
        -------
        The strings list without bibtex blocks
        """
    for x, element in enumerate(string_list):
        bib_references = regular_expressions.extract_bibtex(element)
        if len(bib_references) > 0:
            top = element.find(bib_references[0])
            init = element.rfind("```", 0, top)
            end = element.find("```", init + 3)
            substring = element[init:end + 3]
            string_list[x] = element.replace(substring, "")
    print("Extraction of bibtex citation from readme completed. \n")
    return string_list


def create_excerpts(string_list):
    """
    Function takes readme text as input and divides it into excerpts
    Parameters
    ----------
    string_list: Markdown text passed as input
    Returns
    -------
    Extracted excerpts
    """
    print("Splitting text into valid excerpts for classification")
    string_list = remove_bibtex(string_list)
    # divisions = createExcerpts.split_into_excerpts(string_list)
    divisions = parser_somef.extract_blocks_excerpts(string_list)
    print("Text Successfully split. \n")
    output = {}
    for division in divisions:
        original = division
        division = regular_expressions.remove_links_images(division)
        if len(division) > 0:
            output[division] = original
    return output


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
        for category in constants.categories:
            if category not in file_paths.keys():
                sys.exit("Error: Category " + category + " file path not present in config.json")
            file_name = file_paths[category]
            if not path.exists(file_name):
                sys.exit(f"Error: File/Directory {file_name} does not exist")
            print("Classifying excerpts for the category", category)
            classifier = pickle.load(open(file_name, 'rb'))
            scores = classifier.predict_proba(text_to_classifier)
            score_dict[category] = {'excerpt': text_to_results, 'confidence': scores[:, 1]}
            print("Excerpt Classification Successful for the Category", category)
        print("\n")

    return score_dict


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
                res.append({'confidence': [prob], 'output': [cat], 'technique': 'Supervised classification'})
    return res


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
    excerpt_confidence = excerpt_element['confidence']
    if 'originalHeader' in excerpt_element:
        final_excerpt = {'excerpt': "", 'confidence': [], 'technique': 'Supervised classification',
                         'originalHeader': ""}
    else:
        final_excerpt = {'excerpt': "", 'confidence': [], 'technique': 'Supervised classification'}
    final_excerpt['excerpt'] += excerpt_info
    final_excerpt['confidence'] = excerpt_confidence
    if 'originalHeader' in excerpt_element:
        final_excerpt['originalHeader'] += excerpt_element['originalHeader']
    if 'parentHeader' in excerpt_element and excerpt_element['parentHeader'] != "":
        final_excerpt['parentHeader'] = excerpt_element['parentHeader']
    return final_excerpt


def is_in_excerpts_headers(text, set_excerpts):
    """
    Function that checks if some text is included in a set of excerpts
    Parameters
    ----------
    text: text to look for
    set_excerpts: existing set of excerpts

    Returns
    -------
    True if the text is included in the excerpts, False otherwise.
    """
    set_text = set(text.split())
    for excerpt in set_excerpts:
        set_excerpt = set(excerpt.split())
        if set_text.issubset(set_excerpt):
            return True, excerpt

    return False, None


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


def extract_categories_using_header(repo_data):
    """
    Function that adds category information extracted using header information
    Parameters
    ----------
    repo_data data to use the header analysis

    Returns
    -------
    Returns json with the information added.
    """
    print("Extracting information using headers")
    # this is a hack because if repo_data is "" this errors out
    if len(repo_data) == 0:
        return {}, []
    try:
        header_info, string_list = header_analysis.extract_categories_using_headers(repo_data)
        print("Information extracted. \n")
        return header_info, string_list
    except:
        print("Error while extracting headers: ", sys.exc_info()[0])
        return {}, [repo_data]


def merge(header_predictions, predictions, citations, citation_file_text, dois, binder_links, long_title,
          readthedocs_links, repo_status, arxiv_links, logo, images, support_channels, package_distribution,
          wiki_links, category):
    """
    Function that takes the predictions using header information, classifier and bibtex/doi parser
    Parameters
    ----------
    header_predictions: extraction of common headers and their contents
    wiki_links: links to wikis
    package_distribution: packages that appear in the readme
    support_channels: like gitter, discord, etc.
    images: included in the readme
    logo: included in the readme
    arxiv_links: links to arxiv papers
    repo_status: repostatus.org badges
    readthedocs_links: documentation links
    long_title: title of the repository
    binder_links: links to binder notebooks
    citation_file_text: text of the citation file
    header_predictions: predicted headers
    predictions: predictions from classifiers (description, installation instructions, invocation, citation)
    citations: bibtex citations
    dois: identifiers found in readme Zenodo DOIs, or other
    category: prediction of the category of the given repo
    Returns
    -------
    Combined predictions and results of the extraction process
    """
    print("Merge prediction using header information, classifier and bibtex and doi parsers")
    if long_title:
        predictions['longTitle'] = {'excerpt': long_title, 'confidence': [1.0],
                                    'technique': 'Regular expression'}
    for i in range(len(citations)):
        if 'citation' not in predictions.keys():
            predictions['citation'] = []
        if citations[i].find('https://doi.org/') >= 0 or citations[i].find('doi ') >= 0:
            doi_text = ""
            text_citation = citations[i]
            if text_citation.find("https://doi.org/") >= 0:
                doi_pos = text_citation.find("doi.org/")
                starts = text_citation[:doi_pos].rindex("http")
                ends = text_citation[starts:].find("}")
                doi_text = text_citation[starts:starts + ends]
            elif text_citation.find("doi") >= 0:
                doi_pos = text_citation.find("doi")
                starts = text_citation[doi_pos:].find("{")
                ends = text_citation[starts + doi_pos:].find("}")
                doi_text = "https://doi.org/" + text_citation[starts + doi_pos + 1:doi_pos + starts + ends]
            predictions['citation'].insert(0, {'excerpt': citations[i], 'confidence': [1.0],
                                               'technique': 'Regular expression', 'doi': doi_text,
                                               'format': 'bibtex'})
        else:
            predictions['citation'].insert(0, {'excerpt': citations[i], 'confidence': [1.0],
                                               'technique': 'Regular expression', 'format': 'bibtex'})
    if len(citation_file_text) != 0:
        if 'citation' not in predictions.keys():
            predictions['citation'] = []
        predictions['citation'].insert(0, {'excerpt': citation_file_text, 'confidence': [1.0],
                                           'technique': 'File Exploration', 'format': 'citation file format'})
    if len(dois) != 0:
        predictions['identifier'] = []
        for identifier in dois:
            # The identifier is in position 1. Position 0 is the badge id, which we don't want to export
            predictions['identifier'].insert(0, {'excerpt': identifier[1], 'confidence': [1.0],
                                                 'technique': 'Regular expression'})
    if len(binder_links) != 0:
        predictions['executableExample'] = {'excerpt': binder_links, 'confidence': [1.0],
                                            'technique': 'Regular expression'}
    if len(repo_status) != 0:
        predictions['repoStatus'] = {
            'excerpt': "https://www.repostatus.org/#" + repo_status[0:repo_status.find(" ")].lower(),
            'description': repo_status,
            'confidence': [1.0],
            'technique': 'Regular expression'}

    if len(arxiv_links) != 0:
        predictions['arxivLinks'] = {'excerpt': arxiv_links, 'confidence': [1.0],
                                     'technique': 'Regular expression'}

    if len(logo) != 0:
        predictions['logo'] = {'excerpt': logo, 'confidence': [1.0],
                               'technique': 'Regular expression'}

    if len(images) != 0:
        badges = []
        for image in images:
            if image.find('badge') >= 0:
                badges.append(image)
        for badge in badges:
            images.remove(badge)
        if len(images) > 0:
            predictions['image'] = []
            for image in images:
                predictions['image'].insert(0, {'excerpt': image, 'confidence': [1.0],
                                                'technique': 'Regular expression'})

    if len(support_channels) != 0:
        predictions['supportChannels'] = {'excerpt': support_channels, 'confidence': [1.0],
                                          'technique': 'Regular expression'}

    if len(package_distribution) != 0:
        predictions['packageDistribution'] = {'excerpt': package_distribution, 'confidence': [1.0],
                                              'technique': 'Regular expression'}

    for i in range(len(readthedocs_links)):
        if 'documentation' not in predictions.keys():
            predictions['documentation'] = []
        predictions['documentation'].insert(0, {'excerpt': readthedocs_links[i], 'confidence': [1.0],
                                                'technique': 'Regular expression', 'type': 'readthedocs'})

    for i in range(len(wiki_links)):
        if 'documentation' not in predictions.keys():
            predictions['documentation'] = []
        predictions['documentation'].insert(0, {'excerpt': wiki_links[i], 'confidence': [1.0],
                                                'technique': 'Regular expression', 'type': 'wiki'})

    if category:
        predictions['category'] = category

    for headers in header_predictions:
        if headers not in predictions.keys():
            predictions[headers] = header_predictions[headers]
        else:
            for h in header_predictions[headers]:
                predictions[headers].insert(0, h)
    print("Merging successful. \n")
    return predictions


def format_output(git_data, repo_data, gitlab_url=False):
    """
    Function takes metadata, readme text predictions, bibtex citations and path to the output file
    Performs some combinations
    Parameters
    ----------
    git_data GitHub obtained data
    repo_data Data extracted from the code repo by SOMEF

    Returns
    -------
    json representation of the categories found in file
    """
    text_technique = 'GitHub API'
    if gitlab_url:
        text_technique = 'GitLab API'
    print("formatting output")
    file_exploration = ['hasExecutableNotebook', 'hasBuildFile', 'hasDocumentation', 'codeOfConduct',
                        'contributingGuidelines', 'licenseFile', 'licenseText', 'acknowledgments', 'contributors',
                        'hasScriptFile', 'ontologies']
    for i in git_data.keys():
        if i == 'description':
            if 'description' not in repo_data.keys():
                repo_data['description'] = []
            if git_data[i] != "":
                repo_data['description'].append(
                    {'excerpt': git_data[i], 'confidence': [1.0], 'technique': text_technique})
        else:
            if i in file_exploration:
                if i == 'hasExecutableNotebook':
                    repo_data[i] = {'excerpt': git_data[i], 'confidence': [1.0], 'technique': 'File Exploration',
                                    'format': 'jupyter notebook'}
                elif i == 'hasBuildFile':
                    docker_files = []
                    docker_compose = []
                    for data in git_data[i]:
                        if data.lower().endswith('docker-compose.yml'):
                            docker_compose.append(data)
                        else:
                            docker_files.append(data)
                    repo_data[i] = []
                    if len(docker_files) > 0:
                        repo_data[i].insert(0, {'excerpt': docker_files, 'confidence': [1.0],
                                                'technique': 'File Exploration',
                                                'format': 'Docker file'})
                    if len(docker_compose) > 0:
                        repo_data[i].insert(0, {'excerpt': docker_compose, 'confidence': [1.0],
                                                'technique': 'File Exploration',
                                                'format': 'Docker compose file'})
                else:
                    repo_data[i] = {'excerpt': git_data[i], 'confidence': [1.0], 'technique': 'File Exploration'}
            elif git_data[i] != "" and git_data[i] != []:
                repo_data[i] = {'excerpt': git_data[i], 'confidence': [1.0], 'technique': text_technique}
    # remove empty categories from json
    return remove_empty_elements(repo_data)


def remove_empty_elements(d):
    """recursively remove empty lists, empty dicts, or None elements from a dictionary"""

    def empty(x):
        return x is None or x == {} or x == []

    if not isinstance(d, (dict, list)):
        return d
    elif isinstance(d, list):
        return [v for v in (remove_empty_elements(v) for v in d) if not empty(v)]
    else:
        return {k: v for k, v in ((k, remove_empty_elements(v)) for k, v in d.items()) if not empty(v)}


def save_json_output(repo_data, outfile, missing, pretty=False):
    """Function that saves the final json Object in the output file"""
    print("Saving json data to", outfile)
    if missing:
        missing = create_missing_fields(repo_data)
        repo_data["missingCategories"] = missing["missingCategories"]
    with open(outfile, 'w') as output:
        if pretty:
            json.dump(repo_data, output, sort_keys=True, indent=2)
        else:
            json.dump(repo_data, output)


def save_json(git_data, repo_data, outfile):
    """Performs some combinations and saves the final json Object in output file"""
    repo_data = format_output(git_data, repo_data)
    save_json_output(repo_data, outfile, None)


def save_codemeta_output(repo_data, outfile, pretty=False):
    """Function that saves a JSONLD file with the codemeta results"""
    def data_path(path):
        return DataGraph.resolve_path(repo_data, path)

    def format_date(date_string):
        date_object = date_parser.parse(date_string)
        return date_object.strftime("%Y-%m-%d")

    latest_release = None
    releases = data_path(["releases", "excerpt"])

    if releases is not None and len(releases) > 0:
        latest_release = releases[0]
        latest_pub_date = date_parser.parse(latest_release["datePublished"])
        for index in range(1, len(releases)):
            release = releases[index]
            pub_date = date_parser.parse(release["datePublished"])

            if pub_date > latest_pub_date:
                latest_release = release
                latest_pub_date = pub_date

    def release_path(path):
        return DataGraph.resolve_path(latest_release, path)

    code_repository = None
    if "codeRepository" in repo_data:
        code_repository = data_path(["codeRepository", "excerpt"])

    author_name = data_path(["owner", "excerpt"])

    # do the descriptions

    def average_confidence(x):
        confs = x["confidence"]

        if len(confs) > 0:
            try:
                return max(sum(confs) / len(confs))
            except:
                return 0
        else:
            return 0

    descriptions = data_path(["description"])
    descriptions_text = []
    if descriptions is not None:
        descriptions.sort(key=lambda x: (average_confidence(x) + (1 if x["technique"] == "GitHub API" else 0)),
                          reverse=True)
        descriptions_text = [x["excerpt"] for x in descriptions]

    published_date = ""
    try:
        published_date = format_date(release_path(["datePublished"]))
    except:
        print("Published date is not available")

    codemeta_output = {
        "@context": "https://doi.org/10.5063/schema/codemeta-2.0",
        "@type": "SoftwareSourceCode"
    }
    if "license" in repo_data:
        codemeta_output["license"] = data_path(["license", "excerpt"])
    if code_repository is not None:
        codemeta_output["codeRepository"] = code_repository
        codemeta_output["issueTracker"] = code_repository + "/issues"
    if "dateCreated" in repo_data:
        codemeta_output["dateCreated"] = format_date(data_path(["dateCreated", "excerpt"]))
    if "dateModified" in repo_data:
        codemeta_output["dateModified"] = format_date(data_path(["dateModified", "excerpt"]))
    if "downloadUrl" in repo_data:
        codemeta_output["downloadUrl"] = data_path(["downloadUrl", "excerpt"])
    if "name" in repo_data:
        codemeta_output["name"] = data_path(["name", "excerpt"])
    if "logo" in repo_data:
        codemeta_output["logo"] = data_path(["logo", "excerpt"])
    if "releases" in repo_data:
        codemeta_output["releaseNotes"] = release_path(["body"])
        codemeta_output["version"] = release_path(["tag_name"])
    if "topics" in repo_data:
        codemeta_output["keywords"] = data_path(["topics", "excerpt"])
    if "languages" in repo_data:
        codemeta_output["programmingLanguage"] = data_path(["languages", "excerpt"])
    if "requirement" in repo_data:
        codemeta_output["softwareRequirements"] = data_path(["requirement", "excerpt"])
    if "installation" in repo_data:
        codemeta_output["buildInstructions"] = data_path(["installation", "excerpt"])
    if "owner" in repo_data:
        codemeta_output["author"] = [
            {
                "@type": "Person",
                "@id": "https://github.com/" + author_name
            }
        ]
    if "citation" in repo_data:
        codemeta_output["citation"] = data_path(["citation", "excerpt"])
    if "identifier" in repo_data:
        codemeta_output["identifier"] = data_path(["identifier", "excerpt"])
    if "issueTracker" in repo_data:
        codemeta_output["issueTracker"] = data_path(["issueTracker", "excerpt"])
    if "readme_url" in repo_data:
        codemeta_output["readme"] = data_path(["readme_url", "excerpt"])
    if "contributors" in repo_data:
        codemeta_output["contributor"] = data_path(["contributors", "excerpt"])
    if descriptions_text:
        codemeta_output["description"] = descriptions_text
    if published_date != "":
        codemeta_output["datePublished"] = published_date
    pruned_output = {}

    for key, value in codemeta_output.items():
        if not (value is None or ((isinstance(value, list) or isinstance(value, tuple)) and len(value) == 0)):
            pruned_output[key] = value

    # now, prune out the variables that are None

    save_json_output(pruned_output, outfile, None, pretty=pretty)


def create_missing_fields(repo_data):
    """Function to create a small report with the categories SOMEF was not able to find"""
    categs = ["installation", "citation", "acknowledgement", "run", "download", "requirement", "contact", "description",
              "contributor", "documentation", "license", "usage", "faq", "support", "identifier",
              "hasExecutableNotebook", "hasBuildFile", "hasDocumentation", "executableExample"]
    missing = []
    out = {}
    for c in categs:
        if c not in repo_data:
            missing.append(c)
    out["missingCategories"] = missing
    return out


def create_missing_fields_report(repo_data, out_path):
    """Function to create a small report with the categories SOMEF was not able to find"""
    categs = ["installation", "citation", "acknowledgement", "run", "download", "requirement", "contact", "description",
              "contributor", "documentation", "license", "usage", "faq", "support", "identifier",
              "hasExecutableNotebook", "hasBuildFile", "hasDocumentation", "executableExample"]
    missing = []
    out = {}
    for c in categs:
        if c not in repo_data:
            missing.append(c)
    out["missing"] = missing
    export_path = ""
    if "json" in out_path:
        export_path = out_path.replace(".json", "_missing.json")
    elif "ttl" in out_path:
        export_path = out_path.replace(".ttl", "_missing.json")
    else:
        export_path = out_path + "_missing.json"
    save_json_output(out, export_path, False)


def cli_get_data(threshold, ignore_classifiers, repo_url=None, doc_src=None, local_repo=None,
                 ignore_github_metadata=False, readme_only=False, keep_tmp=None):
    """
    Main function to get the data through the command line
    Parameters
    ----------
    threshold: threshold to filter annotations. 0.8 by default
    ignore_classifiers: flag to indicate if the output from the classifiers should be ignored
    repo_url: URL of the repository to analyze
    doc_src: path to the src of the target repo
    local_repo: flag to indicate that the repo is local
    ignore_github_metadata: flag used to avoid doing extra requests to the GitHub API
    readme_only: flag to indicate that only the readme should be analyzed
    keep_tmp: path where to store TMP files in case SOMEF is instructed to keep them

    Returns
    -------
    JSON file with the results found by SOMEF.
    """
    file_paths = configuration.get_configuration_file()
    header = {}
    if 'Authorization' in file_paths.keys():
        header['Authorization'] = file_paths['Authorization']
    header['accept'] = 'application/vnd.github.v3+json'
    if repo_url is not None:
        # assert (doc_src is None)
        try:
            text, github_data = process_repository.load_online_repository_metadata(repo_url, header, ignore_github_metadata, readme_only, keep_tmp)
            if text == "":
                print("Warning: README document does not exist in the repository")
        except process_repository.GithubUrlError:
            return None
    elif local_repo is not None:
        # assert (local_repo is not None)
        try:
            text, github_data = process_repository.load_local_repository_metadata(local_repo)
            if text == "":
                print("Warning: README document does not exist in the local repository")
        except process_repository.GithubUrlError:
            return None
    else:
        assert (doc_src is not None)
        if not path.exists(doc_src):
            sys.exit("Error: Document does not exist at given path")
        with open(doc_src, 'r', encoding="UTF-8") as doc_fh:
            text = doc_fh.read()
        github_data = {}

    unfiltered_text = text
    header_predictions, string_list = extract_categories_using_header(unfiltered_text)
    text = markdown_utils.unmark(text)
    category = run_category_classification(unfiltered_text, threshold)
    excerpts = create_excerpts(string_list)
    if ignore_classifiers or unfiltered_text == '':
        predictions = {}
    else:
        excerpts_headers = parser_somef.extract_text_excerpts_header(unfiltered_text)
        header_parents = parser_somef.extract_headers_parents(unfiltered_text)
        score_dict = run_classifiers(excerpts, file_paths)
        predictions = classify(score_dict, threshold, excerpts_headers, header_parents)
    if text != '':
        citations = regular_expressions.extract_bibtex(text)
        citation_file_text = ""
        if 'citation' in github_data.keys():
            citation_file_text = github_data['citation']
            del github_data['citation']
        dois = regular_expressions.extract_dois(unfiltered_text)
        binder_links = regular_expressions.extract_binder_links(unfiltered_text)
        title = regular_expressions.extract_title(unfiltered_text)
        readthedocs_links = regular_expressions.extract_readthedocs(unfiltered_text)
        repo_status = regular_expressions.extract_repo_status(unfiltered_text)
        arxiv_links = regular_expressions.extract_arxiv_links(unfiltered_text)
        wiki_links = regular_expressions.extract_wiki_links(unfiltered_text, repo_url)
        # logo = extract_logo(unfiltered_text, repo_url)
        logo, images = regular_expressions.extract_images(unfiltered_text, repo_url, local_repo)
        support_channels = regular_expressions.extract_support_channels(unfiltered_text)
        package_distribution = regular_expressions.extract_package_distributions(unfiltered_text)
    else:
        citations = []
        citation_file_text = ""
        dois = []
        binder_links = []
        title = ""
        readthedocs_links = []
        repo_status = ""
        arxiv_links = []
        wiki_links = []
        logo = ""
        images = []
        support_channels = []
        package_distribution = ""

    predictions = merge(header_predictions, predictions, citations, citation_file_text, dois, binder_links, title,
                        readthedocs_links, repo_status, arxiv_links, logo, images, support_channels,
                        package_distribution, wiki_links, category)
    gitlab_url = False
    if repo_url is not None:
        if repo_url.rfind("gitlab.com") > 0:
            gitlab_url = True
    return format_output(github_data, predictions, gitlab_url)


def run_cli_document(doc_src, threshold, output):
    """Runs all the required components of the cli on a given document file"""
    return run_cli(threshold=threshold, output=output, doc_src=doc_src)


def run_cli(*,
            threshold=0.8,
            ignore_classifiers=False,
            repo_url=None,
            ignore_github_metadata=False,
            readme_only=False,
            doc_src=None,
            local_repo=None,
            in_file=None,
            output=None,
            graph_out=None,
            graph_format="turtle",
            codemeta_out=None,
            pretty=False,
            missing=False,
            keep_tmp=None
            ):
    """Function to run all the required components of the cli for a repository"""
    # check if it is a valid url
    if repo_url:
        if not validators.url(repo_url):
            print("Not a valid repository url. Please check the url provided")
            return None
    multiple_repos = in_file is not None
    if multiple_repos:
        with open(in_file, "r") as in_handle:
            # get the line (with the final newline omitted) if the line is not empty
            repo_list = [line[:-1] for line in in_handle if len(line) > 1]

        # convert to a set to ensure uniqueness (we don't want to get the same data multiple times)
        repo_set = set(repo_list)
        # check if the urls in repo_set if are valids
        remove_urls = []
        for repo_elem in repo_set:
            if not validators.url(repo_elem):
                print("Not a valid repository url. Please check the url provided: " + repo_elem)
                # repo_set.remove(repo_url)
                remove_urls.append(repo_elem)
        # remove non valid urls in repo_set
        for remove_url in remove_urls:
            repo_set.remove(remove_url)
        if len(repo_set) > 0:
            repo_data = [cli_get_data(threshold, ignore_classifiers, repo_url=repo_url, keep_tmp=keep_tmp) for repo_url in repo_set]
        else:
            return None

    else:
        if repo_url:
            repo_data = cli_get_data(threshold, ignore_classifiers, repo_url=repo_url,
                                     ignore_github_metadata=ignore_github_metadata, readme_only=readme_only, keep_tmp=keep_tmp)
        elif local_repo:
            repo_data = cli_get_data(threshold, ignore_classifiers, local_repo=local_repo, keep_tmp=keep_tmp)
        else:
            repo_data = cli_get_data(threshold, ignore_classifiers, doc_src=doc_src, keep_tmp=keep_tmp)

    if output is not None:
        save_json_output(repo_data, output, missing, pretty=pretty)

    if graph_out is not None:
        print("Generating Knowledge Graph")
        data_graph = DataGraph()
        if multiple_repos:
            for repo in repo_data:
                data_graph.add_somef_data(repo)
        else:
            data_graph.add_somef_data(repo_data)

        print("Saving Knowledge Graph ttl data to", graph_out)
        with open(graph_out, "wb") as out_file:
            out_file.write(data_graph.g.serialize(format=graph_format, encoding="UTF-8"))

    if codemeta_out is not None:
        save_codemeta_output(repo_data, codemeta_out, pretty=pretty)

    if missing is True:
        # save in the same path as output
        # if output is not None:
        #    create_missing_fields_report(repo_data, output)
        # elif codemeta_out is not None:
        if codemeta_out is not None:
            create_missing_fields_report(repo_data, codemeta_out)
        elif graph_out is not None:
            create_missing_fields_report(repo_data, graph_out)
