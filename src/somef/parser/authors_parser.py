import re
from ..utils import constants

# def parse_author_file(author_str):

#     """
#     Proccess a text with possible authors
#     """
#     if not author_str:
#         return []

#     authors = []

#     for line in author_str.splitlines():
#         line = line.strip()
#         if not line or line.startswith("#"):
#             continue

#         email_match = re.search(r'<([^>]+)>', line)
#         if email_match:
#             email = email_match.group(1)
#             name = line[:email_match.start()].strip()
#         else:
#             name = line
#             email = None

#         if name:
#             if re.search(constants.REGEXP_LTD_INC, name, re.IGNORECASE):
#                 type_author = "Organization"
#                 author_info = {
#                     "name": name,
#                     "email": email,
#                     "value": name,
#                     "type": type_author
#                 }
#             else:
#                 type_author = "Person"
#                 name_parts = name.split()
#                 given_name = name_parts[0] if name_parts else None
#                 last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else None
#                 author_info = {
#                     "name": name,
#                     "email": email,
#                     "value": name,
#                     "type": type_author,
#                     "given_name": given_name,
#                     "last_name": last_name
#                 }

#             authors.append(author_info)

#     return authors

# def parse_author_file(author_str):
#     """
#     Process a text with possible authors from markdown-style AUTHORS files.
#     """
#     if not author_str:
#         return []

#     authors = []

#     for line in author_str.splitlines():
#         line = line.strip()

#         if (
#             not line or
#             line.startswith("#") or
#             line.startswith("*") or
#             re.match(r"^[=\-*]{2,}$", line) or
#             "\t" in line or
#             re.match(r'^\s*\{.*\}\s*$', line) or
#             re.match(r'^https?://', line) or
#             len(re.findall(r'[A-Za-z]', line)) < 2
#         ):
#             continue

#         email_match = re.search(r'<([^>]+)>', line)
#         if email_match:
#             email = email_match.group(1)
#             name = line[:email_match.start()].strip()
#         else:
#             name = line
#             email = None

#         if name and name.lower() != "none":
#             if re.search(constants.REGEXP_LTD_INC, name, re.IGNORECASE):
#                 type_author = "Organization"
#                 raw_author_info = {
#                     "name": name,
#                     "email": email,
#                     "value": name,
#                     "type": type_author
#                 }
#             else:
#                 type_author = "Person"
#                 name_parts = name.split()
#                 given_name = name_parts[0] if name_parts else None
#                 last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else None
#                 raw_author_info = {
#                     "name": name,
#                     "email": email,
#                     "value": name,
#                     "type": type_author,
#                     "given_name": given_name,
#                     "last_name": last_name
#                 }

#             print(raw_author_info)

#             author_info = {}
#             for k, v in raw_author_info.items():
#                 if v is not None:
#                     author_info[k] = v

#             authors.append(author_info)

#     return authors


def parse_author_file(author_str):
    """
    Process a text with possible authors from markdown-style AUTHORS files.
    Filters and extracts only lines that match expected person or organization patterns.
    """
    if not author_str:
        return []
    
    author_str = re.sub(r'\{[^}]*\}', '', author_str, flags=re.DOTALL)

    authors = []
    lines = author_str.splitlines()

    for i, line in enumerate(lines):
        line = line.replace("\t", " ").strip()
        next_line = lines[i + 1].strip() if i + 1 < len(lines) else ""
        email_match = re.search(r'<[^<>@ ]+@[^<>@ ]+\.[^<>@ ]+>', line)

        if (
            not line or
            line.startswith("#") or
            line.startswith("*") or
            line.startswith("=") or
            (line[0].islower() and not email_match) or
            re.match(r'^\s*\{.*\}\s*$', line) or
            re.match(r'^https?://', line) or
            len(re.findall(r'[A-Za-z]', line)) < 2 or
            (
                line.endswith(".") 
                and not re.match(r'^([A-Z][a-zA-Z0-9&\-\.]+(?:\s+[A-Z][a-zA-Z0-9&\-\.]+){0,3})\.$', line)
                and not re.search(constants.REGEXP_LTD_INC, line, re.IGNORECASE)
            ) or
            line.endswith(",") or
            re.match(r'^[A-Z][a-z]+ *:$', line) or
            re.match(r"^[=\-*]{2,}$", next_line)
        ):
            continue

        email_match = re.search(r'<(.*?)>', line)
        email = email_match.group(1) if email_match else None
        name_part = line[:email_match.start()].strip() if email_match else line

        name_part = re.sub(r'\(.*?\)', '', name_part)

        parts = name_part.split('-')
        if len(parts) > 1 and parts[0].strip() == "":
            name_part = parts[1].strip()
        else:
            name_part = parts[0].strip()

        name_words = name_part.split()

        if re.search(constants.REGEXP_LTD_INC, name_part, re.IGNORECASE):
            raw_author = {
                "type": "Organization",
                "name": name_part,
                "value": name_part
            }
            if email:
                raw_author["email"] = email
            authors.append(raw_author)
            continue

        if email or len(name_words) >= 2 and len(name_words) <= 4:
            raw_author = {
                "type": "Person",
                "name": name_part,
                "value": name_part,
                "given_name": name_words[0]
            }
            if len(name_words) > 1:
                raw_author["last_name"] = " ".join(name_words[1:])
            if email:
                raw_author["email"] = email
            authors.append(raw_author)

    return authors