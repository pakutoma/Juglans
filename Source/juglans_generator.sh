#!/bin/sh
echo フォント生成
mkdir ../Work

terminals=(
	"WindowsTerminal"
	"iTerm2"
)

weights=(
	"Regular"
	"Bold"
)

for terminal in "${terminals[@]}" ; do
	for weight in "${weights[@]}" ; do
		echo "${terminal} ${weight} フォント生成"
		fontforge -lang=py -script juglans_generator.py $terminal $weight 2> /dev/null

		src_ttf="../SourceTTF/Inconsolata-${weight}.ttf"
		work_ttf="../Work/Juglans-${weight}-for-${terminal}.ttf"
		src_ttx="../Work/Inconsolata-${weight}.ttx"
		work_ttx="../Work/Juglans-${weight}-for-${terminal}.ttx"
		dst_ttf="../product/Juglans-${weight}-for-${terminal}.ttf"
		
		echo xAvgCharWidthの書き換え
		ttx -f -t 'OS/2' -d ../Work $work_ttf
		ttx -f -t 'OS/2' -d ../Work $src_ttf
		xAvgCharWidth=$(grep xAvgCharWidth $src_ttx | sed -e 's/.*value="\([0-9]*\)".*/\1/')
		sed -i -e "s/^\(.*<xAvgCharWidth value=\"\)[0-9]*\(.*\)/\1$xAvgCharWidth\2/" $work_ttx
		ttx -f -m $work_ttf $work_ttx

		# productにコピー
		cp $work_ttf $dst_ttf
	done
done

echo 圧縮ファイルの作成
find ../product -name '*.ttf' -printf "%f\0" | xargs -0 tar -Jcf ../product/Juglans.tar.xz -C ../ LICENSE README.md サードパーティーライセンス.txt -C product
zip -q ../product/Juglans.zip -j ../product/*.ttf ../LICENSE ../README.md ../サードパーティーライセンス.txt
