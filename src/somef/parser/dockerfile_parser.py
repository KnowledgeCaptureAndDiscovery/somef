import logging
import os
import re
from ..utils import constants

def extract_dockerfile_maintainer(file_path):
    print(f"Extracting maintainers from Dockerfile: {file_path}")
    maintainers = []
    unique_maintainers = [] 
    try:
        with open(file_path, "rb") as file:
            raw_data = file.read()

        try:
            content = raw_data.decode("utf-8")
        except UnicodeDecodeError:
            logging.warning(f"File {file_path} is not UTF-8 decodable. Skipping.")
            return maintainers

        # not sure if should be better property author or a new property of maintainer
        oci_match = re.findall(
            constants.REGEXP_MAINTAINER_LABEL_OCI,
            content,
            re.IGNORECASE | re.MULTILINE
        )
        # LABEL maintainer free
        label_match = re.findall(
            constants.REGEXP_MAINTAINER_LABEL_FREE,
            content,
            re.IGNORECASE | re.MULTILINE
        )
        # Deprecated maintainer
        maintainer_match = re.findall(
            constants.REGEXP_MAINTAINER,
            content,
            re.IGNORECASE | re.MULTILINE
        )

        maintainers.extend(oci_match)
        maintainers.extend(label_match)
        maintainers.extend(maintainer_match)

        unique_maintainers = list({m.strip() for m in maintainers if m.strip()})
    except OSError:
        logging.warning(f"Could not read Dockerfile {file_path}")

    return unique_maintainers
