import unittest
import os
from pathlib import Path

from ..parser_somef import extract_headers, extract_headers_with_tags, extract_content_per_header, \
    extract_bash, extract_blocks_excerpts, extract_text_excerpts_header, extract_headers_parents, is_header

# Test data for tests
test_data_path = str(Path(__file__).parent / "test_data") + os.path.sep


class TestParserSomef(unittest.TestCase):

    def test_extract_header_content(self):
        """Test to check if the markdown parser works against hash headers"""
        with open(test_data_path + "README-widoco.md", "r") as data_file:
            text = data_file.read()
            headers = extract_headers(text)
            assert len(headers) == 15

    def test_extract_header_content_hash(self):
        """Test to check if the markdown parser works against hash headers"""
        with open(test_data_path + "README-widoco.md", "r") as data_file:
            text = data_file.read()
            headers = extract_headers_with_tags(text)
            assert len(headers) == 15

    def test_extract_content_per_header(self):
        """Test to check if the markdown parser gets the content of headers"""
        with open(test_data_path + "README-widoco.md", "r") as data_file:
            text = data_file.read()
            headers = extract_headers(text)
            content, non_header_content  = extract_content_per_header(text, headers)
            assert len(content) == 14

    def test_extract_bash(self):
        """Test to check if the markdown extracts bash code"""
        with open(test_data_path + "README-widoco.md", "r") as data_file:
            text = data_file.read()
            text, content = extract_bash(text)
            assert len(content.keys()) == 6

    def test_extract_blocks_excerpts(self):
        """Test to check if the markdown parser detects the right text blocks"""
        with open(test_data_path + "README-widoco.md", "r") as data_file:
            text = data_file.read()
            headers = extract_headers(text)
            content, non_header_content  = extract_content_per_header(text, headers)
            excerpts = extract_blocks_excerpts(content)
            assert len(excerpts) == 48

    def test_extract_text_excerpts_header(self):
        """Test to check if the markdown parser detects the correct headers"""
        with open(test_data_path + "README-widoco.md", "r") as data_file:
            text = data_file.read()
            excerpts = extract_text_excerpts_header(text)
            assert len(excerpts.index) == 48

    def test_extract_headers_parents(self):
        """Test to check if the markdown parser detects header partents correctly"""
        with open(test_data_path + "README-widoco.md", "r") as data_file:
            text = data_file.read()
            parents = extract_headers_parents(text)
            assert len(parents) == 15

    def test_issue_431(self):
        # Changed method is_header to avoid false positive
        # It will return true only when there is an opening and closing header tag in string input
        first_header = '''<h1 align="center">\n
        '''
        second_header = '''<h1>WIzard for DOCumenting Ontologies (WIDOCO)</h1>'''
        print(is_header(first_header))
        print(is_header(second_header))
        assert (not is_header(first_header) and is_header(second_header))