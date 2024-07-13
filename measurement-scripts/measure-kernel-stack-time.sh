# assumes run-wordcount.sh
JAR=$1
LABEL=$2
PROGRAM=$3
NUM_REPS=$4
shift 4
DATASETS=("$@")
NUM_DS=${#DATASETS[@]}
SPARK_MASTER=spark://localhost:7077
TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)
OUTFILE="./results/$PROGRAM/$LABEL/results_$TIMESTAMP/time.csv"
OUTDIR=$(dirname $OUTFILE)
OUTDIR_STDOUT=$OUTDIR/stdout
OUTDIR_STDERR=$OUTDIR/stderr
GLOBAL_CSV=./results/combined/all-data.csv
mkdir -p $OUTDIR &> /dev/null
mkdir -p $OUTDIR_STDOUT &> /dev/null
mkdir -p $OUTDIR_STDERR &> /dev/null
mkdir -p $(dirname $GLOBAL_CSV) &> /dev/null
cp $GLOBAL_CSV "$GLOBAL_CSV"_$TIMESTAMP 
PFX="[measure-kernel-stack-time.sh] "
SOCKET_STATS_FILE="/tmp/socket_stats"

debuglog() {
    PRINT_STR="$1"
    echo $PFX $PRINT_STR
}

cleanup(){
    EBPF_PROGRAM_PID=$(pgrep -af 'python3 combined' | egrep -v sudo | cut -d" " -f1)
    debuglog "killing bpf program pid: $EBPF_PROGRAM_PID..."
    sudo kill $EBPF_PROGRAM_PID
    wait $EBPF_PROGRAM_PID &> /dev/null
    sudo bpftool net detach xdp dev lo
    return 0
}

exit_with_failure(){
    cleanup
    debuglog "FAILED! Exiting with error..."
    exit 1
}

exit_with_force(){
    cleanup
    debuglog "Script stopped with Ctrl+C"
    exit 1
}

get_app_id_from_logs() {
    logfile=$1
    egrep -o "app-[0-9]{14}-[0-9]{4}" $logfile | head -1
}

trap exit_with_force SIGINT

echo -e "ID,TOTAL_JOB_TIME,TOTAL_DIFF_SUM" > $OUTFILE
echo -e "ID,TOTAL_JOB_TIME,TOTAL_DIFF_SUM" > $GLOBAL_CSV
echo -e "ID,TOTAL_JOB_TIME,TOTAL_DIFF_SUM" >> $GLOBAL_LOG_FILE

# Ensure we have the latest version of the map reader
debuglog "Compiling map reader..."
gcc -o read-map-u64 read-map-u64.c -l bpf

DS_STR="${DATASETS[@]:0:NUM_DS}"

debuglog "NUM_DATSETS $NUM_DS"
debuglog "DATASETS: $DS_STR"

pushd /home/ahmad/Desktop/bpf-playground/learning-ebpf/chapter3/spark-ebpf-measure
for (( i=0; i < $NUM_REPS; i+=1 )); do

    debuglog " ============ ITERATION $i ============"

    # Load eBPF program for monitoring network packets
    debuglog "Loading eBPF programs..."
    sudo python3 combined-ebpf-loader.py &

    # Wait for the program to load
    debuglog "Waiting for eBPF programs to be loaded..."
    sleep 10
    debuglog "PID of BPF program is $EBPF_PROGRAM_PID"

    # Get bpf map ID for the program
    debuglog "Getting BPF map ID..."
    BPF_MAP_ID=$(sudo bpftool map list | grep socket_stats | tr -s ":" "\n" | head -1)
    debuglog "Got $BPF_MAP_ID"
    debuglog "Running $PROGRAM with datasets $DS_STR..."

    # ====== Run and time the spark job =======
    STDERR=$OUTDIR_STDERR/run.$i.err
    STDOUT=$OUTDIR_STDOUT/run.$i.out
    START_TIME=$(date +%s)
    JOB_NAME="$PROGRAM"_"$LABEL"_"$i"
    spark-submit --name $JOB_NAME --class examples.benchmarks.$PROGRAM --master $SPARK_MASTER $JAR $DS_STR 2> $STDERR 1>$STDOUT
    
    if [ $? -ne 0 ]; then
        exit_with_failure
    fi
    
    END_TIME=$(date +%s)
    TOTAL_JOB_TIME=$((END_TIME - START_TIME))
    # =========================================

    debuglog "Spark job took $TOTAL_JOB_TIME seconds"
    debuglog "Writing eBPF-collected socket info to $SOCKET_STATS_FILE"
    sudo ./read-map-u64 $BPF_MAP_ID > $SOCKET_STATS_FILE
    TOTAL_DIFF_SUM=$(python3 analyze-packet-time.py $SOCKET_STATS_FILE)
    ROW="$JOB_NAME,$TOTAL_JOB_TIME,$TOTAL_DIFF_SUM"
    debuglog "Recorded: $ROW"
    echo "$ROW" >> $OUTFILE
    echo "$ROW" >> $GLOBAL_CSV
    echo "$ROW" >> $GLOBAL_LOG_FILE

    cleanup
done
popd
