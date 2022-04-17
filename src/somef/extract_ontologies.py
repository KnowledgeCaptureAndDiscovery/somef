from rdflib import Graph
from rdflib.plugins.sparql import prepareQuery


def is_file_ontology(file_path):
    """
    Method that, given a file, returns its URI.
    This method is in a separate file in case we want to extract additional metadata if required
    Parameters
    ----------
    file_path path of the candidate ontology

    Returns the URI of the target ontology (if there is one)
    -------
    """
    # load in rdf lib
    try:
        g = Graph()
        g.parse(file_path)
        q1 = prepareQuery('''
          SELECT ?onto
          WHERE { 
            ?onto a <http://www.w3.org/2002/07/owl#Ontology>. 
          }
          ''')
        # TO DO: extract title, preferred ns.
        # there should be only one ontology per file
        for r in g.query(q1):
            print("Found that %s is an ontology" % file_path)
            return r.onto
    except:
        # If the candidate file could not be read, pass
        pass
