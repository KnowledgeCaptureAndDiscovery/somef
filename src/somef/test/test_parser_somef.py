import unittest

from somef.parser_somef import extract_headers, extract_headers_with_tags, extract_content_per_header, \
    extract_bash, extract_blocks_excerpts, extract_text_excerpts_header, extract_headers_parents

# Test data for tests
test_data_path = "test_data/"


class TestParserSomef(unittest.TestCase):

    def test_extract_header_content(self):
        with open(test_data_path + "README-widoco.md", "r") as data_file:
            text = data_file.read()
            headers = extract_headers(text)
            assert len(headers) == 15

    def test_extract_header_content_hash(self):
        with open(test_data_path + "README-widoco.md", "r") as data_file:
            text = data_file.read()
            headers = extract_headers_with_tags(text)
            assert len(headers) == 15

    def test_extract_content_per_header(self):
        with open(test_data_path + "README-widoco.md", "r") as data_file:
            text = data_file.read()
            headers = extract_headers(text)
            content = extract_content_per_header(text, headers)
            assert len(content) == 14

    def test_extract_bash(self):
        with open(test_data_path + "README-widoco.md", "r") as data_file:
            text = data_file.read()
            text, content = extract_bash(text)
            assert len(content.keys()) == 6

    def test_extract_blocks_excerpts(self):
        with open(test_data_path + "README-widoco.md", "r") as data_file:
            text = data_file.read()
            headers = extract_headers(text)
            content = extract_content_per_header(text, headers)
            excerpts = extract_blocks_excerpts(content)
            assert len(excerpts) == 48

    def test_extract_text_excerpts_header(self):
        with open(test_data_path + "README-widoco.md", "r") as data_file:
            text = data_file.read()
            excerpts = extract_text_excerpts_header(text)
            assert len(excerpts.index) == 48

    def test_extract_headers_parents(self):
        with open(test_data_path + "README-widoco.md", "r") as data_file:
            text = data_file.read()
            parents = extract_headers_parents(text)
            assert len(parents) == 15
