#include <arpa/inet.h> // for some reason the order matters, if i include this last, compile errors
#include <linux/bpf.h>
#include <bpf/bpf_helpers.h>
#include <linux/if_ether.h>
#include <linux/ip.h>
#include <linux/in.h>
#include <linux/tcp.h>

struct packet_info {
    __u64 timestamp_ns;
    __u16 src_port;
    __u16 dest_port;
};

struct packet_id {
    __be32 daddr;
    __be32 saddr;
    __u16 dport;
    __u16 sport;

};

struct bpf_map_def SEC("maps") packet_log_map = {
    .type = BPF_MAP_TYPE_HASH,
    .key_size = sizeof(struct packet_id),
    .value_size = sizeof(struct packet_info),
    .max_entries = 1024,
};


SEC("xdp")
int xdp_main(struct xdp_md *ctx) {

    void *data_end = (void *)(long)ctx->data_end;
    void *data = (void *)(long)ctx->data;
    const int l3_off = ETH_HLEN;                       // IP header offset
    const int l4_off = l3_off + sizeof(struct iphdr);  // TCP header offset
    struct ethhdr *eth = data;
    unsigned long ts = bpf_ktime_get_ns();
    // __u64 key = ts; // bpf_get_smp_processor_id(); // Use CPU ID as key for simplicity
    // __u32 key = (__u32) ts;
    struct packet_info info = {};
    info.timestamp_ns = ts;

    // Need to add this check otherwise verifier rejects it
    if (data + sizeof(*eth) > data_end)
        return XDP_PASS;

    // Assuming IPv4, check for IP packet
    if (eth->h_proto != __constant_htons(ETH_P_IP))
        return XDP_PASS;

    // Add the size of the the ethernet header 
    // to the start to get a pointer to the ip header
    // This is possible because the ethernet header 
    // length is static (14 bytes)
    struct iphdr *ip = (struct iphdr *)(data + l3_off); // data + sizeof(*eth);

    // Check for packet bounds otherwise verifier won't shutup
    if ((void *)ip + sizeof(*ip) > data_end)
        return XDP_PASS;


    // Check if tcp packet, didn't really need 
    // this but good to have for future  
    if (ip->protocol != IPPROTO_TCP)
        return XDP_PASS;

    struct tcphdr *tcp = (struct tcphdr *)(data + l4_off); // (void *)ip + (ip->ihl * 4);


    if ((void *)tcp + sizeof(*tcp) > data_end)
        return XDP_PASS;
    

    info.src_port = tcp->source;
    info.dest_port = tcp->dest;

    info.src_port = htons(info.src_port);
    info.dest_port = htons(info.dest_port);
    
    struct packet_id key = {};
    key.daddr = ip->daddr;
    key.saddr = ip->saddr;
    key.dport = info.dest_port;
    key.sport = info.src_port;

    bpf_map_update_elem(&packet_log_map, &key, &info, BPF_ANY);
    bpf_printk("[xdp] %d -> %d | %lu ns\n", info.src_port, info.dest_port, ts);
    

    return XDP_PASS;
}

char _license[] SEC("license") = "GPL";
