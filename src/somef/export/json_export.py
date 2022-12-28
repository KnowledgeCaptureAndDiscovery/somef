import json
from dateutil import parser as date_parser
from ..utils import constants
from .data_to_graph import DataGraph
from ..process_results import Result


def save_json_output(repo_data, out_path, missing, pretty=False):
    """
    Function that saves the final json Object in the output file
    Parameters
    ----------
    @param repo_data: dictionary with the metadata to be saved
    @param out_path: output path where to save the JSON
    @param missing: print the categories SOMEF was not able to find
    @param pretty: format option to print the JSON in a human-readable way

    Returns
    -------
    @return: Does not return a value
    """
    print("Saving json data to", out_path)
    if missing:
        # add a new key-value papir to the dictionary
        repo_data[constants.CAT_MISSING] = create_missing_fields(repo_data)
    with open(out_path, 'w') as output:
        if pretty:
            json.dump(repo_data, output, sort_keys=True, indent=2)
        else:
            json.dump(repo_data, output)


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

    # def average_confidence(x):
    #     confs = x["confidence"]
    #
    #     if len(confs) > 0:
    #         try:
    #             return max(sum(confs) / len(confs))
    #         except:
    #             return 0
    #     else:
    #         return 0

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


def create_missing_fields(result):
    """Function to create a small report with the categories SOMEF was not able to find.
    The categories are added to the JSON results. This won't be added if you export TTL or Codemeta"""
    missing = []
    repo_data = result
    for c in constants.categories_files_header:
        if c not in repo_data:
            missing.append(c)
    return missing
