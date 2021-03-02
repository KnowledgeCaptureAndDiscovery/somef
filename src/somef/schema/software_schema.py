from rdflib import XSD

software_prefixes = {
    "schema": "https://schema.org/",
    "sd": "https://w3id.org/okn/o/sd#",
    "xsd": str(XSD),
    "obj": "http://w3id.org/okn/o/i/"
}

software_schema = {
    # class and id
    "@class": "sd:Software",
    "@id": {
        "@format": "obj:Software/{name}",
        "name": "fullName"
    },
    # data from SoMEF
    "sd:description": [
        {
            "@path": "description",
            "@type": "xsd:string"
        },
        {
            "@path": "issues",
            "@type": "xsd:string"
        }
    ],
    "sd:citation": {
        "@path": "citation",
        "@type": "xsd:string"
    },
    "sd:hasInstallInstructions": {
        "@path": "installation",
        "@type": "xsd:string"
    },
    "sd:hasExecutionCommand": [
        {
            "@path": "run",
            "@type": "xsd:string"
        },
        {
            "@path": "invocation",
            "@type": "xsd:string"
        }
    ],
    "sd:hasUsageNotes": {
        "@path": "usage",
        "@type": "xsd:string"
    },
    "sd:downloadUrl": [
        {
            "@path": "downloadUrl",
            "@type": "xsd:anyURI"
        },
        {
            "@path": "download",
            "@type": "xsd:string"
        }
    ],
    "sd:softwareRequirements": {
        "@path": "requirement",
        "@type": "xsd:string"
    },
    "sd:contactDetails": {
        "@path": "contact",
        "@type": "xsd:string"
    },
    "sd:contributionInstructions": {
        "@path": "contributor",
        "@type": "xsd:string"
    },
    # issues was moved in with sd:description
    "sd:supportDetails": {
        "@path": "support",
        "@type": "xsd:string"
    },
    "sd:name": {
        "@path": "fullName",
        "@type": "xsd:string"
    },
    "sd:license": {
        "@path": ["license", "url"],
        "@type": "xsd:anyURI"
    },
    "sd:keywords": {
        "@path": "topics",
        "@type": "xsd:string"
    },
    "sd:hasSourceCode": {
        "@class": "sd:SoftwareSource",
        "@id": {
            "@format": "obj:SoftwareSource/{name}",
            "name": "fullName"
        },
        "sd:codeRepository": {
            "@path": "codeRepository",
            "@type": "xsd:anyURI"
        },
        "sd:programmingLanguage": {
            "@path": "languages",
            "@type": "xsd:string"
        }
    },
    "sd:author": {
        "@class": "schema:Person",
        "@id": {
            "@format": "obj:Person/{name}",
            "name": "owner"
        },
        "sd:additionalName": {
            "@path": "owner",
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
        # "sd:author": {
        #     "@class": "schema:Person",
        #     "@id": {
        #         "@format": "obj:Person/{name}",
        #         "name": ["releases", "author_name"]
        #     },
        #     "sd:additionalName": {
        #         "@path": ["releases", "author_name"],
        #         "@type": "xsd:string"
        #     }
        # },
        "sd:hasVersionId": {
            "@path": ["releases", "tag_name"],
            "@type": "xsd:string"
        },
        "sd:description": {
            "@path": ["releases", "body"],
            "@type": "xsd:string"
        },
        "sd:downloadUrl": [
            {
                "@path": ["releases", "tarball_url"],
                "@type": "xsd:anyURI"
            },
            {
                "@path": ["releases", "zipball_url"],
                "@type": "xsd:anyURI"
            },
            {
                "@path": ["releases", "html_url"],
                "@type": "xsd:anyURI"
            }
        ]
    },
    "sd:hasDocumentation": {
        "@path": "hasDocumentation",
        "@type": "xsd:anyURI"
    },
    "sd:hasBuildFile": {
        "@path": "hasBuildFile",
        "@type": "xsd:string"
    },
    "sd:hasExecutableNotebook": {
        "@path": "hasExecutableNotebook",
        "@type": "xsd:string"
    }
}