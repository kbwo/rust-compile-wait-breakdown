#!/usr/bin/env python3
"""Measure build wait times inside the container.

Usage:
  python3 scripts/bench.py clean <repo>            # clean debug / release builds
  python3 scripts/bench.py incr <repo> <linker>    # incremental changes with one linker
  python3 scripts/bench.py kak                     # Kakoune (C++) .cc / header changes

Every measured condition runs 1 warm-up + RUNS measured iterations.
Raw rows are appended to results/raw/<repo>.jsonl (one JSON object per run).
Builds happen in /tmp (the container's own filesystem), not in the bind-mounted
/work, so that host file sharing does not slow down compilation.
"""
import json
import os
import shutil
import subprocess
import sys
import time

WORK = "/work"
RUNS = 5
WARMUP = 1
TRIPLE_ENV = "CARGO_TARGET_AARCH64_UNKNOWN_LINUX_GNU" if os.uname().machine == "aarch64" else "CARGO_TARGET_X86_64_UNKNOWN_LINUX_GNU"
TOOLCHAIN = "1.99.1"

# Each change is a one-line edit inserted right after the opening "{" of the
# function whose definition line starts with `anchor` (body change), or a
# replacement of that definition line (signature change, toggled on/off).
REPOS = {
    "ripgrep": {
        "leaf": {"file": "crates/core/main.rs",
                 "anchor": "fn search(args: &HiArgs, mode: SearchMode) -> anyhow::Result<bool> {"},
        "core": {"file": "crates/searcher/src/searcher/mod.rs",
                 "anchor": "    pub fn line_number(&mut self, yes: bool) -> &mut SearcherBuilder {"},
        "sig": {"file": "crates/searcher/src/searcher/mod.rs",
                "anchor": "    pub fn line_number(&mut self, yes: bool) -> &mut SearcherBuilder {",
                "replace": "    pub fn line_number(&mut self, yes: impl Into<bool>) -> &mut SearcherBuilder { let yes: bool = yes.into();"},
    },
    "helix": {
        "leaf": {"file": "helix-term/src/commands.rs",
                 "anchor": "fn move_char_left(cx: &mut Context) {"},
        "core": {"file": "helix-core/src/graphemes.rs",
                 "anchor": "pub fn ensure_grapheme_boundary_next(slice: RopeSlice, char_idx: usize) -> usize {"},
        "sig": {"file": "helix-core/src/graphemes.rs",
                "anchor": "pub fn ensure_grapheme_boundary_next(slice: RopeSlice, char_idx: usize) -> usize {",
                "replace": "pub fn ensure_grapheme_boundary_next(slice: RopeSlice, char_idx: impl Into<usize>) -> usize { let char_idx: usize = char_idx.into();"},
    },
    "mdbook": {
        "leaf": {"file": "src/cmd/build.rs",
                 "anchor": "pub fn execute(args: &ArgMatches) -> Result<()> {"},
        "core": {"file": "crates/mdbook-core/src/utils/fs.rs",
                 "anchor": "pub fn remove_dir_content(dir: &Path) -> Result<()> {"},
        "sig": {"file": "crates/mdbook-core/src/utils/fs.rs",
                "anchor": "pub fn remove_dir_content(dir: &Path) -> Result<()> {",
                "replace": "pub fn remove_dir_content(dir: impl AsRef<Path>) -> Result<()> { let dir: &Path = dir.as_ref();"},
    },
}

KAK = {
    "cc": {"file": "src/normal.cc", "anchor": "void replace_with_char(Context& context, NormalParams)"},
    "header": {"file": "src/string.hh", "anchor": "inline String& operator+=(String& lhs, StringView rhs)"},
}

LINKERS = {
    "default": "",
    "lld": "-C link-arg=-fuse-ld=lld",
    "mold": "-C link-arg=-fuse-ld=mold",
    # Supplementary: mold limited to 2 threads, matching the container's 2-CPU quota
    # (mold otherwise starts one thread per visible CPU; nproc shows 14 here).
    "mold-t2": "-C link-arg=-fuse-ld=mold -C link-arg=-Wl,--thread-count=2",
    "lld-t2": "-C link-arg=-fuse-ld=lld -C link-arg=-Wl,--threads=2",
}


def log(msg):
    print(time.strftime("%H:%M:%S"), msg, flush=True)


def append(repo, row):
    os.makedirs(f"{WORK}/results/raw", exist_ok=True)
    with open(f"{WORK}/results/raw/{repo}.jsonl", "a") as f:
        f.write(json.dumps(row) + "\n")


def base_env():
    env = dict(os.environ)
    env.update({
        "RUSTUP_TOOLCHAIN": TOOLCHAIN,  # override rust-toolchain.toml in the repos
        "CARGO_HOME": "/tmp/cargo-home",
        "CARGO_BUILD_JOBS": "2",  # the container is limited to 2 CPUs
        "CARGO_TERM_COLOR": "never",
        "HELIX_DISABLE_AUTO_GRAMMAR_BUILD": "1",  # do not fetch/compile tree-sitter grammars
        f"{TRIPLE_ENV}_LINKER": f"{WORK}/scripts/timed-cc",
    })
    return env


def setup_cargo_home():
    # Reuse downloaded crates between sessions to avoid re-downloading from crates.io.
    cache = f"{WORK}/targets/cargo-home"
    if os.path.isdir(cache) and not os.path.isdir("/tmp/cargo-home"):
        shutil.copytree(cache, "/tmp/cargo-home", symlinks=True)
    os.makedirs("/tmp/cargo-home", exist_ok=True)


def save_cargo_home():
    cache = f"{WORK}/targets/cargo-home"
    for sub in ("registry",):
        src = f"/tmp/cargo-home/{sub}"
        if os.path.isdir(src):
            shutil.rmtree(f"{cache}/{sub}", ignore_errors=True)
            shutil.copytree(src, f"{cache}/{sub}", symlinks=True)


def copy_src(name):
    dst = f"/tmp/w/{name}"
    shutil.rmtree(dst, ignore_errors=True)
    shutil.copytree(f"{WORK}/src/{name}", dst, symlinks=True)
    return dst


def run_timed(argv, cwd, env):
    link_log = "/tmp/link.log"
    if os.path.exists(link_log):
        os.remove(link_log)
    env = dict(env)
    env["LINK_LOG"] = link_log
    t0 = time.monotonic()
    p = subprocess.run(argv, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    dt = time.monotonic() - t0
    links = []
    if os.path.exists(link_log):
        with open(link_log) as f:
            for line in f:
                s, e, out = line.split(" ", 2)
                links.append((int(s) / 1e9, int(e) / 1e9, out.strip()))
    return p.returncode, dt, links, p.stdout


def link_stats(links):
    """Sum of linker durations, and the wall time covered by at least one linker
    (links of several test binaries can run in parallel, so the sum can exceed
    the wall time of the whole command)."""
    total = sum(e - s for s, e, _ in links)
    wall, cur_s, cur_e = 0.0, None, None
    for s, e, _ in sorted(links):
        if cur_e is None or s > cur_e:
            if cur_e is not None:
                wall += cur_e - cur_s
            cur_s, cur_e = s, e
        else:
            cur_e = max(cur_e, e)
    if cur_e is not None:
        wall += cur_e - cur_s
    return {"link_seconds": round(total, 3), "link_wall_seconds": round(wall, 3), "link_count": len(links)}


def check_ok(rc, out, what):
    if rc != 0:
        print(out[-6000:])
        raise SystemExit(f"FAILED: {what}")


class Mutator:
    """Applies one-line edits to a file; restore() puts the original back."""

    def __init__(self, root, spec, lang="rust"):
        self.path = os.path.join(root, spec["file"])
        self.spec = spec
        self.lang = lang
        with open(self.path) as f:
            self.orig = f.read()
        lines = self.orig.split("\n")
        idx = [i for i, l in enumerate(lines) if l == spec["anchor"]]
        if len(idx) != 1:
            raise SystemExit(f"anchor not unique/found ({len(idx)}): {spec}")
        self.anchor = idx[0]
        brace = self.anchor
        while not lines[brace].rstrip().endswith("{"):
            brace += 1
        self.brace = brace
        self.counter = 0

    def apply(self):
        self.counter += 1
        lines = self.orig.split("\n")
        if "replace" in self.spec:
            # toggle: odd counter -> changed signature, even -> original signature
            if self.counter % 2 == 1:
                lines[self.anchor] = self.spec["replace"]
        elif self.lang == "rust":
            lines.insert(self.brace + 1, f"    let _ = std::hint::black_box({self.counter}u64);")
        else:
            lines.insert(self.brace + 1, f"    [[maybe_unused]] volatile int kak_probe = {self.counter};")
        with open(self.path, "w") as f:
            f.write("\n".join(lines))

    def restore(self):
        with open(self.path, "w") as f:
            f.write(self.orig)


def cargo_argv(cmd, release=False):
    base = {"check": ["cargo", "check"], "build": ["cargo", "build"], "test": ["cargo", "test", "--no-run"]}[cmd]
    argv = base + ["--locked", "--timings"]
    if release:
        argv.append("--release")
    return argv


def save_timings(target, label):
    d = os.path.join(target, "cargo-timings")
    if not os.path.isdir(d):
        return
    files = sorted(f for f in os.listdir(d) if f.startswith("cargo-timing-") and f.endswith(".html"))
    if files:
        os.makedirs(f"{WORK}/results/timings", exist_ok=True)
        shutil.copy(os.path.join(d, files[-1]), f"{WORK}/results/timings/{label}.html")
    shutil.rmtree(d, ignore_errors=True)


def linker_comment(binary):
    p = subprocess.run(["readelf", "-p", ".comment", binary], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return " | ".join(l.strip() for l in p.stdout.splitlines() if "Linker" in l or "mold" in l or "LLD" in l) or "(no linker note: GNU ld)"


def main_binary(repo, target, profile):
    name = {"ripgrep": "rg", "helix": "hx", "mdbook": "mdbook"}[repo]
    return os.path.join(target, profile, name)


def phase_clean(repo):
    setup_cargo_home()
    root = copy_src(repo)
    env = base_env()
    rc, _, _, out = run_timed(["cargo", "fetch", "--locked"], root, env)
    check_ok(rc, out, "fetch")
    save_cargo_home()
    for profile in ("debug", "release"):
        target = f"/tmp/t/clean-{profile}"
        env["CARGO_TARGET_DIR"] = target
        for it in range(WARMUP + RUNS):
            shutil.rmtree(target, ignore_errors=True)
            rc, dt, links, out = run_timed(cargo_argv("build", release=(profile == "release")), root, env)
            check_ok(rc, out, f"clean {profile}")
            row = {"repo": repo, "kind": "clean", "change": "clean", "cmd": "build", "profile": profile,
                   "linker": "default", "iter": it, "warmup": it < WARMUP, "seconds": round(dt, 3),
                   **link_stats(links),
                   "linker_note": linker_comment(main_binary(repo, target, profile))}
            append(repo, row)
            log(json.dumps(row))
        save_timings(target, f"{repo}-clean-{profile}")
        shutil.rmtree(target, ignore_errors=True)


def phase_incr(repo, linker):
    setup_cargo_home()
    root = copy_src(repo)
    env = base_env()
    target = f"/tmp/t/incr-{linker}"
    shutil.rmtree(target, ignore_errors=True)
    env["CARGO_TARGET_DIR"] = target
    if LINKERS[linker]:
        env[f"{TRIPLE_ENV}_RUSTFLAGS"] = LINKERS[linker]  # merged with repo's target.cfg rustflags
    cmds = ["check", "build", "test"] if linker == "default" else ["build", "test"]
    # Prime: full build of everything we will measure (not recorded).
    for cmd in cmds:
        rc, dt, _, out = run_timed(cargo_argv(cmd), root, env)
        check_ok(rc, out, f"prime {cmd}")
        log(f"primed {repo} {linker} {cmd} in {dt:.1f}s")
    note = linker_comment(main_binary(repo, target, "debug"))
    for change in ("leaf", "core", "sig"):
        m = Mutator(root, REPOS[repo][change])
        try:
            for cmd in cmds:
                for it in range(WARMUP + RUNS):
                    m.apply()
                    rc, dt, links, out = run_timed(cargo_argv(cmd), root, env)
                    check_ok(rc, out, f"{change} {cmd} iter {it}")
                    row = {"repo": repo, "kind": "incr", "change": change, "cmd": cmd, "profile": "debug",
                           "linker": linker, "iter": it, "warmup": it < WARMUP, "seconds": round(dt, 3),
                           **link_stats(links),
                           "linker_note": note,
                           "units": [l for l in out.splitlines() if l.strip().startswith(("Compiling", "Checking"))]}
                    append(repo, row)
                    log(json.dumps({k: v for k, v in row.items() if k != "units"}))
                save_timings(target, f"{repo}-incr-{linker}-{change}-{cmd}")
        finally:
            m.restore()


def phase_kak():
    root = copy_src("kakoune")
    env = dict(os.environ)
    make = ["make", "-j2", "debug=yes"]
    rc, dt, _, out = run_timed(make, root, env)
    check_ok(rc, out, "kak prime")
    row = {"repo": "kakoune", "kind": "clean", "change": "clean", "cmd": "make", "profile": "debug",
           "linker": "default", "iter": 0, "warmup": False, "seconds": round(dt, 3), "note": "single run, reference only"}
    append("kakoune", row)
    log(json.dumps(row))
    for change in ("cc", "header"):
        m = Mutator(root, KAK[change], lang="cpp")
        try:
            for it in range(WARMUP + RUNS):
                m.apply()
                rc, dt, _, out = run_timed(make, root, env)
                check_ok(rc, out, f"kak {change} {it}")
                compiled = [l for l in out.splitlines() if " -c " in l]
                row = {"repo": "kakoune", "kind": "incr", "change": change, "cmd": "make", "profile": "debug",
                       "linker": "default", "iter": it, "warmup": it < WARMUP, "seconds": round(dt, 3),
                       "compiled_files": len(compiled)}
                append("kakoune", row)
                log(json.dumps(row))
        finally:
            m.restore()


if __name__ == "__main__":
    phase = sys.argv[1]
    if phase == "clean":
        phase_clean(sys.argv[2])
    elif phase == "incr":
        phase_incr(sys.argv[2], sys.argv[3])
    elif phase == "kak":
        phase_kak()
    else:
        raise SystemExit(__doc__)
