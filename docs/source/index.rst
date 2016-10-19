.. dexpy documentation master file

dexpy - Design of Experiments in Python
=======================================

dexpy is a package for doing Design of Experiments in Python. If you don't know what Design of Experiments is, this
probably isn't the package for you, but `here is a primer anyway
<http://www.statease.com/media/productattachments/files/d/o/doeprimer.pdf>`_.

The primary purpose of this package is to construct designs, which can then be analyzed using packages such as
`statsmodels <https://github.com/statsmodels/statsmodels/>`_. However, there are also functions that fill in holes in
the existing statistical analysis packages, for example :ref:`statistical power <power>`.

As of this writing there are only a handful of :ref:`Factorial designs <factorial>` available, but the catalog will be expanding to include
standard textbook designs like `Central Composite designs <https://en.wikipedia.org/wiki/Central_composite_design>`_,
as well as more flexible `Optimal designs <https://en.wikipedia.org/wiki/Optimal_design>`_.

.. toctree::
    :maxdepth: 2

    design-build
    evaluation
    analysis
    confirmation
    optimization


Indices and tables
==================

* :ref:`genindex`
* :ref:`search`
