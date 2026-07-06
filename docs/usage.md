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
  --download-limit INTEGER        Download size limit in MB for repository
                                  archives. Overrides the value set in the
                                  configuration file.

  -all, --requirements_all        Export all detected requirements, including
                                  text and libraries (default).

  -v, --requirements_v            Export only requirements from structured
                                  sources (pom.xml, requirements.txt, etc.)


  -ra, --reconcile_authors         SOMEF will extract additional information 
                                  from certain files like CODEOWNERS. 
                                  This may require extra API
                                  requests and increase execution time

  -h, --help                      Show this message and exit.

  -e, --enrichment                Enrich metadata with external APIs (OpenAlex, 
                                  OpenAIRE, Zenodo)

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

  --tag TEXT                      Tag of the repository to analyze. Cannot be used together with --branch and --commit
  
  --commit TEXT                   Commit SHA to analyze. Cannot be used together with --branch or --tag.
```

Note about tokens: GitHub, Codeberg and Bitbucket APIs can be used without authentication for basic metadata extraction. GitLab may require a token for self-hosted instances. User enrichment via CODEOWNERS (--reconcile_authors) works for 
GitHub, GitLab and Codeberg; Bitbucket does not expose a public user API, so enrichment is not supported for that platform.

Alternatively, you can set tokens via environment variables or by running `somef configure`, which stores them permanently.
The CLI flags take precedence over stored config when valid.

### Enrichment with `-e`

The `-e` (or `--enrichment`) flag queries external APIs to complete the extracted metadata:
- **OpenAlex**: Adds `openalex_id` to DOIs of publications and reconciles missing author ORCIDs.
- **OpenAIRE**: Adds `openaire_id` to publications/identifiers and enriches project funding metadata.
- **Zenodo**: Adds `swhid` (Software Heritage ID) for records matching Zenodo DOIs.

For a detailed technical breakdown of the fields mapped by each external service, please refer to the specific documentation pages:
- See the [OpenAlex Mapping Guide](openalex.md) for citation and author properties.
- See the [OpenAIRE and Zenodo Mapping Guide](openaire.md) for funding and identifier properties.

**Note:** Enrichment makes additional network requests to external services, which may slow down the overall execution time. Use this flag only when you need the extra metadata.

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

## Configuration parameters

SOMEF uses a configuration file located at `~/.somef/config.json` that can be edited to customize its behavior. 
To generate it, run `somef configure`. The following parameters are available:

### Similarity threshold

Controls the minimum similarity score required for a README header to be matched to a 
category (e.g., installation, usage, license). SOMEF uses WordNet path similarity to 
compare header words against known category terms.

- **Default value**: `0.8`
- **Range**: `0.0` to `1.0` (higher values = stricter matching, lower values = more permissive)

To change it, edit your `~/.somef/config.json`:

```json
{
    "similarity_threshold": 0.75
}
```

Note: This parameter is different from the `-t` threshold used in `somef describe`, 
which controls the confidence of the supervised classifiers.


### Download size limit

Controls the maximum size (in MB) of repository archives that SOMEF will download.
Repositories larger than this limit are skipped.

- **Default value**: `200`

To change it, run `somef configure` and enter the desired value when prompted,
or edit your `~/.somef/config.json`:

```json
{
    "download_limit_mb": 500
}
```
You can also override it per command with the --download-limit option:


```bash
somef describe -r https://github.com/owner/repo --download-limit 1000 -o output.json
```

To see a live usage example, try our Binder Notebook: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/KnowledgeCaptureAndDiscovery/somef/HEAD?filepath=notebook%2FSOMEF%20Usage%20Example.ipynb)