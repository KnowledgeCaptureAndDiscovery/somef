
![logo](https://github.com/oeg-upm/wot-hive/blob/AndreaCimminoArriaga-wothive-logo/logo.png)

[![Version](https://img.shields.io/badge/Version-0.2.2-orange)](https://github.com/oeg-upm/wot-hive/releases/tag/v0.2.2) [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

WoT Hive is an implementation of a [W3C Web of Things directory ](https://www.w3.org/TR/wot-discovery/). This implementation is compliant with the standard specification but aims at providing enriched features thanks to the usage of other W3C standards related to Semantic Web technologies.

**Checkout our [wiki for more documentation](https://github.com/oeg-upm/wot-hive/wiki)**

**Temporally the functionality that introduces the registration information in the Things has been disable (version 0.2.0 and above). Also, at the light of a new update in the [Thing Descriptions the semantic validation lacks of a proper shacl shape file](https://github.com/w3c/wot-thing-description/issues/1345) and therefore it is strongly recomended to disable this kind of validation.**

##  Docker quick start
Copy this receipt in a *docker-compose.yml* file

```yaml
version: '2'
services:
  triplestore:
    image: acimmino/auroral-fuseky:latest
    environment:
     ADMIN_PASSWORD: pw123
    volumes:
    - triplestore:/fuseki
    ports:
      - '3030:3030'
  wothive:
    image: acimmino/wot-hive:auroral-dev
    # volumes:
    # - ./configuration.json:/usr/src/wothive/configuration.json
    ports:
      - '9000:9000'
volumes:
  triplestore:
```

Run the docker command

```bash
docker-compose up
```


[OPTIONAL] Uncomment wothive volume to bind your own configuration file for the wothive. Default file is configured to connect the fuseki service running in the docker-compose network.

[OPTIONAL 2] If you want to change the fuseki service location (Move outside docker for instance), you can change the configuration of the wothive also via API. A `POST` request must be sent to `/configuration/triplestore` containing the in the body the following JSON. This 

```json
{
    "updateEnpoint": "http://triplestore:3030/sparql",
    "queryEnpoint": "http://triplestore:3030/sparql",
    "queryUsingGET": true
}
```

##  Jar quick start  
##### `Requires a triple store service publishing a SPARQL endpoint to store the Thing Descriptions`
#### 1. Download the WoT Hive service
Download the latest release of WoT Hive into a folder. Notice that the releases have several files that must be downloaded and placed in the same folder:
* **log4j.properties** allows to customise the logs of the service
* **schema.json** allows to perform JSON schema validation over the Thing Descriptions
* **shape.ttl** allows to perform SHACL shapes validation over the Thing Descriptions
* **wothive.jar** is the jar of the service

Once downloaded all the resources in the same folder the service can be ran using the command

```bash
java -jar wothive.jar
```

When the service is up and running a file called *configuration.json* will be created in the directory of the jar.  The service will run by default in port 9000. 
#### 2. Set up the triple store
In order to connect the WoT Hive to a remote triple store a `POST` request must be sent to `/configuration/triplestore` containing the in the body the following JSON

```json
{
    "updateEnpoint": "http://localhost:3030/sparql",
    "queryEnpoint": "http://localhost:3030/sparql",
    "queryUsingGET": true
}
```

Notice that `"queryEndpoint"`and `"updateEndpoint"` must have as value the correct endpoints of the triple store for either querying or inserting data. Finally, if the triple store implements the SPARQL protocol through `GET` requests then leave `"queryUsingGET": true`, otherwise, for using `POST`set it to false `"queryUsingGET": false`.

## WoT Hive API

| Endpoint 	| Method 	| Headers 	| Reference 	| Description 	|
|---	|---	|---	|---	|---	|
| `/.well-known/wot-thing-description` 	| `GET` 	| `N/A` 	| [Introduction Mechanim](https://w3c.github.io/wot-discovery/#introduction-well-known) 	| Provides the Thing Description of the WoT Hive directory 	|
| `/configuration` 	| `GET` 	| `N/A` 	| [Management](https://w3c.github.io/wot-discovery/#exploration-directory-api-management) 	| Provides a JSON with the all the configurations of the WoT Hive 	|
| `/configuration` 	| `POST` 	| `N/A` 	| [Management](https://w3c.github.io/wot-discovery/#exploration-directory-api-management) 	| The body of the request must contain a JSON with all the configurations of the WoT Hive. 	|
| `/api/things{?offset,limit,sort_by,sort_order}` 	| `GET` 	| `Accept`: `application/td+json`or `text/turtle`  	| [Listing](https://w3c.github.io/wot-discovery/#exploration-directory-api-registration-listing) 	| Provides a listing of the stored Thing Descriptions in JSON-LD framed or Turtle 	|
| `/api/things` 	| `POST` 	| `Content-Type`: `application/td+json` 	| [Creation (Anonymous)](https://w3c.github.io/wot-discovery/#exploration-directory-api-registration-creation) 	| Creates an [anonymous Thing Description](https://w3c.github.io/wot-discovery/#dfn-wot-anonymous-thing-description), provided in the body as JSON-LD framed. The generated `:id` is output in the response headers  	|
| `/api/things/{:id}` 	| `GET` 	| `Accept`: `application/td+json`or `text/turtle` 	| [Retrieval](https://w3c.github.io/wot-discovery/#exploration-directory-api-registration-retrieval) 	| Retrieves the Thing Description with the provided id, in either JSON-LD framed or turtle 	|
| `/api/things/{:id}` 	| `PUT` 	| `Content-Type`: `application/td+json`or `text/turtle` 	| [Creation](https://w3c.github.io/wot-discovery/#exploration-directory-api-registration-creation) or [Update](https://w3c.github.io/wot-discovery/#exploration-directory-api-registration-update) 	| Creates an Thing Description, provided in the body as JSON-LD framed or turtle 	|
| `/api/things/{:id}` 	| `PATCH` 	| `Content-Type`: `application/merge-patch+json` 	| [Partial Update](https://w3c.github.io/wot-discovery/#exploration-directory-api-registration-update) 	| Partially updates an existing Thing Description, the updates must be provided in JSON-LD framed 	|
| `/api/things/{:id}` 	| `DELETE` 	| `N/A` 	| [Deletion](https://w3c.github.io/wot-discovery/#exploration-directory-api-registration-deletion) 	| Partially updates an existing Thing Description, the updates must be provided in JSON-LD framed 	|
| `api/search/jsonpath{?query}` 	| `GET` 	| `N/A` 	| [JSON path search](https://w3c.github.io/wot-discovery/#jsonpath-semantic) 	| Filters existing Thing Descriptions based on the provided JSON path, the output will be always in JSON-LD framed 	|
| `api/search/sparql{?query}` 	| `GET` 	| `Accept` : `application/sparql-results+json`, `application/sparql-results+xml`, `text/csv`, or `text/tab-separated-values` 	| [SPARQL search](https://w3c.github.io/wot-discovery/#search-semantic) 	| Solves a SPARQL query following the [standard](https://www.w3.org/TR/sparql11-protocol/<br>), results format are in JSON by default if no header is specified. Otherwise available formats are JSON(application/sparql-results+json), XML (application/sparql-results+xml), CSV (text/csv), or TSV (text/tab-separated-values)  	|
| `api/events{?diff}` 	| `GET` 	| `N/A` 	| [Notifications](https://w3c.github.io/wot-discovery/#exploration-directory-api-notification) 	| Subscribe to all the events of the service (`create`, `update`, and `delete`) using the Server-Sends-Events (SSE) protocol 	|
| `api/events/create{?diff}` 	| `GET` 	| `N/A` 	| [Notifications](https://w3c.github.io/wot-discovery/#exploration-directory-api-notification) 	| Subscribe to all the `create` events of the service using the Server-Sends-Events (SSE) protocol 	|
| `api/events/update{?diff}` 	| `GET` 	| `N/A` 	| [Notifications](https://w3c.github.io/wot-discovery/#exploration-directory-api-notification) 	| Subscribe to all the `update` events of the service using the Server-Sends-Events (SSE) protocol 	|
| `api/events/delete{?diff}` 	| `GET` 	| `N/A` 	| [Notifications](https://w3c.github.io/wot-discovery/#exploration-directory-api-notification) 	| Subscribe to all the `delete` events of the service using the Server-Sends-Events (SSE) protocol 	|

[Validation](https://w3c.github.io/wot-discovery/#validation) can  be configured to ran using the JSON schema of the Thing Descriptions and/or their SHACL shapes.

---
### Acknowledgements
This project has been partially funded by the European project AURORAL from the European Union's Horizont 2020 research and innovation programme under grant agreement Nº101016854.

<img src="https://user-images.githubusercontent.com/4105186/141472288-1b15e0ba-8ae1-414a-a849-222b6bc27754.png" height="75" /> <img src="https://www.auroral.eu/img/logos/bandeira.png"  height="80" />

