import sys
import validators
import logging
import os
import tempfile

from os import path
from . import header_analysis, regular_expressions, process_repository, configuration, process_files, \
    supervised_classification
from .process_results import Result
from .utils import constants, markdown_utils
from .parser import mardown_parser, create_excerpts
from .export.turtle_export import DataGraph
from .export import json_export
from .extract_software_type import check_repository_type


def cli_get_data(threshold, ignore_classifiers, repo_url=None, doc_src=None, local_repo=None,
                 ignore_github_metadata=False, readme_only=False, keep_tmp=None, authorization=None) -> Result:
    """
    Main function to get the data through the command line
    Parameters
    ----------
    @param threshold: threshold to filter annotations. 0.8 by default
    @param ignore_classifiers: flag to indicate if the output from the classifiers should be ignored
    @param repo_url: URL of the repository to analyze
    @param doc_src: path to the src of the target repo
    @param local_repo: flag to indicate that the repo is local
    @param ignore_github_metadata: flag used to avoid doing extra requests to the GitHub API
    @param readme_only: flag to indicate that only the readme should be analyzed
    @param keep_tmp: path where to store TMP files in case SOMEF is instructed to keep them
    @param authorization: GitHub authorization token

    Returns
    -------
    @return: Dictionary with the results found by SOMEF, formatted as a Result object.
    """
    file_paths = configuration.get_configuration_file()
    repo_type = constants.RepositoryType.GITHUB
    repository_metadata = Result()
    def_branch = "main"
    if repo_url is not None:
        try:
            if repo_url.rfind("gitlab.com") > 0:
                repo_type = constants.RepositoryType.GITLAB
            repository_metadata, owner, repo_name, def_branch = process_repository.load_online_repository_metadata(
                repository_metadata,
                repo_url,
                ignore_github_metadata,
                repo_type,
                authorization
                )
            # download files and obtain path to download folder
            if readme_only:
                # download readme only with the information above
                readme_text = process_repository.download_readme(owner, repo_name, def_branch, repo_type, authorization)

            elif keep_tmp is not None:  # save downloaded files locally
                os.makedirs(keep_tmp, exist_ok=True)
                local_folder = process_repository.download_repository_files(owner, repo_name, def_branch, repo_type,
                                                                            keep_tmp, repo_url, authorization)
                readme_text, full_repository_metadata = process_files.process_repository_files(local_folder,
                                                                                               repository_metadata,
                                                                                               repo_type, owner,
                                                                                               repo_name,
                                                                                               def_branch)
                repository_metadata = check_repository_type(local_folder,repo_name,full_repository_metadata) 
            else:  # Use a temp directory
                with tempfile.TemporaryDirectory() as temp_dir:
                    local_folder = process_repository.download_repository_files(owner, repo_name, def_branch, repo_type,
                                                                                temp_dir, repo_url, authorization)
                    readme_text, full_repository_metadata = process_files.process_repository_files(local_folder,
                                                                                                   repository_metadata,
                                                                                                   repo_type, owner,
                                                                                                   repo_name,
                                                                                                   def_branch)
                    repository_metadata = check_repository_type(local_folder,repo_name,full_repository_metadata) 
            if readme_text == "":
                logging.warning("README document does not exist in the target repository")
        except process_repository.GithubUrlError:
            logging.error("Error processing the target repository")
            return repository_metadata
    elif local_repo is not None:
        try:
            readme_text, full_repository_metadata = process_files.process_repository_files(local_repo,
                                                                                           repository_metadata,
                                                                                           repo_type)
            if readme_text == "":
                logging.warning("Warning: README document does not exist in the local repository")
        except process_repository.GithubUrlError:
            logging.error("Error processing the input repository")
            return repository_metadata
    else:
        if doc_src is None or not path.exists(doc_src):
            logging.error("Error processing the input repository")
            sys.exit()
        with open(doc_src, 'r', encoding="UTF-8") as doc_fh:
            readme_text = doc_fh.read()
    try:
        readme_unfiltered_text = readme_text
        # remove html comments from unfiltered text (to avoid detecting commented out (wrong) metadata
        readme_unfiltered_text = markdown_utils.remove_comments(readme_unfiltered_text)
        repository_metadata, string_list = header_analysis.extract_categories(readme_unfiltered_text, repository_metadata)
        readme_text_unmarked = markdown_utils.unmark(readme_text)
        if not ignore_classifiers and readme_unfiltered_text != '':
            repository_metadata = supervised_classification.run_category_classification(readme_unfiltered_text, threshold,
                                                                                        repository_metadata)
            excerpts = create_excerpts.create_excerpts(string_list)
            excerpts_headers = mardown_parser.extract_text_excerpts_header(readme_unfiltered_text)
            header_parents = mardown_parser.extract_headers_parents(readme_unfiltered_text)
            score_dict = supervised_classification.run_classifiers(excerpts, file_paths)
            repository_metadata = supervised_classification.classify(score_dict, threshold, excerpts_headers,
                                                                     header_parents, repository_metadata)
        if readme_text_unmarked != "":
            try:
                readme_source = repository_metadata.results[constants.CAT_README_URL][0]
                readme_source = readme_source[constants.PROP_RESULT][constants.PROP_VALUE]
            except:
                readme_source = "README.md"
            repository_metadata = regular_expressions.extract_bibtex(readme_unfiltered_text, repository_metadata, readme_source)
            repository_metadata = regular_expressions.extract_doi_badges(readme_unfiltered_text, repository_metadata,
                                                                         readme_source)
            repository_metadata = regular_expressions.extract_title(readme_unfiltered_text, repository_metadata, readme_source)
            repository_metadata = regular_expressions.extract_binder_links(readme_unfiltered_text, repository_metadata,
                                                                           readme_source)
            repository_metadata = regular_expressions.extract_readthedocs(readme_unfiltered_text, repository_metadata,
                                                                          readme_source)
            repository_metadata = regular_expressions.extract_repo_status(readme_unfiltered_text, repository_metadata,
                                                                          readme_source)
            repository_metadata = regular_expressions.extract_wiki_links(readme_unfiltered_text, repo_url, repository_metadata,
                                                                         readme_source)
            repository_metadata = regular_expressions.extract_support_channels(readme_unfiltered_text, repository_metadata,
                                                                               readme_source)
            repository_metadata = regular_expressions.extract_package_distributions(readme_unfiltered_text,
                                                                                    repository_metadata,
                                                                                    readme_source)
            repository_metadata = regular_expressions.extract_images(readme_unfiltered_text, repo_url, local_repo,
                                                                     repository_metadata, readme_source, def_branch)
            repository_metadata = regular_expressions.extract_arxiv_links(readme_unfiltered_text,repository_metadata,readme_source)
            logging.info("Completed extracting regular expressions")

        return repository_metadata


    except Exception as e:
        logging.error("Error processing repository " + str(e))
        return repository_metadata


def run_cli_document(doc_src, threshold, output):
    """Runs all the required components of the cli on a given document file"""
    return run_cli(threshold=threshold, output=output, doc_src=doc_src)


def run_cli(*,
            threshold=0.8,
            ignore_classifiers=False,
            repo_url=None,
            ignore_github_metadata=False,
            readme_only=False,
            doc_src=None,
            local_repo=None,
            in_file=None,
            output=None,
            graph_out=None,
            graph_format="turtle",
            codemeta_out=None,
            pretty=False,
            missing=False,
            keep_tmp=None
            ):
    """Function to run all the required components of the cli for a repository"""
    # check if it is a valid url
    if repo_url:
        if not validators.url(repo_url):
            logging.error("Not a valid repository url. Please check the url provided")
            return None
    multiple_repos = in_file is not None
    if multiple_repos:
        with open(in_file, "r") as in_handle:
            # get the line (with the final newline omitted) if the line is not empty
            repo_list = [line[:-1] for line in in_handle if len(line) > 1]

        # convert to a set to ensure uniqueness (we don't want to get the same data multiple times)
        repo_set = set(repo_list)
        # check if the urls in repo_set if are valid
        remove_urls = []
        for repo_elem in repo_set:
            if not validators.url(repo_elem):
                logging.error("Not a valid repository url. Please check the url provided: " + repo_elem)
                remove_urls.append(repo_elem)
        # remove non valid urls in repo_set
        for remove_url in remove_urls:
            repo_set.remove(remove_url)
        if len(repo_set) > 0:
            repo_data = [cli_get_data(threshold=threshold, ignore_classifiers=ignore_classifiers, repo_url=repo_url,
                                      keep_tmp=keep_tmp) for repo_url in repo_set]
        else:
            return None

    else:
        if repo_url:
            repo_data = cli_get_data(threshold=threshold, ignore_classifiers=ignore_classifiers, repo_url=repo_url,
                                     ignore_github_metadata=ignore_github_metadata, readme_only=readme_only,
                                     keep_tmp=keep_tmp)
        elif local_repo:
            repo_data = cli_get_data(threshold=threshold, ignore_classifiers=ignore_classifiers,
                                     local_repo=local_repo, keep_tmp=keep_tmp)
        else:
            repo_data = cli_get_data(threshold=threshold, ignore_classifiers=ignore_classifiers,
                                     doc_src=doc_src, keep_tmp=keep_tmp)

    if output is not None:
        json_export.save_json_output(repo_data.results, output, missing, pretty=pretty)

    if graph_out is not None:
        logging.info("Generating triples...")
        data_graph = DataGraph()
        if multiple_repos:
            for repo in repo_data:
                data_graph.somef_data_to_graph(repo.results)
        else:
            data_graph.somef_data_to_graph(repo_data.results)

        data_graph.export_to_file(graph_out, graph_format)

    if codemeta_out is not None:
        json_export.save_codemeta_output(repo_data.results, codemeta_out, pretty=pretty)
