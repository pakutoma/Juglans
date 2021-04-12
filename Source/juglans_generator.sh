#!/bin/sh
mkdir ../Work
fontforge -lang=py -script juglans_generator.py

echo TTCの作成
../unitettc64 ../product/Juglans.TTC ../Work/JuglansM.ttf ../Work/JuglansP.ttf ../Work/JuglansN.ttf

echo 圧縮ファイルの作成
tar -Jcf ../product/Juglans.tar.xz -C ../product/ Juglans.TTC -C ../ LICENSE README.md サードパーティーライセンス.txt
zip ../product/Juglans.zip -j ../product/Juglans.TTC ../LICENSE ../README.md ../サードパーティーライセンス.txt
