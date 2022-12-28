import json
import os
import unittest

from pathlib import Path

from ..header_analysis import extract_header_content, extract_categories_using_headers, extract_bash_code
from ..process_results import Result
from ..utils import constants

# Test data for tests
test_data_path = str(Path(__file__).parent / "test_data") + os.path.sep


class TestHeaderAnalysis(unittest.TestCase):

    def test_extract_header_content_hash(self):
        """Test to check if the Markdown parser works against hash headers"""
        with open(test_data_path + "test_extract_header_content_hash.txt", "r") as data_file:
            text = data_file.read()
            result, non_header_content = extract_header_content(text)
            print(result)
            assert len(result.index) == 6

    def test_extract_header_content_hash_complex(self):
        """Test to check if the markdown parser works in a more complex setting"""
        with open(test_data_path + "test_extract_header_content_hash_complex.txt", "r") as data_file:
            text = data_file.read()
            result, non_header_content  = extract_header_content(text)
            print(result)
            # Should return 2: we select the maximum amount of headers we can match
            assert len(result.index) == 3

    def test_extract_header_content_underline(self):
        """Parser checks in case header are underlined (e.g., '___')"""
        with open(test_data_path + "test_extract_header_content_underline.txt", "r") as data_file:
            text = data_file.read()
            result, non_header_content  = extract_header_content(text)
            print(result)
            assert len(result.index) == 3

    def test_extract_categories_using_headers(self):
        """More markdown checks to see if all categories are recognized."""
        with open(test_data_path + "widoco_readme.md", "r") as data_file:
            file_text = data_file.read()
            result, list = extract_categories_using_headers(file_text, Result())
            # At least 5 categories are extracted from the header analysis
            assert len(result.results) >= 5

    def test_extract_bash_code(self):
        """Test to check if bash code can be detected in readme files"""
        with open(test_data_path + "extract_bash_code.txt", "r") as data_file:
            text = data_file.read()
            output = extract_bash_code(text)
            assert len(output) == 3

    def test_issue_232(self):
        """Test to avoid a bug in header analysis, where no installation instructions were detected"""
        with open(test_data_path + "pyansys-README.rst", "r") as data_file:
            file_text = data_file.read()
            results, non_header_content  = extract_header_content(file_text)
            print(results)
            assert len(results) == 8
        with open(test_data_path + "rasterio-README.md", "r") as data_file:
            file_text = data_file.read()
            results, non_header_content  = extract_header_content(file_text)
            print(results)
            assert len(results) == 16

    def test_issue_237(self):
        """Test to check excerpt division and classification"""
        with open(test_data_path + "README-manim.md", "r") as data_file:
            file_text = data_file.read()
            json_results, results = extract_categories_using_headers(file_text, Result())
            element = results[0]
            split = element.split("\n")
            assert len(split) > 1
            print(split)

    def test_issue_313(self):
        """Test to see if the original title of a section is returned"""
        with open(test_data_path + "README-manim.md", "r") as data_file:
            file_text = data_file.read()
            json, results = extract_categories_using_headers(file_text, Result())
            element = json.results[constants.CAT_DOCUMENTATION]
            elem = element[0][constants.PROP_RESULT]
            title = elem.get(constants.PROP_ORIGINAL_HEADER)
            assert title == 'Documentation'

    def test_issue_425(self):
        """Checks that the confidence value of fields extracted using header extraction technique is 1.0"""
        with open(test_data_path + "README-mapshaper.md", "r") as data_file:
            file_text = data_file.read()
            json, results = extract_categories_using_headers(file_text, Result())
            print(json.results)
            element = json.results[constants.CAT_DESCRIPTION]
            confidence = element[0][constants.PROP_CONFIDENCE]
            assert confidence == 1

    def test_issue_465(self):
        """
        Test targeted towards creating the right excerpts when breaking a problematic file. Requirements should
        only return a single line.
        """
        with open(test_data_path + "test_465.md", "r") as data_file:
            file_text = data_file.read()
            json_test, results = extract_categories_using_headers(file_text, Result())
            #print(json_test.results[constants.CAT_REQUIREMENTS])
            reqs = json_test.results[constants.CAT_REQUIREMENTS][0][constants.PROP_RESULT][constants.PROP_VALUE]
            assert reqs.replace('\n', '') == "Python 2.7 and 3.4+"
