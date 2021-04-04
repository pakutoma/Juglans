# プログラミング用フォント Juglans
Juglans （ユグランス）は、フリーなプログラミング用 TrueType フォント Myrica の改変フォントです。

## Myrica からの変更点
- Myricaで行われていた多くの字形変更を元に戻す
- Mgen+ 版の削除
- ビルド環境を Linux (Arch Linux を想定) に変更
- 生成スクリプトを Python 3 に変更
- 7z 圧縮を xz 圧縮に変更

## 合成元フォントからの字形の変更点 (全てMyrica由来の変更です)
U+0044 D : LATIN CAPITAL LETTER D (Inconsolata内の別グリフ)  
U+002A * : ASTERISK (Myrica ReplaceParts)  
U+002D - : HYPHEN-MINUS (Myrica ReplaceParts)  
U+0072 r : LATIN SMALL LETTER R (Inconsolata内の別グリフ)  
U+007C | : VERTICAL LINE (Inconsolata内の別グリフ)  
U+2013 – : EN DASH (Myrica ReplaceParts)  
U+2014 — : EM DASH (Myrica ReplaceParts)  
U+301C 〜 : WAVE DASH (Myrica ReplaceParts)  

## License
SIL OPEN FONT LICENSE Version 1.1

## 利用フォント
Myrica (ReplaceParts の一部)  
Inconsolata (ASCII 文字)  
源真ゴシック (ASCII 文字以外)

## Myrica について
改変元フォント Myrica の説明は、こちらの URL を参照して下さい。  
http://myrica.estable.jp/

## Q&A
Q. これは名前を変えるほどの変更ですか？  
A. "Myrica" が予約フォント名でないという確証がなかったため変えました。（Myrica 自身のライセンスファイルが存在しないため）  
  
Q. "Juglans" は予約フォント名ですか？  
A. いいえ。本フォントの派生フォントは、 "Juglans" というフォント名を自由に利用可能です。  
