import os
from pathlib import Path
import nbformat
from chardet import detect
import re
from .extract_workflows import is_file_workflow
from .process_results import Result
from .utils import constants
from .extract_ontologies import is_file_ontology




def check_repository_type(path_repo,title,metadata_result:Result):
    """ Function that adds the metadata result in the JSON 
        output depending on the software type or if the repository is not considered software"""
    if check_extras(path_repo):
        metadata_result.add_result(constants.CAT_TYPE,
                                    {
                                        constants.PROP_VALUE: 'non-software',
                                        constants.PROP_TYPE: constants.STRING,

                                    },
                                    1,
                                    constants.TECHNIQUE_HEURISTICS)
    elif check_static_websites(path_repo):
        metadata_result.add_result(constants.CAT_TYPE,
                                    {
                                        constants.PROP_VALUE: 'static-website',
                                        constants.PROP_TYPE: constants.STRING,
                                        
                                    },
                                    1,
                                    constants.TECHNIQUE_HEURISTICS)
    elif check_ontologies(path_repo,title):
        metadata_result.add_result(constants.CAT_TYPE,
                                    {
                                        constants.PROP_VALUE: 'ontology',
                                        constants.PROP_TYPE: constants.STRING,
                                        
                                    },
                                    1,
                                    constants.TECHNIQUE_HEURISTICS)
    elif check_notebooks(path_repo):
        metadata_result.add_result(constants.CAT_TYPE,
                                    {
                                        constants.PROP_VALUE: 'notebook-application',
                                        constants.PROP_TYPE: constants.STRING,
                                        
                                    },
                                    1,
                                    constants.TECHNIQUE_HEURISTICS)
    elif check_workflow(path_repo):
        metadata_result.add_result(constants.CAT_TYPE,
                                    {
                                        constants.PROP_VALUE: 'workflow',
                                        constants.PROP_TYPE: constants.STRING,
                                        
                                    },
                                    1,
                                    constants.TECHNIQUE_HEURISTICS)
    elif check_command_line(path_repo):
        metadata_result.add_result(constants.CAT_TYPE,
                                    {
                                        constants.PROP_VALUE: 'commandline-application',
                                        constants.PROP_TYPE: constants.STRING,
                                        
                                    },
                                    0.82,
                                    constants.TECHNIQUE_HEURISTICS)
    else:
        metadata_result.add_result(constants.CAT_TYPE,
                                    {
                                        constants.PROP_VALUE: 'uncategorized',
                                        constants.PROP_TYPE: constants.STRING,
                                        
                                    },
                                    1,
                                    constants.TECHNIQUE_HEURISTICS)
    return metadata_result


def check_notebooks(path_repo):
    """Function which checks if the specified repository is a Notebook Application
       depending on the extensions present and number of notebooks which contain code

       @useful_percentage_notebooks: this variable denotes the percentage of notebook files
       that can be considered useful in terms of running a program. The threshold is set above 30% in order 
       to omit repositories which are used more for explanatory reasons instead of actual running of code ."""
    total_notebooks = 0
    code_notebooks = 0
    total_files=0

    bad_extensions=False
    for root, dirs, files in os.walk(path_repo):
        for file in files:
            if file.endswith(constants.media_files):
                continue
            total_files+=1

            if file.endswith((".ipynb", ".rmd",'.Rmd',".jl")):
                notebook_path = os.path.join(root, file)
                try:
                    if file.endswith(".ipynb"):
                        if is_notebook_code(notebook_path):
                            code_notebooks+=1
                    elif file.endswith(".rmd") or file.endswith('.Rmd'):
                        if has_code_in_rmd(notebook_path):
                            code_notebooks += 1
                    elif file.endswith('.jl'):
                        code_notebooks +=1

                    total_notebooks += 1
                except Exception as e:
                    print(f"Error reading notebook file {notebook_path}: {str(e)}")
                    pass
            if file.endswith(constants.code_extensions):
                bad_extensions=True
    if code_notebooks>0:
        useful_percentage_notebooks=code_notebooks/total_notebooks
    else:
        useful_percentage_notebooks=0
    if useful_percentage_notebooks>=0.3 and bad_extensions==False:
        return True
    else:
        return False


def check_ontologies(path_repo):
    """Function which detects if repository is an Ontology based on files present
       and the non-existence of code files"""
    ontology=False
    for root, dirs, files in os.walk(path_repo):
        repo_relative_path = os.path.relpath(root, path_repo)
        for file in files:
            file_path = os.path.join(repo_relative_path, file)
            print(os.path.join(repo_relative_path,file_path))
            if file.endswith(constants.code_extensions):
                return False
            elif file.endswith(constants.ontology_extensions):
                if ontology==False:
                    ontology=is_file_ontology(os.path.join(path_repo,file_path))
    return ontology

def check_command_line(path_repo):
    """Function which detects if repository is a Commandline Application
       based on README analysis of commandline arguments and implementations"""
    pattern_commandline= r"(?i)command[-\s]?line"
    pattern_cmd_arg = r"(?i)(explanation\s+of\s+)?arguments\b"
    pattern_cmd_arg2 = r"(?i)-\w+:"
    for dir_path, dir_names, filenames in os.walk(path_repo):
        repo_relative_path = os.path.relpath(dir_path, path_repo)
        for filename in filenames:
            file_path = os.path.join(repo_relative_path, filename)
            filename_no_ext = os.path.splitext(filename)[0]
            if "README" == filename_no_ext.upper():
                if repo_relative_path == ".":
                    
                        print(os.path.join(dir_path, filename))
                        with open(os.path.join(dir_path, filename), "r") as data_file:
                            data_file_text = data_file.read()
                            try:
                                cmd_match2=re.search(pattern_commandline,data_file_text)
                                cmd_match3=re.search(pattern_cmd_arg,data_file_text)
                                cmd_match4=re.search(pattern_cmd_arg2,data_file_text)
                                if cmd_match2 or (cmd_match3 and cmd_match4):
                                    return True
                            except:
                                return False
                    

    return False   



def check_extras(path_repo):
    """Function which detects if a repository is non-software by checking against
       software related files"""
    for root, dirs, files in os.walk(path_repo):
        for file in files:
            if file.endswith(constants.code_extensions) or file.endswith(constants.ontology_extensions):
                return False
    return True


def check_static_websites(path_repo):
    """Function that analyzes byte size of js,css,html languages and checks if 
       repository contains files not associated with static websites
    """
    nr_files=0
    web_files=0
    for root, dirs, files in os.walk(path_repo):
        for file in files:
            if file.endswith(constants.media_files):
                continue
            if file.endswith(constants.code_extensions) or file.endswith(constants.ontology_extensions):
                return False
            elif file.endswith((".js",".css",".html",".scss")):
                web_files+=1
            nr_files+=1
    if web_files>0:
        percentage=web_files/nr_files
    else:
        percentage=0
    if percentage>=0.8:
        return True
    else:
        return False


def check_workflow(repo_path,title):
    """Function which checks inside text for presence of repository being a workflow and analysis of the 
       files inside to check if they are correct workflow files. Also checks for repositories with no information
       the name of the files which might point to it being a workflow.
     """
    list=[]
    total_workflows=0
    good_workflows=0
    extensions=('.ga','.cwl','.nf','.knwf','.t2flow','.dag','.kar','.wdl',".smk",".snake")
    for root, dirs, files in os.walk(repo_path):
        repo_relative_path = os.path.relpath(root, repo_path)
        for file in files:
            file_path = os.path.join(repo_relative_path, file)
            filename_no_ext = os.path.splitext(file)[0]
            if "README" == filename_no_ext.upper():
                if repo_relative_path == ".":
                    try:
                        
                        with open(os.path.join(root, file), "r") as readme_file:
                            readme_contents = readme_file.read()
                            
                            title_words = title.split()

                            pattern = r'([^.?!]*(?:\b|\W){}(?:\b|\W)[^.?!]*[.?!])'.format('|'.join(map(re.escape, title_words)))
                            sentences = re.findall(pattern, readme_contents, flags=re.IGNORECASE)
                            for sentence in sentences:
                                if re.search(rf'\b{title}\b', sentence, flags=re.IGNORECASE) and re.search(r'\b(pipeline|workflow)\b', sentence, flags=re.IGNORECASE):
                                    return True

                            pattern_md=r'##.*\b(workflow|pipeline)\b'
                            pattern_rst=r'^([^=\n]+(?:\n(?![-=]).*)*\b(workflow|pipeline)\b(?:\n(?![-=]).*)*)\n=+'
                            
                            match_md=re.findall(pattern_md,readme_contents,re.IGNORECASE)
                            match_rst=re.findall(pattern_rst,readme_contents, re.MULTILINE | re.IGNORECASE)
                            
                            if match_md or match_rst:
                                return True

                    except:
                        continue

            if file.endswith(extensions) or file =="Snakefile":
                total_workflows+=1
                file_path = os.path.join(root, file)
                if is_file_workflow(file_path):
                    list.append(file_path)
                    good_workflows+=1
                else:
                    continue
            if check_name(file)==True:
                return True
    if list!=[] and good_workflows!=0:
        return True
    else:
        return False

def check_name(filename):
    """Assisting function for check_workflow to look for specific named files"""
    pattern1 = re.compile(r"pipeline", re.IGNORECASE)
    pattern2=re.compile(r"(model|example)",re.IGNORECASE)
    programming_language_extensions = (".py", ".java", ".cpp", ".c", ".php", ".rb", ".js", ".html", ".css", ".go", ".swift", ".scala", ".pl",".ipynb")
    if pattern1.search(filename) and pattern2.search(filename):
        if filename.endswith(programming_language_extensions):
            return True
    elif pattern1.search(filename) and not pattern2.search(filename):
        return False
    elif (not pattern1.search(filename) and not pattern2.search(filename)) or (not pattern1.search(filename) and pattern2.search(filename)):
        return False

def is_notebook_code(file_path):
    has_code = False
    num_code_cells = 0
    num_total_cells = 0
    nb = nbformat.read(file_path, as_version=4)
    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            num_total_cells += 1
            if cell['source'].strip():
                num_code_cells += 1
                has_code = True
    if has_code and num_code_cells / num_total_cells >= 0.55:
        return True
    else:
        return False

def has_code_in_rmd(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        if "```{r" in content or "```{python" in content or "```{bash" in content:
            return True
    return False