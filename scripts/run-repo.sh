#!/bin/sh
# Run every Rust measurement for the given repositories, one after another.
set -e
chmod +x /work/scripts/timed-cc
for r in "$@"; do
  python3 /work/scripts/bench.py clean "$r"
  for l in default lld mold; do
    python3 /work/scripts/bench.py incr "$r" "$l"
  done
done
