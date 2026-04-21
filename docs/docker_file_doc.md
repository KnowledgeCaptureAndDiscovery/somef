The following metadata fields can be extracted from a Dockerfile.
These fields are defined using Dockerfile `LABEL` instructions as described in the
[Dockerfile reference](https://docs.docker.com/reference/dockerfile/) and are interpreted
according to the OCI Image Specification, following the
[mapping for OCI image annotations](https://github.com/opencontainers/image-spec/blob/main/annotations.md#pre-defined-annotation-keys).

| Software metadata category  | SOMEF metadata JSON path                | DOCKERFILE metadata file field     |
|-----------------------------|-----------------------------------------|------------------------------------| 
| authors                       |     authors[i].result.value           |   org.opencontainers.image.authors *(1)*  |
| authors                       |     authors[i].result.value           |   LABEL maintainer *(1)*  |
| code_repository               |     code_repository[i].result.value   |   org.opencontainers.image.url     |
| description                   |     description[i].result.value       |     org.opencontainers.image.description    |
| documentation                 |     documentation[i].result.value     |   org.opencontainers.image.documentation    |
| license                       |     license[i].result.value           |     org.opencontainers.image.licenses    |
| name                          |     name[i].result.value              |     org.opencontainers.image.ref.name         |
| owner                         |     owner[i].result.value             |   org.opencontainers.image.vendor    |
| version                       |     version[i].result.value           |   org.opencontainers.image.version     |


---


*(1)*  
- Example: 
```
LABEL maintainer="The Prometheus Authors <prometheus-developers@googlegroups.com>"
LABEL org.opencontainers.image.authors="The Prometheus Authors" \
```


