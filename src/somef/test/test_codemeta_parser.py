import unittest
import os
import yaml
from pathlib import Path

from somef.parser.codemeta_parser import parse_codemeta_json_file
from somef.process_results import Result
from somef.utils import constants

TEST_ROOT = Path(__file__).parent
REPOS_DIR = TEST_ROOT / "test_data" / "repositories"
EXPECT_DIR = TEST_ROOT / "test_data" / "expected"

class TestCodemetaParser(unittest.TestCase):

    def load_expected(self, repo_name):
        """Load expected YAML for a given repo."""
        yaml_path = EXPECT_DIR / f"{repo_name}.yaml"
        if not yaml_path.exists():
            self.skipTest(f"No expected YAML for repository '{repo_name}'")
        with open(yaml_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def test_parse_multiple_codemeta_files(self):
        for repo_folder in os.listdir(REPOS_DIR):
            print(f"################# Testing {repo_folder} #################")
            repo_path = REPOS_DIR / repo_folder
            codemeta_path = repo_path / "codemeta.json"
            if not codemeta_path.is_file():
                continue 

            expected = self.load_expected(repo_folder)
            result = Result()
            metadata_result = parse_codemeta_json_file(
                str(codemeta_path),
                result,
                "https://example.org/codemeta.json"
            )

            with self.subTest(repo=repo_folder):
                # In order for us to check every test, we need every file in "expected" directory to be of .yaml, 
                # and make sure the name is the same as the repo folder  
                print(f"################# Processing expectation of {repo_folder} #################")
                for cat_name, expected_val in expected.items():
                    cat_const = getattr(constants, cat_name)
                    actual_list = metadata_result.results.get(cat_const, [])
                    self.assertTrue(
                        actual_list,
                        f"[{repo_folder}] No results for {cat_name}"
                    )

                    first = actual_list[0]["result"]
                    if isinstance(expected_val, dict):
                        for key, val in expected_val.items():
                            self.assertEqual(
                                first.get(key), val,
                                f"[{repo_folder}] Mismatch in {cat_name}.{key}"
                            )
                    else:
                        self.assertEqual(
                            first.get("value"), expected_val,
                            f"[{repo_folder}] Mismatch in {cat_name}"
                        )


    def test_parse_contributors(self):
        codemeta_path = REPOS_DIR / "codemeta_repo" / "codemeta.json"
        result = Result()

        metadata_result = parse_codemeta_json_file(codemeta_path, result, "https://example.org/codemeta.json")
        
        self.assertIn(constants.CAT_CONTRIBUTORS, metadata_result.results)
        contributors = result.results[constants.CAT_CONTRIBUTORS]
 
        self.assertTrue(any(
            c["result"]["name"] == "Abby Cabunoc Mayes" and
            c["result"].get("given_name") == "Abby Cabunoc"
            for c in contributors
        ))

        self.assertTrue(any(
            c["result"]["name"] == "Arfon Smith" and
            c["result"].get("identifier") == "http://orcid.org/0000-0002-3957-2474"
            for c in contributors
        ))

        self.assertTrue(any(
            c["result"]["name"] == "Dan Katz" and
            c["result"].get("email") == "dskatz@illinois.edu"
            for c in contributors
        ))


if __name__ == "__main__":
    unittest.main()
