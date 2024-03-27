// BPF_HASH(counter_table);

int hello(void *ctx) {
    bpf_trace_printk("hello world!\n");
//    u64 uid;
//    u64 counter = 0;
//    u64 *p;

//    uid = bpf_get_current_uid_gid() & 0xFFFFFFFF;
//    p = counter_table.lookup(&uid);
//    if (p != 0) {
//       counter = *p;
//    }
//    counter++;
//    counter_table.update(&uid, &counter);
//    return 0;
}