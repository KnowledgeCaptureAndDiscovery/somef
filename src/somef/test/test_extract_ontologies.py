import unittest

import os
from pathlib import Path
from .. import extract_ontologies
from ..utils import constants

test_data_repositories = str(Path(__file__).parent / "test_data" / "repositories") + os.path.sep


class TestOntologies(unittest.TestCase):
    def test_is_ontology(self):
        """This test checks if a file containing an ontology is really there."""
        onto = extract_ontologies.is_file_ontology(test_data_repositories + "Widoco/example_onto/ontology.ttl")
        # assert("https://w3id.org/example" in onto)
        assert onto is not None
        assert onto[constants.PROP_URI] == "https://w3id.org/example"
        assert onto[constants.PROP_TITLE] == "The example ontology"
        assert onto[constants.PROP_VERSION] == "1.0.1"
        assert onto[constants.PROP_AUTHOR] == [
            {"type": "Agent", "name": "Daniel Garijo"},
            {"type": "Agent", "name": "Maria Poveda-Villalon"}
        ]
        assert onto[constants.PROP_LICENSE] == "http://creativecommons.org/licenses/by/2.0/"
        assert onto[constants.PROP_PREFERRED_NS_PREFIX] == "exo"

    def test_is_ontology_fake(self):
        """This test checks that a RDF file with no ontology is not detected, as it should not."""
        onto = extract_ontologies.is_file_ontology(test_data_repositories + "Widoco/example_onto/test.ttl")
        assert(onto is None)

    def test_is_ontology_orcid_name(self):
        """This test checks if we get correctly url and name from authors."""
        onto = extract_ontologies.is_file_ontology(test_data_repositories + "ecfo/ontology.ttl")

        assert onto is not None
        assert onto[constants.PROP_URI] == "https://w3id.org/ecfo"
        assert onto[constants.PROP_TITLE] == "The Emission Conversion Factor Ontology"
        assert onto[constants.PROP_VERSION] == "1.0.0"
        expected_author = {
            'type': 'Agent',
            'url': 'https://orcid.org/0000-0003-0454-7145',
            'name': 'Daniel Garijo'
        }
        assert expected_author in onto[constants.PROP_AUTHOR]
