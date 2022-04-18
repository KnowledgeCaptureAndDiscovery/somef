import unittest

import os
from pathlib import Path

from .. import extract_ontologies

test_data_repositories = str(Path(__file__).parent / "test_data" / "repositories") + os.path.sep


class TestOntologies(unittest.TestCase):
    def test_is_ontology(self):
        """This test checks if a file containing an ontology is really there."""
        onto = extract_ontologies.is_file_ontology(test_data_repositories + "Widoco/example_onto/ontology.ttl")
        assert("https://w3id.org/example" in onto)

    def test_is_ontology_fake(self):
        """This test checks that a RDF file with no ontology is not detected, as it should not."""
        onto = extract_ontologies.is_file_ontology(test_data_repositories + "Widoco/example_onto/test.ttl")
        assert(onto is None)