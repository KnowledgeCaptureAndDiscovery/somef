
software_prefixes = {
    "schema": "https://schema.org/",
    "sd": "https://w3id.org/okn/o/sd#",
    "xsd": str(XSD),
    "obj": "http://w3id.org/okn/o/i/"
}


codemeta_schema = {
    "schema:codeRepository": {
        "@path": "codeRepository",
        "@type": "schema:URL"
    },
    "schema:url": {
        "@path": "codeRepository",
        "@type": "schema:URL"
    },
    "schema:programmingLanguage": {
        "@path": "languages",
        "@type": "schema:Text"
    },
    "schema:keywords": {
        "@path": ["topics"],
        "@type": "schema:Text"
    },
    "schema:license": {
        "@path": ["license", "url"],
        "@type": "schema:URL"
    },
    "schema:author": {
        "@class": "schema:Person",
        "@id": {
            "@format": "obj:Person/{name}",
            "name": "owner"
        },
        "schema:additionalName": {
            "@path": "owner",
            "@type": "schema:Text"
        }
    },
    "meta:issueTracker": {
        "@path": "issueTracker",
        "@type": "schema:URL"
    },
    # how do I add the reference citation
    # How do we deal with versions? It seems like codemeta is expecting it to only be one version?
    # Question: It looks like our outputted object should be of class schema:SoftwareSourceCode rather than schema:SoftwareApplication?
    # we can link back to a targetProduct. Should we?
    # I am having trouble understanding the domains and ranges of the terms defined by codemeta

    # version specific stuff:
    "schema:downloadUrl": [
        {
            "@path": ["releases", "tarball_url"],
            "@type": "schema:URL"
        },
        {
            "@path": ["releases", "zipball_url"],
            "@type": "schema:URL"
        },
    ],
    "schema:softwareVersion": {
        "@path": ["releases", "tag_name"],
        "@type": "schema:Text",
    },
    "schema:releaseNotes": {
        "@path": ["releases", "body"],
        "@type": "schema:Text",
    },
    "schema:dateCreated": {
        "@path": ["releases", "dateCreated"],
        "@type": "schema:DateTime"
    },
    "schema:datePublished": {
        "@path": ["releases", "datePublished"],
        "@type": "schema:DateTime"
    },
}