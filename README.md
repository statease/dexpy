# dexpy

[![CircleCI](https://circleci.com/gh/statease/dexpy.svg?style=svg&circle-token=f7db0120c3ec3786badb247f492d233e59977f62)](https://circleci.com/gh/statease/dexpy)
[![codecov](https://codecov.io/gh/statease/dexpy/branch/master/graph/badge.svg)](https://codecov.io/gh/statease/dexpy)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/cc9c5a5d892f4f87b130c6b06cc85e21)](https://www.codacy.com/app/hank-p-anderson/dexpy?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=statease/dexpy&amp;utm_campaign=Badge_Grade)
[![Code Health](https://landscape.io/github/statease/dexpy/master/landscape.svg?style=flat)](https://landscape.io/github/statease/dexpy/master)

**dexpy** is a Python package for [Design of Experiments](http://www.itl.nist.gov/div898/handbook/pri/section1/pri1.htm).

## Installation

dexpy can be installed using `pip`, which will install the dependencies
automatically. Windows users should see the note below.

    pip install dexpy

### Dependencies on Windows

dexpy uses `numpy` and `scipy`, which can be difficult to build on Windows via
pip. You may consider to using [Anaconda](https://www.continuum.io/downloads)
or [Miniconda](http://conda.pydata.org/miniconda.html) to install prebuilt
numpy/scipy binaries. This can be done by creating an environment containing
these packages.

    conda create --name dexpy_env numpy scipy pandas patsy
    activate dexpy_env
    pip install dexpy

## Documentation

See https://statease.github.io/dexpy.

## License

**dexpy** is licensed under the Apache 2.0 license. Details can be found in the `LICENSE` file.
