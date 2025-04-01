import logging
import lxml.etree
from nltk.sem.hole import Constants

from ..process_results import Result
from ..utils import constants
"""
This code is inspired by Codemeta Project parsers, specifically java.py
https://github.com/proycon/codemetapy/blob/master/codemeta/parsers/java.py
"""
processed_pom = False
POM_NAMESPACE = "http://maven.apache.org/POM/4.0.0"

def parse_node(node):
    for subnode in node:
        if isinstance(subnode.tag, str) and subnode.tag.startswith(
            "{" + POM_NAMESPACE + "}"
        ):
            key = subnode.tag[len(POM_NAMESPACE) + 2 :]
            yield key, subnode

def parse_pom_file(file_path, metadata_result: Result, source):
    """

    Parameters
    ----------
    file_path: path to the package file being analysed
    metadata_result: metadata result where all categories are saved
    source: Source of the file being processed

    Returns
    -------

    """
    global processed_pom
    if processed_pom:
        logging.info(f"Skipping POM file {file_path} as another POM file was already processed")
        return metadata_result
    with open(file_path, 'rb') as file:
        data = lxml.etree.parse(file)
        
        root = data.getroot()
        if root.tag != "{" + POM_NAMESPACE + "}project":
            logging.warning(f"Expected root tag 'project' in {POM_NAMESPACE} namespace, got {root.tag} instead")
            return metadata_result

        group_id = None
        artifact_id = None
        version_value = None
        repositories = None

        project_data = {
            "identifier": None,
            "version": None,
            "name": None,
            "description": None,
            "url": None,
            "licenses": [],
            "dependencies": [],
            "developers": [],
            "issue_tracker": None,
            "scm_url": None
        }

        for key, node in parse_node(root):
            if key == "groupId":
                group_id = node.text
            elif key == "artifactId":
                artifact_id = node.text
            elif key == "version":
                version_value = node.text
            elif key == "name":
                project_data["name"] = node.text
            elif key == "licenses":
                project_data["licenses"] = parse_licenses(node)
            elif key == "repositories":
                repositories = parse_repositories(node)
            elif key == "issueManagement":
                project_data["issue_tracker"] = parse_issue_management(node)
            elif key == "scm":
                project_data["scm_url"] = parse_scm(node)        
            elif key == "developers":
                project_data["developers"] = parse_developers(node)              
            elif key == "dependencies":
                project_data["dependencies"] = parse_dependencies(node)
        
        if group_id or artifact_id:
            identifier_value = f"{group_id or ''}.{artifact_id or ''}".strip(':')
            metadata_result.add_result(
                constants.CAT_PACKAGE_ID,
                {
                    "value": identifier_value,
                    "type": constants.STRING
                },
                1,
                constants.TECHNIQUE_CODE_CONFIG_PARSER,
                source
            )

        if version_value:
            metadata_result.add_result(
                constants.CAT_VERSION,
                {
                    "value": version_value,
                    "type": constants.RELEASE
                },
                1,
                constants.TECHNIQUE_CODE_CONFIG_PARSER,
                source
            )
        
        if project_data["issue_tracker"]:
            metadata_result.add_result(
                constants.CAT_ISSUE_TRACKER,
                {
                    "value": project_data["issue_tracker"],
                    "type": constants.URL
                },
                1,
                constants.TECHNIQUE_CODE_CONFIG_PARSER,
                source
            )
    
        if project_data["scm_url"]:
            metadata_result.add_result(
                constants.CAT_PACKAGE_DISTRIBUTION,
                {
                    "value": project_data["scm_url"],
                    "type": constants.URL
                },
                1,
                constants.TECHNIQUE_CODE_CONFIG_PARSER,
                source
            )

        if project_data["dependencies"]	:
            metadata_result.add_result(
                constants.CAT_REQUIREMENTS ,
                {
                    "value": project_data["dependencies"],
                    "type": constants.URL
                },
                1,
                constants.TECHNIQUE_CODE_CONFIG_PARSER,
                source
            )
        
        if project_data["developers"]	:
            metadata_result.add_result( 
                constants.CAT_AUTHORS ,
                {
                    "value": project_data["developers"],
                    "type": constants.URL
                },
                1,
                constants.TECHNIQUE_CODE_CONFIG_PARSER,
                source
            )

        if repositories:
            metadata_result.add_result(
                constants.CAT_PACKAGE_DISTRIBUTION,
                {
                    "value": repositories,
                    "type": constants.URL
                },
                1,
                constants.TECHNIQUE_CODE_CONFIG_PARSER,
                source
            )

        metadata = {}
        for k, v in project_data.items():
            if v: 
                metadata[k] = v
        
        metadata_result.add_result(
            constants.CAT_HAS_PACKAGE_FILE,
            {
                "value": "pom.xml",
                "type": constants.URL
            },
            1,
            constants.TECHNIQUE_CODE_CONFIG_PARSER,
            source
        )
        
        processed_pom = True

    return metadata_result

def parse_licenses(licenses_node):
    licenses = []
    for key, node in parse_node(licenses_node):
        if key == "license":
            license_data = {}
            for key2, node2 in parse_node(node):
                if key2 in ["name", "url"] and node2.text:
                    license_data[key2] = node2.text
            if license_data:
                licenses.append(license_data)
    return licenses

def parse_dependencies(dependencies_node):
    dependencies = []
    for key, node in parse_node(dependencies_node):
        if key == "dependency":
            dep_data = {}
            for key2, node2 in parse_node(node):
                if key2 in ["groupId", "artifactId", "version"] and node2.text:
                    dep_data[key2] = node2.text
            if dep_data:
                dependencies.append(dep_data)
    return dependencies

def parse_developers(developers_node):
    developers = []
    for key, node in parse_node(developers_node):
        if key == "developer":
            dev_data = {}
            author_data = {
                "name": None,
                "email": None,
                "url": None,
                "organization": None,
                "type": constants.AGENT
            }
            for key2, node2 in parse_node(node):
                if key2 == "name" and node2.text:
                    author_data["name"] = node2.text
                    author_data["value"] = node2.text 
                elif key2 == "email" and node2.text:
                    author_data["email"] = node2.text
                elif key2 == "url" and node2.text:
                    author_data["url"] = node2.text
                elif key2 == "organization" and node2.text:
                    author_data["organization"] = node2.text

            if not author_data["value"]:
                author_data["value"] = author_data["email"] or author_data["organization"]
            dev_data.update({k: v for k, v in author_data.items() if k != "type"})
            developers.append(dev_data)
    return developers

def parse_issue_management(issue_node):
    for key, node in parse_node(issue_node):
        if key == "url" and node.text and "$" not in node.text:
            return node.text
    return None

def parse_scm(scm_node):
    for key, node in parse_node(scm_node):
        if key == "url" and node.text and "$" not in node.text:
            return node.text
    return None

def parse_repositories(repo_node):
    repos = []
    for key, node in parse_node(repo_node):
        if key == "repository":
            repo_data = {}
            for key2, node2 in parse_node(node):
                if key2 in ["id", "name", "url"] and node2.text:
                    repo_data[key2] = node2.text
            if repo_data:
                repos.append(repo_data)
    return repos