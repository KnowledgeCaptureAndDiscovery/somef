
<img src="./EUVpy_logo.png" width="400">

[_(EUV imagery of the solar disk, taken by NASA SDO)_](https://www.nist.gov/image/1280px-sun-august12010jpg)

# Overview
`EUVpy` is a Python module that contains the NEUVAC empirical model of solar EUV irradiance for use primarily in thermosphere-ionosphere models. 
Conceptual development was carried out by Dr. Aaron J. Ridley and analysis and contributions were made by Dr. Daniel A. Brandt and Dr. Joseph Paki.

`EUVpy` also contains code for running, comparing, and analyzing the performance of NEUVAC in comparison to other 
empirical models such as EUVAC, HEUVAC, HFG, and FISM2. As such, the package includes access to EUVAC, HEUVAC, and HFG,
and allows the user to download the F10.7 index at will.

# Installation

You can obtain `EUVpy` with a simple git clone command. In the terminal, execute the following command:

> git clone https://github.com/DanBrandt/EUVpy.git

The EUVpy package provides access to the HEUVAC model, which is written in Fortran and requires gfortran to be installed. To 
install gfortran (if you don't already have it), open a terminal and execute the following command:

> sudo apt-get install gfortran

Now, enter into the package folder and run the following command in order to compile the Fortran code that HEUVAC 
alone depends upon:

> cd EUVpy\
> . install_heuvac.sh

If this step gives you trouble, try executing the following code **first**, and then retry the above commands.

> git submodule update --init --recursive --remote

After HEUVAC is compiled once, you should never have to compile it again.

Now you are in a position to install the rest of the EUVpy package. Before doing this, you will first want to initialize a Python virtual environment.

> cd ~/.virtualenvs\
> python**3.x** -m venv myVenv\
> pip install --upgrade pip\
> pip install wheel\
> source myVenv/bin/activate

Above, 'python**3.x**' refers to whatever version of Python 3 you have installed. EUVpy works with any version of Python 3.
You may now use one of two ways to install EUVpy. You can install from the cloned repo directly, or you can install from PyPI.

## Installing from the Cloned Repository

Navigate back to the package folder:

> cd\
> cd myDirectory/EUVpy

After this is done, simply execute the following command:

> pip install .

## Installing from PyPI

A simpler way to install also involves just entering the following in the terminal:

> pip install EUVpy

**Note:** If you choose this route, you'll have to install HEUVAC differently than described above. You will have to 
navigate the directory containing the HEUVAC files, and execute the following command, as follows:

> cd src/EUVpy/empiricalModels/models/HEUVAC/srcHEUVAC
> . compile.sh

You can then return to the top package directory. This should only have to be done once. 
This approach will be replaced with a user-friendly console script in the next release of this package.

### Unit Testing

**Note: this section only applies if you installed from the cloned repo.** 

Just to make sure everything installed correctly, while in the package folder, run the following command in the terminal.

> pytest

If all of the tests pass, you should be good to go! If you find an issue at this step (or any other) please don't hesitate
to reach out!

# Usage
EUVpy contains modules for **4** different EUV irradiance models. These models include:
* NEUVAC
* EUVAC
* HEUVAC
* HFG (SOLOMON)

We note that SOLOMON in the literature can either refer to the empirical model between F10.7 and 81 day-averaged F10.7 
centered on the current day (hereafter F10.7A) and EUV irradiance in 22 overlapping bands as described by Solomon and
Qian 2005, or it can refer to _any_ EUV irradiance data summed into those 22 overlapping bins (referred to as the STAN 
BANDS). In this package, SOLOMON only refers to the former, though functionality does exist to run all other models in
the STAN BANDS.

## Finding your way around

There are few folders in this package:
* **empiricalModels**: Contains code and data for EUVAC, HEUVAC, and SOLOMON, as well as FISM:
* **experiments**: Contains code and figures related to the publication associated with NEUVAC. In this folder, the file
_fitNeuvac.py_ s used for actually performing the NEUVAC fits between F10.7, F10.7A, and FISM2, while _uncNeuvac.py_ 
contains code for computing the correlation matrix used to enable running NEUVAC ensembles, as well as generating plots 
of the squared difference between NEUVAC and FISM2 in different bands.
* **NEUVAC**: Contains the code for running NEUVAC.
* **solarIndices**: Contains F10.7 solar index data, from both OMNIWeb and Penticton.
* **tools**: Contains code for miscellaneous helper functions. In this folder appears the following:
    * _EUV_: Contains numerous functions within fism2_process.py for reading in and rebinning FISM2 data.
    * _processIndices.py_: Contains functions for reading in, downloading, and cleaning OMNIWeb data.
    * _processIrradiances.py_: Contains functions for reading in data from TIMED/SEE, SDO/EVE, and FISM.
    * _spectralAnalysis.py_: Contains functions for converting between solar spectral irradiance and solar spectral flux.
    * _toolbox.py_: Contains miscellaneous helper functions that mainly focus on directory management, loading and saving data, statistics, and fitting.

Each of the models in EUVpy requires F10.7 as an input. To grab F10.7 between any two dates, simply do the following:

> from EUVpy.tools import processIndices
> 
> f107times, f107, f107a, f107b = processIndices.getCLSF107('YYYY-MM-DD', 'YYYY-MM-DD', truncate=False)

To import any of the models, simply do as follows:

<ins>NEUVAC</ins>
> from EUVpy.NEUVAC import neuvac
> 
> neuvacIrr, _, _, _ = neuvac.neuvacEUV(f107, f107b, bands='EUVAC')

<ins>EUVAC</ins>
> from EUVpy.empiricalModels.models.EUVAC import euvac
> 
> euvacFlux, euvacIrr, _, _, _ = euvac.euvac(f107, f107a)

<ins>HEUVAC</ins>
> from EUVpy.empiricalModels.models.HEUVAC import heuvac
> 
> heuvac_wav, heuvacFlux, heuvacIrr, _, _, _ = heuvac.heuvac(f107, f107a, torr=True)

<ins>SOLOMON</ins>
> from EUVpy.empiricalModels.models.SOLOMON import solomon
> 
> solomonFluxHFG, solomonIrrHFG = SOLOMON.solomon.solomon(f107, f107a, model='HFG')
>
> solomonFluxEUVAC, solomonIrrEUVAC = SOLOMON.solomon.solomon(f107, f107a, model='EUVAC')

# Examples

There is a [Python notebook](https://github.com/DanBrandt/EUVpy/blob/main/examples/euvpy_examples.ipynb) you can walk through in order to get familiar with the basic functionality of EUVpy.

We encourage you to peruse [more examples](https://github.com/DanBrandt/EUVpy/blob/main/docs/source/examples.rst) in the documentation for guidelines on how to run each of the models.

Due to the unique construction of NEUVAC, at present, we only recommend running ensembles for NEUVAC, and not any of the
other models.

# Code of Conduct
In using this code, depending on the module used, proper citations should be given to the original authors responsible
for developing each model or dataset:

<ins>NEUVAC:</ins> [Brandt and Ridley, 2024](https://agupubs.onlinelibrary.wiley.com/doi/pdfdirect/10.1029/2024SW004043)

<ins>EUVAC:</ins> [Richards, et al. 1994](https://agupubs.onlinelibrary.wiley.com/doi/abs/10.1029/94ja00518)

<ins>HEUVAC</ins> [Richards, et al. 2006](https://www.sciencedirect.com/science/article/pii/S0273117705008288?casa_token=zEhwbyXrC8MAAAAA:qHFmKe0ZDE4gMsAX9qAHESvPyoEDFLBlhHuLaEsIwYFykhFXN79--XttCW-QDg1sA4wgD54ysFc)

<ins>SOLOMON</ins> [Solomon and Qian, 2005](https://agupubs.onlinelibrary.wiley.com/doi/pdf/10.1029/2005JA011160)

<ins>FISM2:</ins> [Chamberlin, et al. 2020](https://agupubs.onlinelibrary.wiley.com/doi/pdf/10.1029/2020SW002588)
