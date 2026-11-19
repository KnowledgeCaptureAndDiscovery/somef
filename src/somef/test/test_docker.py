import os
import tempfile
import unittest
from pathlib import Path

from ..parser.docker_references import detect_docker_commands
from ..parser.dockerfile_parser import parse_dockerfile
from ..process_results import Result
from ..utils import constants

test_data_path = str(Path(__file__).parent / "test_data") + os.path.sep

LABELLED = """FROM python:3.11
LABEL org.opencontainers.image.title="My tool"
LABEL org.opencontainers.image.description="Does useful things"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.url="https://example.org/mytool"
LABEL org.opencontainers.image.version="1.2.3"
LABEL org.opencontainers.image.vendor="ACME"
LABEL org.opencontainers.image.documentation="https://example.org/docs"
MAINTAINER Ana <ana@example.org>
"""


class TestContainerFromDockerfile(unittest.TestCase):

    def _parse(self, content):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "Dockerfile")
            with open(path, "w") as f:
                f.write(content)
            result = Result()
            parse_dockerfile(path, result, "https://example.org/Dockerfile")
            return result.results

    def test_container_from_labels(self):
        container = self._parse(LABELLED)[constants.CAT_CONTAINER][0][constants.PROP_RESULT]
        assert container[constants.PROP_NAME] == "My tool"
        assert container[constants.PROP_DESCRIPTION] == "Does useful things"
        assert container[constants.PROP_LICENSE] == "MIT"
        assert container[constants.PROP_SPDX_ID] == "MIT"
        assert container[constants.PROP_VERSION] == "1.2.3"
        assert container[constants.PROP_DOCUMENTATION] == "https://example.org/docs"
        assert container[constants.PROP_AUTHOR][0][constants.PROP_VALUE] == "Ana <ana@example.org>"

    def test_no_container_without_labels(self):
        assert constants.CAT_CONTAINER not in self._parse("FROM python:3.11\nRUN pip install foo\n")


class TestDockerCommandsInReadme(unittest.TestCase):

    def _detect(self, filename):
        with open(test_data_path + filename) as f:
            return detect_docker_commands(f.read())

    def test_widoco_build_and_run(self):
        found = self._detect("README-widoco.md")
        assert {c["subcommand"] for c in found} == {"build", "run"}
        assert all(c["reference"] == "dgarijo/widoco" for c in found)

    def test_pylops_tag(self):
        found = self._detect("README-pylops.md")
        assert found[0]["reference"] == "mrava87/pylops:notebook"
        assert found[0]["tag"] == "notebook"

    def test_raidologist_indented_block(self):
        found = self._detect("README-raidologist.md")   # FALLA hoy: bloque indentado
        assert found[0]["reference"] == "elviish/raidologist:latest"
        assert found[0]["tag"] == "latest"

    def test_no_false_positives_in_prose(self):
        for filename in ["README-mapshaper.md", "README-tensorflow-2.6.0.md",
                         "README-ci-sample-project.md"]:
            assert self._detect(filename) == [], filename
            
    def test_no_placeholder_images(self):
        with open(test_data_path + "repositories/soca/README.md") as f:
            assert detect_docker_commands(f.read()) == []