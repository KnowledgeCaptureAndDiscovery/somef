import logging
import os
import re
import markdown
import requests
import validators
from .utils import constants
from .process_results import Result
from urllib.parse import urlparse
import bibtexparser

def extract_title(unfiltered_text, repository_metadata: Result, readme_source) -> Result:
    """
    Regexp to extract title (first header) from a repository
    Parameters
    ----------
    @param unfiltered_text: repo text
    @param repository_metadata: Result with the extractions so far
    @param readme_source: url to the file used (for provenance)

    Returns
    -------
    @returns a Result including the title (if found)

    """
    html_text = markdown.markdown(unfiltered_text)
    splitted = html_text.split("\n")
    index = 0
    limit = len(splitted)
    output = ""
    regex = r'<[^<>]+>'
    while index < limit:
        line = splitted[index]
        if line.startswith("<h"):
            if line.startswith("<h1>"):
                output = re.sub(regex, '', line)
            break
        index += 1

    # If the output is empty or none, the category doesn't make sense and shouldn't be displayed in the final result
    if has_valid_output(output):
        repository_metadata.add_result(constants.CAT_FULL_TITLE,
                                   {
                                       constants.PROP_TYPE: constants.STRING,
                                       constants.PROP_VALUE: output
                                   }, 1, constants.TECHNIQUE_REGULAR_EXPRESSION, readme_source)

    return repository_metadata


def extract_title_old(unfiltered_text):
    """
    Function to extract a title based on the first header in the readme file
    Parameters
    ----------
    unfiltered_text unfiltered text of the title

    Returns
    -------
    Full title of the repo (if found)
    """
    underline_header = re.findall('.+[\n]={3,}[\n]', unfiltered_text)
    # header declared with ====
    title = ""
    if len(underline_header) != 0:
        title = re.split('.+[=]+[\n]+', unfiltered_text)[0].strip()
    else:
        # The first occurrence is assumed to be the title.
        title = re.findall(r'# .+', unfiltered_text)[0]
        # Remove initial #
        if title is not None and len(title) > 0:
            title = title[1:].strip()
    # Remove other markup (links, etc.)
    if "[!" in title:
        title = re.split('\[\!', title)[0].strip()
    return title


def extract_readthedocs(readme_text, repository_metadata: Result, readme_source) -> Result:
    """
    Function to extract readthedocs links from text
    Parameters
    ----------
    @param readme_text: raw text of the readme file
    @param repository_metadata: Result where to deposit the findings of the README
    @param readme_source: URL of the README file

    Returns
    -------
    @return Result including links to the readthedocs documentation
    """
    readthedocs_links = re.findall(constants.REGEXP_READTHEDOCS, readme_text)
    name = ""
    try:
        name = repository_metadata.results[constants.CAT_NAME][0]
        name = name[constants.PROP_RESULT][constants.PROP_VALUE]
    except:
        pass

    if has_valid_links(readthedocs_links):

        for link in list(dict.fromkeys(readthedocs_links)):

            if not has_valid_link(link):
                continue  

            result = {
                constants.PROP_TYPE: constants.URL,
                constants.PROP_VALUE: link,
                constants.PROP_FORMAT: constants.FORMAT_READTHEDOCS
            }
            try:
                # if name of the repo is known then compare against the readthedocs one. Only add it if it's similar/same
                name_in_link = re.findall('https://([^.]+)\.readthedocs\.io', link)
                name_in_link = name_in_link[0]
                if name == "" or name_in_link.lower() == name.lower():
                    repository_metadata.add_result(constants.CAT_DOCUMENTATION, result, 1,
                                                constants.TECHNIQUE_REGULAR_EXPRESSION, readme_source)
                else:
                    repository_metadata.add_result(constants.CAT_RELATED_DOCUMENTATION, result, 1,
                                                constants.TECHNIQUE_REGULAR_EXPRESSION, readme_source)
            except:
                # add link as a regular doc link if we cannot retrieve name or there is an error
                repository_metadata.add_result(constants.CAT_DOCUMENTATION, result, 1,
                                            constants.TECHNIQUE_REGULAR_EXPRESSION, readme_source)

    return repository_metadata


def extract_support_channels(readme_text, repository_metadata: Result, readme_source) -> Result:
    """
    Function to extract support channels links from text
    Parameters
    ----------
    @param readme_text: raw text of the readme file
    @param repository_metadata: Result where to deposit the findings of the README
    @param readme_source: URL of the README file

    Returns
    -------
    @return Result including links to the support channels (Gitter, reddit, discord)
    """
    results = []

    index_gitter_chat = readme_text.find(constants.REGEXP_GITTER)
    if index_gitter_chat > 0:
        init = readme_text.find(")](", index_gitter_chat)
        end = readme_text.find(")", init + 3)
        gitter_chat = readme_text[init + 3:end]
        results.append(gitter_chat)

    init = readme_text.find(constants.REGEXP_REDDIT)
    if init > 0:
        end = readme_text.find(")", init)
        repo_status = readme_text[init + 1:end]
        results.append(repo_status)

    init = readme_text.find(constants.REGEXP_DISCORD)
    if init > 0:
        end = readme_text.find(")", init)
        repo_status = readme_text[init + 1:end]
        results.append(repo_status)

    for link in results:
        repository_metadata.add_result(constants.CAT_SUPPORT_CHANNELS,
                                       {
                                           constants.PROP_TYPE: constants.URL,
                                           constants.PROP_VALUE: link,
                                       }, 1, constants.TECHNIQUE_REGULAR_EXPRESSION, readme_source)

    return repository_metadata


def extract_repo_status(unfiltered_text, repository_metadata: Result, readme_source) -> Result:
    """
    Function takes readme text as input and extracts the repostatus.org badge

    Parameters
    ----------
    @param unfiltered_text: Text of the readme
    @param repository_metadata: Result with all the processed results so far
    @param readme_source: source to the readme file used
    """

    repo_status = ""
    init = unfiltered_text.find("[![Project Status:")
    if init > 0:
        end = unfiltered_text.find("](", init)
        repo_status = unfiltered_text[init + 3:end]
        repo_status = repo_status.replace("Project Status: ", "")
        short_status = repo_status[0:repo_status.find(" ")].lower()
        repository_metadata.add_result(constants.CAT_STATUS,
                                       {
                                           constants.PROP_TYPE: constants.URL,
                                           constants.PROP_VALUE: "https://www.repostatus.org/#" + short_status,
                                           constants.PROP_DESCRIPTION: repo_status
                                       }, 1, constants.TECHNIQUE_REGULAR_EXPRESSION, readme_source)
    return repository_metadata


def extract_arxiv_links(unfiltered_text, repository_metadata: Result, readme_source) -> Result:
    """
    Regexp to extract arxiv url from a repository
    Parameters
    ----------
    @param unfiltered_text: repo text
    @param repository_metadata: Result with the extractions so far
    @param readme_source: url to the file used (for provenance)

    Returns
    -------
    @returns a Result including the arxiv url 
    """
    result_links = [m.start() for m in re.finditer('https://arxiv.org/', unfiltered_text)]
    result_refs = [m.start() for m in re.finditer('arXiv:', unfiltered_text)]
    results = []
    for position in result_links:
        end = unfiltered_text.find(')', position)
        if end < 0:
            end = unfiltered_text.find('}', position)
        link = unfiltered_text[position:end]
        results.append(link)
    for position in result_refs:
        end = unfiltered_text.find('}', position)
        link = unfiltered_text[position:end]
        results.append(link.replace('arXiv:', 'https://arxiv.org/abs/'))

    for link in set(results):
        repository_metadata.add_result(constants.CAT_RELATED_PAPERS,
                                       {
                                           constants.PROP_TYPE: constants.URL,
                                           constants.PROP_VALUE: link
                                       },
                                       1, constants.TECHNIQUE_REGULAR_EXPRESSION, readme_source
                                       )
    return repository_metadata


def extract_wiki_links(unfiltered_text, repo_url, repository_metadata: Result, readme_source) -> Result:
    """

    Parameters
    ----------
    @param unfiltered_text: text from readme
    @param repo_url: repository URL
    @param repository_metadata: results found in the repository so far
    @param readme_source: readme URL/path

    Returns
    -------
    @return a Result with the wiki documentation links found in the README
    """
    """Extracts wiki links from a given text"""
    links = re.findall(r"\[[^\]]*\]\((.*?)?\)", unfiltered_text)
    output = []
    ends = 0
    for link in links:
        if validators.url(link):
            if link.endswith("/wiki"):
                if link not in output:
                    output.append(link)
            else:
                ends = unfiltered_text.find("(" + link + ")") - 1
                if unfiltered_text[:ends].find("[") != -1:
                    position = unfiltered_text[:ends].rindex("[") + 1
                    if unfiltered_text[position:ends].find("wiki") >= 0:
                        if link not in output:
                            output.append(link)
            unfiltered_text = unfiltered_text[ends + len(link):]

    # to check if a wiki url is available in the repository
    if repo_url != "" and repo_url is not None and validators.url(repo_url):
        if repo_url.endswith("/"):
            repo_url = repo_url + "wiki"
        else:
            repo_url = repo_url + "/wiki"
        wiki = requests.get(repo_url, allow_redirects=False)
        if wiki.status_code == 200:
            page_content = wiki.text.strip()
            if page_content:
                if "Create the first page" in page_content and "wiki/_new" in page_content:
                    logging.info("Wiki 200 without content. NOT added to output")    
                else:
                    logging.info("Wiki 200 with content. Added to output")
                    # sometimes the repo starts with caps
                    links_in_list = [x.lower() for x in output]
                    if repo_url.lower() not in links_in_list:
                        output.append(repo_url)
            else:
                logging.info("Wiki 200 without content. NOT added to output") 

    for link in output:
        repository_metadata.add_result(constants.CAT_DOCUMENTATION,
                                       {
                                           constants.PROP_TYPE: constants.URL,
                                           constants.PROP_VALUE: link,
                                           constants.PROP_FORMAT: constants.FORMAT_WIKI
                                       },
                                       1, constants.TECHNIQUE_REGULAR_EXPRESSION, readme_source)
    return repository_metadata


def extract_images(unfiltered_text, repo_url, local_repo, repository_metadata: Result, readme_source,
                   def_branch) -> Result:
    """
    Function that takes readme text as input and extracts logos and images

    Parameters
    ----------
    @param unfiltered_text: Text of the readme
    @param repo_url: Repository URL
    @param local_repo: Local repo path
    @param repository_metadata: Result with all the processed results so far
    @param readme_source: source to the readme file used
    @param def_branch: default branch of the repo

    Returns
    -------
    A Result object with the logos and images from the given text
    """
    logo = ""
    images = []
    repo_name = ""
    if repo_url is not None and repo_url != "":
        url = urlparse(repo_url)
        path_components = url.path.split('/')
        repo_name = path_components[2]

    html_text = markdown.markdown(unfiltered_text)
    img_md = re.findall(constants.REGEXP_IMAGES, html_text)
    img_html = [_.start() for _ in re.finditer("<img ", html_text)]
    for img in img_md:
        img = img[1]  # the 0 position is the name used in the link
        # if the image contains jitpack.io, the element is not processed
        if img.find("jitpack.io") > 0 or img.find("/badge") >= 0 or img.find("/travis-ci.") >= 0 \
                or img.find("img.shields.io") >= 0:
            pass
        elif logo == "" and repo_url is not None:
            start = img.rindex("/")
            if img.find(repo_name, start) > 0:
                logo = rename_github_image(img, repo_url, local_repo, def_branch)
            elif get_alt_text_md(html_text, img) == repo_name or get_alt_text_md(html_text, img).upper() == "LOGO":
                logo = rename_github_image(img, repo_url, local_repo, def_branch)
            else:
                start = img.rindex("/")
                if img.upper().find("LOGO", start) > 0:
                    logo = rename_github_image(img, repo_url, local_repo, def_branch)
                else:
                    images.append(rename_github_image(img, repo_url, local_repo, def_branch))
        else:
            images.append(rename_github_image(img, repo_url, local_repo, def_branch))

    for index_img in img_html:
        init = html_text.find("src=\"", index_img)
        end = html_text.find("\"", init + 5)
        img = html_text[init + 5:end]
        # if the image contains jitpack.io, the element is not processed
        if img.find("jitpack.io") > 0 or img.find("/badge") >= 0 or img.find("/travis-ci.") >= 0 \
                or img.find("img.shields.io") >= 0:
            pass
        elif logo == "" and repo_url is not None:
            start = 0
            if img.find("/") > 0:
                start = img.rindex("/")
            image_name = img[start:]
            if image_name.find(repo_name) > 0 or image_name.upper().find("LOGO") > 0:
                logo = rename_github_image(img, repo_url, local_repo, def_branch)
            elif get_alt_text_img(html_text, index_img) == repo_name or get_alt_text_img(html_text,
                                                                                         index_img).upper() == "LOGO":
                logo = rename_github_image(img, repo_url, local_repo, def_branch)
            else:
                images.append(rename_github_image(img, repo_url, local_repo, def_branch))
        else:
            start = img.rindex("/")
            if img.upper().find("LOGO", start) > 0:
                logo = rename_github_image(img, repo_url, local_repo, def_branch)
            else:
                images.append(rename_github_image(img, repo_url, local_repo, def_branch))
    if logo != "":
        repository_metadata.add_result(constants.CAT_LOGO,
                                       {
                                           constants.PROP_TYPE: constants.URL,
                                           constants.PROP_VALUE: logo
                                       }, 1, constants.TECHNIQUE_REGULAR_EXPRESSION, readme_source)
    for image in images:
        repository_metadata.add_result(constants.CAT_IMAGE,
                                       {
                                           constants.PROP_TYPE: constants.URL,
                                           constants.PROP_VALUE: image
                                       }, 1, constants.TECHNIQUE_REGULAR_EXPRESSION, readme_source)
    return repository_metadata


def extract_package_distributions(unfiltered_text, repository_metadata: Result, readme_source) -> Result:
    """
    Function that takes readme text as input (cleaned from markdown notation) and runs a regex expression on top of it.
    Extracts package distributions from a given text

    Parameters
    ----------
    @param unfiltered_text: Text of the readme
    @param repository_metadata: Result with all the processed results so far
    @param readme_source: source to the readme file used

    Returns
    -------
    A Result object with the package distributions found in the repo (Python packages for now)
    """
    output = ""
    index_package_distribution = unfiltered_text.find(constants.REGEXP_PYPI)
    # If not found, we try again with the other regexp
    if index_package_distribution <= 0:
        index_package_distribution = unfiltered_text.find(constants.REGEXP_PYPI_2)
    if index_package_distribution > 0:
        init = unfiltered_text.find(")](", index_package_distribution)
        end = unfiltered_text.find(")", init + 3)
        package_distribution = unfiltered_text[init + 3:end]
        output = requests.get(package_distribution).url

        # If the output is empty or none, the category doesn't make sense and shouldn't be displayed in the final result
        if has_valid_output(output):
            repository_metadata.add_result(constants.CAT_PACKAGE_DISTRIBUTION,
                                       {
                                           constants.PROP_TYPE: constants.URL,
                                           constants.PROP_VALUE: output
                                       }, 1, constants.TECHNIQUE_REGULAR_EXPRESSION, readme_source)

    return repository_metadata


def extract_colab_links(text):
    """
    Method designed to find colab notebooks in readmes
    Parameters
    ----------
    text: markdown text where the links to colab will be searched.

    Returns
    -------
    A list of colab links found in the text passed as a parameter.
    """
    output = []
    links = re.findall(constants.REGEXP_LINKS, text)
    for link in links:
        link_url = link[1]
        if link_url.startswith(constants.REGEXP_COLAB):
            output.append(link_url)
    return output


def remove_html_tags(text):
    regex = re.compile('<.*?>')
    clean_text = re.sub(regex, '', text)
    return clean_text


def remove_links_images(text):
    """Removes links from images in a given text"""
    # process images
    images = re.findall(constants.REGEXP_IMAGES, text)
    for image in images:
        link_text = image[1]
        pos = text.find(link_text)
        if pos != -1:
            init = text[:pos].rindex("![")
            end = text[pos:].index(")")
            image_text = text[init:pos + end + 1]
            text = text.replace(image_text, "")

    # process links
    links = re.findall(constants.REGEXP_LINKS, text)
    for link in links:
        link_text = link[1]
        pos = text.find("(" + link_text + ")")
        if pos != -1:
            init = text[:pos].rindex("[")
            end = text[pos:].index(")")
            link_text = text[init:pos + end + 1]
            text = text.replace(link_text, "")

    # remove blank spaces and \n
    return text.strip()


def extract_bibtex(readme_text, repository_metadata: Result, readme_source) -> Result:
    """
    Function takes readme text as input (cleaned from markdown notation) and runs a regex expression on top of it.
    Returns list of bibtex citations

    Parameters
    ----------
    @param readme_text: Text of the readme
    @param repository_metadata: Result with all the processed results so far
    @param readme_source: source to the readme file used

    Returns
    -------
    @returns Result object with the bibtex associated with this software component
    """
    try:
        bib_database = bibtexparser.loads(readme_text)
        entries = bib_database.entries
        for entry in entries:
            # dumping the found fields does not seem to work, so rebuilding the object:
            exported_bibtex = f"@{entry['ENTRYTYPE']}{{{entry['ID']},\n"
            for key, value in entry.items():
                if key not in ('ENTRYTYPE', 'ID'):
                    exported_bibtex += f"    {key} = {{{value}}},\n"
            exported_bibtex += "}"
            result = {
                constants.PROP_VALUE: exported_bibtex,
                constants.PROP_TYPE: constants.TEXT_EXCERPT,
                constants.PROP_FORMAT: constants.FORMAT_BIB
            }
            if constants.PROP_DOI in entry:
                result[constants.PROP_DOI] = entry[constants.PROP_DOI]
            if constants.PROP_TITLE in entry:
                result[constants.PROP_TITLE] = entry[constants.PROP_TITLE]
            if constants.PROP_AUTHOR in entry:
                result[constants.PROP_AUTHOR] = entry[constants.PROP_AUTHOR]
            if constants.PROP_URL in entry:
                result[constants.PROP_URL] = entry[constants.PROP_URL]
            repository_metadata.add_result(constants.CAT_CITATION, result, 1,
                                           constants.TECHNIQUE_REGULAR_EXPRESSION, readme_source)
    except Exception as e:
        logging.warning("An error occurred when trying to extract bibtex from README " + str(e))
    return repository_metadata


def extract_doi_badges(readme_text, repository_metadata: Result, source) -> Result:
    """
    Function that takes the text of a readme file and searches if there are any DOIs badges.
    Parameters
    ----------
    @param readme_text: Text of the readme
    @param repository_metadata: Result with all the findings in the repo
    @param source: source file on top of which the extraction is performed (provenance)
    Returns
    -------
    @returns Result with the DOI badges found
    """
    # regex = r'\[\!\[DOI\]([^\]]+)\]\(([^)]+)\)'
    # regex = r'\[\!\[DOI\]\(.+\)\]\(([^)]+)\)'
    doi_badges = re.findall(constants.REGEXP_DOI, readme_text)
    # The identifier is in position 1. Position 0 is the badge id, which we don't want to export
    for doi in doi_badges:
        repository_metadata.add_result(constants.CAT_IDENTIFIER,
                                       {
                                           constants.PROP_TYPE: constants.URL,
                                           constants.PROP_VALUE: doi[1]
                                       }, 1, constants.TECHNIQUE_REGULAR_EXPRESSION, source)
        
    return repository_metadata

def extract_project_homepage_badges(readme_text, repository_metadata: Result, source) -> Result:
    """
    Function that takes the text of a readme file and searches if there are any project homepages.
    Parameters
    ----------
    @param readme_text: Text of the readme
    @param repository_metadata: Result with all the findings in the repo
    @param source: source file on top of which the extraction is performed (provenance)
    Returns
    -------
    @returns Result with the Sofware heritage badges found
    """
    homepage_badges = re.findall(constants.REGEXP_PROJECT_HOMEPAGE, readme_text)
    # The identifier is in position 1. Position 0 is the badge id, which we don't want to export

    for homepage in homepage_badges:
        repository_metadata.add_result(constants.CAT_HOMEPAGE,
                                       {
                                           constants.PROP_TYPE: constants.URL,
                                           constants.PROP_VALUE: homepage[1]
                                       }, 1, constants.TECHNIQUE_REGULAR_EXPRESSION, source)
        
    return repository_metadata

def extract_swh_badges(readme_text, repository_metadata: Result, source) -> Result:
    """
    Function that takes the text of a readme file and searches if there are any Software Heritage (swh) badges.
    Parameters
    ----------
    @param readme_text: Text of the readme
    @param repository_metadata: Result with all the findings in the repo
    @param source: source file on top of which the extraction is performed (provenance)
    Returns
    -------
    @returns Result with the Sofware heritage badges found
    """
    swh_badges = re.findall(constants.REGEXP_SWH, readme_text)
    # The identifier is in position 1. Position 0 is the badge id, which we don't want to export

    for swh in swh_badges:

        identifier = extract_swh_identifier_from_url(swh[1])
        if identifier:
            url_identifier = constants.SWH_ROOT + identifier
            repository_metadata.add_result(constants.CAT_IDENTIFIER,
                                       {
                                           constants.PROP_TYPE: constants.URL,
                                           constants.PROP_VALUE: url_identifier
                                       }, 1, constants.TECHNIQUE_REGULAR_EXPRESSION, source)
        
    return repository_metadata

def extract_swh_identifier_from_url(url: str) -> str | None:
    """
    Function that look for a correct identifier en the swh url
    """

    #  If anchor look for identifier
    anchor_match = re.search(constants.REGEXP_SWH_ANCHOR, url)
    if anchor_match:
        return anchor_match.group(1)

    #  If no anchor look for all identifiers
    all_matches = re.findall(constants.REGEXP_SWH_ALL_IDENTIFIERS, url)
    if all_matches:
        for preferred_type in ['rev', 'snp', 'dir', 'cnt']:
            for match in all_matches:
                if f"swh:1:{preferred_type}:" in match:
                    return match

    return None

def extract_binder_links(readme_text, repository_metadata: Result, source) -> Result:
    """
    Function that does a regex to extract binder and colab links used as reference in the readme.
    There could be multiple binder links for one repository
    Parameters
    ----------
    @param readme_text: Text of the readme
    @param repository_metadata: Result with all the findings in the repo
    @param source: source file on top of which the extraction is performed (provenance)
    Returns
    -------
    Links with binder notebooks/scripts that are ready to be executed.
    """
    links = re.findall(constants.REGEXP_BINDER, readme_text, re.IGNORECASE)
    binder_links = [result[1] for result in links]
    # extract binder links and remove duplicates
    binder_links += extract_colab_links(readme_text)
    for link in list(dict.fromkeys(binder_links)):
        repository_metadata.add_result(constants.CAT_EXECUTABLE_EXAMPLE,
                                       {
                                           constants.PROP_TYPE: constants.URL,
                                           constants.PROP_VALUE: link
                                       }, 1, constants.TECHNIQUE_REGULAR_EXPRESSION, source)
    return repository_metadata


def rename_github_image(img, repo_url, local_repo, default_branch):
    """Renames GitHub image links so they can be accessed raw"""
    if img.startswith("http"):
        if "/raw/" in img:
            # raw link is already in there: do nothing
            return img
        if img.find("github.com") > 0:
            img = img.replace("/blob", "")
            img = img.replace("github.com", "raw.githubusercontent.com")
    if not img.startswith("http") and (
            (repo_url is not None and repo_url != "") or (local_repo is not None and local_repo != "")):
        if repo_url is not None and repo_url != "":
            if repo_url.find("/tree/") > 0:
                repo_url = repo_url.replace("/tree/", "/")
            else:
                repo_url = repo_url + "/" + default_branch + "/"
            repo_url = repo_url.replace("github.com", "raw.githubusercontent.com")
            if not repo_url.endswith("/"):
                repo_url = repo_url + "/"
            img = repo_url + img
        else:
            img = local_repo + os.path.sep + img
    return img


def get_alt_text_md(text, image):
    stop = text.find(image) - 2
    start = text[:stop].rindex("![") + 2
    return text[start:stop]


def get_alt_text_img(html_text, index):
    """Processing alt names for images"""
    end = html_text.find(">", index)
    output = ""
    if html_text.find("alt=", index, end) > 0:
        texto = html_text[index:end]
        init = texto.find("alt=\"") + 5
        end = texto.index("\"", init)
        output = texto[init:end]
    return output


def get_alt_text_html(text, image):
    """Processing alt names for images in html"""
    stop = text.find(image)
    start = text[:stop].rindex("<img")
    if text[start:stop].find("alt=") != -1:
        start = text.find("alt=", start) + 4
        stop = text.find("\"", start) - 1
        return text[start:stop]
    return ""

def has_valid_output(text):
    """Returns True if text is not None, not empty, and not 'null'."""
    return bool(text and text.strip().lower() != "null")

def has_valid_link(link):
    """Returns True if the link is a non-empty, non-null string."""
    return isinstance(link, str) and link.strip().lower() not in ["", "none", "null"]

def has_valid_links(link_list):
    """Returns True if the list has at least one valid link."""
    return any(has_valid_link(link) for link in link_list)

def detect_license_spdx(license_text, type):
    """
    Function that given a license text, infers the name and spdx id in a JSON format
    Parameters
    ----------
    license_text

    Returns
    -------
    A JSON dictionary with name and spdx id
    """
    for license_name, license_info in constants.LICENSES_DICT.items():
        if re.search(license_info["regex"], license_text, re.IGNORECASE):
            if type == 'JSON':
                return {
                    "name": license_name,
                    "spdx_id": f"{license_info['spdx_id']}",
                    "@id": f"https://spdx.org/licenses/{license_info['spdx_id']}"
                }
            else:
                return {
                    "name": license_name,
                    "identifier": f"https://spdx.org/licenses/{license_info['spdx_id']}"
                }
    return None

# def detect_license(license_text):
#     for license_name, license_info in constants.LICENSES_DICT.items():
#         if re.search(license_info["regex"], license_text, re.IGNORECASE):
#             return {
#                 "name": license_name,
#                 "identifier": f"https://spdx.org/licenses/{license_info['spdx_id']}"
#             }
#     return None

def extract_scholarly_article_properties(bibtex_entry, scholarlyArticle, type):
    """
    Extract datePublished, issn and pagination fromg BibTeX and append to scholarlyArticle object
    
    Params:
        - bibtex_entry (str): BibTeX entry in string format.
        - scholarlyArticle (dict): Dictionary where the extracted data will be stored.
        - type (str): from codemeta or json
    """

    # regular expresions properties
    issn_match = re.search(constants.REGEXP_ISSN, bibtex_entry)
    year_match = re.search(constants.REGEXP_YEAR, bibtex_entry)
    month_match = re.search(constants.REGEXP_MONTH, bibtex_entry)
    pages_match = re.search(constants.REGEXP_PAGES, bibtex_entry)
    author_match = re.search(r'author\s*=\s*\{([^}]+)\}', bibtex_entry) 
    orcid_match = re.search(r'orcid\s*=\s*\{([^}]+)\}', bibtex_entry)  # Look for ORCID explícit
    note_orcid_match = re.search(r'ORCID[:\s]*([\d-]+X?)', bibtex_entry)  # Look in notes

    issn = issn_match.group(1) if issn_match else None
    year = year_match.group(1) if year_match else None
    month = month_match.group(1) if month_match else None
    pagination = pages_match.group(1) if pages_match else None
    authors = author_match.group(1) if author_match else None
    orcid = orcid_match.group(1) if orcid_match else None

    date_published = f"{year}-{month.zfill(2)}" if year and month else year 

    if issn:
        scholarlyArticle["issn"] = issn
    if date_published:
        scholarlyArticle["datePublished"] = date_published
    if pagination:
        scholarlyArticle["pagination"] = pagination

    if author_match:
        author_list = []
        authors = author_match.group(1).split(" and ")  # Split several authors

        for author in authors:
            parts = author.split(", ") 
            if len(parts) == 2:
                family_name, given_name = parts
            else:
                family_name = author
                given_name = None  

            if type == 'JSON':
                author_entry = {
                    "type": "Agent",
                    "name": f"{given_name} {family_name}",
                    "family_name": family_name.strip(),
                    "given_name": given_name.strip() if given_name else None
                }
            else:
                author_entry = {
                    "@type": "Person",
                    "familyName": family_name.strip(),
                    "givenName": given_name.strip() if given_name else None
                }
            
            # in bibtext orcid do not works correctly and in case we have several authors 
            # if could be dificult to asign the orcid because bibtext just manage one.
            if len(author_list) == 1 and orcid:
                if not orcid.startswith("http"):  # check if is a url
                    orcid = f"https://orcid.org/{orcid}"
                if type == 'JSON':
                   author_list[0]["url"] = f"https://orcid.org/{orcid}" 
                else:
                    author_list[0]["@id"] = f"https://orcid.org/{orcid}"

            author_list.append({k: v for k, v in author_entry.items() if v is not None}) 

        if author_list:
            scholarlyArticle["author"] = author_list  # Add to authors list

    return scholarlyArticle

def extract_scholarly_article_natural(citation_text, scholarly_article, type):
    """
    Extracts information from a natural language citation and structures it as a ScholarlyArticle.
    Params:
        - citation_text (str): The citation text in natural language.
        - scholarly_article (dict): Dictionary where the extracted data will be stored.
         - type (str): from codemeta or json
    Returns:
        - dict: Dictionary with the extracted data in the desired format.
    """

    # regular expresions
    doi_match = re.search(constants.REGEXP_DOI_NATURAL, citation_text)
    year_match = re.search(constants.REGEXP_YEAR_NATURAL, citation_text)
    url_match = re.search(constants.REGEXP_URL_NATURAL, citation_text)
    author_match = re.search(constants.REGEXP_AUTHOR_NATURAL, citation_text)
    title_match = re.search(constants.REGEXP_TITLE_NATURAL, citation_text)

    if doi_match:
        scholarly_article["identifier"] = doi_match.group(0)
        scholarly_article["url"] = f"https://doi.org/{doi_match.group(0)}"
    
    if year_match:
        scholarly_article["datePublished"] = year_match.group(0)
    
    if url_match and "url" not in scholarly_article:
        scholarly_article["url"] = url_match.group(0)

    if title_match:
        scholarly_article["name"] = title_match.group(1)

    # Authors in format surname, name 
    if author_match:
        authors_text = author_match.group(0).replace(" et al.", "").strip()
        author_list = []
        for author in authors_text.split(", "):
            parts = author.split(" ")
            family_name = parts[-1]
            given_name = " ".join(parts[:-1])
            if type == 'JSON':
                author_list.append({"type": "Agent", "name": f"{given_name} {family_name}","family_name": family_name, "given_name": given_name})
            else:
                author_list.append({"@type": "Person", "familyName": family_name, "givenName": given_name})

        scholarly_article["author"] = author_list

    return scholarly_article