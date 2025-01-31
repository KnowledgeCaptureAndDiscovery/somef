import os
from pathlib import Path
import json
import sys
import logging

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


def configure(authorization="",
              description=default_description,
              invocation=default_invocation,
              installation=default_installation,
              citation=default_citation,
              base_uri=constants.CONF_DEFAULT_BASE_URI):
    """ Function to configure the main program"""
    import nltk
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
        constants.CONF_AUTHORIZATION: "token " + authorization,
        constants.CONF_DESCRIPTION: description,
        constants.CONF_INVOCATION: invocation,
        constants.CONF_INSTALLATION: installation,
        constants.CONF_CITATION: citation,
        constants.CONF_BASE_URI: base_uri
    }

    if data[constants.CONF_AUTHORIZATION] == "token ":
        del data[constants.CONF_AUTHORIZATION]

    with credentials_file.open("w") as fh:
        credentials_file.parent.chmod(0o700)
        credentials_file.chmod(0o600)
        json.dump(data, fh)
        logging.info("Configuration file saved at "+os.path.dirname(credentials_file))
