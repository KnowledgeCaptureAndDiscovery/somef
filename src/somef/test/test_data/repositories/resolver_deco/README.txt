========================================
Decorator for resolve function arguments
========================================

.. image:: https://api.travis-ci.org/zzzsochi/resolver_deco.svg
  :target:  https://secure.travis-ci.org/zzzsochi/resolver_deco
  :align: center

.. image:: https://coveralls.io/repos/zzzsochi/resolver_deco/badge.svg
  :target:  https://coveralls.io/r/zzzsochi/resolver_deco
  :align: center

-----
Usage
-----

.. code:: python

    from resolver_deco import resolver


    @resolver('obj')
    def get_attribute(obj, name):
        return getattr(obj, name)


    import os.path
    assert get_attribute('os.path', 'isdir') == os.path.isdir


You can resolve more than one argument:

.. code:: python

    from resolver_deco import resolver


    @resolver('obj', 'value')
    def set_attribute(obj, name, value):
        return setattr(obj, name, value)


    set_attribute('collections.UserDict', 'val', 'os.path')

    import collections, os.path
    assert collections.UserDict.val is os.path


-----
Tests
-----

.. code:: shell

    $ pip install pytest
    $ py.test tests.py -v
