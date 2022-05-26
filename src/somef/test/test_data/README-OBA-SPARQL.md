# OBA Sparql Query Manager [![Build Status](https://travis-ci.com/KnowledgeCaptureAndDiscovery/OBA_sparql.svg?branch=master)](https://travis-ci.com/KnowledgeCaptureAndDiscovery/OBA_sparql) [![codecov](https://codecov.io/gh/KnowledgeCaptureAndDiscovery/OBA_sparql/branch/master/graph/badge.svg)](https://codecov.io/gh/KnowledgeCaptureAndDiscovery/OBA_sparql)



OBA Sparql Query Manager is a Python Module to translate CRUD requests to SPARQL queries. This module is used by
OBA project to generate a REST API from OWL ontologies.

OBA sparql use JSON-LD contexts to translate RDF triples to JSON, and vice versa.

## Quick Start

### Generate the context files

Simply speaking, a context is used to map terms to IRIs. Terms are case sensitive and most valid strings
that are not reserved JSON-LD keywords can be used as a term. 

To generate the context files, we recommend to use:

1. [OBA](https://oba.readthedocs.io/en/latest/quickstart/)
2. [owl2jsonld](https://github.com/stain/owl2jsonld)


TODO: Insert a good example.

```python

from obasparql import QueryManager
from test.settings import dbpedia_queries, dbpedia_context, dbpedia_endpoint, dbpedia_prefix
from obasparql.static import * 
queries = "queries/"
contexts = "contexts/"
dbpedia_endpoint = "https://dbpedia.org/sparql"
dbpedia_prefix = "http://dbpedia.org/resource"
graph = None

query_manager = QueryManager(queries_dir=queries,
                                  context_dir=contexts,
                                  endpoint=dbpedia_endpoint,
                                  named_graph_base=graph,
                                  uri_prefix=dbpedia_prefix)

query_manager.get_one_resource()
query_manager.get_all_resource()
```

## Supported features

OBA sparql supports two types of queries:

- Default queries: queries related to the CRUD requests.
    - Get a resource and get all the resource by type.
- Custom queries: In some cases, users need to implement custom queries that are not the default instances 
    of a class of the ontology (e.g., get all instances of a class that comply with certain conditions)

### Default queries
- GET all: Obtain all the resources with a rdf:type. Needs:
    1. Resource Type IRI. (For example: http://dbpedia.org/ontology/Artist)
- GET one: Obtain the details about a resource with the id. Needs:
    1. Resource IRI: (For example: http://dbpedia.org/ontology/Pink_Floyd)
    2. Resource Type IRI: (For example: http://dbpedia.org/ontology/Artist)
- POST: Insert a new resource:
    1. The JSON request
- PUT: Update a existing resource 
    1. Resource IRI: (For example: http://dbpedia.org/ontology/Pink_Floyd)
- DELETE: Delete a existing resource
    1. Resource IRI: (For example: http://dbpedia.org/ontology/Pink_Floyd)


### Custom queries

- Get all instances of a class that comply with certain conditions
    1. Resource Type IRI: (For example: http://dbpedia.org/ontology/Artist)
- Get one instance of a class that comply with the conditions
    1. Resource IRI: (For example: http://dbpedia.org/ontology/Pink_Floyd)
    2. Resource Type IRI: (For example: http://dbpedia.org/ontology/Artist)
  

## Testing

This repository is using `pytest` for the testing

```bash
$ pip install -r test-requirements.txt
$ pytest
```

For more information. You can inspect the file `.travis.yaml`
