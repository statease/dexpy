
try:
    from setuptools import setup, Command
except ImportError:
    from distutils.core import setup, Command

VERSION = '0.1'
DESCRIPTION = "Design of Experiments for Python"

class TestCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import sys, subprocess
        raise SystemExit(subprocess.call([sys.executable, 'dexpy/tests/__init__.py']))

def run_setup():
    cmdclass = dict(test = TestCommand)

    setup(
        name='dexpy',
        version=VERSION,
        description=DESCRIPTION,
        author='Hank Anderson',
        author_email='hank@statease.com',
        url='https://statease.github.io/dexpy/',
        packages=['dexpy', 'dexpy.tests'],
        install_requires=['numpy'],
    )

run_setup()
