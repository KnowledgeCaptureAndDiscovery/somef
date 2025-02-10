### Demo of Compliance Pipelines

A separate project needs to be setup with its own .yml file to define the `compliance pipeline`. In this compliance project, there is a file [compliance-pipeline.gitlab-ci.yml](https://gitlab.com/sam-s-test-group/compliance-project/-/blob/master/compliance-pipeline.gitlab-ci.yml) which chooses to enforce its jobs while also including an individual project's `.gitlab-ci.yml`.

<details><summary>Compliance pipeline YAML</summary>

```yaml
compliance_print:
    stage: .pre
    rules:
        - when: always
    image: ruby:2.6
    before_script:
        - "# No before scripts."
    script:
        - echo "Compliance prints"
        - echo "$CI_COMMIT_REF_NAME"
    after_script:
        - "# No after scripts."
    allow_failure: false
    interruptible: false
    #secrets:
        # Define any needed secrets

compliance_required_build_job:
    stage: build
    script:
        - echo "Performing compliance build steps"

compliance_required_test_job:
    stage: test
    script:
        - echo "Performing compliance test steps"

include:
    - template: Security/SAST.gitlab-ci.yml
    - project: '$CI_PROJECT_PATH'
      file: '$CI_CONFIG_PATH'
```

</details>

In a different group, [Sam's test group](https://gitlab.com/sam-s-test-group), a compliance framework (`Sam's Framework`) has been created to use that compliance pipeline.

![Sam's Framework Settings](img/compliance-framework.png)

[ExpressExample](https://gitlab.com/sam-s-test-group/expressexample) is a project in Sam's test group. It has `Sam's Framework` assigned as its compliance framework.

![Framework Assignment](img/framework-assignment.png)

Since the compliance pipeline includes individual project pipeline, it will run [ExpressExample's .gitlab-ci.yml](https://gitlab.com/sam-s-test-group/expressexample/-/blob/master/.gitlab-ci.yml)

<details><summary>ExpressExample's .gitlab-ci.yml</summary>

```YAML

image: alpine:latest

variables:
  POSTGRES_USER: user
  POSTGRES_PASSWORD: testing-password
  POSTGRES_ENABLED: "true"
  POSTGRES_DB: $CI_ENVIRONMENT_SLUG

  DOCKER_DRIVER: overlay2

  ROLLOUT_RESOURCE_TYPE: deployment

  DOCKER_TLS_CERTDIR: ""  # https://gitlab.com/gitlab-org/gitlab-runner/issues/4501

stages:
  - build
  - test
  - deploy  # dummy stage to follow the template guidelines
  - dast

# NOTE: These links point to the latest templates for development in GitLab canonical project,
# therefore the actual templates that were included for Auto DevOps pipelines
# could be different from the contents in the links.
# To view the actual templates, please replace `master` to the specific GitLab version when
# the Auto DevOps pipeline started running e.g. `v13.0.2-ee`.
include:
  - template: Jobs/Build.gitlab-ci.yml  # https://gitlab.com/gitlab-org/gitlab/blob/master/lib/gitlab/ci/templates/Jobs/Build.gitlab-ci.yml
  - template: Jobs/Test.gitlab-ci.yml  # https://gitlab.com/gitlab-org/gitlab/blob/master/lib/gitlab/ci/templates/Jobs/Test.gitlab-ci.yml
  - template: Jobs/Code-Quality.gitlab-ci.yml  # https://gitlab.com/gitlab-org/gitlab/blob/master/lib/gitlab/ci/templates/Jobs/Code-Quality.gitlab-ci.yml
  - template: Security/Container-Scanning.gitlab-ci.yml  # https://gitlab.com/gitlab-org/gitlab/blob/master/lib/gitlab/ci/templates/Security/Container-Scanning.gitlab-ci.yml
  - template: Security/Dependency-Scanning.gitlab-ci.yml  # https://gitlab.com/gitlab-org/gitlab/blob/master/lib/gitlab/ci/templates/Security/Dependency-Scanning.gitlab-ci.yml
  - template: Security/License-Scanning.gitlab-ci.yml  # https://gitlab.com/gitlab-org/gitlab/blob/master/lib/gitlab/ci/templates/Security/License-Scanning.gitlab-ci.yml
  - template: Security/Secret-Detection.gitlab-ci.yml  # https://gitlab.com/gitlab-org/gitlab/blob/master/lib/gitlab/ci/templates/Security/Secret-Detection.gitlab-ci.yml

compliance_print:
    rules:
        - when: never
    script:
      - echo "Test this out!"
    after_script:
      - echo "I shouldn't be here ;)"
```

</details>

If you view a [pipeline](https://gitlab.com/sam-s-test-group/expressexample/-/pipelines/319456947) for the ExpressExample it will have the jobs running together. Note that in this case, the compliance pipeline author chose to prefix their compliance jobs with the word compliance.
