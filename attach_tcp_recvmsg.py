from bcc import BPF

# Load eBPF program
bpf_text = open('attach_tcp_recvmsg.c').read()
b = BPF(text=bpf_text)

# Attach to tcp_recvmsg
b.attach_kprobe(event="udp_recvmsg", fn_name="trace_tcp_recvmsg")

# Define a callback for received events
def print_event(cpu, data, size):
    event = b["events"].event(data)
    print(f"IP: {event.saddr} -> {event.daddr}, Port: {event.sport} -> {event.dport}")

# Open perf buffer
# b["events"].open_perf_buffer(print_event)
print("Beginning trace print...")
# b.trace_print()
while True:
    cmd = input("Type q to exit...\n")
    if cmd == "q":
        break
# print("Tracing tcp_recvmsg calls... Press Ctrl-C to stop.")

# Loop to read and print events
# try:
#     while True:
#         b.perf_buffer_poll()
# except KeyboardInterrupt:
#     pass
