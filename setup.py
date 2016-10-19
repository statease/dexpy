"""dexpy: Design of Experiments for Python.

dexpy is a Design of Experiments package based on the Design-Expert (r) software from Stat-Ease, Inc.

See: https://statease.github.io/dexpy
"""

from setuptools import setup

VERSION = '0.11'
DOCLINES = (__doc__ or '').split("\n")

CLASSIFIERS = filter(None, map(str.strip,
"""
Development Status :: 2 - Pre-Alpha
Intended Audience :: Manufacturing
Intended Audience :: Science/Research
License :: OSI Approved :: Apache Software License
Programming Language :: Python
Programming Language :: Python :: 2
Programming Language :: Python :: 3
Topic :: Scientific/Engineering :: Mathematics
""".splitlines()))

def run_setup():
    setup(
        name='dexpy',
        version=VERSION,
        description=DOCLINES[0],
        long_description="\n".join(DOCLINES[2:]),
        classifiers=CLASSIFIERS,
        author='Hank Anderson, Martin Bezener',
        author_email='hank@statease.com',
        license='apache',
        url='https://statease.github.io/dexpy/',
        download_url = 'https://github.com/statease/dexpy/releases',
        packages=['dexpy', 'dexpy.tests'],
        install_requires=['numpy', 'patsy', 'pandas', 'scipy'],
    )

run_setup()
