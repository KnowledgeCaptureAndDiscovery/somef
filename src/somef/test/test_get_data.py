import unittest
import json
from somef.test.utils_for_tests import  almost_equal

from somef.cli import cli_get_data
class CliGetData(unittest.TestCase):

    exclude_paths = [
            ['stargazers_count', 'excerpt', 'date'],
            ['forks_count', 'excerpt', 'date'],
            ['readme_url', 'excerpt']
        ]

    def setUp(self):
        pass


    def test_get_widoco_with_version(self):
        thresh = 0.8
        repo_url = "https://github.com/dgarijo/Widoco/tree/07d138baefd1a20e15740edc484a942328c5e974"

        with open("widoco_reference.json", "r") as data_file:
            widoco_reference = json.load(data_file)


        current_data = cli_get_data(thresh, repo_url=repo_url)
        print(current_data)
        print(widoco_reference)

        self.assertTrue(almost_equal(current_data, widoco_reference, exclude_paths=self.exclude_paths))

    # This test is too restrictive, since we are adding changes to somef almost all the time, and it does not validate
    # functionality.
    # def test_get_widoco_from_readme(self):
    #     thresh = 0.8
    #     doc_src = "widoco_readme.md"
    #
    #     with open("widoco_readme_reference.json", "r") as data_file:
    #         widoco_readme_reference = json.load(data_file)
    #
    #     current_data = cli_get_data(thresh, doc_src=doc_src)
    #
    #     self.assertDictEqual(current_data, widoco_readme_reference)



if __name__ == '__main__':
    unittest.main()