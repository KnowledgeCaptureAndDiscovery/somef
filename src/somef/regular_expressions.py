import os
import re
import markdown
import requests
import validators
from urllib.parse import urlparse


def extract_title(unfiltered_text):
    """Regexp to extract title (first header) from a repository"""
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
    return output


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
    # title = re.sub(r'/\[\!([^\[\]]*)\]\((.*?)\)', '',title)
    return title


def extract_readthedocs(readme_text) -> object:
    """
    Function to extract readthedocs links from text
    Parameters
    ----------
    unfiltered_text text readme

    Returns
    -------
    Links to the readthedocs documentation
    """
    # regex = r'http[s]?://[\w]+.readthedocs.io/'
    regex = r'http[s]?://[-a-zA-Z0-9+&@#/%?=~_|!:,.;]*[-a-zA-Z0-9+&@#/%=~_|]+.readthedocs.io/'
    readthedocs_links = re.findall(regex, readme_text)
    print("Extraction of readthedocs links from readme completed.\n")
    # remove duplicates (links like [readthedocs](readthedocs) are found twice
    return list(dict.fromkeys(readthedocs_links))


def extract_support_channels(readme_text):
    """
    Function to extract Gitter Chat, Reddit and Discord links from text
    Parameters
    ----------
    readme_text text readme

    Returns
    -------
    Link to the Gitter Chat
    """
    results = []

    index_gitter_chat = readme_text.find("[![Gitter chat]")
    if index_gitter_chat > 0:
        init = readme_text.find(")](", index_gitter_chat)
        end = readme_text.find(")", init + 3)
        gitter_chat = readme_text[init + 3:end]
        results.append(gitter_chat)

    init = readme_text.find("(https://www.reddit.com/r/")
    if init > 0:
        end = readme_text.find(")", init)
        repo_status = readme_text[init + 1:end]
        results.append(repo_status)

    init = readme_text.find("(https://discord.com/invite/")
    if init > 0:
        end = readme_text.find(")", init)
        repo_status = readme_text[init + 1:end]
        results.append(repo_status)

    return results


def extract_repo_status(unfiltered_text):
    """Extracts the repostatus.org badge from a given text"""
    repo_status = ""
    init = unfiltered_text.find("[![Project Status:")
    if init > 0:
        end = unfiltered_text.find("](", init)
        repo_status = unfiltered_text[init + 3:end]
        repo_status = repo_status.replace("Project Status: ", "")
    return repo_status


def extract_arxiv_links(unfiltered_text):
    """Extracts arxiv links from a given text"""
    result_links = [m.start() for m in re.finditer('https://arxiv.org/', unfiltered_text)]
    result_refs = [m.start() for m in re.finditer('arXiv:', unfiltered_text)]
    results = []
    for position in result_links:
        end = unfiltered_text.find(')', position)
        link = unfiltered_text[position:end]
        results.append(link)
    for position in result_refs:
        end = unfiltered_text.find('}', position)
        link = unfiltered_text[position:end]
        results.append(link.replace('arXiv:', 'https://arxiv.org/abs/'))

    return results


def extract_wiki_links(unfiltered_text, repo_url):
    """Extracts wiki links from a given text"""
    links = re.findall(r"\[[^\]]*\]\((.*?)?\)", unfiltered_text)
    output = []
    ends = 0
    for link in links:
        if validators.url(link):
            if link.endswith("/wiki"):
                output.append(link)
            else:
                ends = unfiltered_text.find("(" + link + ")") - 1
                if unfiltered_text[:ends].find("[") != -1:
                    position = unfiltered_text[:ends].rindex("[") + 1
                    if unfiltered_text[position:ends].find("wiki") >= 0:
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
            output.append(repo_url)

    return list(dict.fromkeys(output))


# TO DO: join with image detection in a single method
def extract_logo(unfiltered_text, repo_url):
    """Extracts logos from a given text"""
    logo = ""
    index_logo = unfiltered_text.lower().find("![logo]")
    if index_logo >= 0:
        init = unfiltered_text.find("(", index_logo)
        end = unfiltered_text.find(")", init)
        logo = unfiltered_text[init + 1:end]
    else:
        # This is problematic if alt label is used
        # TO DO
        result = [_.start() for _ in re.finditer("<img src=", unfiltered_text)]
        if len(result) > 0:
            for index_img in result:
                init = unfiltered_text.find("\"", index_img)
                end = unfiltered_text.find("\"", init + 1)
                img = unfiltered_text[init + 1:end]
                if img.find("logo") > 0:
                    logo = img
    # processing for those github links that do not resolve correctly
    if logo.startswith("http"):
        if logo.find("github.com") > 0:
            logo = logo.replace("/blob", "")
            logo = logo.replace("github.com", "raw.githubusercontent.com")
    #processing for those logos that are relative paths
    if logo != "" and not logo.startswith("http") and repo_url is not None:
        if repo_url.find("github.com") > 0:
            if repo_url.find("/tree/") > 0:
                repo_url = repo_url.replace("/tree/", "/")
            else:
                repo_url = repo_url + "/master/"
            repo_url = repo_url.replace("github.com", "raw.githubusercontent.com")
            if not repo_url.endswith("/"):
                repo_url = repo_url + "/"
            logo = repo_url + logo
        else:
            if not repo_url.endswith("/"):
                repo_url = repo_url + "/"
            logo = repo_url + logo
    print(logo)
    return logo


def extract_images(unfiltered_text, repo_url, local_repo):
    """Extracts logos from a given text"""
    logo = ""
    has_logo = False
    images = []
    repo = False
    repo_name = ""
    if repo_url is not None and repo_url != "":
        url = urlparse(repo_url)
        path_components = url.path.split('/')
        repo_name = path_components[2]
        repo = True

    html_text = markdown.markdown(unfiltered_text)
    img_md = re.findall(r"!\[[^\]]*\]\((.*?)?\)", html_text)
    result = [_.start() for _ in re.finditer("<img ", html_text)]
    for img in img_md:
        # if the image contains jitpack.io, the element is not processed
        if img.find("jitpack.io") > 0 or img.find("/badge") >= 0 or img.find("/travis-ci.org") >= 0 \
                or img.find("img.shields.io") >= 0:
            None
        elif not has_logo and repo:
            start = img.rindex("/")
            if img.find(repo_name, start) > 0:
                logo = rename_github_image(img, repo_url, local_repo)
                has_logo = True
            elif get_alt_text_md(html_text, img) == repo_name or get_alt_text_md(html_text, img).upper() == "LOGO":
                logo = rename_github_image(img, repo_url, local_repo)
                has_logo = True
            else:
                start = img.rindex("/")
                if img.upper().find("LOGO", start) > 0:
                    logo = rename_github_image(img, repo_url, local_repo)
                    has_logo = True
                else:
                    images.append(rename_github_image(img, repo_url, local_repo))
        else:
            images.append(rename_github_image(img, repo_url, local_repo))
    for index_img in result:
        init = html_text.find("src=\"", index_img)
        end = html_text.find("\"", init + 5)
        img = html_text[init + 5:end]
        # if the image contains jitpack.io, the element is not processed
        if img.find("jitpack.io") > 0 or img.find("/badge") >= 0 or img.find("/travis-ci.org") >= 0 \
                or img.find("img.shields.io") >= 0:
            None
        elif not has_logo and repo:
            start = 0
            if img.find("/") > 0:
                start = img.rindex("/")
            image_name = img[start:]
            if image_name.find(repo_name) > 0 or image_name.upper().find("LOGO") > 0:
                logo = rename_github_image(img, repo_url, local_repo)
                has_logo = True
            elif get_alt_text_img(html_text, index_img) == repo_name or get_alt_text_img(html_text,
                                                                                         index_img).upper() == "LOGO":
                logo = rename_github_image(img, repo_url, local_repo)
                has_logo = True
            else:
                images.append(rename_github_image(img, repo_url, local_repo))
        else:
            start = img.rindex("/")
            if img.upper().find("LOGO", start) > 0:
                logo = rename_github_image(img, repo_url, local_repo)
                has_logo = True
            else:
                images.append(rename_github_image(img, repo_url, local_repo))

    return logo, images


# TO DO: join with logo detection
def extract_images_old(unfiltered_text, repo_url):
    """Extracts images from a given text"""
    logo = ""
    images = []
    html_text = markdown.markdown(unfiltered_text)
    # print(html_text)
    result = [_.start() for _ in re.finditer("<img ", html_text)]
    if len(result) > 0:
        for index_img in result:
            init = html_text.find("src=\"", index_img)
            end = html_text.find("\"", init + 5)
            img = html_text[init + 5:end]
            if img.find("logo") < 0:
                if not img.startswith("http") and repo_url is not None:
                    if repo_url.find("/tree/") > 0:
                        repo_url = repo_url.replace("/tree/", "/")
                    else:
                        repo_url = repo_url + "/master/"
                    repo_url = repo_url.replace("github.com", "raw.githubusercontent.com")
                    if not repo_url.endswith("/"):
                        repo_url = repo_url + "/"
                    img = repo_url + img
                images.append(img)
            else:
                if not img.startswith("http") and repo_url is not None:
                    if repo_url.find("/tree/") > 0:
                        repo_url = repo_url.replace("/tree/", "/")
                    else:
                        repo_url = repo_url + "/master/"
                    repo_url = repo_url.replace("github.com", "raw.githubusercontent.com")
                    if not repo_url.endswith("/"):
                        repo_url = repo_url + "/"
                    img = repo_url + img
                logo = img

    if logo == "" and repo_url != "" and repo_url != None:
        print(repo_url)
        url = urlparse(repo_url)
        path_components = url.path.split('/')
        repo_name = path_components[2]

        for image in images:
            start = image.rindex("/")
            if image.find(repo_name, start) > 0:
                logo = image
                images.remove(image)
                break

    return logo, images


def extract_support(unfiltered_text):
    """Extracts support channels (reddit, discord, gitter) from a given text"""
    results = []
    init = unfiltered_text.find("(https://www.reddit.com/r/")
    if init > 0:
        end = unfiltered_text.find(")", init)
        repo_status = unfiltered_text[init + 1:end]
        results.append(repo_status)

    init = unfiltered_text.find("(https://discord.com/invite/")
    if init > 0:
        end = unfiltered_text.find(")", init)
        repo_status = unfiltered_text[init + 1:end]
        results.append(repo_status)

    return results


def extract_package_distributions(unfiltered_text):
    """Extracts package distributions from a given text"""
    output = ""
    index_package_distribution = unfiltered_text.find("[![PyPI]")
    if index_package_distribution > 0:
        init = unfiltered_text.find(")](", index_package_distribution)
        end = unfiltered_text.find(")", init + 3)
        package_distribution = unfiltered_text[init + 3:end]
        output = requests.get(package_distribution).url

    return output


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
    links = re.findall(r"\[(.*?)?\]\(([^)]+)\)", text)
    for link in links:
        link_url = link[1]
        if link_url.startswith("https://colab.research.google.com/drive"):
            output.append(link_url)
    return output


def remove_html_tags(text):
    regex = re.compile('<.*?>')
    clean_text = re.sub(regex, '', text)
    return clean_text

def remove_links_images(text):
    """Removes links from images in a given text"""
    # process images
    images = re.findall(r"!\[(.*?)?\]\((.*?)?\)", text)
    for image in images:
        link_text = image[1]
        pos = text.find(link_text)
        if pos != -1:
            init = text[:pos].rindex("![")
            end = text[pos:].index(")")
            image_text = text[init:pos + end + 1]
            text = text.replace(image_text, "")

    # process links
    links = re.findall(r"\[(.*?)?\]\(([^)]+)\)", text)
    for link in links:
        link_text = link[1]
        pos = text.find("("+link_text+")")
        if pos != -1:
            init = text[:pos].rindex("[")
            end = text[pos:].index(")")
            link_text = text[init:pos + end + 1]
            text = text.replace(link_text, "")

    # remove blank spaces and \n
    return text.strip()


def extract_bibtex(readme_text) -> object:
    """
    Function takes readme text as input (cleaned from markdown notation) and runs a regex expression on top of it.
    Returns list of bibtex citations
    """
    regex = r'\@[a-zA-Z]+\{[.\n\S\s]+?[author|title][.\n\S\s]+?[author|title][.\n\S\s]+?\n\}'
    citations = re.findall(regex, readme_text)
    return citations


def extract_dois(readme_text) -> object:
    """
    Function that takes the text of a readme file and searches if there are any DOIs badges.
    Parameters
    ----------
    readme_text Text of the readme

    Returns
    -------
    DOIs/identifiers associated with this software component
    """
    # regex = r'\[\!\[DOI\]([^\]]+)\]\(([^)]+)\)'
    # regex = r'\[\!\[DOI\]\(.+\)\]\(([^)]+)\)'
    regex = r'\[\!\[DOI\]([^\]]+)\]\(([^)]+)\)'
    dois = re.findall(regex, readme_text)
    print("Extraction of DOIS from readme completed.\n")
    return dois


def extract_binder_links(readme_text) -> object:
    """
    Function that does a regex to extract binder links used as reference in the readme.
    There could be multiple binder links for one reprository
    Parameters
    ----------
    readme_text

    Returns
    -------
    Links with binder notebooks/scripts that are ready to be executed.
    """
    regex = r'\[\!\[Binder\]([^\]]+)\]\(([^)]+)\)'
    binder_links = re.findall(regex, readme_text)
    print("Extraction of Binder links from readme completed.\n")
    # remove duplicates
    collabs = extract_colab_links(readme_text)
    binder_links += collabs
    return list(dict.fromkeys(binder_links))


def rename_github_image(img, repo_url, local_repo):
    """Renames GitHub image links so they can be accessed raw"""
    if img.startswith("http"):
        if img.find("github.com") > 0:
            img = img.replace("/blob", "")
            img = img.replace("github.com", "raw.githubusercontent.com")
    if not img.startswith("http") and ((repo_url is not None and repo_url != "") or (local_repo is not None and local_repo != "")):
        if repo_url is not None and repo_url != "":
            if repo_url.find("/tree/") > 0:
                repo_url = repo_url.replace("/tree/", "/")
            else:
                repo_url = repo_url + "/master/"
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
