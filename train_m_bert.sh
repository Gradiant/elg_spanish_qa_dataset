#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

TRAIN_FILE=$1
PREDICT_FILE=$2
SQUAD_V2=$3
TRAIN_FROM_MODEL=$4

TRAINING_DIR=${SCRIPT_DIR}/data/training/m-bert_$(basename ${TRAIN_FILE})
mkdir -p ${TRAINING_DIR}

# If no starting model is provided,
# start the training from the Multilingual BERT
if [[ -z ${TRAIN_FROM_MODEL} ]]; then
  TRAIN_FROM_MODEL=bert-base-multilingual-cased
fi
TRANSFORMERS_DIR=${SCRIPT_DIR}/TranslateAlignRetrieve/tools/transformers

if [[ ! -z ${SQUAD_V2} ]]; then
  python ${TRANSFORMERS_DIR}/examples/run_squad.py \
         --model_type bert \
         --model_name_or_path ${TRAIN_FROM_MODEL} \
         --do_train \
         --train_file ${TRAIN_FILE}\
         --save_steps 10000 \
         --predict_file ${PREDICT_FILE} \
         --version_2_with_negative \
         --overwrite_output_dir \
         --overwrite_cache \
         --output_dir ${TRAINING_DIR}
else
  python ${TRANSFORMERS_DIR}/examples/run_squad.py \
         --model_type bert \
         --model_name_or_path ${TRAIN_FROM_MODEL} \
         --do_train \
         --train_file ${TRAIN_FILE}\
         --save_steps 10000 \
         --predict_file ${PREDICT_FILE} \
         --overwrite_output_dir \
         --overwrite_cache \
         --output_dir ${TRAINING_DIR}
fi

