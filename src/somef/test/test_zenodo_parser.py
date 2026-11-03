import unittest
import os
from pathlib import Path
from somef.process_results import Result
from somef.parser.zenodo_parser import parse_zenodo_file

test_data_path = str(Path(__file__).parent / "test_data") + os.path.sep
test_data_repositories = str(Path(__file__).parent / "test_data" / "repositories") + os.path.sep


class TestZenodoParser(unittest.TestCase):

    def test_issue_826_creators_contributors_license(self):
        """Checks if this repository has properties extracted from .zenodo.json. datacarpentry/cloud-genomics repository"""
        zenodo_file_path = test_data_repositories + "cloud-genomics" + os.path.sep + ".zenodo.json"
        result = Result()

        metadata_result = parse_zenodo_file(
            zenodo_file_path,
            result,
            zenodo_file_path
        )

        authors = metadata_result.results.get("author", [])
        author_names = [entry["result"]["value"] for entry in authors]
        self.assertEqual(len(authors), 13)
        self.assertIn("Amanda Charbonneau", author_names)
        self.assertIn("Serah Njambi", author_names)
        for entry in authors:
            self.assertEqual(entry["technique"], "code_parser")

        serah = next(a for a in authors if a["result"]["value"] == "Serah Njambi")
        self.assertEqual(serah["result"]["identifier"], "https://orcid.org/0000-0002-7834-1038")

        contributors = metadata_result.results.get("contributor", [])
        contributor_names = [entry["result"]["value"] for entry in contributors]
        self.assertEqual(contributor_names, ["Amanda Charbonneau", "Wendy Wong", "Anuj Guruacharya"])

        licenses = metadata_result.results.get("license", [])
        self.assertEqual(len(licenses), 1)
        self.assertEqual(licenses[0]["result"]["value"], "CC-BY-4.0")
        self.assertEqual(licenses[0]["result"]["spdx_id"], "CC-BY-4.0")

    def test_issue_826_description_keywords_names(self):
        """Checks description, keywords, license and creators with 'Family, Given' names. EPIC-model/epic repository"""
        zenodo_file_path = test_data_repositories + "epic" + os.path.sep + ".zenodo.json"
        result = Result()

        metadata_result = parse_zenodo_file(
            zenodo_file_path,
            result,
            zenodo_file_path
        )

        descriptions = metadata_result.results.get("description", [])
        self.assertEqual(len(descriptions), 1)
        self.assertEqual(descriptions[0]["result"]["value"],
                         "The Elliptical Parcel-In-Cell (EPIC) model for fluid dynamics")

        keywords = [entry["result"]["value"] for entry in metadata_result.results.get("keywords", [])]
        self.assertEqual(len(keywords), 5)
        self.assertIn("Lagrangian methods", keywords)

        licenses = metadata_result.results.get("license", [])
        self.assertEqual(licenses[0]["result"]["value"], "BSD-3-Clause")
        self.assertEqual(licenses[0]["result"]["spdx_id"], "BSD-3-Clause")

        authors = metadata_result.results.get("author", [])
        self.assertEqual(len(authors), 4)
        frey = authors[0]["result"]
        self.assertEqual(frey["value"], "Matthias Frey")
        self.assertEqual(frey["given_name"], "Matthias")
        self.assertEqual(frey["last_name"], "Frey")
        self.assertEqual(frey["affiliation"], "University of St Andrews")
        self.assertEqual(frey["identifier"], "https://orcid.org/0000-0002-7842-0051")


    def test_issue_826_all_supported_fields(self):
        """Synthetic .zenodo.json covering every field supported by the parser"""
        zenodo_file_path = test_data_repositories + "fake_zenodo" + os.path.sep + ".zenodo.json"
        result = Result()

        metadata_result = parse_zenodo_file(
            zenodo_file_path,
            result,
            zenodo_file_path
        )
        results = metadata_result.results

        self.assertEqual(results["name"][0]["result"]["value"], "Zenodo Test Software")
        self.assertEqual(results["version"][0]["result"]["value"], "1.2.3")
        self.assertEqual(results["date_published"][0]["result"]["value"], "2024-05-17")

        # HTML must be removed from the description
        description = results["description"][0]["result"]["value"]
        self.assertEqual(description, "Software to test the zenodo parser.")
        self.assertNotIn("<", description)

        keywords = [entry["result"]["value"] for entry in results["keywords"]]
        self.assertEqual(keywords, ["metadata", "research software", "zenodo"])

        # Zenodo ids are lowercase ("apache-2.0"); value is kept, spdx_id is the canonical one
        license_result = results["license"][0]["result"]
        self.assertEqual(license_result["value"], "apache-2.0")
        self.assertEqual(license_result["spdx_id"], "Apache-2.0")
        self.assertEqual(license_result["identifier"], "https://spdx.org/licenses/Apache-2.0")

        authors = [entry["result"] for entry in results["author"]]
        self.assertEqual([a["value"] for a in authors],
                         ["Daniel Garijo", "Maintainer Without Comma", "Only Name"])
        # "Family, Given" is split
        self.assertEqual(authors[0]["given_name"], "Daniel")
        self.assertEqual(authors[0]["last_name"], "Garijo")
        self.assertEqual(authors[0]["affiliation"], "Universidad Politécnica de Madrid")
        self.assertEqual(authors[0]["identifier"], "https://orcid.org/0000-0003-0454-7145")
        # names without a comma are not split
        self.assertNotIn("given_name", authors[1])
        self.assertNotIn("last_name", authors[1])
        # an ORCID already given as URL is not prefixed twice
        self.assertEqual(authors[1]["identifier"], "https://orcid.org/0000-0001-2345-6789")
        self.assertNotIn("identifier", authors[2])

        contributors = [entry["result"] for entry in results["contributor"]]
        self.assertEqual([c["value"] for c in contributors], ["Jane Doe", "Contributor Without Comma"])
        self.assertEqual(contributors[0]["given_name"], "Jane")
        self.assertEqual(contributors[0]["affiliation"], "Example University")

        for category in ["name", "description", "version", "keywords", "license",
                         "date_published", "author", "contributor"]:
            for entry in results[category]:
                self.assertEqual(entry["technique"], "code_parser")


if __name__ == "__main__":
    unittest.main()
