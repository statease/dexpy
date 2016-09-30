#!/usr/bin/env bash

# these are duplicated in circle.yml
CONDA_ROOT=${HOME}/.miniconda
DEXPY_ENV_NAME=dexpy_env
DEXPY_ENV_ROOT=${CONDA_ROOT}/envs/${DEXPY_ENV_NAME}
DEXPY_DEPENDENCIES="numpy scipy matplotlib coverage sphinx sphinx_rtd_theme patsy pandas"

if [[ ! -d ${CONDA_ROOT} ]]; then
    echo "Installing Miniconda...";
    wget --quiet https://repo.continuum.io/miniconda/Miniconda3-3.16.0-Linux-x86_64.sh
    bash Miniconda3-3.16.0-Linux-x86_64.sh -bf -p ${CONDA_ROOT};
fi

if [ ! -d ${DEXPY_ENV_ROOT} ]; then
    ${CONDA_ROOT}/bin/conda create -y -n ${DEXPY_ENV_NAME} ${DEXPY_DEPENDENCIES};
else
    ${CONDA_ROOT}/bin/conda install -y -n ${DEXPY_ENV_NAME} ${DEXPY_DEPENDENCIES};
fi
