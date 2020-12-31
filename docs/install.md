## Requirements

- Python 3.6 or above (tested on Python 3.8.6)


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

## Configure
Before running SOMEF, you must configure it appropriately. Run

```bash
somef configure
```

And you will be asked to provide the following: 

- A GitHub authentication token [**optional, leave blank if not used**], which SOMEF uses to retrieve metadata from GitHub. If you don't include an authentication token, you can still use SOMEF. However, you may be limited to a series of requests per hour. For more information, see [https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line) 
- The path to the trained classifiers (pickle files). If you have your own classifiers, you can provide them here. Otherwise, you can leave it blank

If you want to configure SOMEF with the default parameters, just type:

```bash
somef configure -a
```