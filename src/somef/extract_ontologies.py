from rdflib import Graph, Namespace
from rdflib.plugins.sparql import prepareQuery
from .utils import constants


_DC = Namespace(constants.DC_NAMESPACE)
_DCTERMS = Namespace(constants.DCTERMS_NAMESPACE)
_VANN = Namespace(constants.VANN_NAMESPACE)
_OWL = Namespace(constants.OWL_NAMESPACE)

def is_file_ontology(file_path):
    """
    Method that, given a file, returns its URI.
    This method is in a separate file in case we want to extract additional metadata if required
    Parameters
    ----------
    @param file_path: path of the candidate ontology

    Returns
    -------
    @return: The URI of the target ontology (if there is one)
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
        for r in g.query(q1):
          # print("Found that %s is an ontology" % file_path)
          # return r.onto
          onto_uri = r.onto
        
          return {
              constants.PROP_URI: str(onto_uri),
              constants.PROP_TITLE: get_literal(g, onto_uri, _DC.title),
              constants.PROP_DESCRIPTION: (
                  get_literal(g, onto_uri, _DC.description)
                  or get_literal(g, onto_uri, _DCTERMS.abstract)
              ),
              constants.PROP_VERSION: get_literal(g, onto_uri, _OWL.versionInfo),
              constants.PROP_DATE_CREATED: get_literal(g, onto_uri, _DCTERMS.created),
              constants.PROP_LICENSE: get_literal(g, onto_uri, _DCTERMS.license),
              constants.PROP_AUTHOR: get_all_literals(g, onto_uri, _DCTERMS.creator),
              constants.PROP_PREFERRED_NS_PREFIX: get_literal(g, onto_uri, _VANN.preferredNamespacePrefix),
              constants.PROP_PREFERRED_NS_URI: get_literal(g, onto_uri, _VANN.preferredNamespaceUri),
          }
    except Exception:
        # If the candidate file could not be read, pass
        pass
    return None
    
def get_literal(g, subject, predicate):
    value = g.value(subject, predicate)
    return str(value) if value is not None else None

def get_all_literals(g, subject, predicate):
    return [str(o) for o in g.objects(subject, predicate)]
