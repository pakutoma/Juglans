# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## プロジェクト概要

Juglansはプログラミング用合成モノスペースフォント。複数のソースフォント（Inconsolata, 源真ゴシック, DejaVu LGC, Anonymous Pro, Nerd Fonts, Powerline）をFontForgeのPythonスクリプトで合成し、Windows TerminalとiTerm2向けに最適化されたTTFを生成する。

## ビルド

```bash
cd Source/
./juglans_generator.sh
```

これにより4つのフォントバリアント（Regular/Bold × WindowsTerminal/iTerm2）が`product/`に生成され、tar.xzとzipアーカイブも作成される。

### 必要なツール
- FontForge（Python 3バインディング付き）
- fonttools（ttxコマンド）
- tar, xz, zip

テストスイート・リンター・フォーマッターは存在しない。

## アーキテクチャ

### ビルドパイプライン

`juglans_generator.sh`がオーケストレーター。ターミナル種別×ウェイトの各組み合わせに対して：
1. `fontforge -lang=py -script juglans_generator.py {terminal} {weight}` でフォント合成
2. `ttx`でOS/2テーブルの`xAvgCharWidth`をソースInconsolataから転写
3. 最終TTFを`product/`にコピー

### フォント合成処理（juglans_generator.py）

各ソースフォントに対して個別の加工を行い、最後にFontForgeの`mergeFonts`で統合する：

- **Inconsolata**（ASCIIベース）: ゼロをドット付きに置換、アスタリスクとチルダを除去（Anonymous Proから補充）
- **源真ゴシック**（CJK文字）: GSUB/GPOSルックアップ除去、文字種別に応じたスケーリング（0.91/0.97/0.86）
- **DejaVu LGC**（半角記号）: 全角文字を除去、0.83倍にスケーリング
- **Powerline/Nerd Fonts**（アイコン）: ターミナル固有の垂直位置・スケール調整（WindowsTerminal: y=-210, scale=1.09 / iTerm2: y=-175, scale=1.065）

### 主要パラメータ

フォントメトリクスは`juglans_generator.py`冒頭で定数定義。EM=1000（ascent 800 + descent 200）。ターミナル別のPowerline調整値はコマンドライン引数で分岐。

### ユーティリティ

`juglans_generator.py`内のヘルパー関数：
- `Matrix`クラス: 移動・スケーリングの合成変換
- `copyAndPaste()`: フォント間グリフコピー
- `scalingDownIfWidth()`: 幅を保持したスマートスケーリング
- `selectExistAll()`: 出力対象グリフの一括選択

## 言語

プロジェクトのドキュメント・コミットメッセージは日本語。
