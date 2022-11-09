from rdflib import RDF, Graph, Literal, URIRef, Namespace
import datetime

from ..schema.software_schema import get_prefixes, software_schema


class DataGraph:
    def __init__(self):
        self.g = Graph()
        self.prefixes = {}

    def update_lookup_prefixes(self, prefixes):
        self.prefixes.update(prefixes)

    def bind_prefixes(self, prefixes):
        for key, value in prefixes.items():
            self.g.bind(key, Namespace(value))

    def add_somef_data(self, somef_data):
        software_prefixes = get_prefixes()
        current_date = datetime.datetime.now()
        # process the somef output into data
        data = DataGraph.process_somef(somef_data)
        if 'name' not in data.keys():
            data['name'] = 'Software'+current_date.strftime("%Y%m%d%H%M%S")
        if 'fullName' not in data.keys():
            data['fullName'] = 'Software'+current_date.strftime("%Y%m%d%H%M%S")
        # add the prefixes that we use in the software_schema
        self.prefixes.update(software_prefixes)
        self.bind_prefixes(software_prefixes)
        # add the data to the graph, using the software_schema
        self.data_to_graph(data, software_schema)

    # discard the excerpt and confidence stuff
    @staticmethod
    def process_somef(data):
        out = {}
        for key, value in data.items():
            # if the value is a list, preserve the list
            if isinstance(value, list) or isinstance(value, tuple):
                if len(value) > 0:
                    try:
                        out[key] = [obj["excerpt"] for obj in value]
                    except:
                        print("Error when generating "+key)
            # if it is not a list, just get the excerpt
            else:
                out[key] = value["excerpt"]

        return out

    @staticmethod
    def is_array(value):
        return isinstance(value, tuple) or isinstance(value, list)

    @staticmethod
    def combine_dict(in_dict, method=None):
        length = max([len(val) if DataGraph.is_array(val) else -1 for val in in_dict.values()])

        # in this case, we are already flattened
        if length == -1:
            if method is not None:
                return method(in_dict)
            else:
                return in_dict
        else:
            return [
                DataGraph.combine_dict(
                    {key: value[i] if DataGraph.is_array(value) else value
                     for key, value in in_dict.items()},
                    method=method
                ) for i in range(length)
            ]

    def format_string(self, format, data):
        template_string = format["@format"]
        arg_lists = {key: DataGraph.resolve_path(data, path) for (key, path) in format.items() if key[0] != "@"}

    @staticmethod
    def recursive_map(data, method):
        if DataGraph.is_array(data):
            return [DataGraph.recursive_map(value, method) for value in data]
        else:
            return method(data)

    def data_to_graph(self, data, schema):
        assert("@class" in schema and "@id" in schema)

        # TODO: there may be some rare case where we want to allow repeated objects
        # this should be able to be solved via a @repeat flag
        def add_to_g(x_dict):
            x_triple = (x_dict["s"], x_dict["v"], x_dict["o"])
            if None not in x_triple and x_triple not in self.g:
                self.g.add(x_triple)

        # first get the id
        data_id = schema["@id"]
        if isinstance(data_id, dict):
            # resolve the format string
            args = {key: DataGraph.resolve_path(data, path) for (key, path) in data_id.items() if key[0] != "@"}
            # if we can't get all the arguments, our ID won't make sense, and we can't create this object
            if None in args.values():
                return None
            data_id = DataGraph.combine_dict(args, lambda x: data_id["@format"].format(**x))

        rdf_id = self.resolve_type(data_id)

        # then, get the type
        rdf_type = self.resolve_type(schema["@class"])
        triple_dict = {"s": rdf_id, "v": RDF.type, "o": rdf_type}

        # do a flatten operation to get all in the graph
        DataGraph.combine_dict(triple_dict, add_to_g)

        pairs = [(key, value) for key, value in schema.items() if key[0] != "@"]
        for attr_name, attr_schema_list in pairs:
            rdf_attr = self.resolve_type(attr_name)

            if not DataGraph.is_array(attr_schema_list):
                attr_schema_list = [attr_schema_list]

            # the schema can include multiple places to look for the data
            for attr_schema in attr_schema_list:
                if "@class" in attr_schema and "@id" in attr_schema:
                    # in this case, we are dealing with a specific instance of a class
                    # create the instance of that object in the graph
                    rdf_value = self.data_to_graph(data, attr_schema)
                elif "@type" in attr_schema and "@path" in attr_schema:
                    # in this case, we are just dealing with a specific attribute
                    # get the value of the attribute from the data object
                    obj_value = DataGraph.resolve_path(data, attr_schema["@path"])
                    # get the type of the attribute from the schema object
                    obj_type = self.resolve_type(attr_schema["@type"])
                    # combine the value and type in a Literal
                    obj = {"value": obj_value, "type": obj_type}
                    rdf_value = DataGraph.combine_dict(
                        obj,
                        lambda x: Literal(x["value"], datatype=x["type"]) if x["value"] is not None else None
                    )
                else:
                    exit(f"{attr_schema} not a valid value")
                    return None  # needed because the linter doesn't know exit is a return

                # add the object to the graph if it does not already exist


                triple = {"s": rdf_id, "v": rdf_attr, "o": rdf_value}
                DataGraph.combine_dict(triple, add_to_g)

        return rdf_id

    @staticmethod
    def resolve_path(obj, path):
        if isinstance(path, str):
            path = [path]
        return DataGraph.resolve_path_helper(obj, path)

    @staticmethod
    def resolve_path_helper(obj, path):
        if len(path) == 0:
            return obj
        elif isinstance(obj, list) or isinstance(obj, tuple):
            return [DataGraph.resolve_path(item, path) for item in obj]
        else:
            try:
                next_obj = obj[path[0]]
            except KeyError:
                return None
            except TypeError:
                return None

            return DataGraph.resolve_path(next_obj, path[1:])

    def resolve_type(self, type_name):
        return DataGraph.recursive_map(type_name, self.resolve_type_helper)

    def resolve_type_helper(self, type_name):
        # split the string around the colon
        colon_index = type_name.index(":")
        type_prefix = type_name[0:colon_index]
        type_id = type_name[colon_index + 1:]

        # get the namespace corresponding to the type
        if type_prefix in self.prefixes:
            namespace = Namespace(self.prefixes[type_prefix])
            return namespace[type_id]
        # if there is no namespace, then just treat this as a full URI
        else:
            return URIRef(type_name)


if __name__ == "__main__":
    software_prefixes = get_prefixes()
    test_software = {
        "fullName":"test/test",
        "description":"test",
        "owner": {
            "login":"test"
        },
        "releases": [
            {
                "tag_name": "0"
            },
            {
                "tag_name": "1"
            }
        ]
    }

    schema_table = {
        "@class": "sd:Software",
        "@id": {
            "@format": "obj:Software/{name}",
            "name": "fullName"
        },
        "sd:name": {
            "@path": "fullName",
            "@type": "xsd:string"
        },
        "sd:description": {
            "@path": "description",
            "@type": "xsd:string"
        },
        "sd:hasAuthor": {
            "@class": "schema:Person",
            "@id": {
                "@format": "obj:Person/{name}",
                "name": ["owner", "login"]
            },
            "sd:additionalName": {
                "@path": ["owner", "login"],
                "@type": "schema:Text"
            }
        },
        "sd:hasVersion": {
            "@class": "sd:SoftwareVersion",
            "@id": {
                "@format": "obj:SoftwareVersion/{name}/{tag_name}",
                "tag_name": ["releases", "tag_name"],
                "name": "fullName"
            },
            "sd:hasVersionId": {
                "@path": ["releases", "tag_name"],
                "@type": "xsd:string"
            }
        }
    }

    data_graph = DataGraph()
    data_graph.update_lookup_prefixes(software_prefixes)
    data_graph.bind_prefixes(software_prefixes)

    data_graph.data_to_graph(test_software, schema_table)

    print(data_graph.g.serialize(format='turtle').decode('utf-8'))
