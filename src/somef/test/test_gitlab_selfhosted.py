import os
import json
import unittest
from pathlib import Path
from .. import somef_cli
from ..utils import constants

test_data_path = str(Path(__file__).parent / "test_data") + os.path.sep

class TestGitlabSelfHosted(unittest.TestCase):    

    def test_gitlab_self_hosted(self):
            """Checks if SOMEF works against server self_hosted Gitlab . Full analysis"""
            somef_cli.run_cli(threshold=0.8,
                            repo_url="https://gitlab.in2p3.fr/gammalearn/gammalearn",
                            output=test_data_path + "test-self-hosted-gitlab.json",
                            pretty=True,
                            readme_only=False)
            text_file = open(test_data_path + "test-self-hosted-gitlab.json", "r")
            data = text_file.read()
            text_file.close()
            json_content = json.loads(data)
            download = json_content[constants.CAT_DOWNLOAD_URL]
            assert download is not None
            os.remove(test_data_path + "test-self-hosted-gitlab.json")