from somef.header_analysis import extract_header_content

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


#Example: Taguette
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
