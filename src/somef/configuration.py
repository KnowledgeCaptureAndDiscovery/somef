import os
from pathlib import Path
import json
import sys
import logging
import base64
import requests
import nltk
from .utils import constants

path = Path(__file__).parent.absolute()
default_description = os.path.join(str(path), "models", "description.p")
default_invocation = os.path.join(str(path), "models", "invocation.p")
default_installation = os.path.join(str(path), "models", "installation.p")
default_citation = os.path.join(str(path), "models", "citation.p")


def get_configuration_file():
    """
    Function that retrieves the configuration file
    Returns
    -------
    The configuration object in JSON format
    """
    credentials_file = Path(
        os.getenv("SOMEF_CONFIGURATION_FILE", '~/.somef/config.json')
    ).expanduser()
    if credentials_file.exists():
        with credentials_file.open("r") as fh:
            file_paths = json.load(fh)
        if constants.CONF_SIMILARITY_THRESHOLD not in file_paths:
            file_paths[constants.CONF_SIMILARITY_THRESHOLD] = constants.CONF_DEFAULT_SIMILARITY_THRESHOLD
        if constants.CONF_DOWNLOAD_LIMIT_MB not in file_paths:
            file_paths[constants.CONF_DOWNLOAD_LIMIT_MB] = constants.SIZE_DOWNLOAD_LIMIT_MB
    else:
        sys.exit("Error: Please provide a config.json file or run somef configure.")
    return file_paths


def update_base_uri(base_uri):
    credentials_file = Path(
        os.getenv("SOMEF_CONFIGURATION_FILE", constants.__DEFAULT_SOMEF_CONFIGURATION_FILE__)
    ).expanduser()
    os.makedirs(str(credentials_file.parent), exist_ok=True)

    if credentials_file.exists():
        with credentials_file.open("r") as fh:
            data = json.load(fh)
            data[constants.CONF_BASE_URI] = base_uri

        with credentials_file.open("w") as fh:
            credentials_file.parent.chmod(0o700)
            credentials_file.chmod(0o600)
            json.dump(data, fh)


def configure(
        # authorization="",
        github_authorization="",
        gitlab_authorization="",
        codeberg_authorization="",
        bitbucket_authorization="",
        bitbucket_email="",
        description=default_description,
        invocation=default_invocation,
        installation=default_installation,
        citation=default_citation,
        base_uri=constants.CONF_DEFAULT_BASE_URI,
        similarity_threshold=constants.CONF_DEFAULT_SIMILARITY_THRESHOLD,
        download_limit_mb=constants.SIZE_DOWNLOAD_LIMIT_MB):
    
    """ Function to configure the main program"""

    nltk.download('wordnet')
    nltk.download('omw-1.4')
    nltk.download('punkt')
    nltk.download('punkt_tab')
    nltk.download('stopwords')

    credentials_file = Path(
        os.getenv("SOMEF_CONFIGURATION_FILE", constants.__DEFAULT_SOMEF_CONFIGURATION_FILE__)
    ).expanduser()
    os.makedirs(str(credentials_file.parent), exist_ok=True)

    # if credentials_file.exists():
    #     with credentials_file.open("r") as fh:
    #         data = json.load(fh)
    # else:
    data = {
        # constants.CONF_AUTHORIZATION: "token " + authorization,
        constants.CONF_DESCRIPTION: description,
        constants.CONF_INVOCATION: invocation,
        constants.CONF_INSTALLATION: installation,
        constants.CONF_CITATION: citation,
        constants.CONF_BASE_URI: base_uri,
        constants.CONF_SIMILARITY_THRESHOLD: similarity_threshold,
        constants.CONF_DOWNLOAD_LIMIT_MB: download_limit_mb
    }

    # if data[constants.CONF_AUTHORIZATION] == "token ":
    #     del data[constants.CONF_AUTHORIZATION]

    if github_authorization:
        data[constants.CONF_GITHUB_AUTHORIZATION] = "token " + github_authorization

    if gitlab_authorization:
        token = gitlab_authorization
        if not token.lower().startswith("bearer "):
            token = "Bearer " + token
        data[constants.CONF_GITLAB_AUTHORIZATION] = token

    if codeberg_authorization:
        token = codeberg_authorization
        if not token.lower().startswith("token "):
            token = "token " + token
        data[constants.CONF_CODEBERG_AUTHORIZATION] = token


    if bitbucket_authorization:
        token = bitbucket_authorization
        email = bitbucket_email  
        if not token.lower().startswith("basic "):
            raw = f"{email}:{token}"
            token = "Basic " + base64.b64encode(raw.encode()).decode()
        data[constants.CONF_BITBUCKET_AUTHORIZATION] = token

    with credentials_file.open("w") as fh:
        credentials_file.parent.chmod(0o700)
        credentials_file.chmod(0o600)
        json.dump(data, fh)
        logging.info("Configuration file saved at "+os.path.dirname(credentials_file))


def test_configuration_tokens():
    """
    Checks the API tokens stored in the configuration file against each
    provider without running SOMEF.

    Returns
    -------
    dict
        Mapping of provider name to {"ok": bool, "message": str}. Providers
        without a configured token are omitted.
    """

    file_paths = get_configuration_file()
    providers = [
        ("GitHub",    constants.CONF_GITHUB_AUTHORIZATION,    "https://api.github.com/user"),
        ("GitLab",    constants.CONF_GITLAB_AUTHORIZATION,    "https://gitlab.com/api/v4/user"),
        ("Codeberg",  constants.CONF_CODEBERG_AUTHORIZATION,  "https://codeberg.org/api/v1/user"),
        ("Bitbucket", constants.CONF_BITBUCKET_AUTHORIZATION, "https://api.bitbucket.org/2.0/user"),
    ]
    results = {}
    for label, key, url in providers:
        if key not in file_paths:
            results[label] = {"ok": None, "message": "token not configured"}
            continue

        stored = file_paths[key]
        if label == "Bitbucket" and not stored.lower().startswith("basic "):
            results[label] = {
                "ok": False,
                "message": "Bitbucket token has an incorrect format (expected a 'Basic ' prefix). "
                           "Run 'somef configure' to set it correctly.",
            }
            continue

        try:
            resp = requests.get(url, headers={constants.PROP_AUTHORIZATION: file_paths[key]}, timeout=10)
        except requests.RequestException as e:
            results[label] = {"ok": False, "message": f"Could not reach the api: {e}"}
            continue
        if resp.status_code == 200:
            results[label] = {"ok": True, "message": "token valid"}
        elif resp.status_code == 401:
            results[label] = {"ok": False, "message": "token invalid (401)"}
        elif resp.status_code == 403:
            results[label] = {"ok": True, "message": "token valid but with limited permissions (403)"}
        else:
            results[label] = {"ok": False, "message": f"unexpected response ({resp.status_code})"}
    return results