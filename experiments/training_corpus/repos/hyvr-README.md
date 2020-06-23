====================================================================
Introduction
====================================================================

**HyVR: Turning your geofantasy into reality!** 

The Hydrogeological Virtual Reality simulation package (HyVR) is a Python module
that helps researchers and practitioners generate subsurface models with
multiple scales of heterogeneity that are based on geological concepts. The
simulation outputs can then be used to explore groundwater flow and solute
transport behaviour. This is facilitated by HyVR outputs in common flow
simulation packages' input formats. As each site is unique, HyVR has been
designed that users can take the code and extend it to suit their particular
simulation needs.

The original motivation for HyVR was the lack of tools for modelling sedimentary
deposits that include bedding structure model outputs (i.e., dip and azimuth).
Such bedding parameters were required to approximate full hydraulic-conductivity
tensors for groundwater flow modelling. HyVR is able to simulate these bedding
parameters and generate spatially distributed parameter fields, including full
hydraulic-conductivity tensors. More information about HyVR is available in the
online `technical documentation <https://driftingtides.github.io/hyvr/index.html>`_.

I hope you enjoy using HyVR much more than I enjoyed putting it together! I look
forward to seeing what kind of funky fields you created in the course of your
work.

*HyVR can be attributed by citing the following journal article: Bennett, J. P., Haslauer, C. P., Ross, M., & Cirpka, O. A. (2018). An open, object-based framework for generating anisotropy in sedimentary subsurface models. Groundwater. DOI:* `10.1111/gwat.12803 <https://onlinelibrary.wiley.com/doi/abs/10.1111/gwat.12803>`_. *A preprint version of the article is available* `here <https://github.com/driftingtides/hyvr/blob/master/docs/Bennett_GW_2018.pdf>`_.

Installing the HyVR package
--------------------------------------

Installing Python
^^^^^^^^^^^^^^^^^


Windows
"""""""

If you are using Windows, we recommend installing the `Anaconda distribution
<https://www.anaconda.com/download/>`_ of Python 3. This distribution has the
majority of dependencies that HyVR requires.

It is also a good idea to install the HyVR package into a `virtual environment
<https://conda.io/docs/user-guide/tasks/manage-environments.html>`_. Do this by
opening a command prompt window and typing the following::

    conda create --name hyvr_env

You need to then activate this environment::

    conda activate hyvr_env
	

Linux
"""""

Depending on your preferences you can either use the Anaconda/Miniconda
distribution of python, or the version of your package manager. If you choose
the former, follow the same steps as for Windows.

If you choose the latter, you probably already have Python 3 installed. If not,
you can install it using your package manager (e.g. ``apt`` on Ubuntu/Debian).

In any way we recommend using a virtual environment. Non-conda users can use
`virtualenvwrapper <https://virtualenvwrapper.readthedocs.io/en/latest/>`_ or
`pipenv <https://docs.pipenv.org/>`_.


Installing HyVR
^^^^^^^^^^^^^^^

Once you have activated your virtual environment, you can install HyVR from PyPI using ``pip``::

    pip install hyvr

The version on PyPI should always be up to date. If it's not, you can also
install HyVR from github::

    git clone https://github.com/driftingtides/hyvr.git
    pip install hyvr

To install from source you need a C compiler.

Installation from conda-forge will (hopefully) be coming soon.


Usage
-----

To use HyVR you have to create a configuration file with your settings.
You can then run HyVR the following way::

    (hyvr_env) $ python -m hyvr my_configfile.ini

HyVR will then run and store all results in a subdirectory. If no configfile is
given, it will run a test case instead::

    (hyvr_env) $ python -m hyvr

If you want to use HyVR in a script, you can import it and use the ``run`` function::

    import hyvr
    hyvr.run('my_configfile.ini')
    
Examples can be found in the ``testcases`` directory of the `github repository
<https://github.com/driftingtides/hyvr/>`_, the general setup and possible
options of the config-file are described in the documentation.
Currently only ``made.ini`` is ported to version 1.0.0.

Source
------
The most current version of HyVR will be available at this `github repository
<https://github.com/driftingtides/hyvr/>`_; a version will also be available on
the `PyPI index <https://pypi.python.org/pypi/hyvr/>`_ which can be installed
using ``pip``.


Requirements
------------

Python
^^^^^^
HyVR was developed for use with Python 3.4 or greater. It may be possible to use
with earlier versions of Python 3, however this has not been tested.

Dependencies
^^^^^^^^^^^^^^

* `numpy <http://www.numpy.org/>`_ <= 1.13.3
* `matplotlib <https://matplotlib.org/>`_ <= 2.1.0
* `scipy <https://www.scipy.org/scipylib/index.html>`_ = 1.0.0
* `pandas <https://pandas.pydata.org/>`_ = 0.21.0
* `flopy <https://github.com/modflowpy/flopy>`_ == 3.2.9 (optional for modflow output)
* `pyevtk <https://pypi.python.org/pypi/PyEVTK>`_ = 1.1.0 (optional for VTK output)
* `h5py <https://www.h5py.org/>`_ (optional for HDF5 output)


Development
-----------
HyVR has been developed by Jeremy
Bennett (`website <https://jeremypaulbennett.weebly.com>`_) as part of his
doctoral research at the University of Tübingen and by Samuel Scherrer as a
student assistant.

You can contact the developer(s) of HyVR by `email <mailto:hyvr.sim@gmail.com>`_
or via github.

Problems, Bugs, Unclear Documentation
-------------------------------------

If you have problems with HyVR have a look at the `troubleshooting
<https://driftingtides.github.io/hyvr/troubleshooting.html>`_ section. If this
doesn't help, don't hesitate to contact us via email or at github.

If you find that the documentation is unclear, lacking, or wrong, please also contact us.
