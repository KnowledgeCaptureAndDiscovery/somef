import unittest

from somef.header_analysis import extract_header_content, extract_categories_using_headers, extract_bash_code

# Test data for tests
test_data_path = "test_data/"


class TestHeaderAnalysis(unittest.TestCase):

    def test_extract_header_content_hash(self):
        with open(test_data_path + "test_extract_header_content_hash.txt", "r") as data_file:
            text = data_file.read()
            result = extract_header_content(text)
            # print(result)
            assert len(result.index) == 6

    def test_extract_header_content_hash_complex(self):
        with open(test_data_path + "test_extract_header_content_hash_complex.txt", "r") as data_file:
            text = data_file.read()
            result = extract_header_content(text)
            print(result)
            # Should return 2: we select the maximum amount of headers we can match
            assert len(result.index) == 3

    def test_extract_header_content_underline(self):
        with open(test_data_path + "test_extract_header_content_underline.txt", "r") as data_file:
            text = data_file.read()
            result = extract_header_content(text)
            print(result)
            assert len(result.index) == 3

    def test_extract_categories_using_headers(self):
        with open(test_data_path + "widoco_readme.md", "r") as data_file:
            file_text = data_file.read()
            json, results = extract_categories_using_headers(file_text)
            # At least 5 categories are extracted from the header analysis
            assert len(json) == 5

    def test_extract_bash_code(self):
        with open(test_data_path + "extract_bash_code.txt", "r") as data_file:
            text = data_file.read()
            output = extract_bash_code(text)
            assert len(output) == 3

    def test_issue_232(self):
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
        with open(test_data_path + "README-manim.md", "r") as data_file:
            file_text = data_file.read()
            json, results = extract_categories_using_headers(file_text)
            element = results[0]
            split = element.split("\n")
            assert len(split) > 1
            print(split)

    def test_issue_313(self):
        with open(test_data_path + "README-manim.md", "r") as data_file:
            file_text = data_file.read()
            json, results = extract_categories_using_headers(file_text)
            element = json.get('documentation')
            elem = element[0]
            title = elem.get('originalHeader')
            assert title == 'Documentation'
