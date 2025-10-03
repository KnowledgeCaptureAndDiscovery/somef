import re
import logging

Galaxy_pattern = r"(?i)a[_\s-]?galaxy[_\s-]?workflow"
CWL_pattern = r"\bclass:\s*[Ww]orkflow\b"
Workflow_content_pattern = r"in:\s*[^}]*\s*out:\s*(?:\[.*?\]|.*?(?=\n\s*\S+:|$))"
workflow_pattern = r'\bworkflow\b'
Nextflow_pattern = r"(?i)nextflow[\s\S]*?(workflow\s*\{[\s\S]*?\})"
GitLab_ContinuosIntegration_pattern = r"(?i)stages:\s*\n\s*-\s*\w+"
GitLab_ContinuosIntegration_keywords = [r"script:", r"rules:", r"variables:", r"before_script:", r"after_script:", r"image:"]


def is_file_workflow(file_path):
    try:
        with open(file_path, "rb") as file:
            raw_data = file.read()

        try:
            content = raw_data.decode("utf-8")
        except UnicodeDecodeError:
            logging.warning(f"File {file_path} is not UTF-8 decodable. Skipping.")
            return False

        Galaxy_match = re.search(Galaxy_pattern, content)
        CWL_match = re.search(CWL_pattern, content)
        Workflow_match = re.search(Workflow_content_pattern, content)
        Workflow_match_2 = re.search(workflow_pattern, content, re.IGNORECASE)
        Nextflow_match = re.search(Nextflow_pattern, content)

        if Galaxy_match or CWL_match or Workflow_match or Workflow_match_2 or Nextflow_match:
            return True
        else:
            return False

    except Exception as e:
        logging.warning(f"Error reading file {file_path}: {e}")
        return False
    
# def is_file_workflow(file_path):

#     print(file_path)
#     with open(file_path, 'r') as file:
#         print(file)
#         content = file.read()
#         try:
#             Galaxy_match = re.search(Galaxy_pattern, content)
#             CWL_match = re.search(CWL_pattern, content)
#             Workflow_match = re.search(Workflow_content_pattern, content)
#             Workflow_match_2 = re.search(workflow_pattern, content, re.IGNORECASE)
#             Nextflow_match = re.search(Nextflow_pattern, content)
#             if Galaxy_match or CWL_match or Workflow_match or Workflow_match_2 or Nextflow_match:
#                 return True
#             else:
#                 return False
#         except Exception:
#             pass

def is_file_continuous_integration_gitlab(file_path):
    """Detects if a file is a GitLab CI/CD pipeline."""
    with open(file_path, 'r') as file:
        content = file.read()
        try:
            # Check if the file contains 'stages:' followed by at least one stage
            if re.search(GitLab_ContinuosIntegration_pattern, content):
                return True
            
              # If 'stages:' is not found, check for other GitLab CI/CD keywords
            for keyword in GitLab_ContinuosIntegration_keywords:
                if re.search(keyword, content, re.IGNORECASE):
                    return True
            
            return False
        except Exception:
            return False