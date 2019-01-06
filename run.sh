#!/bin/bash

export SQUAD_DIR=/users/sulixin/research/sigir/pytorch-pretrained-BERT/data/datasets/squad

python3 examples/run_squad.py \
  --learning_rate 3e-5 \
  --doc_stride 128 \
  --config $1
