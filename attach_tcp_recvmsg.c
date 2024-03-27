#include <uapi/linux/ptrace.h>
// #define BPF_SK_LOOKUP 36
#include <net/sock.h>
#include <bcc/proto.h>
// #include <bpf/bpf_helpers.h>
#include <net/inet_sock.h>
// Define output data structure
// #include <linux/net/inet_sock.h>


struct packet_id {
    __be32 daddr;
    __be32 saddr;
    __u16 dport;
    __u16 sport;

};

// // Create a map to store the output
// BPF_PERF_OUTPUT(events);

int trace_tcp_recvmsg(struct pt_regs *ctx, struct sock *sk) {
    struct packet_id data = {};
     unsigned long ts = bpf_ktime_get_ns();

    //Casting `sock` to `inet_sock` to access IP and port information
    struct inet_sock *inet = inet_sk(sk);

    //Extracting IP addresses and ports
    data.saddr = inet->inet_saddr;
    data.daddr = inet->inet_daddr; 
    data.sport = inet->inet_sport;
    data.dport = inet->inet_dport;

    data.sport = htons(data.sport); // for some reason data.sport = htons(inet->inet_sport) fails to pass verifier, probably has something to do with needing to copy kernel datastructures before manipulating them
    data.dport =  htons(data.dport);

    //Output the data
    // events.perf_submit(ctx, &data, sizeof(data));

    bpf_trace_printk("[udp_recvmsg] %d -> %d | %lu ns\n",data.sport, data.dport, ts);
    return 0; // Always return 0 in tracepoints
}
