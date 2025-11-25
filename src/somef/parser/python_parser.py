import ast
import os
import tomli
import logging
import re
from pathlib import Path
from ..process_results import Result
from ..utils import constants 
from ..regular_expressions import detect_license_spdx
"""
This code is inspired by Codemeta Project parsers, specifically python.py
https://github.com/proycon/codemetapy/blob/master/codemeta/parsers/python.py
"""

def parse_dependency(dependency_str):

    if not dependency_str:
        return None, None
    # parts = re.split(r'(>=|<=|==|!=|>|<|~=|\[)', dependency_str, 1)
    parts = re.split(r'(>=|<=|==|!=|>|<|~=)', dependency_str, 1)
    name = parts[0].strip()
    if len(parts) > 1:
        version = ''.join(parts[1:])
    else:
        version = ""

    # version = version.strip("[]() -.,:")
    version = re.sub(r'[\[\]\(\)]', '', version)

    return name, version

def parse_url_type(url_label):
    label = url_label.lower()
    
    if "repository" in label or label in ("git", "github", "code", "sourcecode", "source"):
        return constants.CAT_CODE_REPOSITORY
    elif "issue" in label or label in ("bug tracker", "tracker", "issues"):
        return constants.CAT_ISSUE_TRACKER
    elif "doc" in label or label in ("documentation", "api reference", "reference"):
        return constants.CAT_DOCUMENTATION
    elif label == "readme":
        return constants.CAT_README_URL
    elif "download" in label:
        return constants.CAT_DOWNLOAD_URL
    elif "homepage" in label:
        return constants.CAT_HOMEPAGE
    else:
        return constants.CAT_RELATED_DOCUMENTATION

def parse_author_string(author_str):
    if not author_str:
        return {"name": None, "email": None}
    
    email_match = re.search(r'<([^>]+)>', author_str)
    if email_match:
        email = email_match.group(1)
        name = author_str[:email_match.start()].strip()
        return {"name": name, "email": email}
    
    return {"name": author_str, "email": None}

def get_project_data(data):
    project = data.get("project", {})
    if not project and "tool" in data and "poetry" in data["tool"]:
        project = data["tool"]["poetry"]
    return project

def parse_pyproject_toml(file_path, metadata_result: Result, source):
    """

    Parameters
    ----------
    file_path: path to the package file being analysed
    metadata_result: Metadata object dictionary
    source: source of the package file (URL)

    Returns
    -------

    """
    try:
        if Path(file_path).name == "pyproject.toml":
            metadata_result.add_result(
                constants.CAT_HAS_PACKAGE_FILE,
                {
                    "value": "pyproject.toml",
                    "type": constants.URL,
                },
                1,
                constants.TECHNIQUE_CODE_CONFIG_PARSER,
                source
            )
            with open(file_path, "rb") as f:
                data = tomli.load(f)
                
                project = get_project_data(data)
                if "name" in project:
                    metadata_result.add_result(
                        constants.CAT_PACKAGE_ID,
                        {
                            "value": project["name"], 
                            "type": constants.STRING
                        },
                        1,
                        constants.TECHNIQUE_CODE_CONFIG_PARSER,
                        source
                    )
                
                if "description" in project:
                    metadata_result.add_result(
                        constants.CAT_DESCRIPTION,
                        {
                            "value": project["description"], 
                            "type": constants.STRING
                        },
                        1,
                        constants.TECHNIQUE_CODE_CONFIG_PARSER,
                        source
                    )

                if "homepage" in project:
                    metadata_result.add_result(
                        constants.CAT_HOMEPAGE,
                        {
                            "value": project["homepage"], 
                            "type": constants.URL
                        },
                        1,
                        constants.TECHNIQUE_CODE_CONFIG_PARSER,
                        source
                    )

                if "version" in project:
                    metadata_result.add_result(
                        constants.CAT_VERSION,
                        {
                            "value": project["version"],
                            "type": constants.RELEASE,
                            "tag": project["version"]
                        },
                        1,
                        constants.TECHNIQUE_CODE_CONFIG_PARSER,
                        source
                    )
                
                dependencies = project.get("dependencies", [])
                if isinstance(dependencies, list):
                    for req in dependencies:
                        name, version = parse_dependency(req)
                        if name:
                            metadata_result.add_result(
                                constants.CAT_REQUIREMENTS,
                                {
                                    "value": req,
                                    "name": name, 
                                    "version": version, 
                                    "type": constants.SOFTWARE_APPLICATION
                                },
                                1,
                                constants.TECHNIQUE_CODE_CONFIG_PARSER,
                                source
                            )
                elif isinstance(dependencies, dict):
                    for name, version in dependencies.items():
                        req = f"{name}{version}" if version else name
                        metadata_result.add_result(
                            constants.CAT_REQUIREMENTS,
                            {
                                "value": req, 
                                "name": name, 
                                "version": version, 
                                "type": constants.SOFTWARE_APPLICATION
                            },
                            1,
                            constants.TECHNIQUE_CODE_CONFIG_PARSER,
                            source
                        )
                        
                # This is for detecting the "requires" section in a pyrpoject.toml file      
                if "build-system" in data and "requires" in data["build-system"]:
                    build_requires = data["build-system"]["requires"]
                    if isinstance(build_requires, list):
                        for req in build_requires:
                            name, version = parse_dependency(req)
                            if name:
                                metadata_result.add_result(
                                    constants.CAT_REQUIREMENTS,
                                    {
                                        "value": req,
                                        "name": name,
                                        "version": version,
                                        "type": constants.SOFTWARE_APPLICATION
                                    },
                                    1,
                                    constants.TECHNIQUE_CODE_CONFIG_PARSER,
                                    source
                                )
                
                urls = project.get("urls", {})

                if not urls and "tool" in data and "poetry" in data["tool"]:             
                    poetry = data["tool"]["poetry"]
                    if "repository" in poetry:
                        urls["repository"] = poetry["repository"]
                    if "homepage" in poetry:
                        urls["homepage"] = poetry["homepage"]
                    if "documentation" in poetry:
                        urls["documentation"] = poetry["documentation"]
                
                for url_type, url in urls.items():
                    # print(url_type)
                    category = parse_url_type(url_type)
                    metadata_result.add_result(
                        category,
                        {
                            "value": url, 
                            "type": constants.URL
                        },
                        1,
                        constants.TECHNIQUE_CODE_CONFIG_PARSER,
                        source
                    )
                
                authors = project.get("authors", [])
                if isinstance(authors, list):
                    for author in authors:
                        if isinstance(author, dict):
                            author_data = {
                                "name": author.get("name"),
                                "email": author.get("email"),
                                "type": constants.AGENT,
                                "value": author.get("name")
                            }
                            if author.get("url") is not None:
                                author_data["url"] = author.get("url")
                        else:
                
                            parsed = parse_author_string(author)
                            author_data = {
                                "name": parsed["name"],
                                "email": parsed["email"],
                                "type": constants.AGENT,
                                "value": parsed["name"]
                            }
                        
                        metadata_result.add_result(
                            constants.CAT_AUTHORS,
                            author_data,
                            1,
                            constants.TECHNIQUE_CODE_CONFIG_PARSER,
                            source
                        )

                if "license" in project:
                    license_info = project["license"]
                    license_text = ""

                    if isinstance(license_info, dict):
                        # Check if license is specified as a file
                        license_path_file = license_info["file"]
                        dir_path_license = os.path.dirname(file_path)
                        license_path = os.path.join(dir_path_license, license_path_file)

                        if os.path.exists(license_path):
                            with open(license_path, "r", encoding="utf-8") as f:
                                license_text = f.read()

                        if "file" in license_info:
                            license_value = f"License file: {license_info['file']}"
                        else:
                            license_text = license_info.get("text", "")
                            license_value = license_info.get("type", "")
                    else:
                        license_text = ""
                        license_value = license_info

                    license_info_spdx = detect_license_spdx(license_text, 'JSON')
                    spdx_id = ""
                    spdx_name = ""

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

                if "keywords" in project:
                    for keyword in project["keywords"]:
                        metadata_result.add_result(
                            constants.CAT_KEYWORDS,
                            {
                                "value": keyword, 
                                "type": constants.STRING
                            },
                            1,
                            constants.TECHNIQUE_CODE_CONFIG_PARSER,
                            source
                        )
                

                runtimes = parse_runtime_platform_from_pyproject(project)

                if runtimes:
                    for runtime in runtimes:
                        metadata_result.add_result(
                            constants.CAT_RUNTIME_PLATFORM,
                            {
                                "value": runtime["value"],
                                "version": runtime["version"],
                                "name": runtime["name"],
                                "type": constants.STRING
                            },
                            1,
                            constants.TECHNIQUE_CODE_CONFIG_PARSER,
                            source
                        )
                        
                
    except Exception as e:
        logging.error(f"Error parsing pyproject.toml from {file_path}: {str(e)}")

    return metadata_result    

def parse_requirements_txt(file_path, metadata_result: Result, source):
    """
    Parameters
    ----------
    file_path: path to the requirements.txt file being analyzed
    metadata_result: Metadata object dictionary
    source: source of the package file (URL)

    Returns
    -------
    metadata_result: Updated metadata result object
    """
    try:
        if Path(file_path).name.lower() in ["requirements.txt", "requirement.txt"]:
  
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

                for line in lines:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    name, version = parse_dependency(line)
                    if name:
                        req = {
                                "value": line,
                                "name": name,
                                "type": constants.SOFTWARE_APPLICATION
                            }
                        if version:
                            req['version'] = version
                        
                        metadata_result.add_result(
                            constants.CAT_REQUIREMENTS,
                            req,
                            1,
                            constants.TECHNIQUE_CODE_CONFIG_PARSER,
                            source
                        )
     

                runtimes = parse_runtime_platform_from_requirements(lines)
                if runtimes:
                    for runtime in runtimes:
                        metadata_result.add_result(
                            constants.CAT_RUNTIME_PLATFORM,
                            {
                                "value": runtime["value"],
                                "version": runtime["version"],
                                "name": runtime["name"],
                                "type": constants.STRING
                            },
                            1,
                            constants.TECHNIQUE_CODE_CONFIG_PARSER,
                            source
                        )
    except Exception as e:
        logging.error(f"Error parsing requirements.txt from {file_path}: {str(e)}")

    return metadata_result

def parse_setup_py(file_path, metadata_result: Result, source):
    """

    Parameters
    ----------
    file_path: file path of the package files being assessed.
    metadata_result: metadata dictionary object
    source: source file being assessed (URL)

    Returns
    -------

    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                file_content = f.read()
                tree = ast.parse(file_content)
                
                module_vars = {}
                for node in ast.iter_child_nodes(tree):
                    if isinstance(node, ast.Assign):
                        for target in node.targets:
                            if isinstance(target, ast.Name):
                                try:
                                    value = ast.literal_eval(node.value)
                                    module_vars[target.id] = value
                                except (ValueError, SyntaxError):
                                    pass
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.Call) and hasattr(node.func, 'id') and node.func.id == 'setup':
        
                        for keyword in node.keywords:
                            if keyword.arg == "name":
                                try:
                                    if isinstance(keyword.value, ast.Name) and keyword.value.id in module_vars:
                                        value = module_vars[keyword.value.id]
                                    else:
                                        value = ast.literal_eval(keyword.value)
                                    
                                    metadata_result.add_result(
                                        constants.CAT_PACKAGE_ID,
                                        {"value": value, 
                                        "type": constants.STRING
                                        },
                                        1,
                                        constants.TECHNIQUE_CODE_CONFIG_PARSER,
                                        source
                                    )
                                except (ValueError, SyntaxError):
                                    pass
                                    
                            elif keyword.arg.lower() == "author" :
                                try:
                                    if isinstance(keyword.value, ast.Name) and keyword.value.id in module_vars:
                                        value = module_vars[keyword.value.id]
                                    else:
                                        value = ast.literal_eval(keyword.value)
                                    
                                    metadata_result.add_result(
                                        constants.CAT_AUTHORS,
                                        {
                                            "name": value,
                                            # "email": None,
                                            "type": constants.AGENT,
                                        },
                                        1,
                                        constants.TECHNIQUE_CODE_CONFIG_PARSER,
                                        source
                                    )
                                except (ValueError, SyntaxError):
                                    pass
                                    
                            elif keyword.arg == "author_email" or keyword.arg == "EMAIL":
                                try:
                                    if isinstance(keyword.value, ast.Name) and keyword.value.id in module_vars:
                                        value = module_vars[keyword.value.id]
                                    else:
                                        value = ast.literal_eval(keyword.value)

                                    # author_results = metadata_result.results.get(constants.CAT_AUTHORS, [])
                                    author_results = [
                                        a for a in metadata_result.results.get(constants.CAT_AUTHORS, [])
                                        if a.get("technique") == constants.TECHNIQUE_CODE_CONFIG_PARSER
                                    ]
                                    if author_results:
                                        for result in author_results:
                                            result["result"]["email"] = value
                                    else:
                                        metadata_result.add_result(
                                            constants.CAT_AUTHORS,
                                            {
                                                # "name": None,
                                                "email": value,
                                                "type": constants.AGENT,
                                                "value": value
                                            },
                                            1,
                                            constants.TECHNIQUE_CODE_CONFIG_PARSER,
                                            source
                                        )
                                except (ValueError, SyntaxError):
                                    pass
                                    
                            elif keyword.arg == "description" or keyword.arg == "DESCRIPTION":
                                try:
                                    if isinstance(keyword.value, ast.Name) and keyword.value.id in module_vars:
                                        value = module_vars[keyword.value.id]
                                    else:
                                        value = ast.literal_eval(keyword.value)
                                    
                                    metadata_result.add_result(
                                        constants.CAT_DESCRIPTION,
                                        {
                                            "value": value, 
                                            "type": constants.STRING
                                        },
                                        1,
                                        constants.TECHNIQUE_CODE_CONFIG_PARSER,
                                        source
                                    )
                                except (ValueError, SyntaxError):
                                    pass
                                    
                            elif keyword.arg == "url" or keyword.arg == "URL":
                                try:
                                    if isinstance(keyword.value, ast.Name) and keyword.value.id in module_vars:
                                        value = module_vars[keyword.value.id]
                                    else:
                                        value = ast.literal_eval(keyword.value)
                                    
                                    metadata_result.add_result(
                                        constants.CAT_CODE_REPOSITORY,
                                        {
                                            "value": value, 
                                            "type": constants.URL
                                        },
                                        1,
                                        constants.TECHNIQUE_CODE_CONFIG_PARSER,
                                        source
                                    )
                                except (ValueError, SyntaxError):
                                    pass
                                    
                            elif keyword.arg == "license":
                                try:
                                    if isinstance(keyword.value, ast.Name) and keyword.value.id in module_vars:
                                        value = module_vars[keyword.value.id]
                                    else:
                                        value = ast.literal_eval(keyword.value)
                                    
                                    metadata_result.add_result(
                                        constants.CAT_LICENSE,
                                        {
                                            "value": value,
                                            "type": constants.LICENSE
                                        },
                                        1,
                                        constants.TECHNIQUE_CODE_CONFIG_PARSER,
                                        source
                                    )
                                except (ValueError, SyntaxError):
                                    pass
                                    
                            elif keyword.arg == "keywords":
                                try:
                                    if isinstance(keyword.value, ast.Name) and keyword.value.id in module_vars:
                                        value = module_vars[keyword.value.id]
                                    else:
                                        value = ast.literal_eval(keyword.value)
                                    
                                    if isinstance(value, str):
                                        keywords = [k.strip() for k in value.split(',')]
                                    elif isinstance(value, list):
                                        keywords = value
                                    else:
                                        keywords = []
                                        
                                    for keyword_value in keywords:
                                        metadata_result.add_result(
                                            constants.CAT_KEYWORDS,
                                            {
                                                "value": keyword_value, 
                                                "type": constants.STRING
                                            },
                                            1,
                                            constants.TECHNIQUE_CODE_CONFIG_PARSER,
                                            source
                                        )
                                except (ValueError, SyntaxError):
                                    pass
                                    
                            elif keyword.arg == "classifiers":
                                try:
                                    if isinstance(keyword.value, ast.Name) and keyword.value.id in module_vars:
                                        value = module_vars[keyword.value.id]
                                    else:
                                        value = ast.literal_eval(keyword.value)
                                    
                                    if isinstance(value, list):
                                        for classifier in value:
                                            if "Programming Language :: Python" in classifier:
                                                metadata_result.add_result(
                                                    constants.CAT_PROGRAMMING_LANGUAGES,
                                                    {
                                                        "value": "Python",
                                                        "type": constants.STRING
                                                    },
                                                    1,
                                                    constants.TECHNIQUE_CODE_CONFIG_PARSER,
                                                    source
                                                )
                                                # TO DO extract version (if available) and add it as a "version" field
                                                # if " :: " in classifier:
                                                #     parts = classifier.split(" :: ")
                                                #     if len(parts) > 2 and parts[1] == "Python":
                                                #         python_version = parts[2]
                                                        
                                except (ValueError, SyntaxError):
                                    pass

            except SyntaxError:
                logging.warning(f"Syntax error in {file_path}, couldn't parse setup.py")
                
    except Exception as e:
        logging.error(f"Error parsing setup.py from {file_path}: {str(e)}")

    return metadata_result

def parse_runtime_platform_from_pyproject(project_section):
    """
    Given the `[tool.poetry]` section from pyproject.toml,
    this method extracts the runtime platform(s) declared (e.g. Python version). Return a list of dicts.

    """
    runtimes = []

    deps = project_section.get("dependencies", {})
    if isinstance(deps, dict):
        python_spec = deps.get("python")
        if python_spec:
            runtimes.append({"name": "Python", "version": python_spec, "value": f'Python {python_spec}'})

    req_python = project_section.get("requires-python")
    if req_python:
        runtimes.append({"name": "Python", "version": req_python, "value": f'Python {python_spec}'})

    return runtimes

def parse_runtime_platform_from_requirements(requirements_lines):
    """
    Extracts runtime information (e.g., Python) from a requirements.txt file.
    Only returns an entry if the runtime is explicitly mentioned with a version.

    Parameters
    ----------
    requirements_lines : 
        Lines from the requirements.txt file.

    Returns
    -------
    list of dict
        Each dictionary has the keys 'name' and 'version', e.g.:
        [{'name': 'Python', 'version': '3.11'}]
        Returns an empty list if no explicit runtime information is found.
    """
    runtimes = []

    if not requirements_lines:
        return runtimes

    for line in requirements_lines:
        clean_line = line.strip()
        if not clean_line or clean_line.startswith('#'):
            continue

        if clean_line.lower().startswith('python'):
            version = None

            for sep in ['==', '>=', '<=', '~=', '>', '<']:
                if sep in clean_line:
                    version = clean_line.split(sep)[1].strip()
                    break

            if version is None:
                match = re.search(r'python\s*([0-9.]+)', clean_line, re.IGNORECASE)
                if not match:
                    match = re.search(r'python([0-9.]+)', clean_line, re.IGNORECASE)
                if match:
                    version = match.group(1)

            if version:
                runtimes.append({'name': 'Python', 'version': version, 'value': f'Python: {version}'})
                break 

    return runtimes