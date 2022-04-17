import unittest

import os

from somef import extract_ontologies


class TestOntologies(unittest.TestCase):
    def test_is_ontology(self):
        """
        This test checks if a file containing an ontology is really there.
        -------
        """
        onto = extract_ontologies.is_file_ontology("test_data/repositories/Widoco/example_onto/ontology.ttl")
        assert("https://w3id.org/example" in onto)

    def test_is_ontology_fake(self):
        """
        This test checks that a RDF file with no ontology is not detected, as it should not.
        -------
        """
        onto = extract_ontologies.is_file_ontology("test_data/repositories/Widoco/example_onto/test.ttl")
        assert(onto is None)