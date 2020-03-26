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
from cli import run_cli

__DEFAULT_SOMEF_CONFIGURATION_FILE__ = "~/.somef/config.json"
# __DEFAULT_SOMEF_CONFIGURATION_FILE__ = "/Users/vedantdiwanji/Desktop/SM2KG/trial.json"

@click.command(help="Configure credentials")
def configure():
    authorization = click.prompt("Authorization",default="")
    description = click.prompt("Documentation model file")
    invocation = click.prompt("Invocation model file")
    installation = click.prompt("Installation model file")
    citation = click.prompt("Citation model file")

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

@click.command(help="Running the Command Line Interface")
def cli():
	github_url = click.prompt("Github URL")
	threshold = click.prompt("Threshold",type=float)
	output_file_path = click.prompt("Output File Path")
	run_cli(github_url,threshold,output_file_path)
	click.secho(f"Success", fg="green")


if __name__=='__main__':
	cli()