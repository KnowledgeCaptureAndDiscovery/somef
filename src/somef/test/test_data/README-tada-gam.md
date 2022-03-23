# tada-gam

[![Build Status](https://semaphoreci.com/api/v1/ahmad88me/tada-gam/branches/master/badge.svg)](https://semaphoreci.com/ahmad88me/tada-gam)
[![codecov](https://codecov.io/gh/oeg-upm/tada-gam/branch/master/graph/badge.svg)](https://codecov.io/gh/oeg-upm/tada-gam)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3545624.svg)](https://doi.org/10.5281/zenodo.3545624)

A scalable version of tada entity using the MapReduce framework

# Install (Mac and Ubuntu)
1. Download the application via `git` or the web interface of github (make sure to include the submodules as well e.g., `git clone --recursive https://github.com/oeg-upm/tada-gam.git`)
1. using the terminal, go to project directory `cd /home/ubuntu/tada-gam` (if `/home/ubuntu/` was your download location)
1. Create virtual environment`virtualenv -p /usr/bin/python2.7 .venv` (you need to have virtualenv installed)
1. Activate the virtual environment `source .venv/bin/activate`
1. Install dependencies via pip `pip install -r requirements.txt ` 

# Download T2Dv2 experimental data via command line 
*This follows the install step* it is only needed if you want to run the experiments 
1. Go to the experiment url using the terminal `cd experiments/t2dv2/data`
1. Download T2Dv2 data via wget `wget http://webdatacommons.org/webtables/extended_instance_goldstandard.tar.gz`
1. Extract the downloaded file `tar -xvzf extended_instance_goldstandard.tar.gz`
1. Delete the archive (optional) `rm extended_instance_goldstandard.tar.gz`
1. Overwrite the gold standard with the fixed one`cp ../classes_GS.fixed classes_GS.csv`
1. Generate CSV copy from the JSON
    1. In the terminal, go to the directory of the application `cd ../../..`
    1. Activate the virtual environment `source .venv/bin/activate`
    1. Go to t2dv2 directory `cd experiments/t2dv2/`
    1. Generate CSV copy `python preprocessing.py`


# Usage
To use this tool, we need to talk with the `captain.py`. It manages the 
other resources and assign tasks and data. Although it can be done
directly, but you need to understand how the flow works.

## Step1: Startup the services
```
python captain.py up --services score=3 combine=2
```
In this command we are running 3 instances of the `score` service and
2 instance of `combine`. You can adjust that to meet your needs 

## Step2: Label columns
```
python captain.py label --files local_data/data.csv --sample all
```
You can specify as much files are you want. You can also make use of 
the wild card like that `local_data/*.csv`.
This can be executed multiple times without the need to restart or 
rebuild the services


*arguments*:
```
usage: label_experiment.py [-h] [--alpha ALPHA] [--fname FNAME]
                           [--sample {all,10}]
                           {start,results,show,collect,single}

Captain to look after the processes

positional arguments:
  {start,results,show,collect,single}
                        "start": To start the experiment "collect": To collect
                        the results from the running combine instances
                        "results": To compute the collected results (to be run
                        after the "collect" option) "show": To show the
                        computed results (to be run after the "results"
                        option) "single": To show the results for a single
                        file with a given alpha (to be run after the
                        "collect")

optional arguments:
  -h, --help            show this help message and exit
  --alpha ALPHA         The alpha to be used (only for single option)
  --fname FNAME         The file name the results will be computed for (only
                        for single option)
  --sample {all,10}     The sampling method
```

# requirements
* `docker`
* `docker-compose`
* `python 2.7`


# To update submodules
```
git submodule foreach git pull origin master
```
[source](https://stackoverflow.com/questions/5828324/update-git-submodule-to-latest-commit-on-origin)



# To run the experiments
## Subject Column Labeling
### T2Dv2
1. Download and locate the data automatically (see above) or manually like here
    1. Download the data from the official [website](http://webdatacommons.org/webtables/goldstandard.html)
    1. Locate the downloaded data into `experiments/t2dv2/data`
    1. Replace the file `experiments/t2dv2/data/classes_GS.csv` with `experiments/t2dv2/classes_GS.fixed`
and rename it to `classes_GS.csv`.
1. In the terminal, go to the directory of the application 
1. Activate the virtual environment `source .venv/bin/activate`
1. Go to the experiment directory `cd experiments/t2dv2`
1. Run the labeling task `python label_experiment.py start --sample all` (note that this will 
use docker-compose and will startup the instances, automatically)
1. In another window, run this command `python label_experiment.py collect --sample all`. This 
will collect the data from the instances, so in case the experiment has been interrupted or
stopped, it will resume (to resume, start from step 4).
1. Once the experiment is done, you can compute the results `python label_experiment.py results --sample all` (it will fetch them from the combine instances) 
1. Show the scores `python label_experiment.py show --sample all` (precision, recall, and F1)

*note: for sample `all`, it will run normally, for sample `10`, it will take the top 10 values from each subject column only*

## Subject Column Detection
### T2Dv2
1. In the terminal, go to the directory of the application
1. Activate the virtual environment `source .venv/bin/activate`
1. Download the data (follow *Download T2Dv2 experimental data via command line* above)
1. Go to the experiment folder (from the app folder) `cd experiments/t2dv2`
1. Run docker images `python col_detect_experiment.py start` 
1. Run the detection experiment ``

### T2D-TAIPAN 
The T2D set used in the TAIPAN 
1. In the terminal, go to the directory of the application
1. Activate the virtual environment `source .venv/bin/activate`
1. Go to Taipan experiment directory `cd experiments/taipan`
1. Download and preprocess `python preprocessing.py` (you must have `wget` installed)
1. Run the experiment `python experiment.py`
1. The scores will be located in `data/scores.csv`
