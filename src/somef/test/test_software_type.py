import unittest
import os
from pathlib import Path

from ..extract_software_type import check_ontologies,check_notebooks,check_command_line,check_extras,check_static_websites,check_workflow

test_data_repositories = str(Path(__file__).parent / "test_data"/ "repositories") + os.path.sep

class TestEXTRAS(unittest.TestCase):
    """The following tests are made to check the workings of the classification
        Each category has two tests with the format test_result-of-test_type 
        in orded to identify what each of them does.
        e.g: test_true_ontology runs the check_ontologies function on auroral-ontology-core which 
        is an ontology and returns true so the assert passes."""

    def test_true_ontology(self):
        path = test_data_repositories + "auroral-ontology-core"
        result = check_ontologies(path)
        assert result
     
    def test_false_ontology(self):
        path = test_data_repositories + "sprint-main"
        result = check_ontologies(path)
        assert (result is False)
    
    def test_true_notebooks(self):
        path=test_data_repositories + "basis_functions_approach_to_GP-master"
        result=check_notebooks(path)
        assert result
    
    def test_false_notebooks(self):
        path=test_data_repositories + "ipynb-master"
        result=check_notebooks(path)
        assert (result is False)
    
    def test_true_commandline(self):
        path=test_data_repositories + "Fermi"
        result=check_command_line(path)
        assert result
    
    def test_false_commandline(self):
        path=test_data_repositories + "Clamp"
        result=check_command_line(path)
        assert (result is False)

    def test_true_extra(self):
        path = test_data_repositories + "OWL-To-OAS-Specification-master"
        result = check_extras(path)
        assert result

    def test_false_extra(self):
        path = test_data_repositories + "ipynb-master"
        result = check_extras(path)
        assert result is False

    def test_true_workflows(self):
        path = test_data_repositories + "JAFFA-master"
        result = check_workflow(path,'JAFFA-master')
        assert result

    def test_false_workflows(self):
        path = test_data_repositories + "A-Dynamic-E-Commerce-Website-master"
        result = check_workflow(path,'DynamicPersonalWebsite-master')
        assert result is False
