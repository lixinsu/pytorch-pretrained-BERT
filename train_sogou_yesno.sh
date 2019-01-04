#!/bin/bash

export PYTHONPATH=`pwd`
export SQUAD_DIR=/users/sulixin/research/sigir/pytorch-pretrained-BERT/data/datasets/sogou_yesno

python3 examples/run_classifier.py \
  --bert_model bert-base-chinese \
  --task_name sogouyesno \
  --do_train \
  --do_eval \
  --data_dir $SQUAD_DIR \
  --train_batch_size 64 \
  --learning_rate 3e-5 \
  --num_train_epochs 3.0 \
  --max_seq_length 144 \
  --output_dir data/models/sogou_yesno_b64_truncated/
