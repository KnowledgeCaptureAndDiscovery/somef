To see the available options for SOMEF:

```bash
somef --help
```
and you will see the main help message:

```bash
Usage: somef [OPTIONS] COMMAND [ARGS]...

Options:
  -h, --help  Show this message and exit.

Commands:
  configure  Configure credentials
  describe   Running the Command Line Interface
  version    Show somef version.
```
The options to run somef are through the `describe` command:

```bash
$ somef describe --help
  SOMEF Command Line Interface
Usage: somef describe [OPTIONS]

  Running the Command Line Interface

Options:
  -t, --threshold FLOAT           Threshold to classify the text  [required]
  Input: [mutually_exclusive, required]
    -r, --repo_url URL            Github/Gitlab/Codeberg/Bitbucket Repository URL
    -d, --doc_src PATH            Path to the README file source
    -i, --in_file PATH            A file of newline separated links to GitHub/
                                  Gitlab/Codeberg/Bitbucket repositories
    -l, --local_repo PATH         Path to the local repository source. No APIs will be used

  Output: [required_any]
    -o, --output PATH             Path to the output file. If supplied, the
                                  output will be in JSON
    -c, --codemeta_out PATH       Path to an output codemeta file
    -g, --graph_out PATH          Path to the output Knowledge Graph export
                                  file. If supplied, the output will be a
                                  Knowledge Graph, in the format given in the
                                  --format option chosen (turtle, json-ld)
    -gc, --google_codemeta_out PATH Path to a Google-compliant Codemeta JSON-LD
                                    file. This output transforms the standard
                                    Codemeta to follow Google’s expected JSON-LD
                                    structure.
                                    
  -f, --graph_format [turtle|json-ld]
                                  If the --graph_out option is given, this is
                                  the format that the graph will be stored in

  -p, --pretty                    Pretty print the JSON output file so that it
                                  is easy to compare to another JSON output
                                  file.

  -m, --missing                   The JSON will include a field
                                  somef_missing_categories to report with the
                                  missing metadata fields that SOMEF was not
                                  able to find.

  -kt, --keep_tmp PATH            SOMEF will NOT delete the temporary folder
                                  where files are stored for analysis. Files
                                  will be stored at the
                                  desired path

  -all, --requirements_all        Export all detected requirements, including
                                  text and libraries (default).

  -v, --requirements_v            Export only requirements from structured
                                  sources (pom.xml, requirements.txt, etc.)


  -ra, --reconcile_authors         SOMEF will extract additional information 
                                  from certain files like CODEOWNERS. 
                                  This may require extra API
                                  requests and increase execution time

  -h, --help                      Show this message and exit.

  --github-token TEXT             GitHub personal access token (if invalid,
                                  stored config is used instead)

  --gitlab-token TEXT             GitLab personal access token (if invalid,
                                  stored config is used instead)

  --codeberg-token TEXT           Codeberg personal access token (if invalid,
                                  stored config is used instead)

  --bitbucket-token TEXT          Bitbucket app password (if invalid, stored 
                                  config is used instead)

  --bitbucket-email TEXT          Bitbucket Atlassian account email (required
                                  with --bitbucket-token)
  
  Repoository versions [mutually_exclusive] (see section *Repository versions*t):
  -b, --branch name branch        Branch of the repository to analyze. Overrides the default branch.

      --tag text                  Tag of the repository to analyze. Cannot be used together with --branch.
```

Alternatively, you can set tokens via environment variables or by running `somef configure`, which stores them permanently.
The CLI flags take precedence over stored config when valid.


## Usage example:
The following command extracts all metadata available from [https://github.com/dgarijo/Widoco/](https://github.com/dgarijo/Widoco/). 

```bash
somef describe -r https://github.com/dgarijo/Widoco/ -o test.json -t 0.8
```

To obtain the same information as a JSON-LD file:

```bash
somef describe -r https://github.com/dgarijo/Widoco/ -g test.jsonld -f json-ld -t 0.8
```

If you prefer to export as a [Codemeta](https://codemeta.github.io/) JSON-LD, just type:

```bash
somef describe -r https://github.com/dgarijo/Widoco/ -c test.json
```

For more information about the output types supported by SOMEF, please see [the output format help page](https://somef.readthedocs.io/en/latest/output/).

We recommend having a high value for the `threshold` parameter, 0.8 (default) or above.

To see a live usage example, try our Binder Notebook: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/KnowledgeCaptureAndDiscovery/somef/HEAD?filepath=notebook%2FSOMEF%20Usage%20Example.ipynb)