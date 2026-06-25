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
  somef describe --help
  SOMEF Command Line Interface
Usage: somef describe [OPTIONS]

  Running the Command Line Interface

Options:
  -t, --threshold FLOAT           Threshold to classify the text  [required]
  Input: [mutually_exclusive, required]
    -r, --repo_url URL            Github Repository URL
    -d, --doc_src PATH            Path to the README file source
    -i, --in_file PATH            A file of newline separated links to GitHub
                                  repositories

  Output: [required_any]
    -o, --output PATH             Path to the output file. If supplied, the
                                  output will be in JSON

    -g, --graph_out PATH          Path to the output Knowledge Graph file. If
                                  supplied, the output will be a Knowledge
                                  Graph, in the format given in the --format
                                  option
    -c, --codemeta_out PATH       Path to an output codemeta file (in JSON-LD)

  -f, --graph_format [turtle|json-ld]
                                  If the --graph_out option is given, this is
                                  the format that the graph will be stored in

  -p, --pretty                    Pretty print the JSON output file so that it
                                  is easy to compare to another JSON output
                                  file.

  -m, --missing                   JSON report with the missing metadata fields
                                  SOMEF was not able to find. The report will
                                  be placed in  $PATH_missing.json, where
                                  $PATH is -o, -c or -g.
  -kt, --keep_tmp PATH            SOMEF will NOT delete the temporary folder
                                  where files are stored for analysis. Files
                                  will be stored at the
                                  desired path

  -h, --help                      Show this message and exit.
```

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

To see a live usage example, try our Binder Notebook: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/KnowledgeCaptureAndDiscovery/somef/HEAD?filepath=notebook%2FSOMEF%20Usage%20Example.ipynb)