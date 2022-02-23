# RDFChess
RDFChess is a web service capable of offering structured information on chess players, chess games and chess openings. 
You may download the project, generate a .war file and deploy it in any servlet container (e.g. Tomcat). Alternatively, you may generate a .jar file which is a self-contained servlet server (jetty) to be run.
In addition, a Fuseki server is needed to serve the information as linked data.

RDFChess includes a dataset of chess games stored as RDF. 
It is an example on how ontology design patterns can guide the creation of linked data
This project was created in connection with the paper presented at COLD2015

Pattern-Based Linked Data Publication: The Linked Chess Dataset Case, V. Rodríguez-Doncel, A. A. Krisnadhi, P. Hitzler, M. Cheatham, N. Karima and R. Amini, in Proc. of the 6rd Int. W. on Consuming Linked Data, ISSN: 1613-0073, CEUR Vol. 1426, O. Hartig et al. (Eds.) (2015)
See the paper here: http://delicias.dia.fi.upm.es/~vrodriguez/pdf/2015.10.cold.pdf

You can also find additional information http://dase.cs.wright.edu/content/pattern-driven-linked-data-publishing-primer, including the ontologies.


## Install
Requirements:
* A web applications server. It can be jetty or even better, Tomcat.
* A triple store and its configuration (change RDFChess.java)
* The data loaded in the triple store!
