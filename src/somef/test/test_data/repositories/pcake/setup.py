import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="pcake",
    version="0.0.3",
    description="Compare numeric properties from SPARQL endpoints",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/oeg-upm/pcake",
    author="Ahmad Alobaid",
    author_email="aalobaid@fi.upm.es",
    license="Apache2",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["pcake"],
    include_package_data=True,
    install_requires=["numpy", "pandas", "six", "seaborn"]
)