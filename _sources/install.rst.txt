Installation
============

dexpy can be installed using `pip`, which will install the dependencies
automatically. Windows users should see the note below.

.. code-block:: batch

    pip install dexpy

Dependencies on Windows
-----------------------

dexpy uses ``numpy`` and ``scipy``, which can be difficult to build on Windows
via pip. You may consider to using `Anaconda
<https://www.continuum.io/downloads>`_ or `Miniconda
<http://conda.pydata.org/miniconda.html>`_ to install prebuilt numpy/scipy
binaries. This can be done by creating an environment containing these packages
, then installing.

.. code-block:: batch

    conda create --name dexpy_env numpy scipy pandas patsy
    activate dexpy_env
    pip install dexpy

You can use whatever name you want in place of ``dexpy_env``.
