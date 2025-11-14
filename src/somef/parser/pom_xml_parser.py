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
            "scm_url": None,
            "homepage": [],
            "runtime_platform": []
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
            # elif key == "dependencies" or key == "dependencyManagement":
            #     project_data["dependencies"] = parse_dependencies(node)
            elif key == "dependencies":
                project_data["dependencies"].extend(parse_dependencies(node))
            elif key == "dependencyManagement":
                for k, n in parse_node(node):
                    if k == "dependencies":
                        project_data["dependencies"].extend(parse_dependencies(n))
            elif key == "properties":
                project_data["runtime_platform"] = parse_runtime_platform(node)

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
     
        if project_data["homepage"]:
            metadata_result.add_result(
                constants.CAT_HOMEPAGE,
                {
                    "value": project_data["homepage"], 
                    "type": constants.URL},
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
 
        if project_data["dependencies"]:
            for dependency in project_data["dependencies"]:
                metadata_result.add_result(
                    constants.CAT_REQUIREMENTS,
                    {
                        "value": f'{dependency.get("groupId", "")}.{dependency.get("artifactId", "")}'.strip("."),
                        "name": dependency.get("artifactId", ""),
                        "version": dependency.get("version", ""),
                        "type": constants.SOFTWARE_APPLICATION
                    },
                    1,
                    constants.TECHNIQUE_CODE_CONFIG_PARSER,
                    source
                )
        

        if project_data["developers"]:
            for author in project_data["developers"]:
  
                if "type" not in author:
                    author["type"] = constants.AGENT
                    
                metadata_result.add_result(
                    constants.CAT_AUTHORS,
                    author,
                    1,
                    constants.TECHNIQUE_CODE_CONFIG_PARSER,
                    source
                )

        if repositories:

            for rep in repositories:
                rep["type"] = constants.URL

                metadata_result.add_result(
                    constants.CAT_PACKAGE_DISTRIBUTION,
                    rep,
                    1,
                    constants.TECHNIQUE_CODE_CONFIG_PARSER,
                    source
                )

                #     constants.CAT_PACKAGE_DISTRIBUTION,
                #     {
                #         # "value": repositories,
                #         rep,
                #         "type": constants.URL
                #     },
                #     1,
                #     constants.TECHNIQUE_CODE_CONFIG_PARSER,
                #     source
                # )
          
        if project_data["runtime_platform"]:
  
            for runtime in project_data["runtime_platform"]:
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

def parse_dependencies(node):
    dependencies = []

    for child in node:
        if not isinstance(child.tag, str):
            continue

        tag = child.tag.split("}")[-1] 
        if tag == "dependencies":
            dependencies.extend(parse_dependencies(child))
        elif tag == "dependency":
            dep_data = {}
            for sub in child:
                if not isinstance(sub.tag, str):
                    continue 
                sub_tag = sub.tag.split("}")[-1]
                if sub_tag in ["groupId", "artifactId", "version"] and sub.text:
                    dep_data[sub_tag] = sub.text.strip()
            if dep_data:
                dependencies.append(dep_data)

    return dependencies

def parse_developers(developers_node):
    developers = []
    for key, node in parse_node(developers_node):
        if key == "developer":
            dev_data = {}
            author_data = {
                # "name": None,
                # "email": None,
                # "url": None,
                # "affiliation": None,
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
                    author_data["affiliation"] = node2.text

            if "value" not in author_data:
                author_data["value"] = author_data["email"] or author_data["affiliation"]
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
                    if key2 == "id":
                        repo_data["value"] = node2.text
                    else:
                        repo_data[key2] = node2.text
            if repo_data:
                repos.append(repo_data)
    return repos

def parse_runtime_platform(properties_node):
    """
    Extracts runtime platform information from a <properties> node in a pom.xml.
    Returns a list of dictionaries with runtime names and versions, or an empty list if none are found.

    Parameters
    ----------
    properties_node : lxml.etree.Element
        The <properties> node from the POM file.

    Returns
    -------
    list of dict
        Each dict has the keys 'name' and 'version', e.g. [{'name': 'Java', 'version': '1.8'}, {'name': 'Python', 'version': '3.11'}].
        Returns an empty list if no runtime information is present.
    """
    runtimes = []

    if properties_node is None:
        return runtimes

    for child in properties_node:
        if not isinstance(child.tag, str):
            continue
        tag = child.tag.split("}")[-1].lower()
        text = (child.text or "").strip()

        if not text:
            continue
        # if tag.startswith(f"{{{POM_NAMESPACE}}}") and tag.endswith(".version") and child.text:
        #     print('entramos')
        #     runtime_name = tag.split("}")[-1].split(".")[0].capitalize()
        #     version_value = child.text.strip()
        #     runtimes.append({"value": f'{runtime_name} {version_value}',"name": runtime_name, "version": version_value})
        if any(x in tag for x in ["java.version", "javaversion", "java_version"]):
            runtimes.append({
                "name": "Java",
                "version": text,
                "value": f"Java: {text}"
            })
        elif any(x in tag for x in ["kotlin.version", "kotlinversion", "kotlin_version"]):
            runtimes.append({
                "name": "Kotlin",
                "version": text,
                "value": f"Kotlin: {text}"
            })
        elif any(x in tag for x in ["scala.version", "scalaversion", "scala_version"]):
            runtimes.append({
                "name": "Scala",
                "version": text,
                "value": f"Scala: {text}"
            })
    
    return runtimes