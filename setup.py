from setuptools import setup

VERSION = '0.1'
DESCRIPTION = "Design of Experiments for Python"

CLASSIFIERS = filter(None, map(str.strip,
"""
Development Status :: 2 - Pre-Alpha
Intended Audience :: Manufacturing
Intended Audience :: Science/Research
License:: OSI Approved:: Apache Software License
Programming Language :: Python
Programming Language :: Python :: 2
Programming Language :: Python :: 3
Topic :: Scientific/Engineering :: Mathematics
""".splitlines()))

def run_setup():
    setup(
        name='dexpy',
        version=VERSION,
        description=DESCRIPTION,
        classifiers=CLASSIFIERS,
        author='Hank Anderson, Martin Bezener',
        author_email='hank@statease.com',
        license='apache',
        url='https://statease.github.io/dexpy/',
        packages=['dexpy', 'dexpy.tests'],
        install_requires=['numpy', 'patsy', 'pandas', 'scipy'],
    )

run_setup()
