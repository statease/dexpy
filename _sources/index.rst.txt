.. dexpy documentation master file
.. include:: <isonum.txt>

dexpy - Design of Experiments (DOE) in Python
=============================================

dexpy is a Design of Experiments (DOE) package based
on the Design-Expert |reg| `software
<http://www.statease.com/software.html>`_ from `Stat-Ease, Inc
<https://www.statease.com/>`_. If you're new to
the area of DOE, `here is a primer
<http://www.itl.nist.gov/div898/handbook/pri/section1/pri1.htm>`_
to help get you started.

The primary purpose of this package is to construct
experimental designs. After performing your experiment, you can
analyze the collected data using packages such
as `statsmodels <https://github.com/statsmodels/statsmodels/>`_.
However, there are also functions that fill in holes in the existing statistical
analysis packages, for example :ref:`statistical power <power>`.

.. toctree::
    :maxdepth: 2

    install
    design-build
    evaluation
    analysis
    confirmation
    optimization
    reference
    example-coffee
    example-optimal


Indices and tables
==================

* :ref:`genindex`
* :ref:`search`
