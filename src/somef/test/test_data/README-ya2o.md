# ya2ro

## Demo

<https://oeg-upm.github.io/ya2ro/output/landing_page.html>

## Installation

To run ya2ro, please follow the next steps:

### Install from PyPI

```text
pip install ya2ro
```

### Install from GitHub

```text
git clone https://github.com/oeg-upm/ya2ro
cd ya2ro
pip install -e .
```

### Installing through Docker

We provide a Dockerfile with ya2ro already installed. To run through Docker, you may build the Dockerfile provided in the repository by running:

```bash
docker build -t ya2ro .
```

Then, to run your image just type:

```bash
docker run -it ya2ro /bin/bash
```

And you will be ready to use ya2ro (see section below). If you want to have access to the results we recommend [mounting a volume](https://docs.docker.com/storage/volumes/). For example, the following command will mount the current directory as the `out` folder in the Docker image:

```bash
docker run -it --rm -v $PWD/:/out ya2ro /bin/bash
```

If you move any files produced by ya2ro into `/out`, then you will be able to see them in your current directory.

## Usage

### Configure

Before running ya2ro, you must configure it appropriately. Run:

```bash
ya2ro -configure GITHUB_PERSONAL_ACCESS_TOKEN
```

or

```bash
ya2ro -c GITHUB_PERSONAL_ACCESS_TOKEN
```

### Test ya2ro installation

```bash
ya2ro --help
```

If everything goes fine, you should see:

```text
                        ad888888b,
                       d8"     "88
                               a8P
8b       d8 ,adPPYYba,      ,d8P"  8b,dPPYba,  ,adPPYba,
`8b     d8' ""     `Y8    a8P"     88P'   "Y8 a8"     "8a
 `8b   d8'  ,adPPPPP88  a8P'       88         8b       d8
  `8b,d8'   88,    ,88 d8"         88         "8a,   ,a8"
    Y88'    `"8bbdP"Y8 88888888888 88          `"YbbdP"'
    d8'
   d8'
_________________________________________________________

usage: ya2ro [-h] (-i YALM_PATH | -c GITHUB_PERSONAL_ACCESS_TOKEN | -l YA2RO_PREV_OUTPUT) [-o OUTPUT_DIR] [-p PROPERTIES_FILE] [-ns]

Human and machine readable input as a yaml file and create RO-Object in jsonld and/or HTML view. Run 'ya2ro -configure GITHUB_PERSONAL_ACCESS_TOKEN' this the first time to configure ya2ro
properly

options:
  -h, --help            show this help message and exit
  -i YALM_PATH, --input YALM_PATH
                        Path of the required yaml input. Follow the documentation or the example given to see the structure of the file.
  -c GITHUB_PERSONAL_ACCESS_TOKEN, --configure GITHUB_PERSONAL_ACCESS_TOKEN
                        Insert Github personal access token. Run this the first time to configure ya2ro properly.
  -l YA2RO_PREV_OUTPUT, --landing_page YA2RO_PREV_OUTPUT
                        Path of a previous output folder using the ya2ro tool. This flag will make a landing page to make all the resources accesible.
  -o OUTPUT_DIR, --output_directory OUTPUT_DIR
                        Output diretory.
  -p PROPERTIES_FILE, --properties_file PROPERTIES_FILE
                        Properties file name.
  -ns, --no_somef       Disable SOMEF for a faster execution (software cards will not work).

```

---

### How to use  

The first thing to do is create some input for ya2ro. To create valid a yalm you should follow the documentation bellow.

Create a yalm from scratch or use one of the supplied templates. Currently ya2ro supports two formats:

* paper
* project

Please find a template for each type under the directory templates.
Once you have a valid yalm (proyect or paper) is time to run ya2ro.

#### Create machine and human readable content

It is possible to process batches of yalms at the same time, to do that just specify as input a folder with all the yalms inside.

##### Simple execution

`ya2ro -i templates`  

`ya2ro -i templates/project_yemplate.yaml`

##### With optional arguments

`ya2ro -input templates --output_directory out --properties_file custom_properties.yaml`  

`ya2ro -i templates -o out -p custom_properties.yaml`

##### Faster execution?

Use the flag --no_somef or -ns for disabling SOMEF which is the most time consuming process.

`ya2ro -i templates -ns`

WARNING: Software cards will no longer work on github links. Therefore you will need to manually insert the software data in the yaml file.

#### Create landing page

ya2ro offers the option to create a landing page where all the resources produced are easilly accesible. Just indicate the folder where this resources are, for example:

`ya2ro -l output`

---

#### Fields supported

#### Paper

Documentation for all supported fields for type paper.

`type:`This field is required and is used to indicate the type of the work.

```yaml
type: "paper"
```

`doi_paper:`All the relevant information of the paper will be retrieved. Such as:

* Title
* Summary
* Bibtext
* Citation/Bibliography
* Authors

```yaml
doi_paper: https://doi.org/xxxxxxxxx
```

`title:`Title of the paper.

```yaml
title: "Paper - Template"
```

`summary:`A brief summary of the paper, also known as an abstract.

```yaml
summary: "This is a summary of the paper."
```

`datasets:` All the datasets used and created during the paper. This tool supports to define each dataset manually specifying all fields or to use a DOI and ya2ro will try to automatically fetch the data.

```yaml
datasets:
  - 
    doi: www.doiDB1.com
  - 
    link: www.D1.com 
    name: "Dataset 1"
    description: "Description dataset 1"
    license: "MIT-License"
    author: "Author name"
-
    path: templates/datasets
    name: "Dataset name"
    author: "Author name"
    description: "Description of a local dataset"
```

`software:` All the relevant software used and created for the paper. If a GitHub Repo is provided ya2ro will use SOMEF to automatically fetch relevant data.

```yaml
software:
  -
    link: https://github.com/KnowledgeCaptureAndDiscovery/somef/
  - 
    link: http://software_1.com 
    name: "Software 1"
    description: "Description software 1"
    license: "MIT-License"
```

`bibliography:`In this field is where the bibliography can be added. Also a doi can be used and the bibliography entry will be fetch automatically.

```yaml
bibliography:
  - "Bibliography entry 1"
  - "Bibliography entry 2"
  - "Bibliography entry 3"
  - https://doi.org/XXXXXXXXX
```

`authors:`In this field is where credit to the creators, collaborators, authors, etc is given. If an ORCID is privided, ya2ro will fetch relevant data automatically. If a photo is not provided, a default one will be used.

```yaml
authors:
    -
      orcid: https://orcid.org/0000-0003-0454-7145
      role: "Coordinator"
    -
      name: "Author"
      position: "Author's position"
      description: "Author's description"
      web: https://author-web.com/
      photo: "author_photo.jpg"
```

---

#### Project

Documentation for all supported fields for type project.

`type:`This field is required and is used to indicate the type of the work.

```yaml
type: "project"
```

`title:`Title of the project.

```yaml
title: "Project - Template"
```

`goal:`In this field you should inlcude the goal for the project.

```yaml
goal: "Here is where a description of what is this project trying to achieve."
```

`social_motivation:`In this field you should include why this project will help in a social way.

```yaml
social_motivation: "This is the social motivation behind this project."
```

`sketch:`Path to an image where a visual description/workflow is shown.

```yaml
sketch: "images/sketch_ya2ro.jpg"
```

`areas:`All the areas involucrated inside this project.

```yaml
areas: 
  - "Area 1: Some description."
  - "Area 2: Some description."
```

`activities:`All the idividual subtasks of the project.

```yaml
activities:
  - "Subtask 1: Some description."
  - "Subtask 2: Some description."
```

`demo:`Link or links to demos of the project.

```yaml
demo: 
  -
    link: http://demo.com
    description: "This is a description for a demo."
  -
    name: "Demo name"
    link: http://demo.com
    description: "This is a description for a demo with name."
```

`datasets:` All the datasets used and created during the paper. This tool supports to define each dataset manually specifying all fields or to use a DOI and ya2ro will try to automatically fetch the data.

```yaml
datasets:
  - 
    doi: www.doiDB1.com
  - 
    link: www.D1.com 
    name: "Dataset 1"
    description: "Description dataset 1"
    license: "MIT-License"
    author: "Author name"
  -
    path: templates/datasets
    name: "Dataset name"
    author: "Author name"
    description: "Description of a local dataset"
```

`software:` All the relevant software used and created for the paper. If a GitHub Repo is provided, ya2ro will use SOMEF to automatically fetch relevant data.

```yaml
software:
  -
    link: https://github.com/KnowledgeCaptureAndDiscovery/somef/
  - 
    link: http://software_1.com 
    name: "Software 1"
    description: "Description software 1"
    license: "MIT-License"
```

`bibliography:`In this field is where the bibliography can be added. Also a doi can be used and the bibliography entry will be fetch automatically.

```yaml
bibliography:
  - "Bibliography entry 1"
  - "Bibliography entry 2"
  - "Bibliography entry 3"
  - https://doi.org/XXXXXXXXX
```

`authors:`In this field is where credit to the creators, collaborators, authors, etc is given. If an ORCID is privided ya2ro will fetch relevant data automatically. If a photo is not provided, a default one will be used.

```yaml
participatns:
    -
      orcid: https://orcid.org/0000-0003-0454-7145
      role: "Coordinator"
    -
      name: "Author"
      position: "Author's position"
      description: "Author's description"
      web: https://author-web.com/
      photo: "author_photo.jpg"
```

`contact:`In this field you can add some contact information.

```yaml
contact:
  email: contact@projectmail.com
  phone: +34 999 999 999
```
