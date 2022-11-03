# -*- coding: utf-8 -*-

import click
from click_option_group import optgroup, RequiredMutuallyExclusiveOptionGroup, RequiredAnyOptionGroup

from . import configuration, constants
from . import __version__


class URLParamType(click.types.StringParamType):
    name = "url"


@click.group(context_settings={'help_option_names': ['-h', '--help']})
@click.version_option(__version__)
def cli():
    click.echo("SOftware Metadata Extraction Framework (SOMEF) Command Line Interface")


@cli.command(help="Configure GitHub credentials and classifiers file path")
@click.option('-a', '--auto', help="Automatically configure SOMEF", is_flag=True, default=False)
@click.option('-b', '--base_uri', type=URLParamType(), help="Base URI for somef transformations",
              default=constants.CONF_DEFAULT_BASE_URI)
def configure(auto, base_uri):
    if auto:
        click.echo(
            "Configuring SOMEF automatically. To assign credentials edit the configuration file or run "
            "the interactive mode")
        configuration.configure()
    elif base_uri is not constants.CONF_DEFAULT_BASE_URI:
        configuration.update_base_uri(base_uri)
    else:
        authorization = click.prompt("Authorization", default="")
        description = click.prompt("Documentation classifier model file", default=configuration.default_description)
        invocation = click.prompt("Invocation classifier model file", default=configuration.default_invocation)
        installation = click.prompt("Installation classifier model file", default=configuration.default_installation)
        citation = click.prompt("Citation classifier model file", default=configuration.default_citation)
        base_uri = click.prompt("Base URI for RDF generation", default=base_uri)
        # configuration.configure()
        configuration.configure(authorization, description, invocation, installation, citation, base_uri)
    click.secho(f"Success", fg="green")


@cli.command(help="Running SOMEF Command Line Interface")
@click.option(
    "--threshold",
    "-t",
    type=float,
    help="Threshold to classify the text",
    required=True,
    default=0.8,
)
@click.option(
    "--ignore_classifiers",
    "-ic",
    is_flag=True,
    default=False,
    help="Flag to ignore running the classifiers (by default False)"
)
@click.option(
    "--ignore_github_metadata",
    "-igm",
    is_flag=True,
    default=False,
    help="Flag to ignore Github Metadata (by default False)"
)
@click.option(
    "--readme_only",
    "-ro",
    is_flag=True,
    default=False,
    help="Flag to retrieve only the README.md file from the Github/Gitlab Repository URL. If such file does not exist, "
         "no metadata will be retrieved (by default False)"
)
@optgroup.group('Input', cls=RequiredMutuallyExclusiveOptionGroup)
@optgroup.option(
    "--repo_url",
    "-r",
    type=URLParamType(),
    help="Github/Gitlab Repository URL",
)
@optgroup.option(
    "--doc_src",
    "-d",
    type=click.Path(exists=True),
    help="Path to the README file source"
)
@optgroup.option(
    "--local_repo",
    "-l",
    type=click.Path(exists=True),
    help="Path to local repository"
)
@optgroup.option(
    "--in_file",
    "-i",
    type=click.Path(exists=True),
    help="A file of newline separated links to GitHub/Gitlab repositories to process in bulk"
)
@optgroup.group('Output', cls=RequiredAnyOptionGroup)
@optgroup.option(
    "--output",
    "-o",
    type=click.Path(),
    help="Path to the output file. If supplied, the output will be in JSON",
)
@optgroup.option(
    "--codemeta_out",
    "-c",
    type=click.Path(),
    help="Path to an output codemeta file"
)
@optgroup.option(
    "--graph_out",
    "-g",
    type=click.Path(),
    help="""Path to the output Knowledge Graph export file. If supplied, the output will be a Knowledge Graph,
            in the format given in the --format option chosen (turtle, json-ld)"""
)
@click.option(
    "--graph_format",
    "-f",
    type=click.Choice(["turtle", "json-ld"]),
    default="turtle",
    help="""If the --graph_out option is given, this is the format that the graph will be stored in"""
)
@click.option(
    "--pretty",
    "-p",
    is_flag=True,
    default=False,
    help="""Pretty print the JSON output file so that it is easy to compare to another JSON output file."""
)
@click.option(
    "--missing",
    "-m",
    is_flag=True,
    default=False,
    help="""The JSON will include a category missingCategories to report with the missing metadata fields SOMEF was not 
    able to find. """
)
@click.option(
    "--keep_tmp",
    "-kt",
    type=click.Path(),
    help="""SOMEF will NOT delete the temporary folder where files are stored for analysis. Files will be stored at the
    desired path"""
)
def describe(**kwargs):
    from . import cli
    cli.run_cli(**kwargs)
    click.secho(f"Success", fg="green")
