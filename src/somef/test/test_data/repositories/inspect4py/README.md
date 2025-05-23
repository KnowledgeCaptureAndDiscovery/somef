# inspect4py 
[![PyPI](https://badge.fury.io/py/inspect4py.svg)](https://badge.fury.io/py/inspect4py) [![DOI](https://zenodo.org/badge/349160905.svg)](https://zenodo.org/badge/latestdoi/349160905) [![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)

<img src="docs/images/logo.png" alt="logo" width="200"/>

Library to allow users inspect a software project folder (i.e., a directory and its subdirectories) and extract all the most relevant information, such as class, method and parameter documentation, classes (and their methods), functions, etc.

## Features:

Given a folder with code, `inspect4py` will:

- Extract all imported modules and how each module is imported as (i.e., whether they are internal or external).
- Extract all functions in the code, including their documentation, parameters, accepted values, and call list.
- Extract all classes in the code, with all their methods and respective documentation
- Extract the control flow of each file.
- Extract the hierarchy of directories and files.
- Extract the requirements used in the software project.
- Classify which files are tests
- Classify the main type of software project (script, package, library or service). Only one type is returned as main type (e.g., if a library has the option to be deployed as a service, `inspect4py` will return `Library` as its main type)
- Return a ranking of the different ways in which a a software component can be run, ordered by relevance.


All metadata is extracted as a JSON file.


Inspect4py currently works **only for Python 3 projects**.

## Background:

`inspect4py` added the functionality of capture [Data Flow Graphs](http://bears.ece.ucsb.edu/research-info/DP/dfg.html) for each function inspired by GraphCodeBERT: [Github](https://github.com/microsoft/CodeBERT) & [Paper](https://arxiv.org/abs/2009.08366). The illustration is given:
|Source Code|List Output|Networkx Image|
|:-:|:-:|:-:|
|<pre>def max(a, b):<br>x = 0<br>    if a > b:<br>    x = a<br>else:<br>    x = b<br>    return x</pre>|<pre>('a', 3, 'comesFrom', [], [])<br>('b', 5, 'comesFrom', [], [])<br>('x', 8, 'computedFrom', ['0'], [10])<br>('0', 10, 'comesFrom', [], [])<br>('a', 12, 'comesFrom', ['a'], [3])<br>('b', 14, 'comesFrom', ['b'], [5])<br>('x', 16, 'computedFrom', ['a'], [18])<br>('a', 18, 'comesFrom', ['a'], [3])<br>('x', 21, 'computedFrom', ['b'], [23])<br>('b', 23, 'comesFrom', ['b'], [5])<br>('x', 25, 'comesFrom', ['x'], [16, 21])</pre>|![image](docs/images/data_flow.png)|

`inspect4py` uses [ASTs](https://en.wikipedia.org/wiki/Abstract_syntax_tree), more specifically
the [ast](https://docs.python.org/3/library/ast.html) module in Python, generating
a tree of objects (per file) whose classes all inherit from [ast.AST](https://docs.python.org/3/library/ast.html#ast.AST).

`inspect4py` parses each of the input file(s) as an AST tree, extracting the relevant information and storing it as a JSON file.  Furthermore, it also captures the control flow of each input file(s), by using another two libraries:

- [staticfg](inspect4py/staticfg): StatiCFG is a package that can be used to produce control flow graphs (CFGs) for Python 3 programs. The CFGs it generates can be easily visualised with graphviz and used for static analysis. We have a flag in the code (FLAG_PNG) to indicate if we want to generate this type of control flow graphs or not. **Note**: The original code of this package can be found [here](https://github.com/coetaur0/staticfg), which has been fixed it in our [repository](inspect4py/staticfg)  

We also use [docstring_parser](https://pypi.org/project/docstring-parser/), which has support for  ReST, Google, and Numpydoc-style docstrings. Some (basic) tests done using this library can be found at [here](./test_docstring_parser/).

Finally, we reuse [Pigar](https://github.com/damnever/pigar) for generating automatically the requirements of a given repository. This is an optional funcionality. In order to activate the argument (`-r`) has to be indicated when running inspect4py.  

## Cite inspect4py
Please cite our MSR 2022 demo paper:
```
@inproceedings{FilgueiraG22,
  author    = {Rosa Filgueira and
               Daniel Garijo},
  title     = {Inspect4py: {A} Knowledge Extraction Framework for Python Code Repositories},
  booktitle = {{IEEE/ACM} 19th International Conference on Mining Software Repositories,
               {MSR} 2022, Pittsburgh, PA, USA, May 23-24, 2022},
  pages     = {232--236},
  publisher = {{IEEE}},
  year      = {2022},
  url       = {https://dgarijo.com/papers/inspect4py_MSR2022.pdf},
  doi       = {10.1145/3524842.3528497}
}
```

## Install

### Preliminaries

Make sure you have tree-sitter installed, C complier is needed, more [info](https://github.com/tree-sitter/tree-sitter):

```
pip install tree-sitter
```
Note that if the ".so" file is not working properly, it is recommended that run the following commeds to generate a so file for your OS:
```
git clone https://github.com/tree-sitter/tree-sitter-python

python inspect4py/build.py
```

Make sure you have graphviz installed:

```
sudo apt-get install graphviz
```

### Python version
We have tested `inspect4py` in Python 3.7+. **Our recommended version is Python 3.9**.


### Operative System
We have tested `inspect4py` in Unix, MacOS and Windows 11(22621.1265).

### Installation from pypi
`inspect4py` is [available in pypi!](https://pypi.org/project/inspect4py/) Just install it like a regular package:

```
pip install inspect4py
```

You are done!

Then try to update the python-dev utilities: `sudo apt-get install python3.X-dev` (where X is your python version)

### Installation from code

Prepare a virtual Python3 enviroment, `cd` into the `inspect4py` folder and install the package as follows:

```
git clone https://github.com/SoftwareUnderstanding/inspect4py
cd inspect4py
pip install -e .
```

You are done!

### Package dependencies:
```
docstring_parser==0.7
astor
graphviz
click
pigar
setuptools==54.2.0
json2html
configparser
bigcode_astgen
GitPython
tree-sitter
```

If you want to run the evaluations, do not forget to add `pandas` to the previous set.

### Installation through Docker

You need to have [Docker](https://docs.docker.com/get-started/) installed.

Next, clone the `inspect4py` repository:

```
git clone https://github.com/SoftwareUnderstanding/inspect4py/
```

Generate a Docker image for `inspect4py`:

```
docker build --tag inspect4py:1.0 .
```

Run the `inspect4py` image:

```
docker run -it --rm inspect4py:1.0 /bin/bash
```

Now you can run `inspect4py`:
```
root@e04792563e6a:/# inspect4py --help
```

For more information about `inspect4py` execution options, please see the section below (Execution).

Note that when running `inspect4py` with Docker, you will need to need to provide a path to the target repository to analyze. You can do this by:

1. Cloning the target repository. For example:

```
docker run -it --rm inspect4py:1.0 /bin/bash
# Docker image starts
root@e04792563e6a:/# git clone https://github.com/repo/id
root@e04792563e6a:/# inspect4py -i id
```
2. Creating a [volume](https://docs.docker.com/storage/volumes/). For example, for mounting the $PWD folder:

```
docker run -it -v -v $PWD:/out --rm inspect4py:1.0 /bin/bash
# Docker image starts
root@e04792563e6a:/# inspect4py -i /out/path/to/repo
```

Other useful commands when using Docker:
```
docker cp [OPTIONS] CONTAINER:SRC_PATH DEST_PATH|-
docker image rm -f inspect4py:1.0
```

## Execution

The tool can be executed to inspect a file, or all the files of a given directory (and its subdirectories).
For example, it can be used to inspect all the python files of a given GitHub repository (that has been previously cloned locally).

The tool by default stores the results in the `OutputDir` directory, but users can specify their own directory name by using `-o` or `--output` flags.


```
inspect4py --input_path <FILE.py | DIRECTORY> [--output_dir "OutputDir", --ignore_dir_pattern "__", ignore_file_pattern "__" --requirements --html_output]
```

For clarity, we have added a `help` command to explain each input parameter:

```
inspect4py --help


Usage: inspect4py [OPTIONS]

Options:
  --version                       Show the version and exit.
  -i, --input_path TEXT           input path of the file or directory to
                                  inspect.  [required]
  -o, --output_dir TEXT           output directory path to store results. If
                                  the directory does not exist, the tool will
                                  create it.
  -ignore_dir, --ignore_dir_pattern TEXT
                                  ignore directories starting with a certain
                                  pattern. This parameter can be provided
                                  multiple times to ignore multiple directory
                                  patterns.
  -ignore_file, --ignore_file_pattern TEXT
                                  ignore files starting with a certain
                                  pattern. This parameter can be provided
                                  multiple times to ignore multiple file
                                  patterns.
  -r, --requirements              find the requirements of the repository.
  -html, --html_output            generates an html file of the DirJson in the
                                  output directory.
  -cl, --call_list                generates the call list in a separate html
                                  file.
  -cf, --control_flow             generates the call graph for each file in a
                                  different directory.
  -dt, --directory_tree           captures the file directory tree from the
                                  root path of the target repository.
  -si, --software_invocation      generates which are the software
                                  invocation commands to run and test the
                                  target repository.
  -ast, -—abstract_syntax_tree    generates abstract syntax tree in json format.
  -sc, --source_code              generates source code of each ast node.
  -ld, --license_detection        detects the license of the target repository.
  -rm, --readme                   extract all readme files in the target repository.
  -md, --metadata                 extract metadata of the target repository using
                                  Github API.
  -df, --data_flow                extract data flow graph for every function, BOOL
  -st, --symbol_table             symbol table file location. STR
  --help                          Show this message and exit.
```

## Documentation

For additional documentation and examples, please have a look at our [online documentation](https://inspect4py.readthedocs.io/en/latest/)

## Contribution guidelines
Contributions to address any of the current issues are welcome. In order to push your contribution, just **push your pull request to the development branch (`dev`)**. The master branch has only the code associated to the latest release. 

## Acknowledgements

We would like to thank Laura Camacho, designer of the logo