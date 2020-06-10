# -*- coding: utf-8 -*-
"""
somef.
:license: Apache 2.0
"""

import configparser
import sys
from pathlib import Path
import click
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

@trycli.command(help="Running the Command Line Interface")
@click.option(
    "--repo_url",
    "-r",
    type=str,
    help="Github Repository URL",
    required=True,
)
@click.option(
    "--threshold",
    "-t",
    type=float,
    help="Threshold to classify the text",
    required=True,
    default=0.8,
)
@click.option(
    "--output",
    "-o",
    type=str,
    help="Path to the output file",
    required=True,
    default="output.json"
)
@click.option(
    "--graph_out",
    "-g",
    type=str,
    help="Optional path to a turtle file",
    required=False
)
def describe(repo_url, threshold, output, graph_out):
    from somef import cli
    cli.run_cli(repo_url,threshold,output,graph_out=graph_out)
    click.secho(f"Success", fg="green")


if __name__=='__main__':
	version()
