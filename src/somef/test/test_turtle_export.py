import os
import unittest
from pathlib import Path
from rdflib import Graph
from .. import somef_cli
from ..export import turtle_export
from .. import process_results

test_data_path = str(Path(__file__).parent / "test_data") + os.path.sep
test_data_repositories = str(Path(__file__).parent / "test_data" / "repositories") + os.path.sep


class TestExportTTL(unittest.TestCase):

    def test_empty(self):
        """Simple test for an empty graph. Prefixes should be added, and no more"""
        g = turtle_export.DataGraph()
        r = process_results.Result()
        g.somef_data_to_graph(r.results)
        assert len(g.g) == 0

    def test_export_url(self):
        """
        Checks whether a repository correctly exports a file in TTL, which can be read.
        Test to make sure it works from URL
        """
        test_path = test_data_path + "test-basic.ttl"
        somef_cli.run_cli(threshold=0.8,
                          ignore_classifiers=False,
                          repo_url="https://github.com/dgarijo/Widoco",
                          local_repo=None,
                          doc_src=None,
                          in_file=None,
                          output=None,
                          graph_out=test_path,
                          graph_format="turtle",
                          codemeta_out=None,
                          pretty=True,
                          missing=False,
                          readme_only=False)
        g = Graph()
        g.parse(test_path)
        assert len(g) > 10
        os.remove(test_path)

    def test_basic_mapping_export(self):
        """ Uses a local JSON to test whether the mapping works"""
        mapping_path = str(Path(__file__).parent.parent) + os.path.sep + "mapping" + os.path.sep + "rml.ttl"
        data_path = str(Path(__file__).parent) + os.path.sep + "test_data" + os.path.sep + "export_test.json"
        a = turtle_export.DataGraph()
        g = a.apply_mapping(mapping_path, data_path)
        # print(g.serialize(format="turtle", encoding="UTF-8"))
        # the transformed graph has more than 10 triples
        # TO DO: Test that checks the dependency between objects is there: Software, Version, License, SourceCode
        assert len(g) > 10
