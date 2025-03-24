import logging
import lxml.etree
from ..process_results import Result
from ..utils import constants

POM_NAMESPACE = "http://maven.apache.org/POM/4.0.0"

def parse_node(node):
    """Function parsing XML nodes from POM file"""
    for subnode in node:
        if isinstance(subnode.tag, str) and subnode.tag.startswith(
            "{" + POM_NAMESPACE + "}"
        ):
            key = subnode.tag[len(POM_NAMESPACE) + 2 :]
            yield key, subnode

def parse_pom_file(file_path, metadata_result: Result):
    """Function parsing a POM.xml file and extract metadata into SOMEF result format"""
    try:
        with open(file_path, 'rb') as file:
            data = lxml.etree.parse(file)
            
            root = data.getroot()
            if root.tag != "{" + POM_NAMESPACE + "}project":
                logging.warning(f"Expected root tag 'project' in {POM_NAMESPACE} namespace, got {root.tag} instead")
                return metadata_result
            
            project_data = {
                "group_id": None,
                "artifact_id": None,
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
                    project_data["group_id"] = node.text
                elif key == "artifactId":
                    project_data["artifact_id"] = node.text
                elif key == "version":
                    project_data["version"] = node.text
                elif key == "name":
                    project_data["name"] = node.text
                elif key == "description":
                    project_data["description"] = node.text
                elif key == "url":
                    project_data["url"] = node.text
                elif key == "licenses":
                    project_data["licenses"] = parse_licenses(node)
                elif key == "issueManagement":
                    project_data["issue_tracker"] = parse_issue_management(node)
                elif key == "scm":
                    project_data["scm_url"] = parse_scm(node)        
                elif key == "developers":
                    project_data["developers"] = parse_developers(node)              
                elif key == "dependencies":
                    project_data["dependencies"] = parse_dependencies(node)
            
            metadata = {}
            for k, v in project_data.items():
                if v: 
                    metadata[k] = v

            metadata_result.add_result(
                constants.CAT_PACKAGE_FILE,
                {
                    "value": file_path,
                    "type": "pom.xml",
                    "metadata": metadata
                },
                1,
                constants.TECHNIQUE_CODE_CONFIG_PARSER,
                file_path
            )
            
            if project_data["group_id"] and project_data["artifact_id"]:
                identifier = f"{project_data['group_id']}.{project_data['artifact_id']}"
                metadata_result.add_result(
                    constants.CAT_IDENTIFIER,
                    {
                        constants.PROP_VALUE: identifier,
                        constants.PROP_TYPE: constants.STRING
                    },
                    1,
                    constants.TECHNIQUE_CODE_CONFIG_PARSER,
                    file_path
                )
            
            return metadata_result
    
    except Exception as e:
        logging.error(f"Error parsing POM file {file_path}: {str(e)}")
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
            for key2, node2 in parse_node(node):
                if key2 in ["name", "email", "organization", "url"] and node2.text:
                    dev_data[key2] = node2.text
            if dev_data:
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