sudo strace -e 'trace=!futex' -fp $1
