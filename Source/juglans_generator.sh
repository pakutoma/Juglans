#!/bin/sh
echo フォント生成
mkdir ../Work
fontforge -lang=py -script juglans_generator.py

echo xAvgCharWidthの書き換え
ttx -f -t 'OS/2' -d ../Work ../Work/Juglans.ttf
ttx -f -t 'OS/2' -d ../Work ../SourceTTF/Inconsolata-Regular.ttf
xAvgCharWidth=$(grep xAvgCharWidth ../Work/Inconsolata-Regular.ttx | sed -e 's/.*value="\([0-9]*\)".*/\1/')
sed -i -e "s/^\(.*<xAvgCharWidth value=\"\)[0-9]*\(.*\)/\1$xAvgCharWidth\2/" ../Work/Juglans.ttx
ttx -f -m ../Work/Juglans.ttf ../Work/Juglans.ttx
cp ../Work/Juglans.ttf ../product/Juglans.ttf

echo 圧縮ファイルの作成
tar -Jcf ../product/Juglans.tar.xz -C ../product/ Juglans.ttf -C ../ LICENSE README.md サードパーティーライセンス.txt
zip ../product/Juglans.zip -j ../product/Juglans.ttf ../LICENSE ../README.md ../サードパーティーライセンス.txt
