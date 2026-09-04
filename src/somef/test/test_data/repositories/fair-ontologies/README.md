# OEG FAIR Ontologies Assessment (FOOPS!)
[![DOI](https://zenodo.org/badge/367292245.svg)](https://doi.org/10.5281/zenodo.14767999)

<img src="html_client/assets/foopsLogo.png" alt="logo" width="200"/>

Authors: Daniel Garijo and María Poveda, with contributions from Jacobo Mata.

FOOPS! is an application for assessing whether a vocabulary (OWL or SKOS) conforms with the FAIR data principles.

Our [ISWC 2021 demo paper](html_client/assets/iswc_2021_demo.pdf) (**best demo award**) provides an overview of the FOOPS! service. Please cite our work as follows:
```
@article{foops2021,
    title        = {FOOPS!: An Ontology Pitfall Scanner for the FAIR Principles},
    author       = {Garijo, Daniel and Corcho, Oscar and Poveda-Villal{\'o}n, Mar{\i}a},
    year         = 2021,
    booktitle    = {International Semantic Web Conference (ISWC) 2021: Posters, Demos, and Industry Tracks},
    publisher    = {CEUR-WS.org},
    series       = {CEUR Workshop Proceedings},
    volume       = 2980,
    url          = {http://ceur-ws.org/Vol-2980/paper321.pdf}
}
```
If you are interested in more information, check [our slides](https://www.slideshare.net/dgarijo/foops-an-ontology-pitfall-scanner-for-the-fair-principles) with the rationale of FOOPS! and the [teaser video](https://www.youtube.com/watch?v=s8FaFl8i6yQ&ab_channel=OEG-UPM) we made for ISWC 2021.

The client application has been integrated from the work in https://github.com/jacobomata/FairValidator. The client would not have been possible without the work from @jacobomata

## Demo
A public demo of FOOPS! is available here: [https://w3id.org/foops/](https://w3id.org/foops/). 

If you want to use the API directly, you may do so at [https://w3id.org/foops/api](https://w3id.org/foops/api) (see the POST `/assessOntology` endpoint).


## Installation instructions
The project was build and tested with JDK 11.0.11 in Ubuntu.

To create the JAR, just run:

```
mvn install
```
on the server folder, or download the JAR from the releases page.

## Running the server
Run the following command

```
java -jar -Dserver.port=PORT fair_ontologies-x.y.z.jar
```

Where PORT is the port you want to run the server, and `x.y.z` is the version you want to build (usually the latest release).

To test the installation, just do a curl command (if the application was run in the port 8083):

```
curl -X POST "http://localhost:8083/assessOntology" -H "accept: application/json;charset=UTF-8" -H "Content-Type: application/json;charset=UTF-8" -d "{ \"ontologyUri\": \"https://w3id.org/okn/o/sd\"}"
```

As a result, you should see a JSON in your console, such as the one in `sample.json` in the root of this repository.

If you'd like to generate the output in a file, then run:
```
curl -X POST "http://localhost:8083/assessOntology" -H "accept: application/json;charset=UTF-8" -H "Content-Type: application/json;charset=UTF-8" -d "{ \"ontologyUri\": \"https://w3id.org/okn/o/sd\"}" -o sample.json
```

### Swagger OpenAPI
When you run the server, FOOPS! will set up a Swagger UI describing the endpoints available in the API. This API is available at `http://localhost:PORT/swagger-ui/index.html#/`


## Running the JAR in local
To create the JAR, just run:

```
mvn install -f pom_jar.xml
```

Then run the following command to test a URI: 

```
java -jar target/fair_ontologies-x.y.z.jar -ontURI https://w3id.org/example
```

You can also test one ontology from a file:

```
java -jar target/fair_ontologies-x.y.z.jar -ontFile filePath
```

As a result, you should see a JSON in your folder (validation.json).


If you want to change the out file path you can use the flag `-out`

## Documentation

### Metrics and tests
The metrics (i.e., conceptual description of what is being assessed) and tests (i.e., implementation of a metric) supported by the tool are available at [https://w3id.org/foops/catalog](https://w3id.org/foops/catalog), along with a detail description of their rationale and means of verification.

### API result specification
FOOPS! supports two result specifications, due to legacy development. The endpoints:
* [POST] /assessOntology and
* [POST] /assessOntologyFile

Follow the classic FOOPS! JSON format. To see an example, please see the [sample json file](./sample.json) in the code repository. This JSON is simple, but may be harder to debug.

The endpoints:
* [GET] /benchmarks/{identifier}
* [GET] /tests
* [GET] /tests/{identifier}
* [GET] /metrics
* [GET] /metrics/{identifier}
* [POST] /assess/resultset/{identifier}
* [POST] /assess/test/{test_identifier}

Follow the [FAIR test resource specification](https://w3id.org/ftr/), providing machine-readable metadata (JSON-LD) on all tests, metrics and groups of tests supported by FOOPS!

## Expanding the list of supported persistent registries
Test [FIND3](https://w3id.org/foops/test/FIND3) assesses whether an ontology complies to a certain URI scheme, based on persistent identifier registries like w3id.org or purl.org. However, your organization may issue persistent URIs too. If you would like us to add your registry scheme into the supported URI schemes, please [open an issue](https://github.com/oeg-upm/fair_ontologies/issues) describing the URI scheme you want to support in FOOPS! and a link to a policy page describing the intention of the organization to support the resources in the long term. A reviewer will check and add it into the tool.
