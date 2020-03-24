OMF-VTK
=======

.. image:: https://img.shields.io/pypi/v/omfvista.svg?logo=python&logoColor=white
   :target: https://pypi.org/project/omfvista/
   :alt: PyPI

.. image:: https://img.shields.io/travis/OpenGeoVis/omfvista/master.svg?label=build&logo=travis
   :target: https://travis-ci.org/OpenGeoVis/omfvista
   :alt: Build Status Linux

.. image:: https://ci.appveyor.com/api/projects/status/49tewkw60mykh1nb?svg=true
   :target: https://ci.appveyor.com/project/banesullivan/omfvista
   :alt: Build Status Windows

.. image:: https://codecov.io/gh/OpenGeoVis/omfvista/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/OpenGeoVis/omfvista

.. image:: https://img.shields.io/github/stars/OpenGeoVis/omfvista.svg?style=social&label=Stars
   :target: https://github.com/OpenGeoVis/omfvista
   :alt: GitHub


A PyVista (and VTK) interface for the `Open Mining Format package`_ (``omf``)
providing Python 3D visualization and useable mesh data structures for
processing datasets in the OMF specification.


.. _Open Mining Format package: https://omf.readthedocs.io/en/latest/

Documentation is hosted at https://opengeovis.github.io/omfvista/


Installation
------------

Installation is simply::

    pip install omfvista

All necessary dependencies will be installed alongside ``omfvista``. Please
note that this package heavily leverages the PyVista_ package.

.. _PyVista: https://github.com/pyvista/pyvista


Questions & Support
-------------------

For general questions about the project, its applications, or about software
usage, please create an issue in the `pyvista/pyvista-support`_ repository
where the  PyVista community can collectively address your questions.
You are also welcome to join us on join `@OpenGeoVis`_ on our
`Slack workspace`_ under the ``#omfvista`` channel or send one of the
developers an email. The project support team can be reached at
`info@opengeovis.org`_.

.. _pyvista/pyvista-support: https://github.com/pyvista/pyvista-support
.. _@OpenGeoVis: https://github.com/OpenGeoVis
.. _Slack workspace: http://slack.opengeovis.org
.. _info@opengeovis.org: mailto:info@opengeovis.org

Example Use
-----------

.. image:: https://mybinder.org/badge_logo.svg
   :target: https://mybinder.org/v2/gh/OpenGeoVis/omfvista/master?filepath=Example.ipynb

Be sure to check out the `Example Notebook`_ that demos ``omfvista`` or our
`Example Gallery`_ in the documentation!
Here's an example using the sample data hosted in the `OMF repository`_.

.. _Example Notebook: https://mybinder.org/v2/gh/OpenGeoVis/omfvista/master?filepath=Example.ipynb
.. _Example Gallery: https://opengeovis.github.io/omfvista/examples/index.html
.. _OMF repository: https://github.com/gmggroup/omf/tree/master/assets

.. code-block:: python

    import pyvista as pv
    import omfvista

    project = omfvista.load_project('test_file.omf')
    project

.. image:: https://github.com/OpenGeoVis/omfvista/raw/master/assets/table-repr.png
   :alt: Table Representation


Once the data is loaded as a ``pyvista.MultiBlock`` dataset from ``omfvista``, then
that object can be directly used for interactive 3D visualization from PyVista_:

.. code-block:: python

    project.plot(notebook=False)

Or an interactive scene can be created and manipulated to create a compelling
figure directly in a Jupyter notebook. First, grab the elements from the project:

.. code-block:: python

    # Grab a few elements of interest and plot em up!
    vol = project['Block Model']
    assay = project['wolfpass_WP_assay']
    topo = project['Topography']
    dacite = project['Dacite']

Then apply a filtering tool from PyVista_ to the volumetric data:

.. code-block:: python

    thresher = pv.Threshold(vol)

.. figure:: https://github.com/OpenGeoVis/omfvista/raw/master/assets/threshold.gif
   :alt: IPython Thresholding Tool

Then you can put it all in one environment!

.. code-block:: python

    # Grab the active plotting window
    #  from the thresher tool
    p = thresher.plotter
    # Add our datasets
    p.add_mesh(topo, cmap='gist_earth', opacity=0.5)
    p.add_mesh(assay, color='blue', line_width=3)
    p.add_mesh(dacite, color='yellow', opacity=0.6)
    # Add the bounds axis
    p.show_bounds()


.. figure:: https://github.com/OpenGeoVis/omfvista/raw/master/assets/interactive.gif
   :alt: Interactive Rendering


And once you like what the render view displays, you can save a screenshot:

.. code-block:: python

    p.screenshot('wolfpass.png')

.. image:: https://github.com/OpenGeoVis/omfvista/raw/master/wolfpass.png
   :alt: Wolf Pass Screenshot
