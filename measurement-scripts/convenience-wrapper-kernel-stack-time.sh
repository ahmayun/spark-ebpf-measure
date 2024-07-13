#!/bin/bash
LABEL=$1
PROG=$2
NUM_REPS=$3
shift 3
PRE=/home/ahmad/Desktop/spark-playground/DepFuzz/data/tpcds_levels
EXP=$(printf "$PRE/%s " "$@")
/home/ahmad/Desktop/bpf-playground/learning-ebpf/chapter3/spark-ebpf-measure/measurement-scripts/measure-kernel-stack-time.sh \
    /home/ahmad/Desktop/spark-playground/DepFuzz/target/scala-2.12/DepFuzz-assembly-1.0.jar \
    $LABEL \
    $PROG \
    $NUM_REPS \
    $EXP
