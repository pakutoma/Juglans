#!/bin/sh
echo フォント生成
mkdir -p ../Work ../product

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
		python3 juglans_generator.py $terminal $weight

		src_ttf="../Work/Juglans-${weight}-for-${terminal}.ttf"
		dst_ttf="../product/Juglans-${weight}-for-${terminal}.ttf"

		# productにコピー
		cp $src_ttf $dst_ttf
	done
done

echo 圧縮ファイルの作成
find ../product -name '*.ttf' -printf "%f\0" | xargs -0 tar -Jcf ../product/Juglans.tar.xz -C ../ LICENSE README.md サードパーティーライセンス.txt -C product
zip -q ../product/Juglans.zip -j ../product/*.ttf ../LICENSE ../README.md ../サードパーティーライセンス.txt
echo 完了
