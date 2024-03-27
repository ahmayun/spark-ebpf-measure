#!/usr/bin/python3  
from bcc import BPF
from time import sleep

program = open("sock-ingress.bpf.c", 'r').read()


b = BPF(text=program)
syscall = b.get_syscall_fnname("recvfrom")
b.attach_kprobe(event=syscall, fn_name="hello")
b.trace_print()

# Attach to a tracepoint that gets hit for all syscalls 
# b.attach_raw_tracepoint(tp="sys_enter", fn_name="hello")

# while True:
#     sleep(2)
#     s = ""
#     for k,v in b["counter_table"].items():
#         s += f"ID {k.value}: {v.value}\t"
#     print(s)
