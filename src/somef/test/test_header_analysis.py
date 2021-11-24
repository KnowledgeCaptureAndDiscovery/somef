import unittest

from somef.header_analysis import extract_header_content,extract_categories_using_headers,extract_bash_code

class TestAlmostEqual(unittest.TestCase):

    def test_extract_header_content_hash(self):
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

    def test_extract_header_content_hash_complex(self):
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
    def test_extract_header_content_underline(self):
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


    def test_extract_categories_using_headers(self):
        with open("widoco_readme.md", "r") as data_file:
            file_text = data_file.read()
            json, results = extract_categories_using_headers(file_text)
            # At least 5 categories are extracted from the header analysis
            assert len(json) == 5


    def test_extract_bash_code(self):
        text = """Another solution is to run Node directly with the `--max-old-space-size` option. The following example (Mac or Linux) allocates 16GB of memory:
```bash
$ node  --max-old-space-size=16000 `which mapshaper` <mapshaper commands>
```

## Installation

Mapshaper requires [Node.js](http://nodejs.org).

With Node installed, you can install the latest release version of mapshaper using npm. Install with the "-g" flag to make the executable scripts available systemwide.

```bash
npm install -g mapshaper
```

To install and run the latest development code from github:

```bash
git clone git@github.com:mbloch/mapshaper.git
cd mapshaper
npm install       # install dependencies
npm run build     # bundle source code files
npm link          # (optional) add global symlinks so scripts are available systemwide
```

## Building and testing

From the project directory, run `npm run build` to build both the cli and web UI modules.

Run `npm test` to run mapshaper's tests.

## License

This software is licensed under [MPL 2.0](http://www.mozilla.org/MPL/2.0/).

According to Mozilla's [FAQ](http://www.mozilla.org/MPL/2.0/FAQ.html), "The MPL's â€˜file-levelâ€™ copyleft is designed to encourage contributors to share modifications they make to your code, while still allowing them to combine your code with code under other licenses (open or proprietary) with minimal restrictions."" \
"""
        output = extract_bash_code(text)
        assert len(output) == 3

    def test_issue_232(self):
        with open("pyansys-README.rst", "r") as data_file:
            file_text = data_file.read()
            results = extract_header_content(file_text)
            print(results)
            assert len(results) == 8
        with open("rasterio-README.md", "r") as data_file:
            file_text = data_file.read()
            results = extract_header_content(file_text)
            print(results)
            assert len(results) == 17