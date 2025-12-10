The following metadata fields can be extracted from a AUTHORS file.   
These fields are defined in the [Authors file specification](https://opensource.google/documentation/reference/releasing/authors/), and are mapped according to the [CodeMeta crosswalk for AUTHORS files](https://github.com/codemeta/codemeta/blob/master/crosswalks/codemeta-V2.csv).

| Software metadata category        |   SOMEF metadata JSON path  | AUTHORS metadata file field               |
|-------------------------------|---------------------------------------------|------------------------------|  
| authors - value                  |  authors[i].result.value   |   *(1)* value    |
| authors - name                 |  authors[i].result.name   |    *(2)*   name  |
| authors - email                 |  authors[i].result.email   |   *(3)*   email      |
| authors - given name                 |  authors[i].result.given_name   | *(4)* if type person      |
| authors - last name                 |  authors[i].result.last_name   |  *(5)* if type person     |

---

*(1)*  
- Regex: line.strip()
- Example: `Jane Doe <jane.doe@example.org>`
- Result: `Jane Doe <jane.doe@example.org>`

*(2)*  
- line[:email_match.start()].strip()
- Example: `Jane Doe <jane.doe@example.org>`
- Result: `Jane Doe`

*(3)*  
- Regex: re.search(r'<([^>]+)>', line)
- Example: `Jane Doe <jane.doe@example.org>`
- Result: `jane.doe@example.org`

*(4)*  
- First part of name
- Example: `Jane Doe <jane.doe@example.org>`
- Result: `Jane`

*(5)*  
- Second part of name
- Example: `Jane Doe <jane.doe@example.org>`
- Result: `Doe`

## Supported files of authors.

The following filenames are recognized and processed automatically:

* `AUTHORS`
* `AUTHORS.md`
* `AUTHORS.txt`

These files are expected to be located at the root of the repository. Filenames are matched case-insensitively.

## Purpose and Format

These files typically contain a list of individuals and/or organizations that have contributed to the project. While there is no universal standard for formatting, a widely referenced convention is Google's guidance:

🔗 [Google Open Source: Authors Files Protocol](https://opensource.google/documentation/reference/releasing/authors/)

The content may be structured as:

* Simple plain text, with one contributor per line.
* Markdown-formatted text (`.md` files).
* Lines including contributor names, emails (e.g., `Name <email>`), and sometimes affiliations.

### Examples of Valid Entries

```text
Jane Doe <jane@example.com>
John Smith
Acme Corporation <acme@mail.com>
Google Inc.
```

### Examples of NON Valid Entries

```text
JetBrains <>
Microsoft
Fraunhofer-Gesellschaft zur Förderung der angewandten Forschung
scrawl - Top contributor
Tom
```
## What Is Read vs. Discarded

When processing these files, the parser will:

**Include** lines that:

* Contain person names, optionally with emails (`Name <email>`).
* Clearly refer to organizations (e.g., "Google LLC", "OpenAI Inc.").

**Discard** lines that:

* Are headers, decorative separators, or markdown formatting (`#`, `*`, `=`, etc.).
* Contain only URLs or links.
* Are single words with no email and no organizational keyword (e.g., `JetBrains <>`).
* Are markdown or structured noise (`---`, `{}`, etc.).
* Contain more than four words and are not recognized as organizations — to avoid capturing generic or descriptive sentences (e.g., This line not is an author).

### Special Cases

* Entries with only a first name and an email are accepted but must not assign an empty `last_name`.
* Lines starting with `-` or `*` are considered lists, but only parsed if the content matches expected author patterns.
* Blocks enclosed in `{}` are stripped before parsing.
* Any line matching known organization suffixes (`Inc.`, `LLC`, `Ltd.`, `Corporation`) is treated as an organization, even if no email is present.
* Some organization names (e.g., Open Source Initiative) may be mistakenly treated as person names if they do not contain a company designator or email. To improve detection, it is recommended to use names like Open Source Initiative Inc.
* In such cases, only the meaningful part (typically the name) is extracted before any descriptive annotations.
For example, the line:
Tom Smith (Tom) - Project leader 2010-2018
Will be interpreted as:
{
  "type": "Person",
  "name": "Tom Smith",
  "value": "Tom Smith",
  "given_name": "Tom",
  "last_name": "Smith"
}
