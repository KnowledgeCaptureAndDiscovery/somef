# -*- coding: utf-8 -*-
"""
somef.
:license: Apache 2.0
"""

import configparser
import os
import sys
from pathlib import Path
import json
import click
import somef
from somef import cli

__DEFAULT_SOMEF_CONFIGURATION_FILE__ = "~/.somef/config.json"
# __DEFAULT_SOMEF_CONFIGURATION_FILE__ = "/Users/vedantdiwanji/Desktop/SM2KG/trial.json"


@click.group(context_settings={'help_option_names':['-h','--help']})
def trycli():
    print("SOMEF Command Line Interface")

@trycli.command(help="Configure credentials")
def configure():
    path = Path(__file__).parent.absolute()
    authorization = click.prompt("Authorization",default="")
    description = click.prompt("Documentation model file", default=str(path)+"/models/description.sk")
    invocation = click.prompt("Invocation model file", default=str(path)+"/models/invocation.sk")
    installation = click.prompt("Installation model file", default=str(path)+"/models/installation.sk")
    citation = click.prompt("Citation model file", default=str(path)+"/models/citation.sk")

    credentials_file = Path(
        os.getenv("SOMEF_CONFIGURATION_FILE", __DEFAULT_SOMEF_CONFIGURATION_FILE__)
    ).expanduser()
    os.makedirs(str(credentials_file.parent), exist_ok=True)

    # credentials_file = Path(os.getenv("SOMEF_CONFIGURATION_FILE", __DEFAULT_SOMEF_CONFIGURATION_FILE__)).expanduser()

    if credentials_file.exists():
        with credentials_file.open("r") as fh:
            data = json.load(fh)


    data = {
        "Authorization": "token "+authorization,
        "description": description,
        "invocation": invocation,
        "installation": installation,
        "citation": citation,
    }

    if data['Authorization']=="token ":
    	del data['Authorization']
    
    with credentials_file.open("w") as fh:
        credentials_file.parent.chmod(0o700)
        credentials_file.chmod(0o600)
        json.dump(data, fh) 
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
def describe(repo_url,threshold,output):
    cli.run_cli(repo_url,threshold,output)
    click.secho(f"Success", fg="green")


if __name__=='__main__':
	version()