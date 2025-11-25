import os
import re
import logging
from pathlib import Path
from ..process_results import Result
from ..utils import constants
from ..regular_expressions import detect_license_spdx

def parse_gemspec_file(file_path, metadata_result: Result, source):
    # To do Version
    # To do Email
    """
    Parse a Ruby gemspec file to extract metadata.

    Parameters
    ----------
    file_path: path of the gemspec file being analysed
    metadata_result: metadata object where the metadata dictionary is kept
    source: source of the package file (URL)

    Returns
    -------
    metadata_result: Updated metadata result object
    """
    try:
        if file_path.endswith('.gemspec'):
            metadata_result.add_result(
                constants.CAT_HAS_PACKAGE_FILE,
                {
                    "value": Path(file_path).name,
                    "type": constants.URL,
                },
                1,
                constants.TECHNIQUE_CODE_CONFIG_PARSER,
                source
            )
            
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

                name_match = re.search(r'gem\.name\s*=\s*["\']([^"\']+)["\']', content)
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
                
                desc_match = re.search(r'gem\.description\s*=\s*%q{([^}]+)}|gem\.description\s*=\s*["\']([^"\']+)["\']', content)
                if desc_match:
                    description = desc_match.group(1) if desc_match.group(1) else desc_match.group(2)
                    metadata_result.add_result(
                        constants.CAT_DESCRIPTION,
                        {
                            "value": description,
                            "type": constants.STRING
                        },
                        1,
                        constants.TECHNIQUE_CODE_CONFIG_PARSER,
                        source
                    )
                
                homepage_match = re.search(r'gem\.homepage\s*=\s*["\']([^"\']+)["\']', content)
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
                
                authors_match = re.findall(r'gem\.author[s]?\s*=\s*(?P<value>"[^"]*"|\[[^\]]*\])', content)

                for match in authors_match:
                    if match.startswith('['):
                        author_list = re.findall(r'["\']([^"\']+)["\']', match)
                    else:
                        author_list = [re.sub(r'["\']', '', match).strip()]
     
                    for author in author_list:
                        metadata_result.add_result(
                            constants.CAT_AUTHORS,
                            {
                                "type": constants.AGENT,
                                "value": author
                            },
                            1,
                            constants.TECHNIQUE_CODE_CONFIG_PARSER,
                            source
                        )

                    # authors_str = authors_match.group(1)
                    # author_list = re.findall(r'["\']([^"\']+)["\']', authors_str)
                    
                    # for author in author_list:
                    #     metadata_result.add_result(
                    #         constants.CAT_AUTHORS,
                    #         {
                    #             "type": constants.AGENT,
                    #             "value": author
                    #         },
                    #         1,
                    #         constants.TECHNIQUE_CODE_CONFIG_PARSER,
                    #         source
                    #     )
                
                # license_match = re.search(r'gem\.license\s*=\s*["\']([^"\']+)["\']', content)
                license_match = re.search(r'gem\.license[s]?\s*=\s*["\']([^"\']+)["\']', content)
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


                dependency_matches = re.search(r'gem\.requirements\s*=\s*(\[.*?\])', content, re.DOTALL)

                if dependency_matches:
                    array_requirements = dependency_matches.group(1)    
                    dependencies = re.findall(r'["\']([^"\']+)["\']', array_requirements)

                    if dependencies:
                        metadata_result.add_result(
                            constants.CAT_REQUIREMENTS,
                            {
                                "value": dependencies,
                                "type": constants.SOFTWARE_APPLICATION,
                            },
                            1,
                            constants.TECHNIQUE_CODE_CONFIG_PARSER,
                            source
                        )


                dependency_matches = re.findall(r'gem\.add_dependency\s*["\']([^"\']+)["\'](?:\s*,\s*["\']([^"\']+)["\'])?', content)
                for dep in dependency_matches:
                    name = dep[0]
                    version = dep[1] if len(dep) > 1 and dep[1] else "any"
                    req = f"{name}: {version}"
                    
                    metadata_result.add_result(
                        constants.CAT_REQUIREMENTS,
                        {
                            "value": req,
                            "name": name,
                            "version": version,
                            "type": constants.SOFTWARE_APPLICATION,
                            "dependency_type": "runtime"
                        },
                        1,
                        constants.TECHNIQUE_CODE_CONFIG_PARSER,
                        source
                    )
                
                dev_dependency_matches = re.findall(r'gem\.add_development_dependency\s*["\']([^"\']+)["\'](?:\s*,\s*["\']([^"\']+)["\'])?', content)
                for dep in dev_dependency_matches:
                    name = dep[0]
                    version = dep[1] if len(dep) > 1 and dep[1] else "any"
                    req = f"{name}: {version}"
                    
                    metadata_result.add_result(
                        constants.CAT_REQUIREMENTS,
                        {
                            "value": req,
                            "name": name,
                            "version": version,
                            "type": constants.SOFTWARE_APPLICATION,
                            "dependency_type": "dev"
                        },
                        1,
                        constants.TECHNIQUE_CODE_CONFIG_PARSER,
                        source
                    )
                
    except Exception as e:
        logging.error(f"Error parsing gemspec file from {file_path}: {str(e)}")
    
    return metadata_result