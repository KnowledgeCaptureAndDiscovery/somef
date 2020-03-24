==========
Tilematrix
==========

Tilematrix handles geographic web tiles and tile pyramids.

.. image:: https://badge.fury.io/py/tilematrix.svg
    :target: https://badge.fury.io/py/tilematrix

.. image:: https://travis-ci.org/ungarj/tilematrix.svg?branch=master
    :target: https://travis-ci.org/ungarj/tilematrix

.. image:: https://coveralls.io/repos/github/ungarj/tilematrix/badge.svg?branch=master
    :target: https://coveralls.io/github/ungarj/tilematrix?branch=master

.. image:: https://img.shields.io/pypi/pyversions/mapchete.svg


The module is designed to translate between tile indices (zoom, row, column) and
map coordinates (e.g. latitute, longitude).

Tilematrix supports **metatiling** and **tile buffers**. Furthermore it makes
heavy use of shapely_ and it can also generate ``Affine`` objects per tile which
facilitates working with rasterio_ for tile based data reading and writing.

It is very similar to mercantile_ but besides of supporting spherical mercator
tile pyramids, it also supports geodetic (WGS84) tile pyramids.

.. _shapely: http://toblerity.org/shapely/
.. _rasterio: https://github.com/mapbox/rasterio
.. _mercantile: https://github.com/mapbox/mercantile

------------
Installation
------------

Use ``pip`` to install the latest stable version:

.. code-block:: shell

    pip install tilematrix

Manually install the latest development version

.. code-block:: shell

    pip install -r requirements.txt
    python setup.py install


-------------
Documentation
-------------

* `API documentation <doc/tilematrix.md>`_
* `examples <doc/examples.md>`_

CLI
---

This package ships with a command line tool ``tmx`` which provides the following
subcommands:

* ``bounds``: Print bounds of given Tile.
* ``bbox``: Print bounding box geometry of given Tile.
* ``tile``: Print Tile covering given point.
* ``tiles``: Print Tiles covering given bounds.

Geometry outputs can either be formatted as ``WKT`` or ``GeoJSON``. For example
the following command will print a valid ``GeoJSON`` representing all tiles
for zoom level 1 of the ``geodetic`` WMTS grid:

.. code-block:: shell

    $ tmx -f GeoJSON tiles -- 1 -180 -90 180 90
    {
      "type": "FeatureCollection",
      "features": [
        {"geometry": {"coordinates": [[[-90.0, 0.0], [-90.0, 90.0], [-180.0, 90.0], [-180.0, 0.0], [-90.0, 0.0]]], "type": "Polygon"}, "properties": {"col": 0, "row": 0, "zoom": 1}, "type": "Feature"},
        {"geometry": {"coordinates": [[[0.0, 0.0], [0.0, 90.0], [-90.0, 90.0], [-90.0, 0.0], [0.0, 0.0]]], "type": "Polygon"}, "properties": {"col": 1, "row": 0, "zoom": 1}, "type": "Feature"},
        {"geometry": {"coordinates": [[[90.0, 0.0], [90.0, 90.0], [0.0, 90.0], [0.0, 0.0], [90.0, 0.0]]], "type": "Polygon"}, "properties": {"col": 2, "row": 0, "zoom": 1}, "type": "Feature"},
        {"geometry": {"coordinates": [[[180.0, 0.0], [180.0, 90.0], [90.0, 90.0], [90.0, 0.0], [180.0, 0.0]]], "type": "Polygon"}, "properties": {"col": 3, "row": 0, "zoom": 1}, "type": "Feature"},
        {"geometry": {"coordinates": [[[-90.0, -90.0], [-90.0, 0.0], [-180.0, 0.0], [-180.0, -90.0], [-90.0, -90.0]]], "type": "Polygon"}, "properties": {"col": 0, "row": 1, "zoom": 1}, "type": "Feature"},
        {"geometry": {"coordinates": [[[0.0, -90.0], [0.0, 0.0], [-90.0, 0.0], [-90.0, -90.0], [0.0, -90.0]]], "type": "Polygon"}, "properties": {"col": 1, "row": 1, "zoom": 1}, "type": "Feature"},
        {"geometry": {"coordinates": [[[90.0, -90.0], [90.0, 0.0], [0.0, 0.0], [0.0, -90.0], [90.0, -90.0]]], "type": "Polygon"}, "properties": {"col": 2, "row": 1, "zoom": 1}, "type": "Feature"},
        {"geometry": {"coordinates": [[[180.0, -90.0], [180.0, 0.0], [90.0, 0.0], [90.0, -90.0], [180.0, -90.0]]], "type": "Polygon"}, "properties": {"col": 3, "row": 1, "zoom": 1}, "type": "Feature"}
      ]
    }



Print ``WKT`` representation of tile ``4 15 23``:

.. code-block:: shell

    $ tmx bbox 4 15 23
    POLYGON ((90 -90, 90 -78.75, 78.75 -78.75, 78.75 -90, 90 -90))


Also, tiles can have buffers around called ``pixelbuffer``:

.. code-block:: shell

    $ tmx --pixelbuffer 10 bbox 4 15 23
    POLYGON ((90.439453125 -90, 90.439453125 -78.310546875, 78.310546875 -78.310546875, 78.310546875 -90, 90.439453125 -90))


Print ``GeoJSON`` representation of tile ``4 15 23`` on a ``mercator`` tile
pyramid:

.. code-block:: shell

    $ tmx -output_format GeoJSON -grid mercator bbox 4 15 15
    {"type": "Polygon", "coordinates": [[[20037508.342789203, -20037508.3427892], [20037508.342789203, -17532819.799940553], [17532819.799940553, -17532819.799940553], [17532819.799940553, -20037508.3427892], [20037508.342789203, -20037508.3427892]]]}



-------
License
-------

MIT License

Copyright (c) 2015, 2016, 2017 `EOX IT Services`_

.. _`EOX IT Services`: https://eox.at/
