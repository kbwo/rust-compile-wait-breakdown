#!/bin/sh
# Record the measurement environment into results/env.txt.
mkdir -p /work/results
{
  echo "date: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "uname: $(uname -a)"
  echo "nproc (host CPUs visible): $(nproc)"
  echo "cgroup cpu.max (quota period): $(cat /sys/fs/cgroup/cpu.max)"
  echo "cgroup memory.max (bytes): $(cat /sys/fs/cgroup/memory.max)"
  grep -m1 -i "model name\|CPU part" /proc/cpuinfo
  echo "rustc: $(RUSTUP_TOOLCHAIN=1.99.1 rustc -Vv | tr '\n' ' ')"
  echo "cargo: $(RUSTUP_TOOLCHAIN=1.99.1 cargo -V)"
  echo "cc: $(cc --version | head -1)"
  echo "c++: $(c++ --version | head -1)"
  echo "ld (GNU): $(ld --version | head -1)"
  echo "lld: $(ld.lld --version)"
  echo "mold: $(mold --version)"
  echo "make: $(make --version | head -1)"
  echo "debian: $(cat /etc/debian_version)"
} > /work/results/env.txt
cat /work/results/env.txt
