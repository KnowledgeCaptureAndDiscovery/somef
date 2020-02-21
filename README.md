# SM2KG
Software Metadata 2 Knowledge Graphs: A tool for automatically extracting relevant information from readme files

Installation Instructions - 

`pip3 install -r requirements.txt`

Create a config.json file using the sample file in the repository.

Command Line Interface - 

createJSON.py generates a JSON object after extracting useful information from the github repository. It classifies the readme file into one of four categories - description, invocation, installation, citation depending on highest confidence above a given threshold.

The createJSON.py file takes as input the following parameters:

-r / --repo_url: Link to the github repository for extracting information

-m / --model_path: Path to the pickled models for extraction

-o / --output: Output file name

-t / --threshold: Threshold to classify the content of the readme file

-d / --doc_src: Path of documentation file


cli.py generates a JSON object after extracting useful information from the github repository. It classifies the readme file into one of four categories - description, invocation, installation, citation depending on confidence above a given threshold.

The cli.py file takes as input the following parameters:

-r / --repo_url: Link to the github repository for extracting information

-o / --output: Output file name

-t / --threshold: Threshold to classify the content of the readme file

-d / --doc_src: Path of documentation file

Example:

`python3 createJSON.py -r https://github.com/{owner}/{repository_name} -m ./models/ -o output.json -t 0.5`

`python3 cli.py -r https://github.com/{owner}/{repository_name} -o output.json -t 0.5`
