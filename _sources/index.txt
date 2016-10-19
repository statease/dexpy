.. dexpy documentation master file
.. include:: <isonum.txt>

dexpy - Design of Experiments in Python
=======================================

dexpy is a Design of Experiments package based on the Design-Expert |reg| `software
<http://www.statease.com/software.html>`_ from `Stat-Ease, Inc.
<https://www.statease.com/>`_. If you're new to
the area of Design of Experiments is, `here is a primer
<https://en.wikipedia.org/wiki/Design_of_experiments>`_
to help get you started.

The primary purpose of this package is to construct
experimental designs. After performing your experiment, you can
analyze the collected data using packages such
as `statsmodels <https://github.com/statsmodels/statsmodels/>`_.
However, there are also functions that fill in holes in the existing statistical
analysis packages, for example :ref:`statistical power <power>`.

As of this writing there are only a handful of designs available,
but the catalog will be expanding to include standard textbook designs
like `Central Composite designs <https://en.wikipedia.org/wiki/Central_composite_design>`_,
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
