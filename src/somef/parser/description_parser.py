import re
import logging
from pathlib import Path
from ..process_results import Result
from ..utils import constants

def parse_description_file(file_path, metadata_result: Result, source):

    """
    Parse a DESCRIPTION file to extract metadata.

    Parameters
    ----------
    file_path: path of the DESCRIPTION file being analysed
    metadata_result: metadata object where the metadata dictionary is kept
    source: source of the package file (URL)

    Returns
    -------
    """

    try:
        if Path(file_path).name.upper() == "DESCRIPTION":
            metadata_result.add_result(
                constants.CAT_HAS_PACKAGE_FILE,
                {
                    # "value": "DESCRIPTION",
                    "value": source,
                    "type": constants.URL,
                    "source": source
                },
                1,
                constants.TECHNIQUE_CODE_CONFIG_PARSER,
                source
            )
            
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

                package_match = re.search(r'Package:\s*([^\n]+)', content)
                if package_match:
                    print("FOUND PACKAGE NAME")
                    package_name = package_match.group(1).strip()
                    metadata_result.add_result(
                        constants.CAT_PACKAGE_ID,
                        {
                            "value": package_name,
                            "type": constants.STRING,
                            "source": source
                        },
                        1,
                        constants.TECHNIQUE_CODE_CONFIG_PARSER,
                        source
                    )
                else:
                    print("NO PACKAGE NAME FOUND")
                    
                desc_match = re.search(r'Description:\s*([^\n]+(?:\n\s+[^\n]+)*)', content)
                if desc_match:
                    description = desc_match.group(1).strip()
                    metadata_result.add_result(
                        constants.CAT_DESCRIPTION,
                        {
                            "value": description,
                            "type": constants.STRING,
                            "source": source
                        },
                        1,
                        constants.TECHNIQUE_CODE_CONFIG_PARSER,
                        source
                    )
                
                version_match = re.search(r'Version:\s*([^\n]+)', content)
                if version_match:
                    version = version_match.group(1).strip()
                    metadata_result.add_result(
                        constants.CAT_VERSION,
                        {
                            "value": version,
                            "type": constants.STRING,
                            "source": source
                        },
                        1,
                        constants.TECHNIQUE_CODE_CONFIG_PARSER,
                        source
                    )
                
             
                authors_section = re.search(r'Authors@R:\s*c\(([\s\S]*?)\)\s*$', content, re.MULTILINE)
                # authors_section = re.search(r'Authors@R:\s*c\(([^)]+)\)', content, re.DOTALL)
                if authors_section:
                    authors_text = authors_section.group(1)
            
                    pattern = re.compile(
                        r'''person\(
                            \s*"([^"]+)"                
                            (?:\s*,\s*"([^"]*)")?      
                            (?:\s*,\s*)*               
                            (?:
                                "(?P<email1>[^"]+@[^"]+)" 
                                |
                                .*?email\s*=\s*"(?P<email2>[^"]+)" 
                            )?                     
                            [^)]*                        
                        \)''',
                        re.VERBOSE
                    )
                    # person_entries = re.findall(r'person\(\s*"([^"]+)"\s*,\s*"([^"]+)"(?:\s*,\s*)?(?:"[^"]*")?(?:\s*,\s*)?(?:"([^"]+)")?', authors_text)
                    person_entries = []
                    for match in pattern.finditer(authors_text):
                        given = match.group(1)
                        family = match.group(2) or ""
                        email = match.group("email1") or match.group("email2") or ""
                        person_entries.append((given, family, email))

                    for given, family, email in person_entries:
                        name = given.strip()
                        if family:
                            name += " " + family.strip()
                        author = {
                                    "value": name,
                                    "type": constants.AGENT,
                                }
     
                        if email:
                            author["email"] = email.strip()

                        metadata_result.add_result(
                                constants.CAT_AUTHORS,
                                author,
                                1,
                                constants.TECHNIQUE_CODE_CONFIG_PARSER,
                                source
                            )
            
                license_match = re.search(r'License:\s*([^\n]+)', content)
                if license_match:
                    license_text = license_match.group(1).strip()
                    metadata_result.add_result(
                        constants.CAT_LICENSE,
                        {
                            "value": license_text,
                            "type": constants.STRING,
                            "source": source
                        },
                        1,
                        constants.TECHNIQUE_CODE_CONFIG_PARSER,
                        source
                    )
                
                url_section = re.search(r'URL:\s*([^\n]+(?:\n\s+[^\n]+)*)', content)
                if url_section:
                    url_text = url_section.group(1).strip()
                    urls = []
                    for url in re.split(r',\s*', url_text):
                        stripped = url.strip()
                        if stripped:
                            urls.append(stripped)
                    
                    for url in urls:
                        if 'github.com' in url.lower() or 'gitlab.com' in url.lower():
                            metadata_result.add_result(
                                constants.CAT_CODE_REPOSITORY,
                                {
                                    "value": url,
                                    "type": constants.URL,
                                },
                                1,
                                constants.TECHNIQUE_CODE_CONFIG_PARSER,
                                source
                            )
                        else:
                            metadata_result.add_result(
                                constants.CAT_HOMEPAGE,
                                {
                                    "value": url,
                                    "type": constants.URL,
                                },
                                1,
                                constants.TECHNIQUE_CODE_CONFIG_PARSER,
                                source
                            )
                
                issue_tracker_match = re.search(r'BugReports:\s*([^\n]+)', content)
                if issue_tracker_match:
                    issue_tracker_url = issue_tracker_match.group(1).strip()
                    metadata_result.add_result(
                        constants.CAT_ISSUE_TRACKER,
                        {
                            "value": issue_tracker_url,
                            "type": constants.URL,
                        },
                        1,
                        constants.TECHNIQUE_CODE_CONFIG_PARSER,
                        source
                    )


    except Exception as e:
        logging.error(f"Error parsing gemspec file from {file_path}: {str(e)}")
    
    return metadata_result


