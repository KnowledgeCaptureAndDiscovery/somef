import os
from pathlib import Path
import json

__DEFAULT_SOMEF_CONFIGURATION_FILE__ = "~/.somef/config.json"

path = Path(__file__).parent.absolute()
default_description = str(path) + "/models/description.sk"
default_invocation = str(path) + "/models/invocation.sk"
default_installation = str(path) + "/models/installation.sk"
default_citation = str(path) + "/models/citation.sk"


def configure(authorization="",
              description=default_description,
              invocation=default_invocation,
              installation=default_installation,
              citation=default_citation):
    import nltk
    nltk.download('wordnet')

    credentials_file = Path(
        os.getenv("SOMEF_CONFIGURATION_FILE", __DEFAULT_SOMEF_CONFIGURATION_FILE__)
    ).expanduser()
    os.makedirs(str(credentials_file.parent), exist_ok=True)

    # credentials_file = Path(os.getenv("SOMEF_CONFIGURATION_FILE", __DEFAULT_SOMEF_CONFIGURATION_FILE__)).expanduser()

    if credentials_file.exists():
        with credentials_file.open("r") as fh:
            data = json.load(fh)

    data = {
        "Authorization": "token " + authorization,
        "description": description,
        "invocation": invocation,
        "installation": installation,
        "citation": citation,
    }

    if data['Authorization'] == "token ":
        del data['Authorization']

    with credentials_file.open("w") as fh:
        credentials_file.parent.chmod(0o700)
        credentials_file.chmod(0o600)
        json.dump(data, fh)
