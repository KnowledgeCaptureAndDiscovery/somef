import logging
from io import StringIO
from markdown import Markdown
from ..utils import constants
import re


## Markdown to plain text conversion: begin ##
# code snippet from https://stackoverflow.com/a/54923798
def unmark_element(element, stream=None):
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


def unmark(text):
    return __md.convert(text)


def remove_bibtex(string_list):
    """
        Function that takes the string list and removes all bibtex blocks of it
        Parameters
        ----------
        string_list: A list of strings to process

        Returns
        -------
        The strings list without bibtex blocks
        """
    for x, element in enumerate(string_list):
        bib_references = re.findall(constants.REGEXP_BIBTEX, element)
        if len(bib_references) > 0:
            top = element.find(bib_references[0])
            init = element.rfind("```", 0, top)
            end = element.find("```", init + 3)
            substring = element[init:end + 3]
            string_list[x] = element.replace(substring, "")
    logging.info("Extraction of bibtex citation from readme completed. \n")
    return string_list


def remove_comments(html_text):
    """
    Function designed to remove HTML comments from a markdown file
    Parameters
    ----------
    html_text input HTML text

    Returns
    -------
    Markdown with no HTML comments
    """
    # comment_pattern = r'<!--(.*?)-->'
    comment_pattern = r'<!--[\s\S]*?--\s*>'

    html_without_comments = re.sub(comment_pattern, '', html_text, flags=re.DOTALL)
    return html_without_comments
