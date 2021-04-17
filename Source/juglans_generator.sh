#!/bin/sh
echo フォント生成
mkdir ../Work
fontforge -lang=py -script juglans_generator.py

echo xAvgCharWidthの書き換え
ttx -f -t 'OS/2' -d ../Work ../Work/JuglansM.ttf
ttx -f -t 'OS/2' -d ../Work ../SourceTTF/Inconsolata-Regular.ttf
xAvgCharWidth=$(grep xAvgCharWidth ../Work/Inconsolata-Regular.ttx | sed -e 's/.*value="\([0-9]*\)".*/\1/')
sed -i -e "s/^\(.*<xAvgCharWidth value=\"\)[0-9]*\(.*\)/\1$xAvgCharWidth\2/" ../Work/JuglansM.ttx
ttx -f -m ../Work/JuglansM.ttf ../Work/JuglansM.ttx

echo TTCの作成
../unitettc64 ../product/Juglans.TTC ../Work/JuglansM.ttf ../Work/JuglansP.ttf ../Work/JuglansN.ttf

echo 圧縮ファイルの作成
tar -Jcf ../product/Juglans.tar.xz -C ../product/ Juglans.TTC -C ../ LICENSE README.md サードパーティーライセンス.txt
zip ../product/Juglans.zip -j ../product/Juglans.TTC ../LICENSE ../README.md ../サードパーティーライセンス.txt
