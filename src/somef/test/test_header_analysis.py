from somef.header_analysis import extract_header_content,extract_categories_using_headers


def test_extract_header_content_hash():
    text = """
# First level header
Content first header
# Empty header (should not be counted, as there is no content)
## Second level header
Content second header
### Third level header
Content third header
#### Fourth level header
Content fourth header
##### Fifth level header
Content fifth header
###### Sixth level header
Content sixth header
"""
    result = extract_header_content(text)
    print(result)
    assert len(result.index) == 6

def test_extract_header_content_hash_complex():
    text = """
First level header
==================
Content first header
## Second level header ##
Content second header
### Third level header ###
Content third header
"""
    result = extract_header_content(text)
    print(result)
    #Should return 2: we select the maximum amount of headers we can match
    assert len(result.index) == 2

# Example: Taguette
def test_extract_header_content_underline():
    text = """
Heading level 1
===============
This is a first level header

Empty level header
=================

Heading level 2
---------------
Content for heading 2

Empty Heading level 2
---------------------

Heading level 1 with incomplete sub
===
Content from incomplete

    """
    result = extract_header_content(text)
    print(result)
    assert len(result.index) == 3


def test_extract_categories_using_headers():
    with open("widoco_readme.md", "r") as data_file:
        file_text = data_file.read()
        json, results = extract_categories_using_headers(file_text)
        # At least 5 categories are extracted from the header analysis
        assert len(json) == 5

