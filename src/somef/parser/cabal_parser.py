import os
import re
import logging
from pathlib import Path
from ..process_results import Result
from ..regular_expressions import detect_license_spdx
from ..utils import constants

def parse_cabal_file(file_path, metadata_result: Result, source):
    """
    Parse a .cabal file and extract relevant metadata.
    
    Parameters
    ----------
    file_path: path of the cabal file being analysed
    metadata_result: metadata object where the metadata dictionary is kept
    source: source of the package file (URL)

    Returns
    """

    try:
        if file_path.endswith('.cabal'):
            metadata_result.add_result(
                constants.CAT_HAS_PACKAGE_FILE,
                {
                    # "value": Path(file_path).name,
                    "value": source,
                    "type": constants.URL,
                },
                1,
                constants.TECHNIQUE_CODE_CONFIG_PARSER,
                source
            )
            
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

                name_match = re.search(r'name:\s*(.*)', content, re.IGNORECASE)
                if name_match:
                    metadata_result.add_result(
                        constants.CAT_PACKAGE_ID,
                        {
                            "value": name_match.group(1),
                            "type": constants.STRING
                        },
                        1,
                        constants.TECHNIQUE_CODE_CONFIG_PARSER,
                        source
                    )
                
                version_match = re.search(r'version:\s*(.*)', content, re.IGNORECASE)
                if version_match:
                    metadata_result.add_result(
                        constants.CAT_VERSION,
                        {
                            "value": version_match.group(1),
                            "type": constants.STRING
                        },
                        1,
                        constants.TECHNIQUE_CODE_CONFIG_PARSER,
                        source
                    )


                # description_match = re.search(r'description:\s*(.*)', content, re.IGNORECASE)
                cleaned_content = content.replace('\r\n', '\n').replace('\r', '\n')
                description_regex = re.compile(
                    r'description:\s*(.*?)(?=\n\S|\Z)', 
                    re.IGNORECASE | re.DOTALL
                )
                
                description_match = description_regex.search(cleaned_content)
                synopsis_match = re.search(r'synopsis:\s*(.*)', content, re.IGNORECASE)
                if description_match:
                         
                    metadata_result.add_result(
                        constants.CAT_DESCRIPTION,
                        {
                            "value": description_match.group(1),
                            "type": constants.STRING
                        },
                        1,
                        constants.TECHNIQUE_CODE_CONFIG_PARSER,
                        source
                    )
                    if synopsis_match:
                        metadata_result.add_result(
                            constants.CAT_DESCRIPTION,
                            {
                                "value": synopsis_match.group(1),
                                "type": constants.STRING
                            },
                            1,
                            constants.TECHNIQUE_CODE_CONFIG_PARSER,
                            source
                        )
                
                homepage_match = re.search(r'homepage:\s*(.*)', content, re.IGNORECASE)
                if homepage_match:
                    metadata_result.add_result(
                        constants.CAT_HOMEPAGE,
                        {
                            "value": homepage_match.group(1),
                            "type": constants.URL
                        },
                        1,
                        constants.TECHNIQUE_CODE_CONFIG_PARSER,
                        source
                    )

                stability_match = re.search(r'stability:\s*(.*)', content, re.IGNORECASE)
                if stability_match:
                    metadata_result.add_result(
                        constants.CAT_DEV_STATUS,  
                        {
                            "value": stability_match.group(1),
                            "type": constants.STRING   
                        },
                        1,
                        constants.TECHNIQUE_CODE_CONFIG_PARSER,
                        source
                    )

                bug_reports_match = re.search(r'bug-reports:\s*(.*)', content, re.IGNORECASE)
                if bug_reports_match:
                    metadata_result.add_result(
                        constants.CAT_ISSUE_TRACKER, 
                        {
                            "value": bug_reports_match.group(1),
                            "type": constants.URL  
                        },
                        1,
                        constants.TECHNIQUE_CODE_CONFIG_PARSER,
                        source
                    )

                license_match = re.search(r'license:\s*(.*)', content, re.IGNORECASE)
                if license_match:
                    license_value = license_match.group(1)
                    license_text = ""
                    
                    dir_path = os.path.dirname(file_path)
                    license_paths = [
                        os.path.join(dir_path, "LICENSE"),
                        os.path.join(dir_path, "LICENSE.txt"),
                        os.path.join(dir_path, "LICENSE.md")
                    ]
                    
                    for license_path in license_paths:
                        if os.path.exists(license_path):
                            with open(license_path, "r", encoding="utf-8") as lf:
                                license_text = lf.read()
                            break
                    
                    license_info_spdx = detect_license_spdx(license_text, 'Ruby')
                    
                    if license_info_spdx:
                        license_data = {
                            "value": license_value,
                            "spdx_id": license_info_spdx.get('spdx_id'),
                            "name": license_info_spdx.get('name'),
                            "type": constants.LICENSE
                        }
                    else:
                        license_data = {
                            "value": license_value,
                            "type": constants.LICENSE
                        }
                    
                    metadata_result.add_result(
                        constants.CAT_LICENSE,
                        license_data,
                        1,
                        constants.TECHNIQUE_CODE_CONFIG_PARSER,
                        source
                    )
                
                library_section_match = re.search(r'library\s*\n(.*?)(?=\n\S|\Z)', content, re.DOTALL | re.IGNORECASE)
                if library_section_match:
                    library_content = library_section_match.group(1)
                    
                    build_depends_match = re.search(
                        r'build-depends:\s*(.*?)(?=\n\s*(?:[A-Za-z0-9_-]+\s*:|if\s|\Z))',
                        library_content,
                        re.DOTALL
                    )
                    # build_depends_match = re.search(r'build-depends:\s*(.*?)(?=\n\s*\w+:|\Z)', library_content, re.DOTALL)
                    if build_depends_match:
                        build_depends_content = build_depends_match.group(1)
                        
                        dependencies = re.split(r'[,\n]', build_depends_content)
                        
                        for dep_line in dependencies:
                            dep_line = dep_line.strip()
                            if dep_line and not dep_line.startswith(','):
                                
                                dep_match = re.match(r'^([a-zA-Z0-9-_]+)\s*(.*?)$', dep_line)
                                if dep_match:
                                    name = dep_match.group(1)
                                    version_constraint = dep_match.group(2).strip() if dep_match.group(2) else "any"
                                    req = f"{name}: {version_constraint}" if version_constraint != "any" else name
                                    
                                    metadata_result.add_result(
                                        constants.CAT_REQUIREMENTS,
                                        {
                                            "value": req,
                                            "name": name,
                                            "version": version_constraint,
                                            "type": constants.SOFTWARE_APPLICATION,
                                            "dependency_type": "runtime"
                                        },
                                        1,
                                        constants.TECHNIQUE_CODE_CONFIG_PARSER,
                                        source
                                    )
                
    except Exception as e:
        logging.error(f"Error parsing gemspec file from {file_path}: {str(e)}")
    
    return metadata_result