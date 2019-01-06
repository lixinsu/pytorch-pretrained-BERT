#!/bin/bash

export PYTHONPATH=`pwd`
export SQUAD_DIR=/users/sulixin/research/sigir/pytorch-pretrained-BERT/data/datasets/sogou_rc

python3 examples/rc_online.py \
  --bert_model bert-base-chinese \
  --task sogou \
  --do_predict \
  --learning_rate 3e-5 \
  --num_train_epochs 2.0 \
  --max_seq_length 200 \
  --max_query_length 20 \
  --doc_stride 128 \
  --output_dir data/models/sogou_rc_b12_truncated/
