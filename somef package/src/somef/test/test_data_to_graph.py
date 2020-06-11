import unittest

from somef.data_to_graph import DataGraph


class Base(unittest.TestCase):
    def setUp(self):
        pass
    # def test_basic(self):
    #     test_software = {
    #         "fullName": "test/test",
    #         "description": "test",
    #         "owner": {
    #             "login": "test"
    #         }
    #     }
    #
    #     schema_table = {
    #         "@class": "sd:Software",
    #         "@id": {
    #             "@format": "obj:Software/{name}",
    #             "name": "fullName"
    #         },
    #         "sd:name": {
    #             "@value": "fullName",
    #             "@type": "xsd:string"
    #         },
    #         "sd:description": {
    #             "@value": "description",
    #             "@type": "xsd:string"
    #         },
    #         "sd:hasAuthor": {
    #             "@class": "schema:Person",
    #             "@id": {
    #                 "@format": "obj:Person/{name}",
    #                 "name": ["owner", "login"]
    #             },
    #             "sd:additionalName": {
    #                 "@value": ["owner", "login"],
    #                 "@type": "schema:Text"
    #             }
    #         }
    #     }
    #
    #     data_graph = DataGraph()
    #     data_graph.somef_to_graph(test_software, schema_table)
    #
    #     for triple in data_graph.g:
    #         print(triple)

class FlattenDict(Base):
    def test_combine_dict(self):

        dict_in = {
            "x": 1,
            "y": [1, 2],
            "z": [[1, 2], ["a", "b"]]
        }

        dict_out = [
            [
                {"x": 1, "y": 1, "z": 1},
                {"x": 1, "y": 1, "z": 2}
            ],
            [
                {"x": 1, "y": 2, "z": "a"},
                {"x": 1, "y": 2, "z": "b"}
            ]
        ]
        dict_actual_out = DataGraph.combine_dict(dict_in)
        for i, _ in enumerate(dict_out):
            for j, _ in enumerate(dict_out[i]):
                self.assertDictEqual(dict_out[i][j], dict_actual_out[i][j])

    def test_combine_dict_method(self):
        dict_in = {
            "x": 1,
            "y": [1, 2]
        }

        string_out = [
            "1/1", "1/2"
        ]

        actual_out = DataGraph.combine_dict(dict_in, method=lambda x: "{x}/{y}".format(**x))

        for i, _ in enumerate(string_out):
            self.assertEqual(string_out[i], actual_out[i])

class ResolvePath(Base):
    def test_resolve_path_array(self):
        test_obj = {
            "x": [
                {
                    "y": [
                        {
                            "z": 1
                        },
                        {
                            "z": 2
                        }
                    ]
                },
                {
                    "y": [
                        {
                            "z": 3
                        },
                        {
                            "z": 4
                        }
                    ]
                }
            ]
        }

        path = ["x", "y", "z"]

        out = DataGraph.resolve_path(test_obj, path)

        self.assertEqual(out, [[1, 2], [3, 4]])


if __name__ == '__main__':
    unittest.main()
