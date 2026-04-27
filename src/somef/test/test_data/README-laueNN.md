
![til](https://github.com/BM32ESRF/LaueNN/blob/main/docs/idea_lauenn/frames_medres.gif)

[![Conda](https://img.shields.io/conda/pn/bm32esrf/lauetoolsnn?color=green&label=supported%20platform)](https://anaconda.org/bm32esrf/lauetoolsnn)
[![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/BM32ESRF/LaueNN?color=blue&label=Github%20tag)](https://github.com/BM32ESRF/LaueNN)

[![Lint, test, build, and publish](https://github.com/BM32ESRF/LaueNN/actions/workflows/complete_workflow.yml/badge.svg)](https://github.com/BM32ESRF/LaueNN/actions/workflows/complete_workflow.yml)
[![PyPI](https://img.shields.io/pypi/v/lauetoolsnn)](https://pypi.python.org/pypi/lauetoolsnn/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/lauetoolsnn.svg)](https://pypi.python.org/pypi/lauetoolsnn/)

[![Anaconda-Server Badge](https://anaconda.org/bm32esrf/lauetoolsnn/badges/license.svg)](https://anaconda.org/bm32esrf/lauetoolsnn)
[![Conda](https://img.shields.io/conda/v/bm32esrf/lauetoolsnn?style=flat-square)](https://anaconda.org/bm32esrf/lauetoolsnn)


[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/BM32ESRF/LaueNN/issues)


# lauetoolsnn/LaueNN
An autonomous feed-forward neural network (FFNN) model to predict the HKL in single/multi-grain/multi-phase Laue patterns with high efficiency and accuracy is introduced. 

Laue diffraction indexation (especially Laue images comprising of diffraction signal from several polycrystals/multi phase materials) can be a very tedious and CPU intensive process. To takle this, LaueNN or LauetoolsNN was developed employing the power of neural network to speed up a part of the indexation process. In the LaueNN_presentation (https://github.com/BM32ESRF/LaueNN/tree/main/presentations/LaueNN_presentation.pdf), several steps of Laue pattern indexation with classical approach is described. We have replaced the most CPU intensive step with the Neural Networks. The step where the Laue indices hkl of each spot os now determined with the Neural networks, alongside the spot hkl index, the neural network also predicts the Material that spot belongs to. This can be useful incase of Laue images comprising of diffraction signal from multi-phases. 
LaueNN uses the existing modules of Lauetools to generate simulated Laue patterns. The whole workflow and the application of this tool is illustrated in this article (https://onlinelibrary.wiley.com/iucr/doi/10.1107/S1600576722004198)

For classical indexation of Laue pattern (GUI and scripts), check out the sister package: https://github.com/BM32ESRF/lauetools

  
### Video tutorial
------------------------------
- Video 1: Working with jupyter notebook scripts : https://cloud.esrf.fr/s/6q4DJfAn7K46BGN
- Video 2: Working with lauetoolsnn GUI : https://cloud.esrf.fr/s/AeGow4CoqZRJiyx


### Requirements: (latest version of each libraries accessed on 03/04/2022) 
------------------------------ 
- PyQt5 (GUI)
- matplotlib
- Keras
- tensorflow 
- numpy 
- scipy (scipy transform rotation is used)
- h5py (required for writing neural network model files)
- scikit-learn (required for generating trained model classification reports)
- fabio (used for opening raw Laue tiff images)
- networkx (to be replaced with numpy in the future)
- scikit-image (used for hough based analysis of Laue patterns)
- tqdm (required only for notebook scripts)
- opencv (for LOG based peak search)
- pandas and pytables (for writing pickle to h5)


### Installation
------------------------------
Lauetoolsnn can be installed either via PYPI usiing the following command in terminal (this installs all dependencies automatically): 

https://pypi.org/project/lauetoolsnn/

https://anaconda.org/bm32esrf/lauetoolsnn

``` bash
$ pip install lauetoolsnn
$ or
$conda install -c bm32esrf lauetoolsnn -c conda-forge
```
For macOS user, please use the conda installation to avoid build errors or can be compiled and installed locally via the setup.py file. Download the Github repository and type the following in terminal. In this case, the dependencies has to be installed manually. The latest version of each dependency works as of (01/04/2022).
``` bash
$ python setup.py install
```

See procedure_usage_lauetoolsnn.pdf for installation and how to write the configuration file to be used with GUI.
This project is also hosted on sourceforge.net https://lauetoolsnn.sourceforge.io


### Documentation
------------------------------
Documentation (under construction) for lauetoolsnn/lauenn is on the following webpage
https://lauenn.readthedocs.io/en/latest/


### Example case
------------------------------
Two example case studies are included in the lauetoolsnn\examples folder.
Run the GUI by either launching directly from the terminal using the 'lauetoolsnn' command or by running it locally with python lauetoolsneuralnetwork.py command.

First step is to load the config.txt from the example folder, it sets all the values of the GUI to the case study.
In the GUI: 
- Step1: File --> load config . Select the config file from the example directory. 
- Step1a: If config file is not available, one can set parameters in the configure parameters window directly.
- Step2: Press the configure parameters button and press Accept button at the end (the values are loaded from the config file).
- Step3: Press Generate Training dataset button. This will generate the training and validation dataset for neural network.
- Step4: Press Train Neural network button. This will start the training process and once finished will save the trained model.
- Step5: Press the Live prediction with IPF map to start the prediction on predefined experimental dataset. Example datafile is included in the examples folder.
- Step6: Once analyzed, the results can be saved using the save results button.

In addition, all the above mentioned steps can be done without the GUI and are detailed in the lauetoolsnn\example_notebook_scripts folder.
Jupyter notebook scripts are provided to run all the steps sequentially.

The indexed orientation matrix is also written in ".ctf" format, which can then be opened with channel 5 Aztec or MTEX software to do post processing related to orientations analysis. MTEX post processing script is also included in the lauetoolsnn\util_script\MTEX_plot.m


### Citation
------------------------------
If you use this software, please cite it using the metadata available in the citation_bibtex.cff file in root.
``` bash
Purushottam Raj Purohit, R. R. P., Tardif, S., Castelnau, O., Eymery, J., Guinebretiere, R., Robach, O., Ors, T. & Micha, J.-S. (2022). J. Appl. Cryst. 55, 737-750.
```


### Known Issues
------------------------------
So far, there is a issue with H5py and HDF5 version in the windows installation with conda. If error with H5py version mismatch exist after conda installation, please try "pip install lauetoolsnn" on windows as this should not have this problem. The other possibility is to install the H5py with pip before or after installing lauetoolsnn with conda.


### Support
------------------------------
Do not hesitate to contact the development team at [purushot@esrf.fr](mailto:purushot@esrf.fr) or [micha@esrf.fr](mailto:micha@esrf.fr).

### Funding
------------------------------
This code was developed as a result of French-German project funded respectively by the ANR and DFG (HoTMiX project reference number ANR-19-CE09-0035-01): https://www.bam.de/Content/EN/Projects/HoTMiX/hotmix.html

### Maintainer(s)
------------------------------
* [Ravi PURUSHOTTAM](https://github.com/ravipurohit1991)
