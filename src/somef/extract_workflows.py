import re
Galaxy_pattern = r"(?i)a[_\s-]?galaxy[_\s-]?workflow"
CWL_pattern = r"\bclass:\s*[Ww]orkflow\b"
Workflow_content_pattern = r"in:\s*[^}]*\s*out:\s*(?:\[.*?\]|.*?(?=\n\s*\S+:|$))"
Nextflow_pattern= r"(?i)nextflow[\s\S]*?(workflow\s*\{[\s\S]*?\})"

def is_file_workflow(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        try:
            Galaxy_match=re.search(Galaxy_pattern,content)
            CWL_match=re.search(CWL_pattern,content)
            Workflow_match=re.search(Workflow_content_pattern,content)
            Nextflow_match=re.search(Nextflow_pattern,content)
            if Galaxy_match or CWL_match or Workflow_match or Nextflow_match:
                return True
            else:
                return False
        except Exception:
            pass