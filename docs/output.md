SOMEF supports three main output formats. Each of them contains different information with different levels of granularity. Below we enumerate them from more granular to less granular:

### JSON format
Simple JSON representation that indicates, for each extracted metadata category, the technique used for its extraction and its confidence, in addition to the detected excerpt. The JSON snippet below shows an example for the Description category of a Python library.

```json
"description": [
    {
      "excerpt": "KGTK is a Python library ...",
      "confidence": [0.8294290479925978],
      "technique": "Supervised classification"
    }
  ]
```
The `confidence` depends on the `technique` used. In this case, the confidence is driven by the classifier which makes the prediction. 

The techniques can be of several types: `header analysis`, `supervised classification`, `file exploration`, `GitHub API` and `regular expression`. Among these, only `supervised classification` provides a confidence different to `1`.

The output may also contain the following fields:

- `format`: format in which a citation is recognized. Supported formats are `bibtex` and `citation file format`.
- `doi`: Digital Object Identifier associated with a paper or a software repository.
- `type`: type of documentation recognized by somef. There are two main recognized types: `readthedocs` and `wiki`.

### Turtle format
RDF representation using the [Software Description Ontology](https://w3id.org/okn/o/sd/). The snippet below shows a sample description of a software entry. The `excerpt` and `confidence` fields are ommitted in this representation (every category with confidence above the threshold specified when running SOMEF will be included in the results)

### Codemeta format
JSON-LD representation following the [Codemeta specification](https://codemeta.github.io/) (which itself extends [Schema.org](https://schema.org/)). The `excerpt` and `confidence` fields are ommitted in this representation (every category with confidence above the threshold specified when running SOMEF will be included in the results). In addition, any metadata category outside from what is defined in Codemeta will be avoided.
