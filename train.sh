#!/bin/bash
# export PATH=/path/to/your/python:$PATH
PYTHON_SCRIPT="train/train.py"
DEVICE="cuda"
OUTPUT_PATH="train/output"
LR=3e-5
DROPOUT=0.1
EPOCHS=3
BATCH_SIZE_TRAIN=16
BATCH_SIZE_EVAL=16
NUM_WORKERS=0
EVAL_STEP=20
MAX_LEN=32
SEED=42
TRAIN_FILE="train/data/nli_for_simcse.csv"
DEV_FILE="train/data/stsbenchmark/sts-dev.csv"
TEST_FILE="train/data/stsbenchmark/sts-test.csv"
PRETRAIN_MODEL_PATH="train/pretrain_models/bert-base-uncased"
POOLER="cls"
TRAIN_MODE="unsupervise"
FILE_TYPE="mysql"
HOST=""
DATABASE=""
USER=""
PASSWORD=""
QUERY=""

python $PYTHON_SCRIPT \
  --device $DEVICE \
  --output_path $OUTPUT_PATH \
  --lr $LR \
  --dropout $DROPOUT \
  --epochs $EPOCHS \
  --batch_size_train $BATCH_SIZE_TRAIN \
  --batch_size_eval $BATCH_SIZE_EVAL\
  --num_workers $NUM_WORKERS \
  --eval_step $EVAL_STEP \
  --max_len $MAX_LEN \
  --seed $SEED \
  --train_file $TRAIN_FILE \
  --dev_file $DEV_FILE \
  --test_file $TEST_FILE \
  --pretrain_model_path $PRETRAIN_MODEL_PATH \
  --pooler $POOLER \
  --train_mode $TRAIN_MODE \
  --overwrite_cache \
  --do_train  \
  --do_predict \
  --file_type $FILE_TYPE \
  --host $HOST \
  --database $DATABASE \
  --user $USER \
  --password $PASSWORD \
  --query "$QUERY"

