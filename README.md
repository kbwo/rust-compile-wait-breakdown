# 「Rust のコンパイルは遅い」はどの待ち時間の話なのか — 測定用リポジトリ

## 確かめる仮説

「Rust のコンパイルは遅い」という評価は、どの待ち時間を指すかで大きく分かれる、という仮説を測って確かめる。

1. 関数の中身を 1 行変えた後の `cargo check`（型検査までで、コード生成をしない）は、調べた 3 つの Rust リポジトリのすべてで 10 秒を下回る。
2. 同じ変更の後の `cargo build` と `cargo test --no-run` は `check` より明らかに長い。その差にはコード生成とリンクが入り、リンカを lld や mold に変えると縮む。
3. 多くのクレートが依存する中心のクレートで、公開関数のシグネチャ（引数や戻り値の型）を変えると、依存するクレートの再検査が伝わり、`check` でも 10 秒を超えることがある。
4. C++ 製のエディタ Kakoune でも、.cc ファイルの変更は速く、多くのファイルが include するヘッダの変更では再ビルドが大きく伸びる。「変更の形で待ち時間が大きく変わる」性質は言語をまたいで共通する。

10 秒という線は、Rust の公式の調査の結果の記事 https://blog.rust-lang.org/2025/09/10/rust-compiler-performance-survey-2025-results/ にある "the fact that 55% of respondents have to wait more than ten seconds for a rebuild is far from ideal." から取った。

## 測った対象

| 名前 | リポジトリ | コミット |
|---|---|---|
| ripgrep | https://github.com/BurntSushi/ripgrep | `91f5d22ef48bde459d90a8c7dbeab416e97d0f2b` |
| helix | https://github.com/helix-editor/helix | `ba40e547426b0f9896c8bdc699a4ab11f2b37dbc` |
| mdBook | https://github.com/rust-lang/mdBook | `0accb8a3ff59e311c60e2267581fea6407d64c73` |
| Kakoune（C++） | https://github.com/mawww/kakoune | `a4466920c2a9223d7ba1feff12f02962d67ece3e` |

コミットの固定は `scripts/fetch.sh` にある。mdBook は、async（`serve` 機能の axum と tokio）と proc macro（コンパイル時にコードを生成するマクロ。serde や clap の derive）を使う中規模のワークスペースとして選んだ。

各リポジトリで変えた場所（1 行の変更）は `scripts/bench.py` の `REPOS` と `KAK` に書いてある。

- 末端のクレートの関数の中身（`leaf`）: 実行ファイルを作るクレートの関数の先頭に `let _ = std::hint::black_box(N);` を 1 行足す。`N` は回ごとに変える。`black_box` は、最適化で消されないようにする標準ライブラリの関数で、毎回コード生成をやり直させるために使った。
- 中心のクレートの関数の中身（`core`）: 多くのクレートが依存するクレート（ripgrep は `grep-searcher`、helix は `helix-core`、mdBook は `mdbook-core`）の公開関数に、同じ 1 行を足す。
- 中心のクレートの公開関数のシグネチャ（`sig`）: 同じ関数の引数の型を `T` から `impl Into<T>`（または `impl AsRef<T>`）に変え、同じ行で元の型に戻す。呼び出し側を書き換えずにコンパイルが通るシグネチャの変更にするためである。回ごとに、変えた形と元の形を交互にする。
- Kakoune: `src/normal.cc` の関数の中身（`cc`）と、多くのファイルが include する `src/string.hh` の inline 関数の中身（`header`）に、`volatile` の変数を置く 1 行を足す。

## 測り方

- 条件ごとに、暖機の 1 回の後に 5 回測る。暖機の回は集計から外す。差分の測定では、毎回、直前の状態までビルドを済ませてから 1 行を変え、コマンドの開始から終了までの壁時計の時間を測る。
- ビルドは、コンテナの中の `/tmp` で行う。作業フォルダ（`/work`）は持ち主のマシンと共有しているフォルダで、そこでビルドするとファイルの読み書きが遅くなり、数字が変わるためである。
- リンカの中で過ごした時間は、リンカを呼ぶ C コンパイラの前に挟んだ `scripts/timed-cc` が測って記録する。
- リンカは、既定（`cc` から呼ばれる GNU ld）、lld、mold の 3 つ。lld と mold は `-C link-arg=-fuse-ld=lld`（mold）を `CARGO_TARGET_<ターゲット>_RUSTFLAGS` で渡す。helix の `.cargo/config.toml` の `rustflags` を上書きしないように、`RUSTFLAGS` ではなくこの変数を使った。実際に使われたリンカは、出来た実行ファイルの `.comment` 節を `readelf` で読み、`linker_note` に残した。
- リンカの 3 種ごとにビルドの置き場（`CARGO_TARGET_DIR`）を分ける。フラグが変わるとビルドの成果物を使い回せないためである。`cargo check` はリンクをしないので、既定のリンカのときだけ測る。
- `CARGO_BUILD_JOBS=2`。コンテナは CPU 2 個とメモリ 4 GB に制限されている。`nproc` はホストの 14 を返すので、並列数をそのままにするとメモリが足りなくなるおそれがある。
- `RUSTUP_TOOLCHAIN=1.99.1` で、各リポジトリの `rust-toolchain.toml` を上書きして、すべて同じコンパイラで測る。
- helix は `HELIX_DISABLE_AUTO_GRAMMAR_BUILD=1` で、tree-sitter の文法（構文解析器）を取ってきてコンパイルする処理を止めた。文法は多数の外部のリポジトリから取ってくるもので、Rust のコンパイルの時間ではないためである。
- Kakoune は `make -j2 debug=yes`（`-O0 -g3`）でビルドした。Rust の `cargo build` が最適化なしの dev profile であるのに揃えた。

## 動かし方

```sh
docker build -t rust-compile-wait .
docker run --rm --cpus 2 --memory 4g -v "$PWD:/work" -w /work rust-compile-wait sh -c '
  chmod +x scripts/timed-cc && sh scripts/fetch.sh &&
  for r in ripgrep helix mdbook; do
    python3 scripts/bench.py clean $r
    for l in default lld mold; do python3 scripts/bench.py incr $r $l; done
  done &&
  python3 scripts/bench.py kak &&
  python3 scripts/summarize.py'
```

時間がかかるので、上のループは何回かの `docker run` に分けて動かしてよい。結果は `results/raw/` に追記される。

補足の測定（リンカのスレッド数を、コンテナに割り当てた CPU の数 2 に合わせたもの）は、次で動かした。mold は見えている CPU の数（ここでは `nproc` の 14）だけスレッドを立てるので、CPU が 2 個に制限されたコンテナでは既定の GNU ld より速くならない条件があった。その理由がスレッド数かどうかを見るためである。

```sh
docker run --rm --cpus 2 --memory 4g -v "$PWD:/work" -w /work rust-compile-wait sh -c '
  chmod +x scripts/timed-cc &&
  for r in ripgrep mdbook helix; do
    for l in mold-t2 lld-t2; do python3 scripts/bench.py incr $r $l; done
  done && python3 scripts/summarize.py'
```

## 結果のファイルの読み方

- `results/env.txt`: CPU、メモリの上限、rustc・cargo・C/C++ コンパイラ・リンカの版。
- `results/raw/<repo>.jsonl`: 1 行が 1 回の実行。`change`（`clean` / `leaf` / `core` / `sig` / `cc` / `header`）、`cmd`、`profile`、`linker`、`iter`、`warmup`（暖機の回なら `true`）、`seconds`（壁時計の秒）、`link_seconds`（リンカの中の秒の合計）、`link_count`（リンカを呼んだ回数）、`units`（cargo が再コンパイルしたクレートの一覧）、`compiled_files`（Kakoune で再コンパイルした .cc の数）。
- `results/summary.csv` と `results/summary.md`: `scripts/summarize.py` が raw から作る集計。暖機を除いた中央値・最小・最大と、仮説ごとの判定。判定の基準は `summary.md` の各節の見出しの下に書いてある。
- `results/timings/*.html`: `cargo build --timings` が出す、クレートごとのコンパイルの時間の図。
- `results/log-*.txt`: 測定を動かしたときのコンテナの中の出力そのもの。`log-linker-threads.txt` は補足の測定のもの。

## 限界

- docker の中（Apple Silicon の macOS の上の Linux、aarch64）での測定で、手元のマシンや CI とは数字が違う。比べられるのは同じ環境の中での相対的な差である。
- lld が既定のリンカになるのは `x86_64-unknown-linux-gnu` ターゲットである。この測定のターゲットは aarch64 なので、既定のリンカは GNU ld である。
