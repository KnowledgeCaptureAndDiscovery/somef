# -*- coding: utf-8 -*-
import unittest
import os
from pathlib import Path

from somef.process_results import Result
from somef.parser.julia_parser import parse_project_toml
from somef.utils import constants

test_data_path = str(Path(__file__).parent / "test_data" / "repositories") + os.path.sep


class TestJuliaParser(unittest.TestCase):

    def test_parse_pluto_project_toml(self):
        """Test parsing Pluto's Project.toml file"""
        project_file_path = test_data_path + "Pluto.jl" + os.path.sep + "Project.toml"
        result = Result()

        metadata_result = parse_project_toml(project_file_path, result, "http://example.com/repo1/Project.toml")

        package_results = metadata_result.results.get(constants.CAT_HAS_PACKAGE_FILE, [])
        self.assertTrue(len(package_results) > 0, "No package file info found")
        self.assertEqual(package_results[0]["result"]["value"], "Project.toml")
        self.assertEqual(package_results[0]["result"]["type"], constants.URL)
        self.assertEqual(package_results[0]["technique"], constants.TECHNIQUE_CODE_CONFIG_PARSER)

        package_id_results = metadata_result.results.get(constants.CAT_PACKAGE_ID, [])
        self.assertTrue(len(package_id_results) > 0, "No package ID found")
        self.assertEqual(package_id_results[0]["result"]["value"], "Pluto")
        self.assertEqual(package_id_results[0]["result"]["type"], constants.STRING)

        version_results = metadata_result.results.get(constants.CAT_VERSION, [])
        self.assertTrue(len(version_results) > 0, "No version found")
        self.assertEqual(version_results[0]["result"]["value"], "0.20.20")
        self.assertEqual(version_results[0]["result"]["type"], constants.STRING)

        identifier_results = metadata_result.results.get(constants.CAT_IDENTIFIER, [])
        self.assertTrue(len(identifier_results) > 0, "No identifier found")
        self.assertEqual(identifier_results[0]["result"]["value"], "c3e4b0f8-55cb-11ea-2926-15256bba5781")
        self.assertEqual(identifier_results[0]["result"]["type"], constants.STRING)

        author_results = metadata_result.results.get(constants.CAT_AUTHORS, [])
        self.assertTrue(len(author_results) > 0, "No author found")
        self.assertEqual(author_results[0]["result"]["name"], "Fons van der Plas")
        self.assertEqual(author_results[0]["result"]["email"], "fons@plutojl.org")
        self.assertEqual(author_results[0]["result"]["type"], constants.AGENT)

        requirements_results = metadata_result.results.get(constants.CAT_REQUIREMENTS, [])
        self.assertTrue(len(requirements_results) > 0, "No dependencies found")

        dep_values = [req["result"]["value"] for req in requirements_results]
        self.assertIn("HTTP", dep_values)
        self.assertIn("Markdown", dep_values)
        self.assertIn("Pkg", dep_values)
        self.assertIn("REPL", dep_values)

        for req in requirements_results:
            self.assertEqual(req["result"]["type"], constants.STRING)
            self.assertEqual(req["technique"], constants.TECHNIQUE_CODE_CONFIG_PARSER)

        runtime_results = metadata_result.results.get(constants.CAT_RUNTIME_PLATFORM, [])
        self.assertTrue(len(runtime_results) > 0, "No runtime platform info found")

        # Random check for runtime platforms with versions
        runtime_dict = {r["result"]["package"]: r["result"]["version"] for r in runtime_results}
        self.assertIn("HTTP", runtime_dict)
        self.assertEqual(runtime_dict["HTTP"], "^1.10.17")
        self.assertIn("julia", runtime_dict)
        self.assertEqual(runtime_dict["julia"], "^1.10")

        for runtime in runtime_results:
            self.assertEqual(runtime["result"]["type"], constants.STRING)
            self.assertEqual(runtime["technique"], constants.TECHNIQUE_CODE_CONFIG_PARSER)

    def test_parse_flux_project_toml(self):
        """Test parsing Flux's Project.toml file"""
        project_file_path = test_data_path + "Flux.jl" + os.path.sep + "Project.toml"
        result = Result()

        metadata_result = parse_project_toml(project_file_path, result, "http://example.com/repo2/Project.toml")

        package_results = metadata_result.results.get(constants.CAT_HAS_PACKAGE_FILE, [])
        self.assertTrue(len(package_results) > 0, "No package file info found")
        self.assertEqual(package_results[0]["result"]["value"], "Project.toml")

        package_id_results = metadata_result.results.get(constants.CAT_PACKAGE_ID, [])
        self.assertTrue(len(package_id_results) > 0, "No package ID found")
        self.assertEqual(package_id_results[0]["result"]["value"], "Flux")
        self.assertEqual(package_id_results[0]["result"]["type"], constants.STRING)

        version_results = metadata_result.results.get(constants.CAT_VERSION, [])
        self.assertTrue(len(version_results) > 0, "No version found")
        self.assertEqual(version_results[0]["result"]["value"], "0.16.5")
        self.assertEqual(version_results[0]["result"]["type"], constants.STRING)

        identifier_results = metadata_result.results.get(constants.CAT_IDENTIFIER, [])
        self.assertTrue(len(identifier_results) > 0, "No identifier found")
        self.assertEqual(identifier_results[0]["result"]["value"], "587475ba-b771-5e3f-ad9e-33799f191a9c")
        self.assertEqual(identifier_results[0]["result"]["type"], constants.STRING)

        author_results = metadata_result.results.get(constants.CAT_AUTHORS, [])
        self.assertEqual(len(author_results), 0, "No authors should be found in Flux's Project.toml")

        requirements_results = metadata_result.results.get(constants.CAT_REQUIREMENTS, [])
        self.assertTrue(len(requirements_results) > 0, "No dependencies found")

        dep_values = [req["result"]["value"] for req in requirements_results]
        self.assertIn("Zygote", dep_values)
        self.assertIn("NNlib", dep_values)
        self.assertIn("Optimisers", dep_values)
        self.assertIn("LinearAlgebra", dep_values)

        runtime_results = metadata_result.results.get(constants.CAT_RUNTIME_PLATFORM, [])
        self.assertTrue(len(runtime_results) > 0, "No runtime platform info found")

        # Random check for runtime platforms with versions
        runtime_dict = {r["result"]["package"]: r["result"]["version"] for r in runtime_results}
        self.assertIn("julia", runtime_dict)
        self.assertEqual(runtime_dict["julia"], "1.10")
        self.assertIn("NNlib", runtime_dict)
        self.assertEqual(runtime_dict["NNlib"], "0.9.22")
        self.assertIn("Zygote", runtime_dict)
        self.assertEqual(runtime_dict["Zygote"], "0.6.67, 0.7")

if __name__ == "__main__":
    unittest.main()