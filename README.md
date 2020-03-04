# SM2KG
Software Metadata 2 Knowledge Graphs: A tool for automatically extracting relevant information from readme files

Installation Instructions - 

`pip3 install -r requirements.txt`

Configuration:

Create a config.json file using the sample file in the repository.

Path to the corresponding Model files are provided as shown in the sample config file.

Optional Authentication:

Add the following line to the config.json to add Authentication for requests to github repository:

`"Authentication": "token PersonalAccessToken"`

Information on generating Personal Access Token - https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line

Command Line Interface - 

cli.py generates a JSON object after extracting useful information from the github repository. It classifies the readme file into one of four categories - description, invocation, installation, citation depending on confidence above a given threshold.

The cli.py file takes as input the following parameters:

-r / --repo_url: Link to the github repository for extracting information

-o / --output: Output file name

-t / --threshold: Threshold to classify the content of the readme file

-d / --doc_src: Path of documentation file

Add/Remove a Category:

If user wants to run the classifier for an additional category or wants to remove an existing category, corresponding path entry in the config.json should be provided and the category type should be added/removed in the category variable in the cli.py

Github Repository Metadata:

In addition to the classified readme file, the metadata from the repository to be shown in the application is part of the keep_keys variable. If more information is to be added/removed then it should be added/removed to the keep_keys variable. 

Example:

`python3 cli.py -r https://github.com/{owner}/{repository_name} -o output.json -t 0.5`
