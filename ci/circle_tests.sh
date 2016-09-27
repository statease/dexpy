# need to switch to conda env in the same shell as the tests are run
# but circle each command has its own environment
source activate dexpy_env
coverage setup.py test
coverage html -d $CIRCLE_ARTIFACTS
