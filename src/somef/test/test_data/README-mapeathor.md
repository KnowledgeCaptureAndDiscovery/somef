 [![Generic badge](https://img.shields.io/badge/Status-Developing-yellow)](https://shields.io/)
 [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/oeg-upm/Mapeathor/blob/master/LICENSE)
 [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6025390.svg)](https://doi.org/10.5281/zenodo.6025390)
 [![version](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/release/python-360/)
 [![Latest PyPI version](https://img.shields.io/pypi/v/mapeathor?style=flat)](https://pypi.python.org/pypi/mapeathor)

<p align="center">
 <img src="https://raw.githubusercontent.com/oeg-upm/Mapeathor/master/imgs/Square_logo_mapeathor.png" alt="workflow" width="150"/>
</p>


# Mapeathor
#### Mapeathor translates your mapping rules specified in spreadsheets to a mapping language.  

[Mapeathor](https://morph.oeg.fi.upm.es/tool/mapeathor) is a simple spreadsheet parser able to generate mapping rules in three mapping languages: R2RML, RML (with extension to functions from FnO) and YARRRML. It takes the mapping rules expressed in a spreadsheet and transforms them into the desired language. The spreadsheet template is designed to facilitate the mapping rules' writting, with the aim of being language independent, and thus, lowering the barrier of generating mappings for non-expert users.

<p align="center">
 <img src="https://raw.githubusercontent.com/oeg-upm/Mapeathor/master/imgs/workflow.png" alt="workflow" width="600"/>
</p>

## Example
A more detailed explanation is provided in the [wiki](https://github.com/oeg-upm/Mapeathor/wiki).

### First Step: Fill the xlsx template with the transformation rules
The template has five mandatory sheets, *Prefixes, Source, Subject PredicateObjectMap* and *Functions*. The last one can be left blank in case there are no functions. The spreadsheet can be in XLSX format or a Google Spreadsheet. Here is an example of the structure of the spreadsheet.

<p align="center">
 <img src="https://raw.githubusercontent.com/oeg-upm/Mapeathor/master/imgs/sheets.png" alt="sheets" width="500"/>
</p>

### Second Step: Choose the output language
One of three options can be chosen: R2RML, RML or YARRRML.

### Third Step: Run it!
The easiest way of running Mapeathor is using the [web service](https://morph.oeg.fi.upm.es/demo/mapeathor) and the [Swagger](https://morph.oeg.fi.upm.es/tool/mapeathor/swagger/) instance. For CLI lovers, the service is available as a [PyPi package](https://pypi.org/project/mapeathor/) and Docker image. The instructions of the latest can be found in the [wiki](https://github.com/oeg-upm/Mapeathor/wiki).

## Publications
Iglesias-Molina, A., Pozo-Gilo, L., Dona, D., Ruckhaus, E., Chaves-Fraga, D., & Corcho, O. (2020, January). *Mapeathor: Simplifying the Specification of Declarative Rules for Knowledge Graph Construction. In ISWC (Demos/Industry).* [Online version](http://ceur-ws.org/Vol-2721/paper488.pdf)

Iglesias-Molina, A., Chaves-Fraga, D., Priyatna, F., & Corcho, O. (2019). Towards the Definition of a Language-Independent Mapping Template for Knowledge Graph Creation. *In Proceedings of the Third International Workshop on Capturing Scientific Knowledge co-located with the 10th International Conference on Knowledge Capture (K-CAP 2019)* (pp. 33-36). [Online version](https://sciknow.github.io/sciknow2019/papers/SciKnow_2019_paper_4.pdf)

## Authors and contact
- [Ana Iglesias-Molina](https://github.com/anaigmo) (ana.iglesiasm@upm.es)
- [Luis Pozo](https://github.com/w0xter) (luis.pozo@upm.es)
- [Daniel Doña](https://github.com/daniel-dona) (daniel.dona@xnor.ga)
