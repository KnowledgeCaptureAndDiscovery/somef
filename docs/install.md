## Requirements

- Python 3.9


## Install from Pypi
SOMEF [is available in Pypi!](https://pypi.org/project/somef/). To install it just type:

```
pip install somef
```

## Install from GitHub
To run SOMEF, please follow the next steps:

Clone this GitHub repository

```
git clone https://github.com/KnowledgeCaptureAndDiscovery/somef.git
```

Install somef (you should be in the folder that you just cloned). Note that for Python 3.7 and 3.8 the module Cython should be installed in advanced (through the command: `pip install Cython`).

```
cd somef
pip install -e .
```

Run SOMEF

```bash
somef --help
```

If everything goes fine, you should see:

```bash
Usage: somef [OPTIONS] COMMAND [ARGS]...

Options:
  -h, --help  Show this message and exit.

Commands:
  configure  Configure credentials
  describe   Running the Command Line Interface
  version    Show somef version.
```


<!--## Install from Pypi 
Just type:

```bash
pip install somef
```

!!! info
    Feature under development
-->

## Installing Through Docker
We provide a Docker image with SOMEF already installed. To run through Docker, you may build the Dockerfile provided in the repository by running:

```bash
docker build -t somef .
```
Or just use the Docker image already built in [DockerHub](https://hub.docker.com/r/kcapd/somef):

```bash
docker pull kcapd/somef
```

Then, to run your image just type:

```bash
docker run -it kcapd/somef /bin/bash
```

And you will be ready to use SOMEF (see section below). If you want to have access to the results we recommend [mounting a volume](https://docs.docker.com/storage/volumes/). For example, the following command will mount the current directory as the `out` folder in the Docker image:

```bash 
docker run -it --rm -v $PWD/:/out kcapd/somef /bin/bash
```
If you move any files produced by somef into `/out`, then you will be able to see them in your current directory.


## Configure

Before running SOMEF for the first time, you must **configure** it appropriately (you only need to do this once). Run:

```bash
somef configure
```

And you will be asked to provide the following:

- A **GitHub** authentication token [**optional, leave blank if not used**], which SOMEF uses to retrieve metadata from GitHub. If you don't include an authentication token, you can still use SOMEF. However, you may be limited to a series of requests per hour. For more information, see [https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line)
- A **GitLab** authentication token [**optional**], used for GitLab.com and self-hosted GitLab instances (e.g., `gitlab.in2p3.fr`). Tokens are per-instance. Note: **a token from GitLab.com does not work for self-hosted servers**. Create one at `https://gitlab.com/-/user_settings/personal_access_tokens` (scope: `read_api`). Without a token, some self-hosted GitLab instances may not return rate limit information.
- A **Codeberg** authentication token [**optional**], used to retrieve metadata from Codeberg. Create one at `https://codeberg.org/user/settings/applications` (permissions: `read:repository`, `read:user`). Codeberg (Forgejo) does not expose rate limit headers even with a token.
- A **Bitbucket** authentication token [**optional**], used for Bitbucket Cloud. Create an API token with scopes at `https://bitbucket.org/account/settings/api-tokens/` (permissions: `read:repository:bitbucket`, `read:account`). You will also need to provide your Atlassian account email, as Bitbucket API tokens use Basic authentication (`email:token` encoded in base64). Without a token you are limited to 60 requests/hour.
- The path to the trained classifiers (pickle files). If you have your own classifiers, you can provide them here. Otherwise, you can leave it blank.


If you want SOMEF to be automatically configured (without any tokens and using the default classifiers) just type:

```bash
somef configure -a
```

For showing help about the available options, run:

```bash
somef configure --help
```

Which displays:

```bash
Usage: somef configure [OPTIONS]

  Configure GitHub credentials and classifiers file path

Options:
  -a, --auto  Automatically configure SOMEF
  -h, --help  Show this message and exit.
```