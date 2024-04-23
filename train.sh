#!/bin/bash
# export PATH=/path/to/your/python:$PATH
PYTHON_SCRIPT="train/train.py"
DEVICE="cuda"
OUTPUT_PATH="train/output"
LR=3e-5
DROPOUT=0.2
EPOCHS=3
BATCH_SIZE_TRAIN=32
BATCH_SIZE_EVAL=64
NUM_WORKERS=0
EVAL_STEP=100
MAX_LEN=256
SEED=42
TRAIN_FILE="train/data/janitor_rec_train.json"
DEV_FILE="train/data/stsbenchmark/sts-dev.csv"
TEST_FILE="train/data/stsbenchmark/sts-test.csv"
PRETRAIN_MODEL_PATH="train/pretrain_models/bert-base-uncased"
POOLER="cls"
TRAIN_MODE="unsupervise"
FILE_TYPE="local"
HOST="1"
DATABASE="1"
USER="1"
PASSWORD="1"
QUERY="1"

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
  --file_type $FILE_TYPE \
  --host $HOST \
  --database $DATABASE \
  --user $USER \
  --password $PASSWORD \
  --query "$QUERY"\
  --do_predict \
  --do_train  

