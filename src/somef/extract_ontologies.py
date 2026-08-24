from rdflib import Graph, Namespace, URIRef
from rdflib.plugins.sparql import prepareQuery
from .utils import constants


_DC = Namespace(constants.DC_NAMESPACE)
_DCTERMS = Namespace(constants.DCTERMS_NAMESPACE)
_VANN = Namespace(constants.VANN_NAMESPACE)
_OWL = Namespace(constants.OWL_NAMESPACE)
_RDFS = Namespace(constants.RDFS_NAMESPACE)
_SCHEMA = Namespace(constants.SCHEMA_NAMESPACE)
_SKOS = Namespace(constants.SKOS_NAMESPACE)
_PROV = Namespace(constants.PROV_NAMESPACE)
_PAV = Namespace(constants.PAV_NAMESPACE)
_MOD = Namespace(constants.MOD_NAMESPACE)
_CC = Namespace(constants.CC_NAMESPACE)
_FOAF = Namespace(constants.FOAF_NAMESPACE)

def is_file_ontology(file_path):
    """
    Method that, given a file, returns its URI.
    This method is in a separate file in case we want to extract additional metadata if required
    Parameters
    ----------
    @param file_path: path of the candidate ontology

    Returns
    -------
    @return: A dictionary with the ontology's URI and any additional metadata found
             (title, description, version, license, authors, date of creation,
             preferred namespace), or None if the file does not contain an ontology.
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
                constants.PROP_NAME: get_first_literal(g, onto_uri, [
                    _RDFS.label, _MOD.acronym, _SKOS.prefLabel, _SCHEMA.alternateName
                ]),
                constants.PROP_TITLE: get_first_literal(g, onto_uri, [
                    _DCTERMS.title, _DC.title, _SCHEMA.name
                ]),
                constants.PROP_DESCRIPTION: get_first_literal(g, onto_uri, [
                    _DCTERMS.description, _DC.description, _RDFS.comment,
                    _SCHEMA.description, _SKOS.note, _DCTERMS.abstract
                ]),
                constants.PROP_VERSION: get_first_literal(g, onto_uri, [
                    _OWL.versionInfo, _PAV.version, _DCTERMS.hasVersion, _SCHEMA.schemaVersion
                ]),
                constants.PROP_DATE_CREATED: get_first_literal(g, onto_uri, [
                    _DCTERMS.created, _SCHEMA.dateCreated, _PROV.generatedAtTime, _PAV.createdOn
                ]),
                constants.PROP_LICENSE: get_first_literal(g, onto_uri, [
                    _DCTERMS.license, _DC.rights, _SCHEMA.license, _CC.license
                ]),
                constants.PROP_AUTHOR: get_author_names(g, onto_uri, [
                    _DCTERMS.creator, _DC.creator, _FOAF.maker, _PAV.authoredBy, _SCHEMA.author
                ]),
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

def get_first_literal(g, subject, predicates):
  """
  Returns the first non-null literal value found among a list of candidate predicates,
  tried in order of preference.
  """
  for p in predicates:
      v = g.value(subject, p)
      if v is not None:
          return str(v)
  return None


def get_author_names(g, subject, predicates):
    """
    Returns the list of creators of a resource as Agent objects.

    Literal values are returned as {"type": "Agent", "name": <literal>}.
    URI values are returned as {"type": "Agent", "url": <uri>}, plus a "name"
    resolved from the same graph (foaf:name, schema:name) when available.
    """
    name_predicates = [_FOAF.name, _RDFS.label, _SCHEMA.name]
    authors = []
    seen = set()

    for predicate in predicates:
        for o in g.objects(subject, predicate):
            if isinstance(o, URIRef):
                resolved = get_first_literal(g, o, name_predicates)
                entry = {"type": constants.AGENT, "url": str(o)}
                if resolved:
                    entry["name"] = resolved
            else:
                entry = {"type": constants.AGENT, "name": str(o)}

            key = (entry.get("name"), entry.get("url"))
            if key not in seen:
                seen.add(key)
                authors.append(entry)

    return authors