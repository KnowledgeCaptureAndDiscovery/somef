import json
import copy
from . import json_export


def save_google_codemeta_output(repo_data, output_path, pretty=False, requirements_mode="all"):
    """
    Generate a Google-compliant Codemeta JSON-LD file from repo_data.
    """

    # Generate base codemeta using SOMEF. It is basically a codemeta file with a few changes.
    # This way we have the core in the codemeta export and changes about content go just in the first method.

    json_export.save_codemeta_output(
        repo_data,
        output_path,
        pretty=pretty,
        requirements_mode=requirements_mode
    )

    # Load the generated codemeta
    with open(output_path, "r") as f:
        codemeta = json.load(f)

    # Apply google-compliant transformations
    codemeta = make_google_compliant(codemeta)

    # Overwrite the same file (no tmp file)
    with open(output_path, "w") as f:
        if pretty:
            json.dump(codemeta, f, indent=2, sort_keys=True)
        else:
            json.dump(codemeta, f)


SCHEMA_ORG_PROPERTIES = { 
    "@type", 
    "name", 
    "description", 
    "author", 
    "keywords",
    "license",
    "url",
    "identifier",
    "programmingLanguage",
    "releaseNotes",
    "releaseDate"
    }

def make_google_compliant(codemeta):
    codemeta = copy.deepcopy(codemeta)

    # context is different from codemeta
    codemeta["@context"] = { 
        "@vocab": "https://schema.org/", 
        "codemeta": "https://w3id.org/codemeta/3.0/" 
        }

    # Some categories must be in a @list even if only one value is present. Required order
    for prop in ["author", "contributor", "editor"]:
        if prop in codemeta:
            codemeta[prop] = wrap_list(codemeta[prop])

    # referencePublication.author is also a list
    if "referencePublication" in codemeta:
        for pub in codemeta["referencePublication"]:
            if "author" in pub:
                pub["author"] = wrap_list(pub["author"])

    if isinstance(codemeta.get("softwareRequirements"), list): 
        codemeta["softwareRequirements"] = [ 
            r for r in codemeta["softwareRequirements"] if isinstance(r, dict) 
            ]
        
    if isinstance(codemeta.get("developmentStatus"), str): 
        codemeta["developmentStatus"] = codemeta["developmentStatus"].capitalize()

    codemeta = prefix_all_codemeta_properties(codemeta)
    for key, value in codemeta.items(): 
        codemeta[key] = normalize_value(value, key)

    # No mappings. No normalizations. No cleaning.
    # The PR only requires @context and @list wrapping.

    return codemeta


# ------------------------------------------------------------
# UTILITIES
# ------------------------------------------------------------

def wrap_list(value):
    """
    Always wrap lists in @list, even if only one element.
    """
    if isinstance(value, list):
        return {"@list": value}
    return value

def prefix_all_codemeta_properties(codemeta): 
    """ Add codemeta: prefix to all properties that are NOT in Schema.org. """ 
    new = {}

    for key, value in codemeta.items(): 
        if key in SCHEMA_ORG_PROPERTIES or key == "@context": 
            new[key] = value 
        else: 
            new[f"codemeta:{key}"] = value 
    
    return new

def normalize_value(value, key=None):
    """
    Minimal normalization:
    - Only normalize keywords (CSV -> list)
    - Only filter softwareRequirements (remove strings)
    - Do NOT touch any other property
    """

    # keywords: convert CSV to list
    if key == "keywords" and isinstance(value, str):
        parts = [p.strip() for p in value.split(",") if p.strip()]
        return parts

    # softwareRequirements: keep only dicts
    if key == "softwareRequirements" and isinstance(value, list):
        return [v for v in value if isinstance(v, dict)]

    return value


# def apply_schemaorg_mappings(c):
#     """
#     Apply mappings from Codemeta to Schema.org for Google compliance.
#     """

#     # referencePublication  -> citation
#     if "referencePublication" in c:
#         c["citation"] = c.pop("referencePublication")

#     # buildInstructions ->  installUrl (if URL) or softwareHelp
#     if "buildInstructions" in c:
#         bi = c.pop("buildInstructions")
#         if isinstance(bi, list) and len(bi) == 1 and is_url(bi[0]):
#             c["installUrl"] = bi[0]
#         else:
#             c.setdefault("softwareHelp", [])
#             c["softwareHelp"].append({"@type": "CreativeWork", "text": bi})

#     # continuousIntegration -> softwareHelp
#     if "continuousIntegration" in c:
#         ci = c.pop("continuousIntegration")
#         c.setdefault("softwareHelp", [])
#         c["softwareHelp"].append({"@type": "CreativeWork", "url": ci})

#     # readme -> softwareHelp
#     if "readme" in c:
#         rd = c.pop("readme")
#         c.setdefault("softwareHelp", [])
#         c["softwareHelp"].append({"@type": "CreativeWork", "url": rd})

#     # developmentStatus normalization
#     if "developmentStatus" in c:
#         status = c["developmentStatus"]
#         if isinstance(status, str):
#             c["developmentStatus"] = status.capitalize()

#     return c



