import logging

from .utils import constants
from . import __version__
import datetime


class Result:
    """
    Class designed to store results found by SOMEF.
    For more information, see the output JSON documentation at: docs/output.md
    """

    def __init__(self):
        """
        init method for the main object to return.
        By default, the provenance of the execution and the version of somef are also returned
        """
        self.results = {
            constants.PROP_PROVENANCE: {
                constants.PROP_SOMEF_VERSION: __version__,
                constants.PROP_SOMEF_SCHEMA_VERSION: "1.0.0",
                constants.PROP_DATE: datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
        }

    def add_result(self, category, result, confidence, technique, source=""):
        """
        Method designed to add a result for a category (i.e., a new description is found)
        Parameters
        ----------
        @param category: one of the fields SOMEF recognizes (see Constants.CAT)
        @param result: a dictionary with at least value and type
        @param confidence: confidence in the extraction (0..1)
        @param technique: technique used in the extraction
        @param source: source file used for the extraction (if any)
        """
        # Sanity check: a result must have a type and a value
        if isinstance(result, dict) and \
                constants.PROP_VALUE in result.keys() and \
                constants.PROP_TYPE in result.keys():
            result = {constants.PROP_RESULT: result,
                      constants.PROP_CONFIDENCE: confidence,
                      constants.PROP_TECHNIQUE: technique}

            if source != "":
                result[constants.PROP_SOURCE] = source

            if category in self.results.keys():
                self.results[category].append(result)
            else:
                # Results should always be a list, even if there is only one value (for consistency)
                self.results[category] = [result]
        else:
            logging.error("Tried to add a result without value or type. Discarding it ...")

    def edit_hierarchical_result(self, category, result, confidence, technique, source=""):
        """
        Method to edit a resource that is supposed to be unique with a higher up in the hierarchy.
        For example, if there are 2 licenses or citation files, we only take the upper level one.
        The value replaced is the one in the same category and technique
        Parameters
        ----------
        category: category of the result
        result: new result value
        confidence: confidence value
        technique: in this case, file exploration
        source: new source link

        Returns
        -------
        N/A edits the  metadata result
        """
        for entry in self.results[category]:
            if entry.get(constants.PROP_SOURCE) is not None and entry[constants.PROP_TECHNIQUE] is constants.TECHNIQUE_FILE_EXPLORATION:
                if source != "":
                    entry[constants.PROP_RESULT] = result
                    entry[constants.PROP_SOURCE] = source

    # def consolidate_results(self):
    #   # TO DO: for each category where we may reduce/ improve the results, do so.
    #   # For example, here is where we would detect if there are redundant citation files, and we would create a single
    #   # publication object.
    #
    #     # if multiple licenses are found, keep only the outmost one.
    #
    #     return self.results
