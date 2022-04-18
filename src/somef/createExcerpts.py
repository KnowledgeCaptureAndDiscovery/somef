from io import StringIO

from markdown import Markdown


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


def unmark(text):
    return __md.convert(text)


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
            divisions = divisions + unmark(text).splitlines()
    divisions = [i for i in divisions if i]
    return divisions
