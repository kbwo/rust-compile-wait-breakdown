#!/bin/sh
# Clone the measured repositories at fixed commits into /work/src.
set -e
mkdir -p /work/src
cd /work/src
fetch() { # name url commit
  if [ ! -d "$1" ]; then
    git init -q "$1"
    git -C "$1" remote add origin "$2"
  fi
  git -C "$1" fetch -q --depth 1 origin "$3"
  git -C "$1" checkout -q -f "$3"
  echo "$1 $2 $(git -C "$1" rev-parse HEAD)"
}
fetch ripgrep https://github.com/BurntSushi/ripgrep 91f5d22ef48bde459d90a8c7dbeab416e97d0f2b
fetch helix https://github.com/helix-editor/helix ba40e547426b0f9896c8bdc699a4ab11f2b37dbc
fetch mdbook https://github.com/rust-lang/mdBook 0accb8a3ff59e311c60e2267581fea6407d64c73
fetch kakoune https://github.com/mawww/kakoune a4466920c2a9223d7ba1feff12f02962d67ece3e
