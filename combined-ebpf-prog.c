// #include <arpa/inet.h> // for some reason the order matters, if i include this last, compile errors
#include <linux/bpf.h>
// #include <bpf/bpf_helpers.h>
#include <linux/if_ether.h>
#include <linux/ip.h>
#include <linux/in.h>
#include <linux/tcp.h>
#include <uapi/linux/ptrace.h>
#include <net/sock.h>
#include <bcc/proto.h>
#include <net/inet_sock.h>


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


BPF_HASH(packet_log_map, struct packet_id, struct packet_info, 1024);
BPF_HASH(diff_sum_map, struct packet_id, u64, 1024);
BPF_HASH(total_size_map, struct packet_id, u64, 1024);
BPF_HASH(packet_counts_map, struct packet_id, u64, 1024);



// SEC("xdp")
int xdp_main(struct xdp_md *ctx) {

    void *data_end = (void *)(long)ctx->data_end;
    void *data = (void *)(long)ctx->data;
    __u64 packet_size = data_end-data;
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

    // bpf_map_update_elem(&packet_log_map, &key, &info, BPF_ANY);
    packet_log_map.update(&key, &info);
    // bpf_trace_printk("[xdp] %d -> %d | %lu ns\n", info.src_port, info.dest_port, ts);
    bpf_trace_printk("[xdp] packet_size = %lu\n", packet_size);
    

    return XDP_PASS;
}

// SEC("kprobe/tcp_recvmsg")
int trace_tcp_recvmsg(struct pt_regs *ctx, struct sock *sk, struct msghdr *msg, size_t len) {
    struct packet_id id = {};
     unsigned long ts = bpf_ktime_get_ns();

    //Casting `sock` to `inet_sock` to access IP and port information
    struct inet_sock *inet = inet_sk(sk);

    //Extracting IP addresses and ports
    id.saddr = inet->inet_saddr;
    id.daddr = inet->inet_daddr; 
    id.sport = inet->inet_sport;
    id.dport = inet->inet_dport;

    id.sport = htons(id.sport); // for some reason id.sport = htons(inet->inet_sport) fails to pass verifier, probably has something to do with needing to copy kernel idstructures before manipulating them
    id.dport =  htons(id.dport);
    
    struct packet_info* pkt_info = packet_log_map.lookup(&id);
    
    if(!pkt_info)
        return 0;

    // bpf_trace_printk("[tcp_recvmsg] %d -> %d | diff: %lu ns\n",pkt_info->src_port, pkt_info->dest_port, ts - pkt_info->timestamp_ns);
    u64 diff = ts - pkt_info->timestamp_ns;
    u64* old_diff_sum = diff_sum_map.lookup(&id);
    u64* old_count = packet_counts_map.lookup(&id);
    u64* old_size = total_size_map.lookup(&id);

    if(old_diff_sum && old_count && old_size) { // these two booleans are linked so should always be T & T or F & F, writing like this will simplify the program 
        u64 new_diff_sum = *old_diff_sum+diff;
        u64 new_count = *old_count+1;
        u64 new_size = *old_size+ (u64)len;
        diff_sum_map.update(&id, &new_diff_sum);
        packet_counts_map.update(&id, &new_count);
        total_size_map.update(&id, &new_size);
    } else {
        u64 zero = 0;
        u64 one = 1;
        diff_sum_map.insert(&id, &diff);
        packet_counts_map.update(&id, &one);
        total_size_map.update(&id, &zero);
    }


    // u64* num = diff_sum_map.lookup(&id);
    // u64* den = packet_counts_map.lookup(&id);
    // if(!num || !den)
    //     return 0;

    u64 encoded_ports = (u64)id.sport * 100000 + id.dport;
    // bpf_trace_printk("[tcp_recvmsg] len = %u bytes\n", len);
    // bpf_trace_printk("[tcp_recvmsg] diff[%u -> %u] = %lu ns\n", id.sport, id.dport, *num);
    // bpf_trace_printk("[tcp_recvmsg] avg_diff[%llu] = %llu/%llu ns\n", encoded_ports, *num, *den);
    
    return 0; // Always return 0 in tracepoints
}


// char _license[] SEC("license") = "GPL";
