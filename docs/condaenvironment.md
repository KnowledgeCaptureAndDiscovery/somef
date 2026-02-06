# Metadata extracted from a Conda `environment.yml` file

The following metadata fields can be extracted from a Conda `environment.yml` or `environment.yaml` file.  
This file format is part of the Conda environment specification and is commonly used to declare software dependencies for reproducible environments.

Only dependency information is mapped, since it is the only part of the Conda environment specification that corresponds to CodeMeta could be `softwareRequirements`.  

---

## Extracted metadata fields

| Software metadata category  | SOMEF metadata JSON path              | ENVIRONMENT.YML metadata file field     |
|-----------------------------|---------------------------------------|------------------------------|
| has_package_file            | has_package_file[i].result.value      | URL of the `environment.yml` file |
| requirements - value          |     requirements[i].result.value      | dependenciees | 
| requirements - name           |     requirements[i].result.name       | dependencies extract name       |        
| requirements - version            |     requirements[i].result.version    | dependencies extract version |
| requirements - dependency type           |     requirements[i].result.dependency_type            | conda if depedencies or pip if dependencie/pip  *(1)* |


---


*(1)* 
- Example of a dependency conda and a dependency pip:
```
name: ldm
dependencies:
  - python=3.8.5
  - pip:
    - albumentations==0.4.3
```
- Result:
```    
    "result": {
        "value": "python=3.8.5",
        "name": "python",
        "version": "3.8.5",
        "type": "Software_application",
        "dependency_type": "conda"
    },
    "result": {
        "value": "albumentations==0.4.3",
        "name": "albumentations",
        "version": "0.4.3",
        "type": "Software_application",
        "dependency_type": "pip"
    },

