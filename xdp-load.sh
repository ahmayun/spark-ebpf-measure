PROG_NAME=xdp-spark.bpf
clang -target bpf -I/usr/include/x86_64-linux-gnu -g -O2 -o $PROG_NAME.o -c $PROG_NAME.c && \
sudo bpftool prog load $PROG_NAME.o /sys/fs/bpf/xdp-spark && \
# sudo bpftool prog dump xlated name xdp_main
# sudo bpftool prog list
sudo rm $PROG_NAME.o && \
sudo bpftool net attach xdp name xdp_main dev lo


# See output
# sudo cat /sys/kernel/debug/tracing/trace_pipe

# Unload
# sudo bpftool net detach xdp dev ens33 # detach
# sudo rm /sys/fs/bpf/hello