# SM2KG
Software Metadata 2 Knowledge Graphs: A tool for automatically extracting relevant information from readme files

Command Line Interface - 

createJSON.py generates a JSON object after extracting useful information from the github repository. It classifies the readme file into one of four categories - description, invocation, installation, citation depending on highest confidence above a given threshold.

The createJSON.py file takes as input the following parameters:

--repo_url: Link to the github repository for extracting information

-m: Path to the pickled models for extraction

-o: Output file name

-t: threshold to classify the content of the readme file

Example:

`python3 createJSON.py --repo_url https://github.com/{owner}/{repository_name} -m ./models/ -o output.json -t 0.5`
