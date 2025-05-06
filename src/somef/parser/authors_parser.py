import re
from ..utils import constants

def parse_author_file(author_str):

    """
    Proccess a text with possible authors
    """
    if not author_str:
        return []

    authors = []

    for line in author_str.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        email_match = re.search(r'<([^>]+)>', line)
        if email_match:
            email = email_match.group(1)
            name = line[:email_match.start()].strip()
        else:
            name = line
            email = None

        if name:
            if re.search(constants.REGEXP_LTD_INC, name, re.IGNORECASE):
                type_author = "Organization"
                author_info = {
                    "name": name,
                    "email": email,
                    "value": name,
                    "type": type_author
                }
            else:
                type_author = "Person"
                name_parts = name.split()
                given_name = name_parts[0] if name_parts else None
                last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else None
                author_info = {
                    "name": name,
                    "email": email,
                    "value": name,
                    "type": type_author,
                    "given_name": given_name,
                    "last_name": last_name
                }

            authors.append(author_info)

    return authors