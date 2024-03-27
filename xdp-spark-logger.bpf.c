#include <linux/bpf.h>
#include <bpf/bpf_helpers.h>
#include <netinet/in.h>
#include <linux/if_ether.h>
#include <linux/ip.h>
#include <linux/udp.h>
#include <linux/tcp.h>

struct packet_info {
    __u64 timestamp_ns;
    __u16 src_port;
    __u16 dest_port;
};

struct bpf_map_def SEC("maps") packet_log_map = {
    .type = BPF_MAP_TYPE_HASH,
    .key_size = sizeof(__u32),
    .value_size = sizeof(struct packet_info),
    .max_entries = 1024,
};

SEC("xdp")
int xdp_main(struct xdp_md *ctx) {
    void* data_end = (void*)(long)ctx->data_end;
    void* data = (void*)(long)ctx->data;
    struct ethhdr *eth = data;
    struct iphdr *ip;
    struct tcphdr *tcp;
    struct udphdr *udp;
    __u32 key = bpf_get_smp_processor_id(); // Use CPU ID as key for simplicity
    struct packet_info info = {};

    // Basic bounds checking
    if (eth + 1 > data_end)
        return XDP_PASS;

    // Check for IPv4
    if (eth->h_proto != htons(ETH_P_IP))
        return XDP_PASS;

    ip = data + sizeof(*eth);
    if (ip + 1 > data_end)
        return XDP_PASS;

    // Initialize info
    info.timestamp_ns = bpf_ktime_get_ns();

    // TCP
    if (ip->protocol == IPPROTO_TCP) {
        tcp = (void*)ip + sizeof(*ip);
        if (tcp + 1 > data_end)
            return XDP_PASS;
        info.src_port = tcp->source;
        info.dest_port = tcp->dest;
    }
    // UDP
    else if (ip->protocol == IPPROTO_UDP) {
        udp = (void*)ip + sizeof(*ip);
        if (udp + 1 > data_end)
            return XDP_PASS;
        info.src_port = udp->source;
        info.dest_port = udp->dest;
    } else {
        return XDP_PASS;
    }

    bpf_map_update_elem(&packet_log_map, &key, &info, BPF_ANY);

    return XDP_PASS;
}

char _license[] SEC("license") = "GPL";
