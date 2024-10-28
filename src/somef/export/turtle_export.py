import datetime
import json
import logging
import os
import tempfile
from pathlib import Path

import morph_kgc
from rdflib import Graph

from ..utils import constants


class DataGraph:
    def __init__(self):
        self.g = Graph()

    def somef_data_to_graph(self, somef_data):
        """
        Method that returns a Result.results (i.e., a JSON with all the categories found) into RDF
        This method does some operations in order to improve the quality of the final graph.
        Parameters
        ----------
        @param somef_data: JSON to transform into RDF

        Returns
        -------
        @returns: No value
        """
        current_date = datetime.datetime.now()
        data = self.reconcile_somef_data(somef_data)
        if len(data.keys()) == 0:
            logging.warning("No fields were found in file")
            return
        if constants.CAT_NAME not in data.keys():
            data['name'] = 'Software' + current_date.strftime("%Y%m%d%H%M%S")
        if constants.CAT_FULL_NAME not in data.keys():
            data['fullName'] = data['name']
        # save JSON in temp file
        temp_file = "tmp"+current_date.strftime("%Y%m%d%H%M%S")+".json"
        with open(temp_file, 'w') as output:
            json.dump(data, output)
        result_graph = self.apply_mapping(constants.mapping_path, output.name)
        self.g += self.g + result_graph
        os.remove(output.name)
        # temp_file = tempfile.NamedTemporaryFile()
        # with open(temp_file.name, 'w') as output:
        #     json.dump(data, output)
        # result_graph = self.apply_mapping(constants.mapping_path, output.name)
        # self.g += self.g + result_graph

    @staticmethod
    def reconcile_somef_data(data):
        """
        Method to reconcile all somef data to produce a KG of the repository
        Mappings cannot be applied due to the nature of the data.
        This method does not export at the moment provenance information.
        Parameters
        ----------
        @param data: JSON data to be processed

        Returns
        -------
        @return a clean JSON output removing confidence and provenance information to transform

        """
        out = {}
        for key, value in data.items():
            # for now, we are not exporting provenance keys. Ignore all keys like somef_provenance
            if "somef" not in key:
                # if the value is a list, preserve the list
                if isinstance(value, list) or isinstance(value, tuple):
                    if len(value) > 0:
                        if key == constants.CAT_LICENSE:
                            # Create a License object with its id, URL, name and sameAs spdx identifier URL.
                            # We don't keep the license content, as in a KG it may be too many file text
                            license_result = {}
                            for l in data[key]:
                                if constants.PROP_SPDX_ID in l[constants.PROP_RESULT].keys():
                                    license_result[constants.PROP_SPDX_ID] = l[constants.PROP_RESULT][
                                        constants.PROP_SPDX_ID]
                                if constants.PROP_NAME in l[constants.PROP_RESULT].keys():
                                    license_result[constants.PROP_NAME] = l[constants.PROP_RESULT][constants.PROP_NAME]
                                if constants.PROP_URL not in license_result.keys() and constants.PROP_URL in \
                                        l[constants.PROP_RESULT].keys():
                                    license_result[constants.PROP_URL] = l[constants.PROP_RESULT][constants.PROP_URL]
                                # We get the first license we find from the repo
                                elif l[constants.PROP_TECHNIQUE] == constants.TECHNIQUE_FILE_EXPLORATION \
                                        and constants.PROP_SOURCE in l.keys() and "api.github.com" in \
                                        license_result[constants.PROP_URL]:
                                    license_result[constants.PROP_URL] = l[constants.PROP_SOURCE]
                            out["license"] = license_result
                        elif key in [constants.CAT_DOWNLOAD, constants.CAT_USAGE, constants.CAT_INSTALLATION]:
                            # if there are multiple excerpts in separate sub-headers we concatenate them
                            aggregated_value = ""
                            other_results = []
                            for result in data[key]:
                                if result[constants.PROP_TECHNIQUE] == constants.TECHNIQUE_HEADER_ANALYSIS:
                                    # Note: this could be improved by adding as many '#' as parent headers
                                    aggregated_value += "##" + result[constants.PROP_RESULT][
                                        constants.PROP_ORIGINAL_HEADER] + "\n"
                                    aggregated_value += result[constants.PROP_RESULT][constants.PROP_VALUE]
                                else:
                                    other_results.append(result[constants.PROP_RESULT][constants.PROP_VALUE])
                            # if there are file dumps like install.md, they are separate values for the property
                            other_results.append(aggregated_value)
                            out[key] = other_results

                        elif key == constants.CAT_CITATION:
                            # from each publication, we take its DOI or URL (if available from the previous extraction)
                            # Note: This is a point of improvement to have a proper Publication object.
                            citation_urls = []
                            for cite in data[key]:
                                result = cite[constants.PROP_RESULT]
                                if constants.PROP_DOI in result.keys():
                                    citation_urls.append(result[constants.PROP_DOI])
                                elif constants.PROP_URL in result.keys():
                                    citation_urls.append(result[constants.PROP_URL])
                            if len(citation_urls) > 0:
                                # remove duplicates
                                citation_urls = list(set(citation_urls))
                                out[key] = citation_urls
                        elif key == constants.CAT_DOCUMENTATION:
                            # we only keep links
                            doc_links = [obj[constants.PROP_RESULT][constants.PROP_VALUE] for obj in value if
                                         obj[constants.PROP_RESULT][constants.PROP_TYPE] == constants.URL]
                            if len(doc_links) > 0:
                                out[key] = doc_links
                        elif key == constants.CAT_OWNER:
                            out[key] = value[0][constants.PROP_RESULT]
                        elif key == constants.CAT_RELEASES:
                            # we keep the full object
                            out[key] = [obj[constants.PROP_RESULT] for obj in value]
                            # we add a special property (hack) for making the mapping work
                            out[constants.AUX_RELEASES_IDS] = [obj[constants.PROP_RESULT][constants.PROP_RELEASE_ID] for obj in value]
                        else:
                            try:
                                if len(value) == 1:
                                    # remove list for easing mapping
                                    out[key] = value[0][constants.PROP_RESULT][constants.PROP_VALUE]
                                else:
                                    out[key] = [obj[constants.PROP_RESULT][constants.PROP_VALUE] for obj in value]
                            except:
                                logging.warning("Error when converting field in RDF: " + key)
                # if it is not a list, just get the excerpt
                else:
                    out[key] = value[constants.PROP_RESULT][constants.PROP_VALUE]
        # print(json.dumps(out))
        return out

    @staticmethod
    def apply_mapping(mapping_path, data_path) -> Graph:
        """
        Given a mapping file and a data file, this method returns the MORPH-KGC materialization for the mapping
        Parameters
        ----------
        @param mapping_path: file path of the mapping
        @param data_path: file path with the JSON data to transform

        Returns
        -------
        An RDF graph with the desired triples
        """
        # mini test for morph-kgc
        config = constants.MAPPING_CONFIG
        # TO DO: Change RML URIs if they have been changed in the configuration.
        config = config.replace("$PATH", mapping_path).replace("$DATA", data_path)
        return morph_kgc.materialize(config)

    def export_to_file(self, path, graph_format):
        """
        Function to save the RDF graph in a file
        Parameters
        ----------
        @param path: output path where to save the file
        @param graph_format: format of the serialization (TTL, JSON-LD)

        Returns
        -------
        @returns no value
        """
        try:
            logging.info("Saving RDF data to " + str(path))
            with open(path, "wb") as out_file:
                out_file.write(self.g.serialize(format=graph_format, encoding="UTF-8"))
        except Exception as e:
            logging.error("Error while saving RDF results "+str(e))
