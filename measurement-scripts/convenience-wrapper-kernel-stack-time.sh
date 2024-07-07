#!/bin/bash
PROG=$1
NUM_REPS=$2
shift 2
PRE=~/Desktop/spark-playground/DepFuzz/data/tpcds_noheader_nocommas
EXP=$(printf "$PRE/%s " "$@")
/home/ahmad/Desktop/bpf-playground/learning-ebpf/chapter3/spark-ebpf-measure/measurement-scripts/measure-kernel-stack-time.sh \
    ~/Desktop/spark-playground/DepFuzz/target/scala-2.12/DepFuzz-assembly-1.0.jar \
    $PROG \
    $NUM_REPS \
    $EXP
