#include <bpf/libbpf.h>
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <linux/bpf.h>
#include <bpf/bpf.h>
#include <arpa/inet.h>
#include <stdlib.h>


struct packet_id {
    __be32 daddr;
    __be32 saddr;
    __u16 dport;
    __u16 sport;

};

struct socket_stats {
    __u64 diff_sum;
    __u64 total_bytes;
    __u64 pkt_count;
    __u64 pid_of_rcvr;
};


int main(int argc, char **argv) {
    int map_fd = 0;
    struct packet_id key, next_key;
    
    struct socket_stats stats;
    if(argc < 2) {
        perror("Too few arguments. Expecting <map_id>");
        return 1;
    }

    int map_id = atoi(argv[1]);
    printf("map_id: %d\n", map_id);

    map_fd = bpf_map_get_fd_by_id(map_id);
    if (map_fd < 0) {
        perror("Failed to get map fd");
        return 1;
    }

    printf("format: {src_ip->dst_ip, src_port->dst_port} = {diff_sum, pkt_count, total_bytes}\n"); 

    char daddr_str[INET_ADDRSTRLEN];
    char saddr_str[INET_ADDRSTRLEN];
    
    while (bpf_map_get_next_key(map_fd, &key, &next_key) == 0) {
        if (bpf_map_lookup_elem(map_fd, &next_key, &stats) == 0) {
            const char* check1 = inet_ntop(AF_INET, &next_key.daddr, daddr_str, INET_ADDRSTRLEN);
            const char* check2 = inet_ntop(AF_INET, &next_key.saddr, saddr_str, INET_ADDRSTRLEN);
            
            if(!check1 || !check2) {
                perror("Conversion failed!");
            }

            printf( 
                "{%s->%s, %u->%u} = {%llu, %llu, %llu, %llu}\n", 
                saddr_str, daddr_str, next_key.sport, next_key.dport, stats.diff_sum, stats.pkt_count, stats.total_bytes, stats.pid_of_rcvr
            );
        }
        key = next_key;
    }

    return 0;
}
