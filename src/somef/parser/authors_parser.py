import re
from ..utils import constants

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
            line.endswith(":") or
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

def parse_bibtex_authors(author_str):
    """
    parses author strings extracted from BibTeX entries.
    """
    if not author_str:
        return []

    clean_str = re.sub(r'\{|\}|\\(?P<char>.)', r'\g<char>', author_str)
    clean_str = clean_str.replace('\n', ' ').strip()

    raw_authors = re.split(r'\s+and\s+', clean_str, flags=re.IGNORECASE)
    
    authors = []
    for raw_name in raw_authors:
        raw_name = raw_name.strip()
        if not raw_name:
            continue

        agent = {
            constants.PROP_TYPE: "Agent",
            constants.PROP_NAME: raw_name 
        }

        if ',' in raw_name:
            last, first = raw_name.split(',', 1)
            last = last.strip()
            first = first.strip()
            agent[constants.PROP_NAME] = f"{first} {last}"
            agent["family_name"] = last
            agent["given_name"] = first
        else:
            words = raw_name.split()
            if len(words) >= 2:
                agent["given_name"] = words[0]
                agent["family_name"] = " ".join(words[1:])

        authors.append(agent)

    return authors