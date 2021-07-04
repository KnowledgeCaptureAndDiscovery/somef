# -*- coding: utf-8 -*-

import os

from setuptools import find_packages, setup

install_requires = [
    "Click",
    "click-option-group",
    "requests",
    "markdown",
    "requests",
    "bs4",
    "matplotlib",
    "nltk",
    "numpy",
   # "scikit-learn==0.21.2",
    "scikit-learn==0.24.2",
    "scikit-learn",
    "pandas",
    "textblob",
    "rdflib",
    "rdflib-jsonld"
]


# Utility function to read the README file.
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


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
    author_email="dgarijo@isi.edu",
    description=__doc__,
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/KnowledgeCaptureAndDiscovery/somef",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
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
    python_requires=">=3.6.0",
)
