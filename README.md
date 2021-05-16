# プログラミング用フォント Juglans
Juglans （ユグランス）は、 Inconsolata と源真ゴシックの合成フォントです。  
[プログラミング用フォント Myrica](https://github.com/tomokuni/Myrica) の改変版として、Myrica のスクリプトおよびフォントを利用しています。  

## Myrica との違い
- 合成元フォントからの字形変更をプログラミングに必要な最小限に留めました。
- Inconsolata のバージョンを3.001（Google Fonts 版）に更新しました。
- 源真ゴシックを Light から Normal に変更しました。
- Mgen+ 版を削除しました。
- Proportional フォントおよび Narrow フォントを削除しました。
- ビルド環境を Linux (Arch Linux を想定) に変更しました。
- 生成スクリプトを Python 3 に変更しました。
- 7z 圧縮を xz 圧縮に変更しました。

## 合成元フォントからの字形の変更点
U+0030 0 : DIGIT ZERO (Inconsolata 内の別グリフ)  
U+002A * : ASTERISK (Myrica ReplaceParts)  
U+2013 – : EN DASH (Myrica ReplaceParts)  
U+2014 — : EM DASH (Myrica ReplaceParts)  
U+301C 〜 : WAVE DASH (Myrica ReplaceParts)  
![字形の変更点](https://user-images.githubusercontent.com/31642509/118390760-c357d000-b66b-11eb-9253-bdf8edd44100.png)

## サンプル
### Notepad++, 14pt
![notepad++](https://user-images.githubusercontent.com/31642509/115114365-dc685500-9fc9-11eb-9651-38ecf0431f8a.png)
### Windows Terminal, 14pt
![windowsterminal](https://user-images.githubusercontent.com/31642509/115113712-99f14900-9fc6-11eb-8e02-b98e60b686dc.png)


## ライセンス
Juglans フォント、生成スクリプト共に SIL OPEN FONT LICENSE Version 1.1 の下で利用できます。  
また、"Juglans" は予約フォント名ではなく、本フォントの派生フォントは、 "Juglans" というフォント名を自由に利用可能です。  

## 利用フォント
Myrica (生成スクリプトおよび ReplaceParts の一部)  
Inconsolata (ASCII 文字)  
源真ゴシック (ASCII 文字以外)  

## 利用フォントのライセンス
サードパーティーライセンス.txt を参照してください。
