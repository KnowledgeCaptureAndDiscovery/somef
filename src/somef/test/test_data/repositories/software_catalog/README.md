# software_catalog
Catalog of software tools developed at the Ontology Engineering Group.
The catalog is automatically created with `scc` (https://github.com/oeg-upm/scc/), using the following command:

```
scc fetch -i oeg-upm --org -o oeg-upm_repos.csv &&
scc extract -i oeg-upm_repos.csv -o oeg-upm_metadata -i4p &&
scc portal -i oeg-upm_metadata -o oeg-upm_portal
```

An online version of the catalog is available here: https://oeg-upm.github.io/software_catalog/

## Creating a new version of the catalog
The commands outlined above will re-generate the full catalog. However, it's possible to curate the list of repositories on top of which `scc` will be run on. The folder `repositories` contain an initial pass donde by scc with the full contents of the oeg organization. Simply modify the file `oeg-upm.csv` and add the repositories you are interested in.

Then, re-run `scc` with the following commands:

```
scc extract -i oeg-upm_repos.csv -o oeg-upm_metadata -i4p &&
scc portal -i oeg-upm_metadata -o oeg-upm_portal
```
