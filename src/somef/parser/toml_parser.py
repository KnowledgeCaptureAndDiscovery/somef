# -*- coding: utf-8 -*-
import tomli
import re
import os
import logging
from pathlib import Path
from ..process_results import Result
from ..utils import constants
from ..regular_expressions import detect_license_spdx, detect_spdx_from_declared


def parse_toml_file(file_path, metadata_result: Result, source):
    """
    Unified TOML parser that handles Cargo.toml, pyproject.toml, and Project.toml files.

    Parameters
    ----------
    file_path: path to the TOML file being analyzed
    metadata_result: Metadata object dictionary
    source: source of the package file (URL)

    Returns
    -------
    metadata_result: Updated metadata result object
    """
    try:
        filename = Path(file_path).name.lower()

        if filename == "cargo.toml":
            file_type = "cargo"
            display_name = "Cargo.toml"

        elif filename == "pyproject.toml":
            file_type = "pyproject"
            display_name = "pyproject.toml"

        elif filename == "project.toml":
            file_type = "julia_project"
            display_name = "Project.toml"

        else:
            logging.warning(f"Unknown TOML file type: {filename}")
            return metadata_result

        metadata_result.add_result(
            constants.CAT_HAS_PACKAGE_FILE,
            {
                # "value": display_name,
                "value": source,
                "type": constants.URL,
            },
            1,
            constants.TECHNIQUE_CODE_CONFIG_PARSER,
            source
        )

        with open(file_path, "rb") as f:
            data = tomli.load(f)

        if file_type == "cargo":
            parse_cargo_metadata(data, metadata_result, source, file_path)
        elif file_type == "pyproject":
            parse_pyproject_metadata(data, metadata_result, source, file_path)
        elif file_type == "julia_project":
            parse_julia_project_metadata(data, metadata_result, source)

    except Exception as e:
        logging.error(f"Error parsing TOML file {file_path}: {str(e)}")

    return metadata_result


def extract_common_name_field(data, metadata_result, source, file_type):
    """
    Extract 'name' field that's common across Cargo.toml, pyproject.toml, and Project.toml.

    For Cargo.toml: data["package"]["name"]
    For pyproject.toml: data["project"]["name"] or data["tool"]["poetry"]["name"]
    For Project.toml: data["name"]
    """
    name_value = None

    if file_type == "cargo" and "package" in data and "name" in data["package"]:
        name_value = data["package"]["name"]

    elif file_type == "pyproject":
        project = get_project_data(data)
        if "name" in project:
            name_value = project["name"]

    elif file_type == "julia_project" and "name" in data:
        name_value = data["name"]

    if name_value:
        metadata_result.add_result(
            constants.CAT_PACKAGE_ID,
            {
                "value": name_value,
                "type": constants.STRING
            },
            1,
            constants.TECHNIQUE_CODE_CONFIG_PARSER,
            source
        )


def extract_common_version_field(data, metadata_result, source, file_type):
    """
    Extract 'version' field that's common across all three TOML types.

    For Cargo.toml: data["package"]["version"]
    For pyproject.toml: data["project"]["version"] or data["tool"]["poetry"]["version"]
    For Project.toml: data["version"]
    """
    version_value = None

    if file_type == "cargo" and "package" in data and "version" in data["package"]:
        version_value = data["package"]["version"]
        version_type = constants.RELEASE

    elif file_type == "pyproject":
        project = get_project_data(data)
        if "version" in project:
            version_value = project["version"]
            version_type = constants.RELEASE

    elif file_type == "julia_project" and "version" in data:
        version_value = data["version"]
        version_type = constants.STRING

    if version_value:
        result_dict = {
            "value": version_value,
            "type": version_type
        }
        if file_type in ["cargo", "pyproject"]:
            result_dict["tag"] = version_value

        metadata_result.add_result(
            constants.CAT_VERSION,
            result_dict,
            1,
            constants.TECHNIQUE_CODE_CONFIG_PARSER,
            source
        )


def extract_common_description_field(data, metadata_result, source, file_type):
    """
    Extract 'description' field common to Cargo.toml and pyproject.toml.

    For Cargo.toml: data["package"]["description"]
    For pyproject.toml: data["project"]["description"] or data["tool"]["poetry"]["description"]
    """
    description_value = None

    if file_type == "cargo" and "package" in data and "description" in data["package"]:
        description_value = data["package"]["description"]

    elif file_type == "pyproject":
        project = get_project_data(data)
        if "description" in project:
            description_value = project["description"]

    if description_value:
        metadata_result.add_result(
            constants.CAT_DESCRIPTION,
            {
                "value": description_value,
                "type": constants.STRING
            },
            1,
            constants.TECHNIQUE_CODE_CONFIG_PARSER,
            source
        )


def extract_common_authors_field(data, metadata_result, source, file_type):
    """
    Extract 'authors' field common across all three TOML types.

    All three formats can have authors with name and email.
    """
    authors = None

    if file_type == "cargo" and "package" in data and "authors" in data["package"]:
        authors = data["package"]["authors"]

    elif file_type == "pyproject":
        project = get_project_data(data)
        if "authors" in project:
            authors = project["authors"]

    elif file_type == "julia_project" and "authors" in data:
        authors = data["authors"]

    if authors:
        for author in authors:
            if isinstance(author, dict):
                # pyproject.toml format: {name: "...", email: "..."}
                author_data = {
                    "name": author.get("name"),
                    "email": author.get("email"),
                    "type": constants.AGENT,
                    "value": author.get("name")
                }
                if author.get("url"):
                    author_data["url"] = author.get("url")
            else:
                # String format "Name <email>" or just "Name"
                match = re.match(r'^(.+?)\s*<(.+?)>$', str(author).strip())
                if match:
                    author_name = match.group(1).strip()
                    author_email = match.group(2).strip()
                    author_data = {
                        "name": author_name,
                        "email": author_email,
                        "type": constants.AGENT,
                        "value": author_name
                    }
                else:
                    author_data = {
                        "name": str(author).strip(),
                        "email": None,
                        "type": constants.AGENT,
                        "value": str(author).strip()
                    }

            metadata_result.add_result(
                constants.CAT_AUTHORS,
                author_data,
                1,
                constants.TECHNIQUE_CODE_CONFIG_PARSER,
                source
            )


def extract_common_keywords_field(data, metadata_result, source, file_type):
    """
    Extract 'keywords' field common to Cargo.toml and pyproject.toml.
    """
    keywords = None

    if file_type == "cargo" and "package" in data and "keywords" in data["package"]:
        keywords = data["package"]["keywords"]
    elif file_type == "pyproject":
        project = get_project_data(data)
        if "keywords" in project:
            keywords = project["keywords"]

    if keywords:
        for keyword in keywords:
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


def parse_cargo_metadata(data, metadata_result, source, file_path):
    """Parse Cargo.toml specific metadata."""

    extract_common_name_field(data, metadata_result, source, "cargo")
    extract_common_version_field(data, metadata_result, source, "cargo")
    extract_common_description_field(data, metadata_result, source, "cargo")
    extract_common_authors_field(data, metadata_result, source, "cargo")
    extract_common_keywords_field(data, metadata_result, source, "cargo")

    if "package" in data and "repository" in data["package"]:
        metadata_result.add_result(
            constants.CAT_CODE_REPOSITORY,
            {
                "value": data["package"]["repository"],
                "type": constants.URL
            },
            1,
            constants.TECHNIQUE_CODE_CONFIG_PARSER,
            source
        )

    if "package" in data and "license" in data["package"]:
        license_value = data["package"]["license"]
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
        
        license_info_spdx = detect_license_spdx(license_text, 'JSON')

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

    if "dependencies" in data:
        dependencies = data["dependencies"]
        for name, info in dependencies.items():
            version, dep_type, req_details = determine_dependency_type(info)
            req = f"{name} = {{ {req_details} }}"

            metadata_result.add_result(
                constants.CAT_REQUIREMENTS,
                {
                    "value": req,
                    "name": name,
                    "version": version,
                    "type": constants.SOFTWARE_APPLICATION,
                    "dependency_type": dep_type
                },
                1,
                constants.TECHNIQUE_CODE_CONFIG_PARSER,
                source
            )

    # target-specific dependencies
    for key in data:
        if key.startswith("target.") and isinstance(data[key], dict) and "dependencies" in data[key]:
            target_deps = data[key]["dependencies"]
            for name, info in target_deps.items():
                version, dep_type, req_details = determine_dependency_type(info)
                req = f"{name} = {{ {req_details} }} (target-specific)"

                metadata_result.add_result(
                    constants.CAT_REQUIREMENTS,
                    {
                        "value": req,
                        "name": name,
                        "version": version,
                        "type": constants.SOFTWARE_APPLICATION,
                        "dependency_type": dep_type
                    },
                    1,
                    constants.TECHNIQUE_CODE_CONFIG_PARSER,
                    source
                )


def parse_pyproject_metadata(data, metadata_result, source, file_path):
    """Parse pyproject.toml specific metadata."""
    project = get_project_data(data)

    extract_common_name_field(data, metadata_result, source, "pyproject")
    extract_common_version_field(data, metadata_result, source, "pyproject")
    extract_common_description_field(data, metadata_result, source, "pyproject")
    extract_common_authors_field(data, metadata_result, source, "pyproject")
    extract_common_keywords_field(data, metadata_result, source, "pyproject")

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

    # build-system requires
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

    if "license" in project:
        license_info = project["license"]
        license_text = ""

        if isinstance(license_info, dict):
            license_path_file = license_info.get("file")
            if license_path_file:
                dir_path_license = os.path.dirname(file_path)
                license_path = os.path.join(dir_path_license, license_path_file)

                if os.path.exists(license_path):
                    with open(license_path, "r", encoding="utf-8") as f:
                        license_text = f.read()

                license_value = f"License file: {license_path_file}"
            else:
                license_text = license_info.get("text", "")
                license_value = license_info.get("type", "")
        else:
            license_text = ""
            license_value = license_info


        licence_info_spdx = None

        if license_text:
            license_info_spdx = detect_license_spdx(license_text, 'JSON')
        else:
            # there is no text in licence and we cant detect license in the text as usual,
            # so we check if the declared license matches an SPDX ID from our dictionary of licences
            license_info_spdx = detect_spdx_from_declared(license_value)

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

    runtimes = parse_runtime_platform_from_pyproject(project)
    if runtimes:
        for runtime in runtimes:
            metadata_result.add_result(
                constants.CAT_RUNTIME_PLATFORM,
                {
                    "value": f'{runtime["name"]}{runtime["version"]}',
                    "name": runtime["name"],
                    "version": runtime["version"],
                    "type": constants.STRING
                },
                1,
                constants.TECHNIQUE_CODE_CONFIG_PARSER,
                source
            )


def parse_julia_project_metadata(data, metadata_result, source):
    """Parse Project.toml (Julia) specific metadata."""
    extract_common_name_field(data, metadata_result, source, "julia_project")
    extract_common_version_field(data, metadata_result, source, "julia_project")
    extract_common_authors_field(data, metadata_result, source, "julia_project")

    if "uuid" in data:
        metadata_result.add_result(
            constants.CAT_IDENTIFIER,
            {
                "value": data["uuid"],
                "type": constants.STRING
            },
            1,
            constants.TECHNIQUE_CODE_CONFIG_PARSER,
            source
        )

    if "deps" in data:
        deps = data["deps"]
        for req in deps.keys():
            metadata_result.add_result(
                constants.CAT_REQUIREMENTS,
                {
                    "value": req,
                    "type": constants.STRING
                },
                1,
                constants.TECHNIQUE_CODE_CONFIG_PARSER,
                source
            )

    if "compat" in data:
        compat = data["compat"]
        for package_name, version in compat.items():
            metadata_result.add_result(
                constants.CAT_RUNTIME_PLATFORM,
                {
                    "value": f"{package_name}",
                    "package": package_name,
                    "version": version,
                    "type": constants.STRING
                },
                1,
                constants.TECHNIQUE_CODE_CONFIG_PARSER,
                source
            )


# Helper functions

def get_project_data(data):
    """Get project section from pyproject.toml (handles both standard and Poetry formats)."""
    project = data.get("project", {})
    if not project and "tool" in data and "poetry" in data["tool"]:
        project = data["tool"]["poetry"]
    return project


def parse_dependency(dependency_str):
    """Parse a dependency string to extract name and version."""
    if not dependency_str:
        return None, None

    parts = re.split(r'(>=|<=|==|!=|>|<|~=)', dependency_str, 1)
    name = parts[0].strip()
    if len(parts) > 1:
        version = ''.join(parts[1:])
    else:
        version = ""

    version = re.sub(r'[\[\]]', '', version)

    return name, version


def parse_url_type(url_label):
    """Determine the category for a URL based on its label."""
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


def determine_dependency_type(info):
    """Determine the type of dependency for Cargo.toml."""
    if isinstance(info, dict):
        if "version" in info:
            version = info["version"]
            req = f"version = {version}"
            dep_type = "version"
        elif "git" in info:
            version = info["git"]
            req = f"git = \"{version}\""
            dep_type = "url"
        elif "path" in info:
            version = info["path"]
            req = f"path = \"{version}\""
            dep_type = "path"
        else:
            version = str(info)
            req = f"other = {version}"
            dep_type = "other"
    else:
        version = info
        req = f"version = {version}"
        dep_type = "version"

    return version, dep_type, req


def parse_runtime_platform_from_pyproject(project_section):
    """Extract runtime platform from pyproject.toml."""
    runtimes = []

    deps = project_section.get("dependencies", {})
    if isinstance(deps, dict):
        python_spec = deps.get("python")
        if python_spec:
            runtimes.append({"name": "Python", "version": python_spec})

    req_python = project_section.get("requires-python")
    if req_python:
        runtimes.append({"name": "Python", "version": req_python})

    return runtimes
