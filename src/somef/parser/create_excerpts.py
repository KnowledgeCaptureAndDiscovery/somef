from io import StringIO

import logging
from markdown import Markdown
from ..utils import markdown_utils
from . import mardown_parser
from .. import regular_expressions



# code snippet from https://stackoverflow.com/a/54923798
def unmark_element(element, stream=None):
    """Markdown to plain text conversion:"""
    if stream is None:
        stream = StringIO()
    if element.text:
        stream.write(element.text)
    for sub in element:
        unmark_element(sub, stream)
    if element.tail:
        stream.write(element.tail)
    return stream.getvalue()


# patching Markdown
Markdown.output_formats["plain"] = unmark_element
__md = Markdown(output_format="plain")
__md.stripTopLevelTags = False


def split_into_excerpts(string_list):
    """
    ## Function takes readme text as input and divides it into excerpts
    Parameters
    ----------
    string_list: input text

    Returns
    -------
    Returns the extracted excerpts
    """
    divisions = []
    for text in string_list:
        if text:
            divisions = divisions + markdown_utils.unmark(text).splitlines()
    divisions = [i for i in divisions if i]
    return divisions


def create_excerpts(string_list):
    """
    Function takes readme text as input and divides it into excerpts
    Parameters
    ----------
    string_list: Markdown text passed as input
    Returns
    -------
    Extracted excerpts
    """
    logging.info("Splitting text into valid excerpts for classification")
    string_list = markdown_utils.remove_bibtex(string_list)
    divisions = mardown_parser.extract_blocks_excerpts(string_list)
    logging.info("Text Successfully split.")
    output = {}
    for division in divisions:
        original = division
        division = regular_expressions.remove_links_images(division)
        if len(division) > 0:
            output[division] = original
    return output
