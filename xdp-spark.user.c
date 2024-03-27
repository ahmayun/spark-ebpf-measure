#include <bpf/libbpf.h>
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <linux/bpf.h>
#include <bpf/bpf.h>
#include <arpa/inet.h>
#include <stdlib.h>

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

int main(int argc, char **argv) {
    int fd, map_fd = 0;
    struct packet_id key, next_key;
    
    struct packet_info value;
    if(argc < 3) {
        perror("Too few arguments. Expecting <filename> <map_id>");
        return 1;
    }

    fd = open(argv[1], O_WRONLY | O_CREAT, 0644);
    int map_id = atoi(argv[2]);
    if (fd < 0) {
        perror("Failed to open file");
        return 1;
    }
    printf("map_id: %d\n", map_id);
    map_fd = bpf_map_get_fd_by_id(map_id);
    if (map_fd < 0) {
        perror("Failed to get map fd");
        return 1;
    }

    while (bpf_map_get_next_key(map_fd, &key, &next_key) == 0) {
        if (bpf_map_lookup_elem(map_fd, &next_key, &value) == 0) {
            dprintf(fd, 
            "{%d->%d, %d->%d} | timestamp: %llu, sport: %u, dport: %u\n", 
            next_key.saddr, next_key.daddr, next_key.sport, next_key.dport, value.timestamp_ns, value.src_port, value.dest_port
            );
        }
        key = next_key;
    }

    close(fd);
    return 0;
}
