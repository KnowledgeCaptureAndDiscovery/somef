# -*- coding: utf-8 -*-
"""
Unified test suite for TOML parser.
Tests Cargo.toml, pyproject.toml, and Project.toml parsing.
"""

import unittest
import os
from pathlib import Path

from somef.process_results import Result
from somef.parser.toml_parser import parse_toml_file
from somef.utils import constants

test_data_path = str(Path(__file__).parent / "test_data" / "repositories") + os.path.sep


class TestTomlParser(unittest.TestCase):
    """Unified test class for all TOML file types"""

    def setUp(self):
        """Set up test file paths"""
        self.test_dir = os.path.dirname(os.path.abspath(__file__))

        # Cargo.toml test file
        self.cargo_toml_path = os.path.join(
            self.test_dir, "test_data", "repositories", "rustdesk", "Cargo.toml"
        )

        # Project.toml test files (Julia)
        self.pluto_project_path = os.path.join(
            test_data_path, "Pluto.jl", "Project.toml"
        )
        self.flux_project_path = os.path.join(
            test_data_path, "Flux.jl", "Project.toml"
        )

        # pyproject.toml test files
        self.gammalearn_pyproject_path = os.path.join(
            test_data_path, "gammalearn", "pyproject.toml"
        )
        self.inspect4py_pyproject_path = os.path.join(
            test_data_path, "inspect4py", "pyproject.toml"
        )
        self.sunpy_pyproject_path = os.path.join(
            test_data_path, "sunpy", "pyproject.toml"
        )

    # ==================== Cargo.toml Tests ====================

    def test_parse_cargo_toml(self):
        """Test parsing Cargo.toml (Rust) file"""
        self.assertTrue(
            os.path.exists(self.cargo_toml_path),
            f"Test file not found: {self.cargo_toml_path}"
        )

        result = Result()
        # parse_toml_file(self.cargo_toml_path, result, "test")
        print("self.cargo_toml_path:", self.cargo_toml_path)
        # parse_toml_file(self.cargo_toml_path, result, "http://example.com/rustdesk/Cargo.toml")
        parse_toml_file(self.cargo_toml_path, result, self.cargo_toml_path)

        self.assertIn(constants.CAT_HAS_PACKAGE_FILE, result.results)
        package_file = result.results[constants.CAT_HAS_PACKAGE_FILE][0]["result"]["value"]

        # self.assertEqual(package_file, "Cargo.toml")
        self.assertEqual(package_file, self.cargo_toml_path)

        self.assertIn(constants.CAT_PACKAGE_ID, result.results)
        package_id = result.results[constants.CAT_PACKAGE_ID][0]["result"]["value"]
        self.assertEqual(package_id, "rustdesk")

        self.assertIn(constants.CAT_VERSION, result.results)
        version = result.results[constants.CAT_VERSION][0]["result"]["value"]
        self.assertEqual(version, "1.4.0")

        self.assertIn(constants.CAT_DESCRIPTION, result.results)
        description = result.results[constants.CAT_DESCRIPTION][0]["result"]["value"]
        self.assertEqual(description, "RustDesk Remote Desktop")

        self.assertIn(constants.CAT_AUTHORS, result.results)
        authors = result.results[constants.CAT_AUTHORS]
        self.assertEqual(len(authors), 1)
        self.assertEqual(authors[0]["result"]["name"], "rustdesk")
        self.assertEqual(authors[0]["result"]["email"], "info@rustdesk.com")

        self.assertIn(constants.CAT_REQUIREMENTS, result.results)
        dependencies = result.results[constants.CAT_REQUIREMENTS]

        dep_names = [d["result"]["name"] for d in dependencies]
        self.assertIn("async-trait", dep_names)
        self.assertIn("serde", dep_names)
        self.assertIn("lazy_static", dep_names)

    # ==================== Project.toml (Julia) Tests ====================

    def test_parse_pluto_project_toml(self):
        """Test parsing Pluto's Project.toml (Julia) file"""
        result = Result()

        # metadata_result = parse_toml_file(
        #     self.pluto_project_path,
        #     result,
        #     "http://example.com/repo1/Project.toml"
        # )
        
        metadata_result = parse_toml_file(
            self.pluto_project_path,
            result,
            self.pluto_project_path
        )

        package_results = metadata_result.results.get(constants.CAT_HAS_PACKAGE_FILE, [])
        self.assertTrue(len(package_results) > 0, "No package file info found")
        # self.assertEqual(package_results[0]["result"]["value"], "Project.toml")
        self.assertEqual(package_results[0]["result"]["value"], self.pluto_project_path)
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
        self.assertEqual(
            identifier_results[0]["result"]["value"],
            "c3e4b0f8-55cb-11ea-2926-15256bba5781"
        )
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

        runtime_dict = {r["result"]["package"]: r["result"]["version"] for r in runtime_results}
        self.assertIn("HTTP", runtime_dict)
        self.assertEqual(runtime_dict["HTTP"], "^1.10.17")
        self.assertIn("julia", runtime_dict)
        self.assertEqual(runtime_dict["julia"], "^1.10")

        for runtime in runtime_results:
            self.assertEqual(runtime["result"]["type"], constants.STRING)
            self.assertEqual(runtime["technique"], constants.TECHNIQUE_CODE_CONFIG_PARSER)

    def test_parse_flux_project_toml(self):
        """Test parsing Flux's Project.toml (Julia) file"""
        result = Result()

        # metadata_result = parse_toml_file(
        #     self.flux_project_path,
        #     result,
        #     "http://example.com/repo2/Project.toml"
        # )
        metadata_result = parse_toml_file(
            self.flux_project_path,
            result,
            self.flux_project_path
        )

        package_results = metadata_result.results.get(constants.CAT_HAS_PACKAGE_FILE, [])
        self.assertTrue(len(package_results) > 0, "No package file info found")
        # self.assertEqual(package_results[0]["result"]["value"], "Project.toml")
        self.assertEqual(package_results[0]["result"]["value"], self.flux_project_path)

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
        self.assertEqual(
            identifier_results[0]["result"]["value"],
            "587475ba-b771-5e3f-ad9e-33799f191a9c"
        )
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

        runtime_dict = {r["result"]["package"]: r["result"]["version"] for r in runtime_results}
        self.assertIn("julia", runtime_dict)
        self.assertEqual(runtime_dict["julia"], "1.10")
        self.assertIn("NNlib", runtime_dict)
        self.assertEqual(runtime_dict["NNlib"], "0.9.22")
        self.assertIn("Zygote", runtime_dict)
        self.assertEqual(runtime_dict["Zygote"], "0.6.67, 0.7")

    # ==================== pyproject.toml Tests ====================

    def test_parse_gammalearn_pyproject_toml(self):
        """Test parsing gammalearn's pyproject.toml file"""
        result = Result()

        metadata_result = parse_toml_file(
            self.gammalearn_pyproject_path,
            result,
            "https://example.org/pyproject.toml"
        )

        package_id = metadata_result.results.get(constants.CAT_PACKAGE_ID, [])
        self.assertTrue(len(package_id) > 0, "No identifier found")
        self.assertEqual(package_id[0]["result"]["value"], "gammalearn")

        self.assertIn(constants.CAT_DESCRIPTION, result.results)
        description = result.results[constants.CAT_DESCRIPTION][0]["result"]["value"]
        self.assertEqual(
            description,
            "A framework to easily train deep learning model on Imaging Atmospheric Cherenkov Telescopes data"
        )

        self.assertIn(constants.CAT_AUTHORS, result.results)
        authors = result.results[constants.CAT_AUTHORS]
        self.assertEqual(len(authors), 2)
        self.assertEqual(authors[0]["result"]["name"], "M. Jacquemont")
        self.assertEqual(authors[0]["result"]["email"], "jacquemont@lapp.in2p3.fr")
        self.assertEqual(authors[1]["result"]["name"], "T. Vuillaume")
        self.assertEqual(authors[1]["result"]["email"], "thomas.vuillaume@lapp.in2p3.fr")

        self.assertIn(constants.CAT_LICENSE, result.results)
        license_info = result.results[constants.CAT_LICENSE][0]["result"]["value"]
        self.assertEqual(license_info, "License file: LICENSE")

        self.assertIn(constants.CAT_CODE_REPOSITORY, result.results)
        repo_url = result.results[constants.CAT_CODE_REPOSITORY][0]["result"]["value"]
        self.assertEqual(repo_url, "https://gitlab.in2p3.fr/gammalearn/gammalearn")

        self.assertIn(constants.CAT_DOCUMENTATION, result.results)
        doc_url = result.results[constants.CAT_DOCUMENTATION][0]["result"]["value"]
        self.assertEqual(doc_url, "https://gammalearn.pages.in2p3.fr/gammalearn/")

        self.assertIn(constants.CAT_ISSUE_TRACKER, result.results)
        issue_url = result.results[constants.CAT_ISSUE_TRACKER][0]["result"]["value"]
        self.assertEqual(issue_url, "https://gitlab.in2p3.fr/gammalearn/gammalearn/-/issues")

        self.assertIn(constants.CAT_REQUIREMENTS, result.results)
        dependencies = result.results[constants.CAT_REQUIREMENTS]
        self.assertEqual(len(dependencies), 25)

    def test_parse_inspect4py_pyproject_toml(self):
        """Test parsing inspect4py's pyproject.toml file"""
        result = Result()

        metadata_result = parse_toml_file(
            self.inspect4py_pyproject_path,
            result,
            "https://example.org/pyproject.toml"
        )

        self.assertIn(constants.CAT_REQUIREMENTS, result.results)
        dependencies = result.results[constants.CAT_REQUIREMENTS]
        self.assertEqual(
            len(dependencies),
            11,
            "Incorrect number of requirements found in pyproject.toml"
        )

        req_names = [req["result"]["name"] for req in dependencies]
        self.assertIn("bs4", req_names)
        self.assertIn("docstring_parser", req_names)

    def test_parse_sunpy_pyproject_toml_requirements_version(self):
        """Test parsing requirements with version and name from sunpy's pyproject.toml"""
        result = Result()

        metadata_result = parse_toml_file(
            self.sunpy_pyproject_path,
            result,
            "https://example.org/pyproject.toml"
        )

        self.assertIn(constants.CAT_REQUIREMENTS, result.results)
        dependencies = result.results[constants.CAT_REQUIREMENTS]

        for item in dependencies:
            result_data = item.get("result", {})
            version = result_data.get("version", None)
            name = result_data.get("name", None)

            self.assertTrue(
                version is None or name is not None,
                f"Error in requirement: {item}"
            )

    def test_parse_sunpy_pyproject_toml_issue_769(self):
        """Test parsing requirements with brackets (issue #769) from sunpy's pyproject.toml"""
        result = Result()

        metadata_result = parse_toml_file(
            self.sunpy_pyproject_path,
            result,
            "https://example.org/pyproject.toml"
        )

        self.assertIn(constants.CAT_REQUIREMENTS, result.results)
        dependencies = result.results[constants.CAT_REQUIREMENTS]

        self.assertTrue(
            any(
                item.get("result", {}).get("name") == "setuptools_scm[toml]"
                and item.get("result", {}).get("version") == ">=8.0.1"
                for item in dependencies
            ),
            "Expected dependency 'setuptools_scm[toml]' with version '>=8.0.1' not found."
        )

    def test_common_fields_across_formats(self):
        """Test that common fields (name, version, authors) work consistently across all formats"""

        # Test Cargo.toml
        cargo_result = Result()
        parse_toml_file(self.cargo_toml_path, cargo_result, "test")
        self.assertIn(constants.CAT_PACKAGE_ID, cargo_result.results)
        self.assertIn(constants.CAT_VERSION, cargo_result.results)
        self.assertIn(constants.CAT_AUTHORS, cargo_result.results)

        # Test Project.toml
        julia_result = Result()
        parse_toml_file(self.pluto_project_path, julia_result, "test")
        self.assertIn(constants.CAT_PACKAGE_ID, julia_result.results)
        self.assertIn(constants.CAT_VERSION, julia_result.results)
        self.assertIn(constants.CAT_AUTHORS, julia_result.results)

        # Test pyproject.toml
        python_result = Result()
        parse_toml_file(self.gammalearn_pyproject_path, python_result, "test")
        self.assertIn(constants.CAT_PACKAGE_ID, python_result.results)
        self.assertIn(constants.CAT_AUTHORS, python_result.results)


if __name__ == "__main__":
    unittest.main()
