#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Build the environment (conda)
conda create -n microservstarenv python=3.8 --yes

# activate the environment
eval "$(conda shell.bash hook)"
conda activate microservstarenv

# Cloning the original project
git clone https://github.com/ccasimiro88/TranslateAlignRetrieve


# install the requirements
pip install -r requirements.txt


# Install non-python libraries
TOOLS_DIR=${SCRIPT_DIR}/TranslateAlignRetrieve/tools
mkdir -p ${TOOLS_DIR}

# Transformers
TRANSFORMERS_DIR=${TOOLS_DIR}/transformers
git clone https://github.com/huggingface/transformers.git --branch v2.5.1 ${TRANSFORMERS_DIR}

# MLQA
MLQA_DIR=${TOOLS_DIR}/MLQA
git clone https://github.com/facebookresearch/MLQA.git ${TOOLS_DIR}/MLQA
