import unittest
import os
from pathlib import Path

from ..header_analysis import extract_header_content, extract_categories_using_headers, extract_bash_code

# Test data for tests
test_data_path = str(Path(__file__).parent / "test_data") + os.path.sep


class TestHeaderAnalysis(unittest.TestCase):

    def test_extract_header_content_hash(self):
        """Test to check if the markdown parser works against hash headers"""
        with open(test_data_path + "test_extract_header_content_hash.txt", "r") as data_file:
            text = data_file.read()
            result = extract_header_content(text)
            # print(result)
            assert len(result.index) == 6

    def test_extract_header_content_hash_complex(self):
        """Test to check if the markdown parser works in a more complex setting"""
        with open(test_data_path + "test_extract_header_content_hash_complex.txt", "r") as data_file:
            text = data_file.read()
            result = extract_header_content(text)
            print(result)
            # Should return 2: we select the maximum amount of headers we can match
            assert len(result.index) == 3

    def test_extract_header_content_underline(self):
        """Parser checks in case header are underlined (e.g., '___')"""
        with open(test_data_path + "test_extract_header_content_underline.txt", "r") as data_file:
            text = data_file.read()
            result = extract_header_content(text)
            print(result)
            assert len(result.index) == 3

    def test_extract_categories_using_headers(self):
        """More markdown checks to see if all categories are recognized."""
        with open(test_data_path + "widoco_readme.md", "r") as data_file:
            file_text = data_file.read()
            json, results = extract_categories_using_headers(file_text)
            # At least 5 categories are extracted from the header analysis
            assert len(json) == 5

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
            results = extract_header_content(file_text)
            print(results)
            assert len(results) == 8
        with open(test_data_path + "rasterio-README.md", "r") as data_file:
            file_text = data_file.read()
            results = extract_header_content(file_text)
            print(results)
            assert len(results) == 16

    def test_issue_237(self):
        """Test to check excerpt division and classification"""
        with open(test_data_path + "README-manim.md", "r") as data_file:
            file_text = data_file.read()
            json, results = extract_categories_using_headers(file_text)
            element = results[0]
            split = element.split("\n")
            assert len(split) > 1
            print(split)

    def test_issue_313(self):
        """Test to see if the original title of a section is returned"""
        with open(test_data_path + "README-manim.md", "r") as data_file:
            file_text = data_file.read()
            json, results = extract_categories_using_headers(file_text)
            element = json.get('documentation')
            elem = element[0]
            title = elem.get('originalHeader')
            assert title == 'Documentation'
