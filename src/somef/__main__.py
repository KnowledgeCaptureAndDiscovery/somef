# -*- coding: utf-8 -*-
"""
somef.
:license: Apache 2.0
"""

import configparser
import sys
from pathlib import Path
import click
from click_option_group import optgroup, RequiredMutuallyExclusiveOptionGroup, RequiredAnyOptionGroup
import somef
from . import configuration


@click.group(context_settings={'help_option_names':['-h','--help']})
def trycli():
    print("SOMEF Command Line Interface")

@trycli.command(help="Configure credentials")
def configure():
    authorization = click.prompt("Authorization",default="")
    description = click.prompt("Documentation model file", default=configuration.default_description)
    invocation = click.prompt("Invocation model file", default=configuration.default_invocation)
    installation = click.prompt("Installation model file", default=configuration.default_installation)
    citation = click.prompt("Citation model file", default=configuration.default_citation)

    configuration.configure(authorization, description, invocation, installation, citation)
    click.secho(f"Success", fg="green")

@trycli.command(help="Show somef version.")
def version(debug=False):
    click.echo(f"{Path(sys.argv[0]).name} v{somef.__version__}")


class URLParamType(click.types.StringParamType):
    name = "url"

@trycli.command(help="Running the Command Line Interface")
@click.option(
    "--threshold",
    "-t",
    type=float,
    help="Threshold to classify the text",
    required=True,
    default=0.8,
)
@optgroup.group('Input', cls=RequiredMutuallyExclusiveOptionGroup)
@optgroup.option(
    "--repo_url",
    "-r",
    type=URLParamType(),
    help="Github Repository URL",
)
@optgroup.option(
    "--doc_src",
    "-d",
    type=click.Path(exists=True),
    help="Path to the README file source"
)
@optgroup.option(
    "--in_file",
    "-i",
    type=click.Path(exists=True),
    help="A file of newline separated links to GitHub repositories"
)
@optgroup.group('Output', cls=RequiredAnyOptionGroup)
@optgroup.option(
    "--output",
    "-o",
    type=click.Path(),
    help="Path to the output file. If supplied, the output will be in JSON",
)
@optgroup.option(
    "--graph_out",
    "-g",
    type=click.Path(),
    help="""Path to the output Knowledge Graph file. If supplied, the output will be a Knowledge Graph,
            in the format given in the --format option"""
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
def describe(**kwargs):
    from somef import cli
    cli.run_cli(**kwargs)
    click.secho(f"Success", fg="green")


if __name__ == '__main__':
    version()
