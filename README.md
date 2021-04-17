# プログラミング用フォント Juglans
Juglans （ユグランス）は、Inconsolataと源真ゴシックの合成フォントです。  
[プログラミング用フォント Myrica](https://github.com/tomokuni/Myrica) の改変版として、Myrica のスクリプトおよびフォントを利用しています。  

## Myrica との違い
- 合成元フォントからの字形変更をプログラミングに必要な最小限に留めました。
- Inconsolataのバージョンを3.001（Google Fonts版）に更新しました。
- 源真ゴシックをLightからNormalに変更しました。
- Mgen+ 版を削除しました。
- ビルド環境を Linux (Arch Linux を想定) に変更しました。
- 生成スクリプトを Python 3 に変更しました。
- 7z 圧縮を xz 圧縮に変更しました。

## 合成元フォントからの字形の変更点
U+0030 0 : DIGIT ZERO (Inconsolata内の別グリフ)  
U+0044 D : LATIN CAPITAL LETTER D (Inconsolata内の別グリフ)  
U+002A * : ASTERISK (Myrica ReplaceParts)  
U+2013 – : EN DASH (Myrica ReplaceParts)  
U+2014 — : EM DASH (Myrica ReplaceParts)  
U+301C 〜 : WAVE DASH (Myrica ReplaceParts)  
![字形の変更点](https://user-images.githubusercontent.com/31642509/115113304-9e1c6700-9fc4-11eb-8ed7-911cb8059bc0.png)

## サンプル
### Notepad++, 14pt
![notepad++](https://user-images.githubusercontent.com/31642509/115114365-dc685500-9fc9-11eb-9651-38ecf0431f8a.png)
### Windows Terminal, 14pt
![windowsterminal](https://user-images.githubusercontent.com/31642509/115113712-99f14900-9fc6-11eb-8e02-b98e60b686dc.png)


## ライセンス
Juglans フォント、生成スクリプト共に SIL OPEN FONT LICENSE Version 1.1 の元で利用できます。  
また、"Juglans" は予約フォント名ではなく、本フォントの派生フォントは、 "Juglans" というフォント名を自由に利用可能です。  

## 利用フォント
Myrica (生成スクリプトおよび ReplaceParts の一部)  
Inconsolata (ASCII 文字)  
源真ゴシック (ASCII 文字以外)  

## 利用フォントのライセンス
サードパーティーライセンス.txtを参照してください。
