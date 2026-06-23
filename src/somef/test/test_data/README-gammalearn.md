# GammaLearn

<p align="left">
<img src="https://gammalearn.pages.in2p3.fr/pages/images/glearn.png" width="60px" >
<b><i>Deep Learning for Imaging Cherenkov Telescopes Data Analysis.</b></i>
</p>

GammaLearn is a collaborative project to apply deep learning to the analysis of low-level Imaging Atmospheric Cherenkov Telescopes such as CTA.
It provides a framework to easily train and apply models from a configuration file.


[![](https://img.shields.io/badge/GammaLearn-Pages-yellow)](https://purl.org/gammalearn)
[![](https://img.shields.io/badge/GammaLearn-Code-blue)](https://gitlab.in2p3.fr/gammalearn/gammalearn)
[![](https://img.shields.io/badge/GammaLearn-Documentation-orange)](https://gammalearn.pages.in2p3.fr/gammalearn)
[![](https://img.shields.io/badge/GammaLearn-Slack-green)](https://gammalearn.slack.com/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5879803.svg)](https://doi.org/10.5281/zenodo.5879803)

[![pipeline status](https://gitlab.in2p3.fr//gammalearn/gammalearn/badges/master/pipeline.svg)](https://gitlab.in2p3.fr//gammalearn/gammalearn/-/commits/master)
[![coverage report](https://gitlab.in2p3.fr/gammalearn/gammalearn/badges/master/coverage.svg)](https://gammalearn.pages.in2p3.fr/gammalearn/htmlcov)

## Table of Contents

1. [Installation](#usage)
  1. [For users](#for-users)
  1. [For Developers](#for-developers)
1. [Contributing](#contributing)
1. [Cite Us](#cite-us)
1. [License](#license)


## Usage

Gammalearn's CI/CD pipelines produce containers that can be used to quickly get a working environment for development or production. The containers are uploaded to the gammalearn's [container registry](https://gitlab.in2p3.fr/gammalearn/gammalearn/container_registry). A set of containers is available for each branch in the repository, and the containers are re-build for any commit that involves modifications  made to the environment or dockerfiles files (anything in the `docker` [directory](https://gitlab.in2p3.fr/gammalearn/gammalearn/-/tree/master/docker)).

Gammalearn containers include the pytorch and cuda dependencies to do computation on nvidia gpus, in addition to a big stack of scientific computing software. They are typically take several GBs. 

### For users

We recommend the use of [apptainer](https://apptainer.org/). To get the production image of the version of gammalearn you want to use, for instance to get gammalearn `v0.13.0`, use `apptainer pull`:
```bash
apptainer pull docker://gitlab-registry.in2p3.fr/gammalearn/gammalearn:v0.13.0
```

This will create a `.sif` container file that contains a ready to use gammalearn installation. Warning: `apptainer` can use several GB of disk space as cache when building the `.sif` file. By default, the cache is located in your home folder `~/.apptainer/cache`. You can change this location by setting the `APPTAINER_CACHEDIR` environment variable. Clean `apptainer`'s cache with `apptainer cache clean`

You can now get a shell inside the container to test gammalearn:
```bash
apptainer shell path_to_your_sif_file.sif
Apptainer> /opt/conda/bin/gammalearn --help
```

#### Run an experiment

You can run an experiment using `apptainer run`. Since apptainer containers are read-only by default, you will need to mount the paths to your input and output files. To use nvidia gpus, you will need to specify the `--nv` option as well. A typical command example:

```bash 
# Run the experiment in the container
# Parameters:
# --nv                  to use nvidia gpus from inside the container
# CUDA_VISIBLE_DEVICES  env variable used by pytorch to discover the gpus
# NUMBA_CACHE_DIR       a writable directory where numba can store its compiled functions
#                       (needs to be outside of the container, which is read-only)
# CTAPIPE_CACHE         ctapipe needs a writable place, to store its downloaded files.
# Mounts: input (data and settings file) and output directories
# 
# We call the gammalearn entrypoint directly in /opt/conda/bin, because micromamba is not initialized
# inside the container for a new user (and every user is new, since with apptainer the user remains the same
# as the user on the host system by default (only users defined in the containers are known))
apptainer run \
    --nv \
    --env "CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES" \
    --env "NUMBA_CACHE_DIR=/tmp/NUMBA" \
    --env "CTAPIPE_CACHE=/tmp/CTAPIPE" \
    --mount type=bind,source=/path/to/input/data_dir/,destination=/corresponding/path/in/container/ \
	--mount type=bind,source=/path/to/output/data_dir/,destination=/corresponding/path/in/container/ \
    path_to_your_sif_file.sif /opt/conda/bin/gammalearn path_to_your_experiment_settings_file.py
```

You can find examples of setting file in the [examples](https://gitlab.in2p3.fr/gammalearn/gammalearn/-/tree/master/gammalearn/configuration/examples) and some sample data in [example data](https://gitlab.in2p3.fr/gammalearn/gammalearn/-/tree/master/share/data)

### For Developers

Developers are encouraged to use the development containers available in the repository [container registry](https://gitlab.in2p3.fr/gammalearn/gammalearn/container_registry/). The development containers contain all gammalearn run-time dependencies, and several tools required to develop the software (for instance to run tests, build the documentation, visualize results, etc.), but it does **NOT** contain gammalearn nor it source code. The goal is to provide a containerized development environment, but leave the source code in the host system. It is recommended to use the development containers with `docker`, either directly or through an IDE.

#### Development container with docker directly

To pull the container of the branch you use to develop:
```bash
docker pull gitlab-registry.in2p3.fr/gammalearn/gammalearn/dev:your_branch_name
```
Clone gammalearn locally and go in the gammalearn directory:
```bash
git clone https://gitlab.in2p3.fr/gammalearn/gammalearn.git && cd gammalearn
```
Enter the container while mounting the source code, and install gammalearn
```bash
# - get a shell with interactive mode
# - mount gammalearn sources in "bind" mode with --mount
# - use your host user uid and gid (-u $(id -u):$(id -g)) to have write permissions in the mounted gammalearn sources
# - set working directory to /src
# - optionally: set pull policy to always to always get the latest image for your branch
docker run --rm -it --mount type=bind,source=.,destination=/src -w /src --pull=always -u $(id -u):$(id -g) gitlab-registry.in2p3.fr/gammalearn/gammalearn/dev:your_branch_name
(base) mambauser@...:/src$ pip install --no-deps -e .
# Develop !
```

#### Usage with an IDE (vscode example)

Many IDE's offer the possibility to start or interact with running docker containers. In VScode, this is handled by the "dev container" extension included in the remote development extension pack (see the extension [documentation](https://code.visualstudio.com/docs/devcontainers/containers)). The extension can start a container and automatically install a vs-code server inside the container, allowing to transparently develop the software while using the environment from inside the container. The following `devcontainer.json` configuration allows to start a development container with the right permissions and build gammalearn from the mounted sources. As examples, the python extension and ruff linter are installed in the vs-code server running in the container.

```json
// For format details, see https://aka.ms/devcontainer.json. For config options, see the
// README at: https://github.com/devcontainers/templates/tree/main/src/miniconda
{
	"image": "gitlab-registry.in2p3.fr/gammalearn/gammalearn/dev:your_dev_branch",
	"workspaceMount": "source=${localWorkspaceFolder},target=/src,type=bind",
	"workspaceFolder": "/src",
	"postAttachCommand": "micromamba run -n base pip install --no-deps -e /src",
	"runArgs": [ "--network=host"],
	"customizations": {
		// Configure properties specific to VS Code.
		"vscode": {
			// Add the IDs of extensions you want installed when the container is created.
			"extensions": [
				"charliermarsh.ruff",
				"ms-python.python",
				"ms-python.vscode-pylance",
				"njpwerner.autodocstring",
				"tamasfe.even-better-toml",
				"wmaurer.change-case"
			]
		}
	}
}
```

Note: By default, the dev containers extension will not re-pull the specified image unless you rebuild the container in vscode. Make sure to pull the latest container for your branch before entering the container.

Once the container is running, you can enter it from another external terminal with
```bash
# Get the container ID of your dev container started with vscode
docker ps
# Get a shell in the container
docker exec -it -w /src container_ID bash​
```

#### Bare-metal installation

Gammalearn dependencies are managed using [Anaconda](https://www.anaconda.com/products/individual). The dependencies are split into run-time, test and development dependencies available in the [docker directory](https://gitlab.in2p3.fr/gammalearn/gammalearn/-/tree/master/docker). According to your usage, install the dependencies you need. For instance:

```bash
conda env create -n glearn -f dependencies.yml
conda env update -n glearn -f test_dependencies.yml
conda activate glearn
```

**Note for OSX and/or no-gpu users:** please edit the environment file to remove `cudatoolkit` from the dependencies.

#### Older version installation

Create the gammalearn release environment:
```bash
VERSION=0.12.0
wget https://gitlab.in2p3.fr/gammalearn/gammalearn/-/raw/v${VERSION}/environment.yml -O glearn_${VERSION}_env.yml
conda env create -f glearn_${VERSION}_env.yml
conda activate glearn
```

**Note for OSX and/or no-gpu users:** please edit the environment file to remove `cudatoolkit` from the dependencies.


## Contributing

Contributions are very much welcome: please see [CONTRIBUTING](https://gitlab.in2p3.fr/gammalearn/gammalearn/-/blob/master/CONTRIBUTING.md).


## Cite Us

Please cite

_Jacquemont M, Vuillaume T, Benoit A, Maurin G, Lambert P, Lamanna G, Brill A._ 
_GammaLearn: A Deep Learning Framework for IACT Data. In36th International Cosmic Ray Conference (ICRC2019) 2019 Jul (Vol. 36, p. 705)._ 
[DOI: https://doi.org/10.22323/1.358.0705](https://doi.org/10.22323/1.358.0705)

For reproducibility purposes, please also cite the exact version of GammaLearn you used by citing the corresponding DOI on Zenodo:  
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5879803.svg)](https://doi.org/10.22323/1.358.0705)


## License

GammaLearn is distributed under an [MIT license](https://gitlab.in2p3.fr/gammalearn/gammalearn/-/blob/master/LICENSE).

## [Back to top](#table-of-contents)