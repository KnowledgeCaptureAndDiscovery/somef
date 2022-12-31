# -*- coding: utf-8 -*-

import os

from setuptools import find_packages, setup

install_requires = [
    "bs4==0.0.1",
    "Click==7.0",
    "click-option-group==0.5.3",
    "markdown==3.3.6",
    "matplotlib==3.5.0",
    "nltk==3.6.6",
    "numpy==1.22.0",
    "pandas==1.3.4",
    "rdflib>=6.0.2",
    "rdflib-jsonld==0.6.2",
    "requests>=2.22.0",
    "scikit-learn==1.0",
    "textblob==0.17.1",
    "validators==0.18.2",
    "xgboost==1.5.0",
    "scipy>=1.7.1",
    "inflect>=5.4.0",
    "contractions>=0.1.66",
    "chardet==5.0.0",
    "imbalanced-learn>=0.8.1",
    "pytest",
    "morph-kgc>=2.3.1"
]


# Utility function to read the README file.
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname), encoding='utf-8').read()


def find_package_data(dirname):
    def find_paths(dirname):
        items = []
        for fname in os.listdir(dirname):
            path = os.path.join(dirname, fname)
            if os.path.isdir(path):
                items += find_paths(path)
            elif not path.endswith(".py") and not path.endswith(".pyc"):
                items.append(path)
        return items

    items = find_paths(dirname)
    return [os.path.relpath(path, dirname) for path in items]


version = {}
with open("src/somef/__init__.py") as fp:
    exec(fp.read(), version)

# Original setup created by Vedant Diwanji
setup(
    name="somef",
    version=version["__version__"],
    author="Daniel Garijo",
    author_email="daniel.garijo@upm.es",
    description="SOftware Metadata Extraction Framework: A tool for automatically extracting relevant software information from readme files",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/KnowledgeCaptureAndDiscovery/somef",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.9",
        "Intended Audience :: Science/Research",
        "Operating System :: Unix",
    ],
    entry_points={"console_scripts": ["somef = somef.__main__:cli"]},
    package_dir={"": "src"},
    packages=find_packages(where="src", exclude=["somef.tests*"]),
    package_data={"somef": find_package_data("src/somef")},
    exclude_package_data={"somef": ["test/*"]},
    zip_safe=False,
    install_requires=install_requires,
    python_requires=">=3.9",
)
