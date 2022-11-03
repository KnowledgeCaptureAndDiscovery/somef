from rdflib import XSD
from .. import configuration, constants


def get_prefixes():
    """
    Function that returns the prefixes to use in the mapping based on the config file
    Returns
    -------
    An object with the prefixes to be used
    """
    config = configuration.get_configuration_file()
    try:
        instance_prefix = config[constants.CONF_BASE_URI]
    except ValueError:
        # An error may occur if somef was not properly configured
        instance_prefix = constants.CONF_DEFAULT_BASE_URI
    software_prefixes = {
        "schema": "https://schema.org/",
        "sd": "https://w3id.org/okn/o/sd#",
        "xsd": str(XSD),
        "obj": instance_prefix
    }
    return software_prefixes


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
    "sd:hasAcknowledgments": {
        "@path": "acknowledgments",
        "@type": "xsd:string"
    },
    "sd:hasInstallationInstructions": {
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
    "sd:hasDownloadUrl": [
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
        "@path": ["license", "licenseFile", "url"],
        "@type": "xsd:anyURI"
    },
    "sd:licenseText": {
        "@path": ["licenseText"],
        "@type": "xsd:string"
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
    "sd:hasFAQ": {
        "@path": ["faq", "excerpt"],
        "@type": "xsd:string",
    },
    "sd:hasExecutableNotebook": {
        "@path": ["executableExample", "excerpt"],
        "@type": "xsd:anyURI"
    },
    "sd:hasCodeOfConduct": {
        "@path": "codeOfConduct",
        "@type": "xsd:anyURI"
    },
    "sd:dateCreated": {
        "@path": "dateCreated",
        "@type": "xsd:dateTime"
    },
    "sd:dateModified": {
        "@path": "dateModified",
        "@type": "xsd:dateTime"
    },
    "sd:hasAcknowledgement": {
        "@path": ["acknowledgement", "excerpt"],
        "@type": "xsd:string"
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
    "sd:referencePublication": {
        "@path": "arxivLinks",
        "@type": "xsd:string"
    },
    "sd:hasBuildFile": {
        "@path": "hasBuildFile",
        "@type": "xsd:string"
    },
    "sd:identifier": {
        "@path": "identifier",
        "@type": "xsd:string"
    },
    "sd:issueTracker": {
        "@path": "issueTracker",
        "@type": "xsd:anyURI"
    },
    "sd:hasLongName": {
        "@path": "long_title",
        "@type": "xsd:string"
    },
    "sd:readme": {
        "@path": "readme_url",
        "@type": "xsd:anyURI"
    },
    "sd:contributor": {
        "@path": "contributors",
        "@type": "xsd:string"
    },
    "sd:contributingGuidelines": {
        "@path": "contributingGuidelines",
        "@type": "xsd:string"
    },
    "sd:datePublished": {
        "@path": "datePublished",
        "@type": "xsd:dateTime"
    },
    "sd:hasExample": {
        "@path": "executableExample",
        "@type": "xsd:string"
    },
    "sd:hasSupportScriptLocation": {
        "@path": "hasScriptFile",
        "@type": "xsd:anyURI"
    },
    "sd:hasExecutableInstructions": [
        {
            "@path": "invocation",
            "@type": "xsd:string"
        },
        {
            "@path": "run",
            "@type": "xsd:string"
        }
    ],
    "sd:supportDetails": {
        "@path": "support_channel",
        "@type": "xsd:anyURI"
    }

}
