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
