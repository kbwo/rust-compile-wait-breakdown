# 測定結果の要約（scripts/summarize.py が results/raw/*.jsonl から生成）

暖機の 1 回を除いた回の、壁時計の時間（秒）。`link` は、少なくとも 1 つのリンカが動いていた時間（並列に走ったリンクは重ねて数えない）の中央値。

| リポジトリ | 変更 | コマンド | profile | リンカ | n | 中央値 | 最小 | 最大 | link | 10 秒の線 |
|---|---|---|---|---|---|---|---|---|---|---|
| helix | クリーンビルド | cargo build | debug | default | 5 | 56.09 | 55.53 | 58.47 | 8.54 | 上 |
| helix | クリーンビルド | cargo build | release | default | 5 | 126.17 | 124.07 | 128.42 | 2.81 | 上 |
| helix | 末端クレートの関数の中身 | cargo check | debug | default | 5 | 0.41 | 0.40 | 0.42 | 0.00 | 下 |
| helix | 末端クレートの関数の中身 | cargo build | debug | default | 5 | 7.92 | 7.75 | 8.45 | 5.99 | 下 |
| helix | 末端クレートの関数の中身 | cargo build | debug | lld | 5 | 3.54 | 3.30 | 4.09 | 1.76 | 下 |
| helix | 末端クレートの関数の中身 | cargo build | debug | lld-t2 | 5 | 3.01 | 2.82 | 3.10 | 1.16 | 下 |
| helix | 末端クレートの関数の中身 | cargo build | debug | mold | 5 | 4.81 | 3.99 | 5.20 | 3.00 | 下 |
| helix | 末端クレートの関数の中身 | cargo build | debug | mold-t2 | 5 | 3.01 | 2.63 | 3.29 | 0.98 | 下 |
| helix | 末端クレートの関数の中身 | cargo test --no-run | debug | default | 5 | 9.77 | 9.47 | 10.63 | 8.14 | 下 |
| helix | 末端クレートの関数の中身 | cargo test --no-run | debug | lld | 5 | 5.55 | 5.40 | 5.94 | 3.84 | 下 |
| helix | 末端クレートの関数の中身 | cargo test --no-run | debug | lld-t2 | 5 | 3.95 | 3.78 | 4.39 | 2.49 | 下 |
| helix | 末端クレートの関数の中身 | cargo test --no-run | debug | mold | 5 | 8.58 | 7.80 | 9.69 | 6.64 | 下 |
| helix | 末端クレートの関数の中身 | cargo test --no-run | debug | mold-t2 | 5 | 4.28 | 4.18 | 4.88 | 2.60 | 下 |
| helix | 中心クレートの関数の中身 | cargo check | debug | default | 5 | 1.08 | 1.06 | 1.20 | 0.00 | 下 |
| helix | 中心クレートの関数の中身 | cargo build | debug | default | 5 | 9.37 | 8.93 | 11.36 | 6.05 | 下 |
| helix | 中心クレートの関数の中身 | cargo build | debug | lld | 5 | 4.74 | 4.65 | 5.01 | 1.93 | 下 |
| helix | 中心クレートの関数の中身 | cargo build | debug | lld-t2 | 5 | 3.77 | 3.49 | 4.04 | 0.93 | 下 |
| helix | 中心クレートの関数の中身 | cargo build | debug | mold | 5 | 5.99 | 5.96 | 6.54 | 3.03 | 下 |
| helix | 中心クレートの関数の中身 | cargo build | debug | mold-t2 | 5 | 3.82 | 3.59 | 4.97 | 0.95 | 下 |
| helix | 中心クレートの関数の中身 | cargo test --no-run | debug | default | 5 | 10.91 | 10.60 | 11.38 | 8.05 | 上 |
| helix | 中心クレートの関数の中身 | cargo test --no-run | debug | lld | 5 | 6.72 | 6.55 | 7.31 | 3.93 | 下 |
| helix | 中心クレートの関数の中身 | cargo test --no-run | debug | lld-t2 | 5 | 5.35 | 5.10 | 5.99 | 2.72 | 下 |
| helix | 中心クレートの関数の中身 | cargo test --no-run | debug | mold | 5 | 10.89 | 10.24 | 12.00 | 7.81 | 上 |
| helix | 中心クレートの関数の中身 | cargo test --no-run | debug | mold-t2 | 5 | 5.71 | 5.54 | 6.01 | 2.87 | 下 |
| helix | 中心クレートの公開関数のシグネチャ | cargo check | debug | default | 5 | 1.15 | 1.08 | 1.22 | 0.00 | 下 |
| helix | 中心クレートの公開関数のシグネチャ | cargo build | debug | default | 5 | 11.21 | 11.00 | 11.39 | 5.83 | 上 |
| helix | 中心クレートの公開関数のシグネチャ | cargo build | debug | lld | 5 | 6.73 | 6.21 | 7.05 | 1.64 | 下 |
| helix | 中心クレートの公開関数のシグネチャ | cargo build | debug | lld-t2 | 5 | 6.11 | 5.70 | 6.90 | 1.16 | 下 |
| helix | 中心クレートの公開関数のシグネチャ | cargo build | debug | mold | 5 | 8.47 | 7.41 | 10.44 | 3.10 | 下 |
| helix | 中心クレートの公開関数のシグネチャ | cargo build | debug | mold-t2 | 5 | 6.14 | 5.74 | 6.47 | 1.01 | 下 |
| helix | 中心クレートの公開関数のシグネチャ | cargo test --no-run | debug | default | 5 | 14.40 | 13.69 | 14.79 | 9.77 | 上 |
| helix | 中心クレートの公開関数のシグネチャ | cargo test --no-run | debug | lld | 5 | 9.41 | 9.08 | 10.01 | 3.70 | 下 |
| helix | 中心クレートの公開関数のシグネチャ | cargo test --no-run | debug | lld-t2 | 5 | 7.93 | 7.65 | 8.34 | 2.75 | 下 |
| helix | 中心クレートの公開関数のシグネチャ | cargo test --no-run | debug | mold | 5 | 13.23 | 12.65 | 13.61 | 7.52 | 上 |
| helix | 中心クレートの公開関数のシグネチャ | cargo test --no-run | debug | mold-t2 | 5 | 8.77 | 8.13 | 8.86 | 3.15 | 下 |
| kakoune | クリーンビルド | make | debug | default | 1 | 21.98 | 21.98 | 21.98 | 0.00 | 上 |
| kakoune | .cc の関数の中身 | make | debug | default | 5 | 2.69 | 2.62 | 2.75 | 0.00 | 下 |
| kakoune | 広く include されるヘッダの inline 関数の中身 | make | debug | default | 5 | 21.81 | 21.55 | 22.03 | 0.00 | 上 |
| mdbook | クリーンビルド | cargo build | debug | default | 5 | 25.00 | 24.68 | 25.31 | 4.08 | 上 |
| mdbook | クリーンビルド | cargo build | release | default | 5 | 50.72 | 50.04 | 51.10 | 2.32 | 上 |
| mdbook | 末端クレートの関数の中身 | cargo check | debug | default | 5 | 0.12 | 0.12 | 0.12 | 0.00 | 下 |
| mdbook | 末端クレートの関数の中身 | cargo build | debug | default | 5 | 2.02 | 1.98 | 2.17 | 1.77 | 下 |
| mdbook | 末端クレートの関数の中身 | cargo build | debug | lld | 5 | 0.80 | 0.79 | 0.95 | 0.58 | 下 |
| mdbook | 末端クレートの関数の中身 | cargo build | debug | lld-t2 | 5 | 0.52 | 0.51 | 0.54 | 0.30 | 下 |
| mdbook | 末端クレートの関数の中身 | cargo build | debug | mold | 5 | 2.01 | 1.61 | 2.19 | 1.74 | 下 |
| mdbook | 末端クレートの関数の中身 | cargo build | debug | mold-t2 | 5 | 0.60 | 0.58 | 0.71 | 0.35 | 下 |
| mdbook | 末端クレートの関数の中身 | cargo test --no-run | debug | default | 5 | 2.01 | 1.97 | 2.04 | 1.82 | 下 |
| mdbook | 末端クレートの関数の中身 | cargo test --no-run | debug | lld | 5 | 1.30 | 1.11 | 1.39 | 1.11 | 下 |
| mdbook | 末端クレートの関数の中身 | cargo test --no-run | debug | lld-t2 | 5 | 0.66 | 0.65 | 0.73 | 0.47 | 下 |
| mdbook | 末端クレートの関数の中身 | cargo test --no-run | debug | mold | 5 | 2.50 | 2.00 | 8.91 | 2.29 | 下 |
| mdbook | 末端クレートの関数の中身 | cargo test --no-run | debug | mold-t2 | 5 | 0.81 | 0.79 | 0.82 | 0.61 | 下 |
| mdbook | 中心クレートの関数の中身 | cargo check | debug | default | 5 | 0.40 | 0.39 | 0.41 | 0.00 | 下 |
| mdbook | 中心クレートの関数の中身 | cargo build | debug | default | 5 | 2.45 | 2.32 | 2.54 | 1.81 | 下 |
| mdbook | 中心クレートの関数の中身 | cargo build | debug | lld | 5 | 1.22 | 1.12 | 1.29 | 0.55 | 下 |
| mdbook | 中心クレートの関数の中身 | cargo build | debug | lld-t2 | 5 | 0.93 | 0.91 | 1.03 | 0.30 | 下 |
| mdbook | 中心クレートの関数の中身 | cargo build | debug | mold | 5 | 1.71 | 1.50 | 2.10 | 1.03 | 下 |
| mdbook | 中心クレートの関数の中身 | cargo build | debug | mold-t2 | 5 | 0.96 | 0.93 | 1.01 | 0.32 | 下 |
| mdbook | 中心クレートの関数の中身 | cargo test --no-run | debug | default | 5 | 4.27 | 3.87 | 4.64 | 3.64 | 下 |
| mdbook | 中心クレートの関数の中身 | cargo test --no-run | debug | lld | 5 | 2.70 | 2.58 | 2.79 | 1.94 | 下 |
| mdbook | 中心クレートの関数の中身 | cargo test --no-run | debug | lld-t2 | 5 | 1.76 | 1.63 | 1.87 | 1.04 | 下 |
| mdbook | 中心クレートの関数の中身 | cargo test --no-run | debug | mold | 5 | 4.29 | 3.60 | 4.91 | 3.53 | 下 |
| mdbook | 中心クレートの関数の中身 | cargo test --no-run | debug | mold-t2 | 5 | 1.87 | 1.82 | 2.01 | 1.25 | 下 |
| mdbook | 中心クレートの公開関数のシグネチャ | cargo check | debug | default | 5 | 0.43 | 0.43 | 0.49 | 0.00 | 下 |
| mdbook | 中心クレートの公開関数のシグネチャ | cargo build | debug | default | 5 | 3.44 | 3.30 | 3.72 | 1.80 | 下 |
| mdbook | 中心クレートの公開関数のシグネチャ | cargo build | debug | lld | 5 | 2.29 | 2.13 | 2.48 | 0.57 | 下 |
| mdbook | 中心クレートの公開関数のシグネチャ | cargo build | debug | lld-t2 | 5 | 1.83 | 1.75 | 2.01 | 0.32 | 下 |
| mdbook | 中心クレートの公開関数のシグネチャ | cargo build | debug | mold | 5 | 2.58 | 2.43 | 2.80 | 0.97 | 下 |
| mdbook | 中心クレートの公開関数のシグネチャ | cargo build | debug | mold-t2 | 5 | 1.84 | 1.81 | 2.00 | 0.33 | 下 |
| mdbook | 中心クレートの公開関数のシグネチャ | cargo test --no-run | debug | default | 5 | 5.62 | 4.98 | 6.46 | 4.19 | 下 |
| mdbook | 中心クレートの公開関数のシグネチャ | cargo test --no-run | debug | lld | 5 | 3.86 | 3.58 | 4.19 | 2.04 | 下 |
| mdbook | 中心クレートの公開関数のシグネチャ | cargo test --no-run | debug | lld-t2 | 5 | 2.82 | 2.65 | 2.87 | 1.11 | 下 |
| mdbook | 中心クレートの公開関数のシグネチャ | cargo test --no-run | debug | mold | 5 | 5.49 | 5.30 | 5.69 | 3.77 | 下 |
| mdbook | 中心クレートの公開関数のシグネチャ | cargo test --no-run | debug | mold-t2 | 5 | 2.92 | 2.82 | 3.00 | 1.36 | 下 |
| ripgrep | クリーンビルド | cargo build | debug | default | 5 | 6.93 | 6.84 | 7.11 | 1.11 | 下 |
| ripgrep | クリーンビルド | cargo build | release | default | 5 | 18.11 | 18.01 | 18.31 | 0.79 | 上 |
| ripgrep | 末端クレートの関数の中身 | cargo check | debug | default | 5 | 0.10 | 0.09 | 0.11 | 0.00 | 下 |
| ripgrep | 末端クレートの関数の中身 | cargo build | debug | default | 5 | 0.83 | 0.81 | 0.91 | 0.64 | 下 |
| ripgrep | 末端クレートの関数の中身 | cargo build | debug | lld | 5 | 0.39 | 0.31 | 0.48 | 0.17 | 下 |
| ripgrep | 末端クレートの関数の中身 | cargo build | debug | lld-t2 | 5 | 0.32 | 0.30 | 0.41 | 0.13 | 下 |
| ripgrep | 末端クレートの関数の中身 | cargo build | debug | mold | 5 | 1.00 | 0.51 | 1.41 | 0.66 | 下 |
| ripgrep | 末端クレートの関数の中身 | cargo build | debug | mold-t2 | 5 | 0.34 | 0.33 | 0.34 | 0.15 | 下 |
| ripgrep | 末端クレートの関数の中身 | cargo test --no-run | debug | default | 5 | 1.31 | 1.12 | 1.41 | 1.09 | 下 |
| ripgrep | 末端クレートの関数の中身 | cargo test --no-run | debug | lld | 5 | 0.78 | 0.69 | 0.81 | 0.41 | 下 |
| ripgrep | 末端クレートの関数の中身 | cargo test --no-run | debug | lld-t2 | 5 | 0.59 | 0.58 | 0.61 | 0.25 | 下 |
| ripgrep | 末端クレートの関数の中身 | cargo test --no-run | debug | mold | 5 | 1.79 | 1.21 | 7.21 | 1.43 | 下 |
| ripgrep | 末端クレートの関数の中身 | cargo test --no-run | debug | mold-t2 | 5 | 0.63 | 0.61 | 0.70 | 0.34 | 下 |
| ripgrep | 中心クレートの関数の中身 | cargo check | debug | default | 5 | 0.21 | 0.19 | 0.27 | 0.00 | 下 |
| ripgrep | 中心クレートの関数の中身 | cargo build | debug | default | 5 | 0.94 | 0.92 | 1.01 | 0.64 | 下 |
| ripgrep | 中心クレートの関数の中身 | cargo build | debug | lld | 5 | 0.50 | 0.49 | 0.52 | 0.19 | 下 |
| ripgrep | 中心クレートの関数の中身 | cargo build | debug | lld-t2 | 5 | 0.45 | 0.43 | 0.58 | 0.13 | 下 |
| ripgrep | 中心クレートの関数の中身 | cargo build | debug | mold | 5 | 0.80 | 0.70 | 0.89 | 0.44 | 下 |
| ripgrep | 中心クレートの関数の中身 | cargo build | debug | mold-t2 | 5 | 0.46 | 0.44 | 0.47 | 0.15 | 下 |
| ripgrep | 中心クレートの関数の中身 | cargo test --no-run | debug | default | 5 | 1.27 | 1.25 | 1.49 | 0.95 | 下 |
| ripgrep | 中心クレートの関数の中身 | cargo test --no-run | debug | lld | 5 | 0.99 | 0.80 | 1.05 | 0.41 | 下 |
| ripgrep | 中心クレートの関数の中身 | cargo test --no-run | debug | lld-t2 | 5 | 0.70 | 0.67 | 0.72 | 0.26 | 下 |
| ripgrep | 中心クレートの関数の中身 | cargo test --no-run | debug | mold | 5 | 1.50 | 1.39 | 2.20 | 1.06 | 下 |
| ripgrep | 中心クレートの関数の中身 | cargo test --no-run | debug | mold-t2 | 5 | 0.79 | 0.75 | 0.85 | 0.34 | 下 |
| ripgrep | 中心クレートの公開関数のシグネチャ | cargo check | debug | default | 5 | 0.19 | 0.19 | 0.21 | 0.00 | 下 |
| ripgrep | 中心クレートの公開関数のシグネチャ | cargo build | debug | default | 5 | 1.03 | 1.02 | 1.09 | 0.67 | 下 |
| ripgrep | 中心クレートの公開関数のシグネチャ | cargo build | debug | lld | 5 | 0.59 | 0.51 | 0.80 | 0.17 | 下 |
| ripgrep | 中心クレートの公開関数のシグネチャ | cargo build | debug | lld-t2 | 5 | 0.53 | 0.52 | 0.54 | 0.13 | 下 |
| ripgrep | 中心クレートの公開関数のシグネチャ | cargo build | debug | mold | 5 | 0.80 | 0.71 | 0.90 | 0.35 | 下 |
| ripgrep | 中心クレートの公開関数のシグネチャ | cargo build | debug | mold-t2 | 5 | 0.55 | 0.53 | 0.63 | 0.17 | 下 |
| ripgrep | 中心クレートの公開関数のシグネチャ | cargo test --no-run | debug | default | 5 | 1.27 | 1.25 | 1.35 | 0.95 | 下 |
| ripgrep | 中心クレートの公開関数のシグネチャ | cargo test --no-run | debug | lld | 5 | 0.90 | 0.85 | 1.66 | 0.46 | 下 |
| ripgrep | 中心クレートの公開関数のシグネチャ | cargo test --no-run | debug | lld-t2 | 5 | 0.73 | 0.72 | 0.93 | 0.32 | 下 |
| ripgrep | 中心クレートの公開関数のシグネチャ | cargo test --no-run | debug | mold | 5 | 1.70 | 1.50 | 1.81 | 1.10 | 下 |
| ripgrep | 中心クレートの公開関数のシグネチャ | cargo test --no-run | debug | mold-t2 | 5 | 0.94 | 0.81 | 1.00 | 0.36 | 下 |

## 仮説ごとの判定（README.md の基準を機械的に当てはめたもの）

### (1) 関数の中身を 1 行変えた後の cargo check は 3 リポジトリすべてで 10 秒未満か

- ripgrep 末端クレートの関数の中身: 中央値 0.10 秒、最大 0.11 秒 → 5 回とも 10 秒未満
- ripgrep 中心クレートの関数の中身: 中央値 0.21 秒、最大 0.27 秒 → 5 回とも 10 秒未満
- helix 末端クレートの関数の中身: 中央値 0.41 秒、最大 0.42 秒 → 5 回とも 10 秒未満
- helix 中心クレートの関数の中身: 中央値 1.08 秒、最大 1.20 秒 → 5 回とも 10 秒未満
- mdbook 末端クレートの関数の中身: 中央値 0.12 秒、最大 0.12 秒 → 5 回とも 10 秒未満
- mdbook 中心クレートの関数の中身: 中央値 0.40 秒、最大 0.41 秒 → 5 回とも 10 秒未満
- 判定（5 回とも 10 秒未満を「下回る」とする）: 成り立った

### (2) build / test は check より明らかに長く、その差はリンカの交換で縮むか

「明らかに長い」= build（または test）の最小が check の最大より大きい。「縮む」= lld / mold の中央値が既定より小さく、かつ lld / mold の最大が既定の最小より小さい。

| リポジトリ | 変更 | コマンド | check 中央値 | 既定 中央値 | 既定 link | 差のうち link の割合 | lld 中央値 | mold 中央値 | 明らかに長い | lld で縮む | mold で縮む |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ripgrep | 末端クレートの関数の中身 | cargo build | 0.10 | 0.83 | 0.64 | 87% | 0.39 | 1.00 | はい | はい | いいえ |
| ripgrep | 末端クレートの関数の中身 | cargo test --no-run | 0.10 | 1.31 | 1.09 | 90% | 0.78 | 1.79 | はい | はい | いいえ |
| ripgrep | 中心クレートの関数の中身 | cargo build | 0.21 | 0.94 | 0.64 | 88% | 0.50 | 0.80 | はい | はい | はい |
| ripgrep | 中心クレートの関数の中身 | cargo test --no-run | 0.21 | 1.27 | 0.95 | 90% | 0.99 | 1.50 | はい | はい | いいえ |
| ripgrep | 中心クレートの公開関数のシグネチャ | cargo build | 0.19 | 1.03 | 0.67 | 79% | 0.59 | 0.80 | はい | はい | はい |
| ripgrep | 中心クレートの公開関数のシグネチャ | cargo test --no-run | 0.19 | 1.27 | 0.95 | 88% | 0.90 | 1.70 | はい | いいえ | いいえ |
| helix | 末端クレートの関数の中身 | cargo build | 0.41 | 7.92 | 5.99 | 80% | 3.54 | 4.81 | はい | はい | はい |
| helix | 末端クレートの関数の中身 | cargo test --no-run | 0.41 | 9.77 | 8.14 | 87% | 5.55 | 8.58 | はい | はい | いいえ |
| helix | 中心クレートの関数の中身 | cargo build | 1.08 | 9.37 | 6.05 | 73% | 4.74 | 5.99 | はい | はい | はい |
| helix | 中心クレートの関数の中身 | cargo test --no-run | 1.08 | 10.91 | 8.05 | 82% | 6.72 | 10.89 | はい | はい | いいえ |
| helix | 中心クレートの公開関数のシグネチャ | cargo build | 1.15 | 11.21 | 5.83 | 58% | 6.73 | 8.47 | はい | はい | はい |
| helix | 中心クレートの公開関数のシグネチャ | cargo test --no-run | 1.15 | 14.40 | 9.77 | 74% | 9.41 | 13.23 | はい | はい | はい |
| mdbook | 末端クレートの関数の中身 | cargo build | 0.12 | 2.02 | 1.77 | 93% | 0.80 | 2.01 | はい | はい | いいえ |
| mdbook | 末端クレートの関数の中身 | cargo test --no-run | 0.12 | 2.01 | 1.82 | 96% | 1.30 | 2.50 | はい | はい | いいえ |
| mdbook | 中心クレートの関数の中身 | cargo build | 0.40 | 2.45 | 1.81 | 88% | 1.22 | 1.71 | はい | はい | はい |
| mdbook | 中心クレートの関数の中身 | cargo test --no-run | 0.40 | 4.27 | 3.64 | 94% | 2.70 | 4.29 | はい | はい | いいえ |
| mdbook | 中心クレートの公開関数のシグネチャ | cargo build | 0.43 | 3.44 | 1.80 | 60% | 2.29 | 2.58 | はい | はい | はい |
| mdbook | 中心クレートの公開関数のシグネチャ | cargo test --no-run | 0.43 | 5.62 | 4.19 | 81% | 3.86 | 5.49 | はい | はい | いいえ |

#### 補足: リンカのスレッド数を CPU の割り当て（2 個）に合わせた場合

`lld-t2` は `-Wl,--threads=2`、`mold-t2` は `-Wl,--thread-count=2` を足したもの。値は中央値（括弧内は最小〜最大）と、リンカが動いていた時間の中央値。

| リポジトリ | 変更 | コマンド | 既定 | lld | lld-t2 | mold | mold-t2 |
|---|---|---|---|---|---|---|---|
| ripgrep | 末端クレートの関数の中身 | cargo build | 0.83 (0.81〜0.91) link 0.64 | 0.39 (0.31〜0.48) link 0.17 | 0.32 (0.30〜0.41) link 0.13 | 1.00 (0.51〜1.41) link 0.66 | 0.34 (0.33〜0.34) link 0.15 |
| ripgrep | 末端クレートの関数の中身 | cargo test --no-run | 1.31 (1.12〜1.41) link 1.09 | 0.78 (0.69〜0.81) link 0.41 | 0.59 (0.58〜0.61) link 0.25 | 1.79 (1.21〜7.21) link 1.43 | 0.63 (0.61〜0.70) link 0.34 |
| ripgrep | 中心クレートの関数の中身 | cargo build | 0.94 (0.92〜1.01) link 0.64 | 0.50 (0.49〜0.52) link 0.19 | 0.45 (0.43〜0.58) link 0.13 | 0.80 (0.70〜0.89) link 0.44 | 0.46 (0.44〜0.47) link 0.15 |
| ripgrep | 中心クレートの関数の中身 | cargo test --no-run | 1.27 (1.25〜1.49) link 0.95 | 0.99 (0.80〜1.05) link 0.41 | 0.70 (0.67〜0.72) link 0.26 | 1.50 (1.39〜2.20) link 1.06 | 0.79 (0.75〜0.85) link 0.34 |
| ripgrep | 中心クレートの公開関数のシグネチャ | cargo build | 1.03 (1.02〜1.09) link 0.67 | 0.59 (0.51〜0.80) link 0.17 | 0.53 (0.52〜0.54) link 0.13 | 0.80 (0.71〜0.90) link 0.35 | 0.55 (0.53〜0.63) link 0.17 |
| ripgrep | 中心クレートの公開関数のシグネチャ | cargo test --no-run | 1.27 (1.25〜1.35) link 0.95 | 0.90 (0.85〜1.66) link 0.46 | 0.73 (0.72〜0.93) link 0.32 | 1.70 (1.50〜1.81) link 1.10 | 0.94 (0.81〜1.00) link 0.36 |
| helix | 末端クレートの関数の中身 | cargo build | 7.92 (7.75〜8.45) link 5.99 | 3.54 (3.30〜4.09) link 1.76 | 3.01 (2.82〜3.10) link 1.16 | 4.81 (3.99〜5.20) link 3.00 | 3.01 (2.63〜3.29) link 0.98 |
| helix | 末端クレートの関数の中身 | cargo test --no-run | 9.77 (9.47〜10.63) link 8.14 | 5.55 (5.40〜5.94) link 3.84 | 3.95 (3.78〜4.39) link 2.49 | 8.58 (7.80〜9.69) link 6.64 | 4.28 (4.18〜4.88) link 2.60 |
| helix | 中心クレートの関数の中身 | cargo build | 9.37 (8.93〜11.36) link 6.05 | 4.74 (4.65〜5.01) link 1.93 | 3.77 (3.49〜4.04) link 0.93 | 5.99 (5.96〜6.54) link 3.03 | 3.82 (3.59〜4.97) link 0.95 |
| helix | 中心クレートの関数の中身 | cargo test --no-run | 10.91 (10.60〜11.38) link 8.05 | 6.72 (6.55〜7.31) link 3.93 | 5.35 (5.10〜5.99) link 2.72 | 10.89 (10.24〜12.00) link 7.81 | 5.71 (5.54〜6.01) link 2.87 |
| helix | 中心クレートの公開関数のシグネチャ | cargo build | 11.21 (11.00〜11.39) link 5.83 | 6.73 (6.21〜7.05) link 1.64 | 6.11 (5.70〜6.90) link 1.16 | 8.47 (7.41〜10.44) link 3.10 | 6.14 (5.74〜6.47) link 1.01 |
| helix | 中心クレートの公開関数のシグネチャ | cargo test --no-run | 14.40 (13.69〜14.79) link 9.77 | 9.41 (9.08〜10.01) link 3.70 | 7.93 (7.65〜8.34) link 2.75 | 13.23 (12.65〜13.61) link 7.52 | 8.77 (8.13〜8.86) link 3.15 |
| mdbook | 末端クレートの関数の中身 | cargo build | 2.02 (1.98〜2.17) link 1.77 | 0.80 (0.79〜0.95) link 0.58 | 0.52 (0.51〜0.54) link 0.30 | 2.01 (1.61〜2.19) link 1.74 | 0.60 (0.58〜0.71) link 0.35 |
| mdbook | 末端クレートの関数の中身 | cargo test --no-run | 2.01 (1.97〜2.04) link 1.82 | 1.30 (1.11〜1.39) link 1.11 | 0.66 (0.65〜0.73) link 0.47 | 2.50 (2.00〜8.91) link 2.29 | 0.81 (0.79〜0.82) link 0.61 |
| mdbook | 中心クレートの関数の中身 | cargo build | 2.45 (2.32〜2.54) link 1.81 | 1.22 (1.12〜1.29) link 0.55 | 0.93 (0.91〜1.03) link 0.30 | 1.71 (1.50〜2.10) link 1.03 | 0.96 (0.93〜1.01) link 0.32 |
| mdbook | 中心クレートの関数の中身 | cargo test --no-run | 4.27 (3.87〜4.64) link 3.64 | 2.70 (2.58〜2.79) link 1.94 | 1.76 (1.63〜1.87) link 1.04 | 4.29 (3.60〜4.91) link 3.53 | 1.87 (1.82〜2.01) link 1.25 |
| mdbook | 中心クレートの公開関数のシグネチャ | cargo build | 3.44 (3.30〜3.72) link 1.80 | 2.29 (2.13〜2.48) link 0.57 | 1.83 (1.75〜2.01) link 0.32 | 2.58 (2.43〜2.80) link 0.97 | 1.84 (1.81〜2.00) link 0.33 |
| mdbook | 中心クレートの公開関数のシグネチャ | cargo test --no-run | 5.62 (4.98〜6.46) link 4.19 | 3.86 (3.58〜4.19) link 2.04 | 2.82 (2.65〜2.87) link 1.11 | 5.49 (5.30〜5.69) link 3.77 | 2.92 (2.82〜3.00) link 1.36 |

### (3) 中心クレートの公開関数のシグネチャを変えると、check でも 10 秒を超えることがあるか

- ripgrep: シグネチャ変更後の check 中央値 0.19 秒、最大 0.21 秒（中身だけの変更の check 中央値は 0.21 秒）
- helix: シグネチャ変更後の check 中央値 1.15 秒、最大 1.22 秒（中身だけの変更の check 中央値は 1.08 秒）
- mdbook: シグネチャ変更後の check 中央値 0.43 秒、最大 0.49 秒（中身だけの変更の check 中央値は 0.40 秒）
- 判定（どれか 1 つで中央値が 10 秒以上なら成り立つ）: 成り立たなかった

### (4) Kakoune で、ヘッダの変更は .cc の変更より再ビルドが大きく伸びるか

- .cc の変更: 中央値 2.69 秒（再コンパイルしたファイル 1 個）
- ヘッダの変更: 中央値 21.81 秒（再コンパイルしたファイル 56 個）
- 比: 8.1 倍。判定（ヘッダの最小が .cc の最大の 2 倍を超えるなら成り立つ）: 成り立った
