# agora-py
<img src="https://dl.dropboxusercontent.com/u/1731751/agora/agora.png" width="200" align="right" alt="" />

**agora-py** is a Python library that supports *Web-scale Ontology-driven Access to Distributed Linked Data*.

Currently, there is a huge number of *dereferenciable* Linked Data resources that are not being properly consumed neither explored.
That is, the absolute majority of approaches for consuming Linked Data either ignore or inhibit such virtue, 
underutilizing the Web as a platform.  
Agora (agora-py) aims to be a tool that enables Linked Data consumers to live-query the Web of Data in a unified and explorative way:
* Driven by known vocabularies;
* Constrained by
   * the scope of the given query,
   * a set of seed resources whose URIs and types are known.
    
Although Agora is designed as well to be deployed as a microservices infrastructure, 
it can be fully used as a Python middleware, without the need for any other external dependency than the Web of Data. 

## Install

agora-py is still not uploaded to PyPi, however the current repository
can be passed as source for pip:

```
$ pip install git+https://github.com/oeg-upm/agora-py.git
```

## Getting Started

Before issuing the first query, Agora needs to know the following:
1. The vocabulary that will drive the exploration;
2. One seed resource whose URI and type (any Class in the vocabulary) is known.

### Register vocabularies

**agora-py** requires to be provided with the vocabularies (RDFS, OWL) that will be used
to drive the exploration of Linked Data resources.

```python
from agora import Agora

a = Agora()

# movies.ttl is in path agora/examples/movies/movies.ttl
with open('movies.ttl') as f:
    a.fountain.add_vocabulary(f.read())

print a.fountain.types

```

### Declare seeds

Once Agora is provided with a vocabulary that defines at least one Class, seed
resources can be declared as follows:

```python
from agora import Agora

a = Agora()
with open('movies.ttl') as f:
    a.fountain.add_vocabulary(f.read())

a.fountain.add_seed('http://dbpedia.org/resource/Blade_Runner', 'dbpedia-owl:Film')
a.fountain.add_seed('http://dbpedia.org/resource/Braveheart', 'dbpedia-owl:Film')
print a.fountain.seeds

```

### Query the Web

Agora enables Linked Data consumers to live-query the Web of Data using
SPARQL. The given queries (in fact, their BGP and filters) together with the registered 
vocabularies and provided seeds, define the scope of the link-traversal exploration.

```python
from agora import Agora

a = Agora()
with open('movies.ttl') as f:
    a.fountain.add_vocabulary(f.read())

a.fountain.add_seed('http://dbpedia.org/resource/Blade_Runner', 'dbpedia-owl:Film')
a.fountain.add_seed('http://dbpedia.org/resource/Braveheart', 'dbpedia-owl:Film')

query = """SELECT DISTINCT ?name ?actor WHERE { 
                [] foaf:name ?name ;
                   dbpedia-owl:starring [
                       dbp:birthName ?actor
                   ]
           }"""
           
for row in a.query(query):
    print row
```

## Background

### Linked Data

The Linked Data principles [^1] enable the creation of the Web of Data:

1. Use URIs as names for things.
2. Use HTTP URIs so that people can look up those things.
3. When someone looks up a URI, provide useful information, using the standards (RDF, SPARQL).
4. Include links to other URIs (within this information) so that they can discover more things.

#### Consuming Linked Data on the Web [^2]

|                             | data warehousing       | search engines | query federation   | link traversal                  | [linked data fragments][ldf] |
|-----------------------------|------------------------|----------------|--------------------|---------------------------------|-----------------------|
| Universe of discourse (UoD) | loaded data            | Web of Data    | known data sources | Web of Data                     | known data sources    |
| Required source interface   | mainly RDF dumps       | arbitrary      | SPARQL endpoints   | **Linked Data (look up) interface** | LDF servers           |
| Access to original data     | no                     | no             | yes                | yes                             | yes                   |
| Supporting data structures  | indices and statistics | crawled index  | statistics         | -                               | ?                     |
| Response and throughput     | fast / fast            | fast / fast    | slow / medium      | medium / slow                   | medium / slow         |
| Recall (w.r.t. UoD)         | 100%                   | <100%          | 100%               | <100%                           | 100%                  |
| Precision                   | 100%                   | <100%          | 100%               | 100%                            | 100%                  |
| Up-to-dateness              | low                    | medium         | high               | high                            | high                  |

#### What about Linked Data principles 2 and 3?
Only link traversal leverages available Linked Data (look-up) interfaces. A URI should not just serve as a global identifier, but also as provider of a structured data representation of the identified entity. The absolute majority of implemented solutions ignore both principles.

Why do not we rely on these HTTP look-up interfaces to directly consume Linked Data? Is it really necessary to give them up in favor of using SPARQL endpoints or any other (non-LD) interface to efficiently access and query Linked Data?

### Web of Data

#### Benefits
The three main benefits of the Web of Data are:

* Feasibility to perform live-querying over a dataspace that integrates a large number of interlinked datasets as if it was a huge multidatabase system.
* Data sources may be considerably lighter, scalable and maintanable than (reliable) SPARQL endpoints. They can be interfaced as just RESTful APIs that provide RDF by dereferencing known resources.
* Enables freshness and serendipitous discovery of data sources and results.

#### Problems
Some problems of (live-)querying the Web of Data:

* Not any approach for executing queries that range over all Linked Data on the Web can guarantee complete query results.
* Its openness and growth introduces data integration issues such as coreferencing and schema heterogeneity.
* Looking up certain URIs may result in the retrieval of an unforeseeable large set of RDF triples.
* Response times may vary significantly between different servers. Look-ups may take unexpectedly long or may not be answered at all.
* Restrictions on clients such as sercing only a limited number of requests per second (rate limits).

### Workload distribution

Can we minimize server resource usage while still enabling clients to query data sources efficiently?

<p align="center">
    <img src="docs/img/workload.png" title="Workload distribution between servers and clients" width="80%">
</p>

## Approach
### Ontology-driven link traversal
Link traversal is focused on querying the whole Web of Data without any prior knowledge about the vocabularies that are being used to describe the data.

Ontology-driven link traversal is less ambitious and aims only at querying the sub-dataspace that is described following the previously known vocabularies. In practice, it is only interested in those resources that are described so that they can be correctly interpreted, explored and consumed without extra effort.

Assuming that data are linked using the properties specified in the selected vocabularies, we can extract and exploit the underlying cabigational paths to easily access reachable and query-relevant fragments of data.

<p align="center">
    <img src="docs/img/approach.png" title="Ontology-driven link traversal approach" width="80%">
</p>

A set of known seeds of any type can be used as starting points of such navigational paths, so that they do not need to be explicitly included in queries. Using those seeds facilitates the selection fo data sources based on different criteria: reliability, security, etc.

Given a graph pattern from a conjuctive query, an executable search plan describing the shortest paths from known seeds can be provided.

<p align="center">
    <img src="docs/img/search.png" title="Search plans from graph patterns" width="80%">
</p>

## Concept
The *gathering place* for Distributed Linked Data.

The Agora was a central space or square in ancient Greek city-states. The literal meaning of the word is "gathering place" or "assembly".

The agora was the centre of athletic, artistic, spiritual and political life of the city.

<p align="center">
    <img src="docs/img/concept.png" title="Concept of Agora">
</p>

## How it works
The simplest Agora Engine is composed by a Fountain and a Planner.

<p align="center">
    <img src="docs/img/core.png" title="Architecture of the Agora Engine" height="80%">
</p>

### Fountain
The Fountain is the *place* where all navigational paths found in known vocabularies are exposed, taking into account a number of heterogeneous seeds to be later on proposed as starting points for search plans.

#### Path extraction from vocabularies
The Fountain queries the given vocabularies in order to create the underlying link graph. Basically, it tries to find out the domain and range of all properties in the vocabulary with the aim of identifying the set of nodes and edges that make up such link graph. In the end, (a subset of) concepts and properties in the ontology become the nodes and edges of the link graph, respectively.

##### Vocabulary registration
The Fountain accepts vocabularies for registration in two different formats: Turtle and RDF/XML. In order to identify the only ontology that should be described in the submitted content, the Fountain parses it and queries the resulting graph with:

```sql
SELECT ?o WHERE {
    ?o a owl:Ontology FILTER (isURI(?o))
}
```

Having the result set, the following restrictions are applied:

* The **size** of the result set must be 1. That is, vocabularies have to be registered one at a time.
* There must be a **declared prefix** that is equal to the URI binded by `?o`. The name of such prefix will be considered by Agora as the **identifier** of the vocabulary.

For example, the following block is declaring the ontology `<http://www.example.org/onto>`, which will be identified by Agora as *onto*.

```text
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix onto: <http://www.example.org/onto#> .

<http://www.example.org/onto> rdf:type owl:Ontology .

onto:Concept a owl:Class .
```

Onwards, when referring to a concept or property that belongs to that ontology, Agora will impose to do it prefixed (`onto:Concept`); otherwise (`<http://www.example.org/onto#Concept>`), it won't understand us.

##### Node extraction
The nodes of the link graph are created from all those concepts described in a given ontology that belong to the result set of the following query:

```sql
SELECT DISTINCT ?c WHERE {
    {
        ?p a owl:ObjectProperty .
        {
            { ?p rdfs:range ?c }
            UNION
            { ?p rdfs:domain ?c }
        }
    }
    UNION
    {
        ?p a owl:DatatypeProperty .
        ?p rdfs:domain ?c .
    }
    UNION
    { ?c a owl:Class }
    UNION
    { ?c a rdfs:Class }
    UNION
    { [] rdfs:subClassOf ?c }
    UNION
    { ?c rdfs:subClassOf [] }
    UNION
    {
        ?r a owl:Restriction ;
           owl:onProperty ?p .
        {
            ?p a owl:ObjectProperty .
            { ?r owl:allValuesFrom ?c }
            UNION
            { ?r owl:someValuesFrom ?c }
        }
        UNION
        { ?r owl:onClass ?c }
    }
    FILTER(isURI(?c))
}
```

Thus, there are some rules that must be taken into account in order to let the Fountain *detect* nodes in ontologies. That is, nodes are all URIs that match at least one of the following:

* It is a class, either an `owl:Class` or a `rdfs:Class`.
* It has at least one subclass in the ontology or it is the superclass of any other.
* It belongs to the domain of a datatype property.
* Given an object property,
    * it is a class that belongs to its range or/and domain.
    * there may be a set of things for which such property may have values of it.

It is important to note that no automatic reasoning is performed in this process. All required information must be materialized in the ontology description that is being submitted. Furthermore, existing conflicts and/or inconsistencies in definitions will not be treated; neither a warning nor an error message will be generated.

##### Edge extraction
Similarly to the process of node extraction, the detection of *valid* edges for the link graph in an ontology is built on the following query:

```sql
SELECT DISTINCT ?p WHERE {
    { ?p a rdf:Property }
    UNION
    { ?p a owl:ObjectProperty }
    UNION
    { ?p a owl:DatatypeProperty }
    UNION
    {
        [] a owl:Restriction ;
           owl:onProperty ?p .
    }
    FILTER(isURI(?p))
}
```

The result set of the corresponding query is composed of all the URIs that have been described in such a way that they can be considered as edges. The corresponding matching rules for edges are:

* It is a `rdf:Property`, an `owl:ObjectProperty` or an `owl:DatatypeProperty`.
* There is some restriction on it as a property.

##### Node properties

Once the Fountain has identified all nodes from the vocabularies, it is prepared to search for the incoming (references) and outgoing (properties) edges for each of them. To do so, it creates and keeps a tuple map that puts nodes and their properties together:

```sql
SELECT DISTINCT ?c ?p WHERE {
    { ?c rdfs:subClassOf [ owl:onProperty ?p ] }
    UNION
    { ?p rdfs:domain ?c }
    FILTER (isURI(?p) && isURI(?c))
}
```

Given a node *n*, its properties are all those URIs that fulfill the following conditions:

*  *n* belongs to its domain.
*  *n* has a constraint on it.

Having such map in memory, it is trivial to filter the properties of each node (fixing a value for *n*).

##### Node references

The process to obtain the incoming edges of all nodes is identical to that of properties. Here, the corresponding query that results in the required tuple map is the following:

```sql
SELECT ?c ?p WHERE {
    {
        ?r owl:onProperty ?p.
        { ?r owl:someValuesFrom ?c }
        UNION
        { ?r owl:allValuesFrom ?c }
        UNION
        { ?r owl:onClass ?c }
    }
    UNION
    { ?p rdfs:range ?c }
    FILTER (isURI(?p) && isURI(?c))
}
```

Given a node *n*, its references are all those URIs that fulfill the following conditions:

* *n* belongs to its range.
* There is a restriction that specifies that any of its values may be of the type represented by *n*.

##### Edge domain

The domain of an edge *e* is composed by all those nodes for which *e* is a property.

```sql
SELECT DISTINCT ?e ?c WHERE {
    { ?p rdfs:domain ?c }
    UNION
    { ?c rdfs:subClassOf [ owl:onProperty ?e ] }
    FILTER (isURI(?e) && isURI(?c))
}
```

##### Edge range

The range of an edge *e* is composed by:

* All those nodes for which *e* is a reference.
* Datatype URIs that appear in a data-range restriction of *e* for a certain node.

```sql
SELECT DISTINCT ?e ?r WHERE {
    {?e rdfs:range ?r}
    UNION
    {
        ?d owl:onProperty ?e.
        { ?d owl:allValuesFrom ?r }
        UNION
        { ?d owl:someValuesFrom ?r }
        UNION
        { ?d owl:onClass ?r }
        UNION
        { ?d owl:onDataRange ?r }
    }
    FILTER(isURI(?e) && isURI(?r))
}
```

##### Edge constraints
TBD


##### Example

<p align="center">
    <img src="docs/img/voc_branch.png" title="Excerpt from vocabulary for path extraction">
</p>

### Planner
Planners follow the claim *"I do not know the answer, but I can tell you where and how you can find it"*. They are given graph patterns and leverage the Fountain to compose search plans that specify how to get all relevant data.

#### Following search plans
Planners use RDF to represent self-contained search plans for a given graph pattern.
```
Graph pattern = {
   ?s atmos:monitors ?c .
   ?c rdfs:label ?comp .
   ?s core:hasValue ?v . 
   ?v core:literalValue ?lv .
   ?v core:timeStamp ?t
}

@prefix agora: <http://agora.org#> .
@prefix atmos: <http://example.org/atmosphere#> .
@prefix core: <http://iot.linkeddata.es/def/core#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix schema: <http://schema.org/> .
@prefix wot: <http://iot.linkeddata.es/def/wot#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

[] a agora:SearchTree ;
    agora:fromType atmos:ObservationContainer ;
    agora:hasSeed <http://localhost:5000/proxy/container/eyIkbGF0IjogIjQwLjQ2NTgyNyIsIiRsbmciOiAiLTMuNjg5Njg0In0%3D> ;
    agora:length 13 ;
    agora:next [ agora:expectedType atmos:ObservationContainer ;
            agora:next [ agora:byPattern _:tp_0 ;
                    agora:expectedType atmos:Observation ;
                    agora:next [ agora:byPattern _:tp_2 ;
                            agora:expectedType atmos:ChemicalCompound ] ;
                    agora:onProperty atmos:monitors ],
                [ agora:byPattern _:tp_3 ;
                    agora:expectedType atmos:Observation ;
                    agora:next [ agora:byPattern _:tp_1 ;
                            agora:expectedType core:Value ],
                        [ agora:byPattern _:tp_4 ;
                            agora:expectedType core:Value ] ;
                    agora:onProperty core:hasValue ] ;
            agora:onProperty atmos:contains ] .

[] a agora:SearchSpace ;
    agora:definedBy _:tp_0,
        _:tp_1,
        _:tp_2,
        _:tp_3,
        _:tp_4 .

_:var_comp a agora:Variable ;
    rdfs:label "?comp"^^xsd:string .

_:var_lv a agora:Variable ;
    rdfs:label "?lv"^^xsd:string .

_:var_t a agora:Variable ;
    rdfs:label "?t"^^xsd:string .

_:var_c a agora:Variable ;
    rdfs:label "?c"^^xsd:string .

_:var_s a agora:Variable ;
    rdfs:label "?s"^^xsd:string .

_:tp_0 a agora:TriplePattern ;
    rdfs:label "tp_0" ;
    agora:object _:var_c ;
    agora:predicate atmos:monitors ;
    agora:subject _:var_s .

_:tp_1 a agora:TriplePattern ;
    rdfs:label "tp_1" ;
    agora:object _:var_lv ;
    agora:predicate core:literalValue ;
    agora:subject _:var_v .

_:tp_2 a agora:TriplePattern ;
    rdfs:label "tp_2" ;
    agora:object _:var_comp ;
    agora:predicate rdfs:label ;
    agora:subject _:var_c .

_:tp_3 a agora:TriplePattern ;
    rdfs:label "tp_3" ;
    agora:object _:var_v ;
    agora:predicate core:hasValue ;
    agora:subject _:var_s .

_:tp_4 a agora:TriplePattern ;
    rdfs:label "tp_4" ;
    agora:object _:var_t ;
    agora:predicate core:timeStamp ;
    agora:subject _:var_v .

_:var_v a agora:Variable ;
    rdfs:label "?v"^^xsd:string .
```

## References

[ldf]: <http://linkeddatafragments.org/>

[^1]: Tim Berners-Lee. Linked data-design issues (2006) http://www.w3.org/DesignIssues/LinkedData.html

[^2]: Hartig et al. A Database Perspective on Consuming Linked Data on the Web (2010)

[^3]: Olaf Hartig. An Overview on Execution Strategies for Linked Data Queries (2013)

[^4]: Olaf Hartig. SQUIN: A Traversal Based Query Execution System for the Web of Linked Data (2013)

[^5]: Olaf Hartig. SPARQL for a Web of Linked Data: Semantics and Computability (2012)

[^6]: Bouquet et al. Querying the Web of Data: A Formal Approach (2009)

## License
agora-py is distributed under the Apache License, version 2.0.