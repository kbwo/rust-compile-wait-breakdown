#!/usr/bin/env python3
"""Aggregate results/raw/*.jsonl into results/summary.csv and results/summary.md.

Warm-up runs are excluded. For each condition: n, median, min, max of the wall
time, and the median of the time spent inside the linker (measured by the
scripts/timed-cc wrapper). The hypothesis table applies the criteria written
in README.md mechanically to these numbers.
"""
import csv
import glob
import json
import statistics
from collections import defaultdict

LINE = 10.0  # seconds; the "ten seconds" line from the 2025 compiler performance survey

rows = []
for path in sorted(glob.glob("/work/results/raw/*.jsonl")):
    with open(path) as f:
        rows += [json.loads(l) for l in f if l.strip()]

groups = defaultdict(list)
for r in rows:
    if r.get("warmup"):
        continue
    key = (r["repo"], r["kind"], r["change"], r["cmd"], r["profile"], r["linker"])
    groups[key].append(r)

stats = {}
for key, rs in groups.items():
    s = [r["seconds"] for r in rs]
    ls = [r.get("link_wall_seconds", 0.0) for r in rs]
    stats[key] = {
        "n": len(s), "median": statistics.median(s), "min": min(s), "max": max(s),
        "link_median": statistics.median(ls),
        "compiled_files": statistics.median([r["compiled_files"] for r in rs]) if "compiled_files" in rs[0] else "",
        "linker_note": rs[0].get("linker_note", ""),
    }

ORDER = {"clean": 0, "leaf": 1, "core": 2, "sig": 3, "cc": 4, "header": 5}
CMD = {"check": 0, "build": 1, "test": 2, "make": 3}
LNK = {"default": 0, "lld": 1, "lld-t2": 2, "mold": 3, "mold-t2": 4}
keys = sorted(stats, key=lambda k: (k[0], k[1] != "clean", ORDER[k[2]], k[4], CMD[k[3]], LNK[k[5]]))

with open("/work/results/summary.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["repo", "kind", "change", "cmd", "profile", "linker", "n", "median_s", "min_s", "max_s",
                "link_median_s", "compiled_files_median", "side_of_10s_line", "linker_note"])
    for k in keys:
        s = stats[k]
        w.writerow(list(k) + [s["n"], f"{s['median']:.2f}", f"{s['min']:.2f}", f"{s['max']:.2f}",
                              f"{s['link_median']:.2f}", s["compiled_files"],
                              "below" if s["median"] < LINE else "above", s["linker_note"]])

CHANGE_JA = {"clean": "クリーンビルド", "leaf": "末端クレートの関数の中身", "core": "中心クレートの関数の中身",
             "sig": "中心クレートの公開関数のシグネチャ", "cc": ".cc の関数の中身", "header": "広く include されるヘッダの inline 関数の中身"}
CMD_JA = {"check": "cargo check", "build": "cargo build", "test": "cargo test --no-run", "make": "make"}

out = []
out.append("# 測定結果の要約（scripts/summarize.py が results/raw/*.jsonl から生成）\n")
out.append("暖機の 1 回を除いた回の、壁時計の時間（秒）。`link` は、少なくとも 1 つのリンカが動いていた時間（並列に走ったリンクは重ねて数えない）の中央値。\n")
out.append("| リポジトリ | 変更 | コマンド | profile | リンカ | n | 中央値 | 最小 | 最大 | link | 10 秒の線 |")
out.append("|---|---|---|---|---|---|---|---|---|---|---|")
for k in keys:
    s = stats[k]
    out.append(f"| {k[0]} | {CHANGE_JA[k[2]]} | {CMD_JA[k[3]]} | {k[4]} | {k[5]} | {s['n']} | {s['median']:.2f} | "
               f"{s['min']:.2f} | {s['max']:.2f} | {s['link_median']:.2f} | {'下' if s['median'] < LINE else '上'} |")


def g(repo, change, cmd, linker="default", kind="incr", profile="debug"):
    return stats.get((repo, kind, change, cmd, profile, linker))


out.append("\n## 仮説ごとの判定（README.md の基準を機械的に当てはめたもの）\n")
RUST = ["ripgrep", "helix", "mdbook"]

# (1)
out.append("### (1) 関数の中身を 1 行変えた後の cargo check は 3 リポジトリすべてで 10 秒未満か\n")
res1 = []
for repo in RUST:
    for change in ("leaf", "core"):
        s = g(repo, change, "check")
        if not s:
            res1.append(None)
            out.append(f"- {repo} {CHANGE_JA[change]}: データなし")
            continue
        below = s["max"] < LINE
        res1.append(below)
        out.append(f"- {repo} {CHANGE_JA[change]}: 中央値 {s['median']:.2f} 秒、最大 {s['max']:.2f} 秒 → "
                   f"{'5 回とも 10 秒未満' if below else '10 秒以上の回がある'}")
verdict1 = "データ不足" if None in res1 else ("成り立った" if all(res1) else "成り立たなかった")
out.append(f"- 判定（5 回とも 10 秒未満を「下回る」とする）: {verdict1}\n")

# (2)
out.append("### (2) build / test は check より明らかに長く、その差はリンカの交換で縮むか\n")
out.append("「明らかに長い」= build（または test）の最小が check の最大より大きい。"
           "「縮む」= lld / mold の中央値が既定より小さく、かつ lld / mold の最大が既定の最小より小さい。\n")
out.append("| リポジトリ | 変更 | コマンド | check 中央値 | 既定 中央値 | 既定 link | 差のうち link の割合 | lld 中央値 | mold 中央値 | 明らかに長い | lld で縮む | mold で縮む |")
out.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
for repo in RUST:
    for change in ("leaf", "core", "sig"):
        c = g(repo, change, "check")
        for cmd in ("build", "test"):
            d, l, m = g(repo, change, cmd), g(repo, change, cmd, "lld"), g(repo, change, cmd, "mold")
            if not (c and d and l and m):
                out.append(f"| {repo} | {CHANGE_JA[change]} | {CMD_JA[cmd]} | データなし |||||||||")
                continue
            diff = d["median"] - c["median"]
            share = d["link_median"] / diff if diff > 0 else float("nan")
            longer = d["min"] > c["max"]
            sl = l["median"] < d["median"] and l["max"] < d["min"]
            sm = m["median"] < d["median"] and m["max"] < d["min"]
            out.append(f"| {repo} | {CHANGE_JA[change]} | {CMD_JA[cmd]} | {c['median']:.2f} | {d['median']:.2f} | "
                       f"{d['link_median']:.2f} | {share:.0%} | {l['median']:.2f} | {m['median']:.2f} | "
                       f"{'はい' if longer else 'いいえ'} | {'はい' if sl else 'いいえ'} | {'はい' if sm else 'いいえ'} |")

out.append("\n#### 補足: リンカのスレッド数を CPU の割り当て（2 個）に合わせた場合\n")
out.append("`lld-t2` は `-Wl,--threads=2`、`mold-t2` は `-Wl,--thread-count=2` を足したもの。値は中央値（括弧内は最小〜最大）と、リンカが動いていた時間の中央値。\n")
out.append("| リポジトリ | 変更 | コマンド | 既定 | lld | lld-t2 | mold | mold-t2 |")
out.append("|---|---|---|---|---|---|---|---|")


def cell(s):
    return f"{s['median']:.2f} ({s['min']:.2f}〜{s['max']:.2f}) link {s['link_median']:.2f}" if s else "—"


for repo in RUST:
    for change in ("leaf", "core", "sig"):
        for cmd in ("build", "test"):
            if not g(repo, change, cmd, "mold-t2"):
                continue
            out.append(f"| {repo} | {CHANGE_JA[change]} | {CMD_JA[cmd]} | " +
                       " | ".join(cell(g(repo, change, cmd, l)) for l in ("default", "lld", "lld-t2", "mold", "mold-t2")) + " |")

# (3)
out.append("\n### (3) 中心クレートの公開関数のシグネチャを変えると、check でも 10 秒を超えることがあるか\n")
any3 = False
for repo in RUST:
    s, b = g(repo, "sig", "check"), g(repo, "core", "check")
    if not s:
        out.append(f"- {repo}: データなし")
        continue
    any3 = any3 or s["median"] >= LINE
    extra = f"（中身だけの変更の check 中央値は {b['median']:.2f} 秒）" if b else ""
    out.append(f"- {repo}: シグネチャ変更後の check 中央値 {s['median']:.2f} 秒、最大 {s['max']:.2f} 秒{extra}")
out.append(f"- 判定（どれか 1 つで中央値が 10 秒以上なら成り立つ）: {'成り立った' if any3 else '成り立たなかった'}\n")

# (4)
out.append("### (4) Kakoune で、ヘッダの変更は .cc の変更より再ビルドが大きく伸びるか\n")
cc, hh = g("kakoune", "cc", "make"), g("kakoune", "header", "make")
if cc and hh:
    ratio = hh["median"] / cc["median"]
    out.append(f"- .cc の変更: 中央値 {cc['median']:.2f} 秒（再コンパイルしたファイル {cc['compiled_files']} 個）")
    out.append(f"- ヘッダの変更: 中央値 {hh['median']:.2f} 秒（再コンパイルしたファイル {hh['compiled_files']} 個）")
    out.append(f"- 比: {ratio:.1f} 倍。判定（ヘッダの最小が .cc の最大の 2 倍を超えるなら成り立つ）: "
               f"{'成り立った' if hh['min'] > 2 * cc['max'] else '成り立たなかった'}")
else:
    out.append("- データなし")

with open("/work/results/summary.md", "w") as f:
    f.write("\n".join(out) + "\n")
print("\n".join(out))
