import unittest
import os
from pathlib import Path

from .. import extract_workflows

test_data_repositories = str(Path(__file__).parent / "test_data") + os.path.sep


class TestWorkflows(unittest.TestCase):
    def test_is_workflow(self):
        workflow = extract_workflows.is_file_workflow(test_data_repositories + "SimulatedReads2Map.wdl")
        assert workflow, "The file does contain a workflow."

    def test_is_workflow_fake(self):
        workflow = extract_workflows.is_file_workflow(
            test_data_repositories + "repositories/wav2letter/scripts/arrayfire_parser.py")
        assert (workflow is False)
