import unittest
import os
from pathlib import Path

from ..extract_software_type import check_ontologies, check_notebooks, check_command_line, check_extras, \
    check_static_websites, check_workflow, check_package_files, check_repository_type
from ..process_results import Result
from ..utils import constants

test_data_repositories = str(Path(__file__).parent / "test_data" / "repositories") + os.path.sep


class TestEXTRAS(unittest.TestCase):
    """The following tests are made to check the workings of the classification
        Each category has two tests with the format test_result-of-test_type 
        in order to identify what each of them does.
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
        path = test_data_repositories + "basis_functions_approach_to_GP-master"
        result = check_notebooks(path)
        assert result

    def test_false_notebooks(self):
        path = test_data_repositories + "ipynb-master"
        result = check_notebooks(path)
        assert (result is False)

    def test_true_commandline(self):
        path = test_data_repositories + "Fermi"
        result = check_command_line(path)
        assert result

    def test_false_commandline(self):
        path = test_data_repositories + "Clamp"
        result = check_command_line(path)
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
        result = check_workflow(path, 'JAFFA-master')
        assert result

    def test_false_workflows(self):
        path = test_data_repositories + "A-Dynamic-E-Commerce-Website-master"
        result = check_workflow(path, 'DynamicPersonalWebsite-master')
        assert result is False

    def test_true_package_files(self):
        path = test_data_repositories + "fuji"
        result = check_package_files(path)
        assert result

    def test_false_package_files(self):
        path = test_data_repositories + "OWL-To-OAS-Specification-master"
        result = check_package_files(path)
        assert result is False

    def test_repository_type_software(self):
        path = test_data_repositories + "fuji"
        result = check_repository_type(path, "fuji", Result())
        values = [r[constants.PROP_RESULT][constants.PROP_VALUE] for r in result.results[constants.CAT_APPLICATION_TYPE]]
        assert "software" in values

    def test_repository_type_non_software(self):
        path = test_data_repositories + "OWL-To-OAS-Specification-master"
        result = check_repository_type(path, "OWL-To-OAS-Specification-master", Result())
        values = [r[constants.PROP_RESULT][constants.PROP_VALUE] for r in result.results[constants.CAT_APPLICATION_TYPE]]
        assert "non-software" in values

    def test_repository_type_ontology(self):
        path = test_data_repositories + "auroral-ontology-core"
        result = check_repository_type(path, "auroral-ontology-core", Result())
        values = [r[constants.PROP_RESULT][constants.PROP_VALUE] for r in result.results[constants.CAT_APPLICATION_TYPE]]
        assert "ontology" in values

    def test_true_static_website(self):
        path = test_data_repositories + "website-static-master"
        result = check_static_websites(path, Result())
        assert result

    def test_false_static_website(self):
        path = test_data_repositories + "rdflib-6.0.2"
        result = check_static_websites(path, Result())
        assert result is False

    def test_high_js_ratio_should_be_false(self):
        path = test_data_repositories + "website-static-master"
        repo_metadata = Result()
        repo_metadata.results = {
            constants.CAT_PROGRAMMING_LANGUAGES: [
                {constants.PROP_RESULT: {constants.PROP_NAME: "javascript", constants.PROP_SIZE: 95}},
                {constants.PROP_RESULT: {constants.PROP_NAME: "html", constants.PROP_SIZE: 5}},
            ]
        }
        result = check_static_websites(path, repo_metadata)
        assert result is False


    def test_low_js_ratio_should_be_true(self):
        path = test_data_repositories + "website-static-master"
        repo_metadata = Result()
        repo_metadata.results = {
            constants.CAT_PROGRAMMING_LANGUAGES: [
                {constants.PROP_RESULT: {constants.PROP_NAME: "javascript", constants.PROP_SIZE: 5}},
                {constants.PROP_RESULT: {constants.PROP_NAME: "html", constants.PROP_SIZE: 95}},
            ]
        }
        result = check_static_websites(path, repo_metadata)
        assert result is True