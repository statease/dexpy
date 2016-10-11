from setuptools import setup

VERSION = '0.1'
DESCRIPTION = "Design of Experiments for Python"

def run_setup():
    setup(
        name='dexpy',
        version=VERSION,
        description=DESCRIPTION,
        author='Hank Anderson',
        author_email='hank@statease.com',
        url='https://statease.github.io/dexpy/',
        packages=['dexpy', 'dexpy.tests'],
        install_requires=['numpy', 'scipy'],
    )

run_setup()
