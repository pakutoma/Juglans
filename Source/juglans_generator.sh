#!/bin/sh
echo フォント生成
mkdir ../Work
echo Regularフォントの生成
fontforge -lang=py -script juglans_generator.py
echo Boldフォントの生成
fontforge -lang=py -script juglans_generator.py bold

echo xAvgCharWidthの書き換え
# Regular
ttx -f -t 'OS/2' -d ../Work ../Work/Juglans-Regular.ttf
ttx -f -t 'OS/2' -d ../Work ../SourceTTF/Inconsolata-Regular.ttf
xAvgCharWidth=$(grep xAvgCharWidth ../Work/Inconsolata-Regular.ttx | sed -e 's/.*value="\([0-9]*\)".*/\1/')
sed -i -e "s/^\(.*<xAvgCharWidth value=\"\)[0-9]*\(.*\)/\1$xAvgCharWidth\2/" ../Work/Juglans-Regular.ttx
ttx -f -m ../Work/Juglans-Regular.ttf ../Work/Juglans-Regular.ttx
# Bold
ttx -f -t 'OS/2' -d ../Work ../Work/Juglans-Bold.ttf
ttx -f -t 'OS/2' -d ../Work ../SourceTTF/Inconsolata-Bold.ttf
xAvgCharWidth=$(grep xAvgCharWidth ../Work/Inconsolata-Bold.ttx | sed -e 's/.*value="\([0-9]*\)".*/\1/')
sed -i -e "s/^\(.*<xAvgCharWidth value=\"\)[0-9]*\(.*\)/\1$xAvgCharWidth\2/" ../Work/Juglans-Bold.ttx
ttx -f -m ../Work/Juglans-Bold.ttf ../Work/Juglans-Bold.ttx
# productにコピー
cp ../Work/Juglans-Regular.ttf ../product/Juglans-Regular.ttf
cp ../Work/Juglans-Bold.ttf ../product/Juglans-Bold.ttf

echo 圧縮ファイルの作成
tar -Jcf ../product/Juglans.tar.xz -C ../product/ Juglans-Regular.ttf Juglans-Bold.ttf -C ../ LICENSE README.md サードパーティーライセンス.txt
zip ../product/Juglans.zip -j ../product/Juglans-Regular.ttf ../product/Juglans-Bold.ttf ../LICENSE ../README.md ../サードパーティーライセンス.txt
