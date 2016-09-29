#!/usr/bin/env bash

# need to switch to conda env in the same shell as the tests are run
# but circle each command has its own environment

set -e # exit on error

source activate dexpy_env
coverage run setup.py test
coverage html -d $CIRCLE_ARTIFACTS
