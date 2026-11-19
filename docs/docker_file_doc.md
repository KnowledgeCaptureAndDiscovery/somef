The following metadata fields can be extracted from a Dockerfile.
These fields are defined using Dockerfile `LABEL` instructions as described in the
[Dockerfile reference](https://docs.docker.com/reference/dockerfile/) and are interpreted
according to the OCI Image Specification, following the
[mapping for OCI image annotations](https://github.com/opencontainers/image-spec/blob/main/annotations.md#pre-defined-annotation-keys).

| Software metadata category  | SOMEF metadata JSON path                | DOCKERFILE metadata file field     |
|-----------------------------|-----------------------------------------|------------------------------------| 
| author                       |     author[i].result.value           |   org.opencontainers.image.authors *(1)*  |
| author                       |     author[i].result.value           |   LABEL maintainer *(1)*  |
| code_repository               |     code_repository[i].result.value   |   org.opencontainers.image.url     |
| container - value                   |  container[i].result.value       |    URL or path of the Dockerfile |
| container - author                   |  container[i].result.author[j].value       |    org.opencontainers.image.authors |
| container - author                   |  container[i].result.author[j].value       |    LABEL maintainer *(1)* |
| container - description                   |  container[i].result.description       |    org.opencontainers.image.description |
| container - documentation                   |  container[i].result.documentation       |    org.opencontainers.image.documentation |
| container - license                   |  container[i].result.license       |    org.opencontainers.image.licenses |
| container - spdx_id                   |  container[i].result.spdx_id       |    org.opencontainers.image.licenses |
| container - name                   |  container[i].result.name       |    org.opencontainers.image.title |
| container - url                   |  container[i].result.url       |    org.opencontainers.image.url |
| container - version                   |  container[i].result.version       |    org.opencontainers.image.version |
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


