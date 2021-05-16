#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Author: Tomokuni SEKIYA
# Modified by: pakutoma
#
# This script is for generating ``juglans'' font
#
# * Inconsolata  : Inconsolata-Regular.ttf           : 1.016 (Google Fonts)
# * 源真ゴシック : GenShinGothic-Monospace-Light.ttf : 1.002.20150607
#
# 以下のように構成されます。
# ・英数字記号は、Inconsolata
# ・他の文字は、源真ゴシック
# ・一部の文字を視認性向上のために migu の特徴を取込み
#     ～〜（FULLWIDTH TILDE・WAVE DASH）の区別

# version
newfont_version = "2.000.20210417"
newfont_sfntRevision = 0x00010000

# set font name
newfont_name = ("../Work/Juglans.ttf", "Juglans", "Juglans", "Juglans")
# source file
srcfontIncosolata = "../SourceTTF/Inconsolata-Regular.ttf"
srcfontGenShin = "../SourceTTF/GenShinGothic-Monospace-Normal.ttf"
srcfontMyricaReplaceParts = "../SourceTTF/myrica_ReplaceParts.ttf"

# out file
outfontNoHint = "../Work/Juglans_NoHint.ttf"

# flag
scalingDownIfWidth_flag = True

# set ascent and descent (line width parameters)
newfont_ascent = 800
newfont_descent = 200
newfont_em = newfont_ascent + newfont_descent

newfont_winAscent = 1004
newfont_winDescent = 454
newfont_typoAscent = 859
newfont_typoDescent = -190
newfont_typoLinegap = 0
newfont_hheaAscent = newfont_typoAscent
newfont_hheaDescent = -newfont_typoDescent
newfont_hheaLinegap = 0

# define
generate_flags = ('opentype', 'PfEd-lookups', 'TeX-table')
panoseBase = (2, 11, 5, 9, 2, 2, 3, 2, 2, 7)

########################################
# setting
########################################

import os
import sys
import fontforge
import psMat

# 縦書きのために指定する
fontforge.setPrefs('CoverageFormatsAllowed', 1)
# 大変更時に命令を消去 0:オフ 1:オン
fontforge.setPrefs('ClearInstrsBigChanges', 0)
# TrueType命令をコピー 0:オフ 1:オン
fontforge.setPrefs('CopyTTFInstrs', 1)

########################################
# pre-process
########################################

print("Juglans generator " + newfont_version)
print("This script is for generating 'Juglans' font")
if os.path.exists(srcfontIncosolata) == False:
    print("Error: " + srcfontIncosolata + " not found")
    sys.exit(1)
if os.path.exists(srcfontMyricaReplaceParts) == False:
    print("Error: " + srcfontMyricaReplaceParts + " not found")
    sys.exit(1)
if os.path.exists(srcfontGenShin) == False:
    print("Error: " + srcfontGenShin + " not found")
    sys.exit(1)


########################################
# define function
########################################
def matRescale(origin_x, origin_y, scale_x, scale_y):
    return psMat.compose(
        psMat.translate(-origin_x, -origin_y), psMat.compose(
            psMat.scale(scale_x, scale_y),
            psMat.translate(origin_x, origin_y)))


def matMove(move_x, move_y):
    return psMat.translate(move_x, move_y)


def rng(start, end):
    return range(start, end + 1)


def flatten(iterable):
    it = iter(iterable)
    for e in it:
        if isinstance(e, (list, tuple, range)):
            for f in flatten(e):
                yield f
        else:
            yield e


def select(font, *codes):
    font.selection.none()
    selectMore(font, codes)


def selectMore(font, *codes):
    flat = flatten(codes)
    for c in flat:
        if isinstance(c, (str,)) and not c.isascii():
            font.selection.select(("more",), ord(c))
        else:
            font.selection.select(("more",), c)


def selectLess(font, *codes):
    flat = flatten(codes)
    for c in flat:
        if isinstance(c, (str,)) and not c.isascii():
            font.selection.select(("more",), ord(c))
        else:
            font.selection.select(("more",), c)


def selectExistAll(font):
    font.selection.none()
    for glyphName in font:
        if font[glyphName].isWorthOutputting() == True:
            font.selection.select(("more",), glyphName)


def copyAndPaste(srcFont, srcCodes, dstFont, dstCodes):
    select(srcFont, srcCodes)
    srcFont.copy()
    select(dstFont, dstCodes)
    dstFont.paste()


def copyAndPasteInto(srcFont, srcCodes, dstFont, dstCodes, pos_x, pos_y):
    select(srcFont, srcCodes)
    srcFont.copy()
    select(dstFont, dstCodes)
    dstFont.transform(matMove(-pos_x, -pos_y))
    dstFont.pasteInto()
    dstFont.transform(matMove(pos_x, pos_y))


def scalingDownIfWidth(font, scaleX, scaleY):
    for glyph in font.selection.byGlyphs:
        width = glyph.width
        glyph.transform(matRescale(width / 2, 0, scaleX, scaleY))
        glyph.width = width


def centerInWidth(font):
    for glyph in font.selection.byGlyphs:
        w = glyph.width
        wc = w / 2
        bb = glyph.boundingBox()
        bc = (bb[0] + bb[2]) / 2
        glyph.transform(matMove(wc - bc, 0))
        glyph.width = w


def setWidth(font, width):
    for glyph in font.selection.byGlyphs:
        glyph.width = width


def setAutoWidthGlyph(glyph, separation):
    bb = glyph.boundingBox()
    bc = (bb[0] + bb[2]) / 2
    nw = (bb[2] - bb[0]) + separation * 2
    if glyph.width > nw:
        wc = nw / 2
        glyph.transform(matMove(wc - bc, 0))
        glyph.width = nw


def autoHintAndInstr(font, *codes):
    removeHintAndInstr(font, codes)
    font.autoHint()
    font.autoInstr()


def removeHintAndInstr(font, *codes):
    select(font, codes)
    for glyph in font.selection.byGlyphs:
        if glyph.isWorthOutputting() == True:
            glyph.manualHints = False
            glyph.ttinstrs = ()
            glyph.dhints = ()
            glyph.hhints = ()
            glyph.vhints = ()


def copyTti(srcFont, dstFont):
    for glyphName in dstFont:
        dstFont.setTableData('fpgm', srcFont.getTableData('fpgm'))
        dstFont.setTableData('prep', srcFont.getTableData('prep'))
        dstFont.setTableData('cvt', srcFont.getTableData('cvt'))
        dstFont.setTableData('maxp', srcFont.getTableData('maxp'))
        copyTtiByGlyphName(srcFont, dstFont, glyphName)


def copyTtiByGlyphName(srcFont, dstFont, glyphName):
    try:
        dstGlyph = dstFont[glyphName]
        srcGlyph = srcFont[glyphName]
        if srcGlyph.isWorthOutputting() == True and dstGlyph.isWorthOutputting() == True:
            dstGlyph.manualHints = True
            dstGlyph.ttinstrs = srcFont[glyphName].ttinstrs
            dstGlyph.dhints = srcFont[glyphName].dhints
            dstGlyph.hhints = srcFont[glyphName].hhints
            dstGlyph.vhints = srcFont[glyphName].vhints
    except TypeError:
        pass


def setFontProp(font, fontInfo):
    font.fontname = fontInfo[1]
    font.familyname = fontInfo[2]
    font.fullname = fontInfo[3]
    font.weight = "Book"
    font.copyright = "Copyright (c) 2021 pakutoma (Juglans)\n"
    font.copyright += "Copyright (c) 2014 Tomokuni SEKIYA (Myrica)\n"
    font.copyright += "Copyright (c) 2006 The Inconsolata Project Authors (Inconsolata)\n"
    font.copyright += "Copyright (c) 2014 MM (GenShinGothic)\n"
    font.copyright += "Copyright (c) 2014 Adobe Systems Incorporated. (NotoSansJP)\n"
    font.copyright += "Licenses:\n"
    font.copyright += "SIL Open Font License Version 1.1 "
    font.copyright += "(http://scripts.sil.org/ofl)\n"
    font.version = newfont_version
    font.sfntRevision = newfont_sfntRevision
    font.sfnt_names = (('English (US)', 'UniqueID', fontInfo[2]),)

    font.hasvmetrics = True
    font.head_optimized_for_cleartype = True

    font.os2_panose = panoseBase
    font.os2_vendor = "ES"
    font.os2_version = 1

    font.os2_winascent = newfont_winAscent
    font.os2_winascent_add = 0
    font.os2_windescent = newfont_winDescent
    font.os2_windescent_add = 0
    font.os2_typoascent = newfont_typoAscent
    font.os2_typoascent_add = 0
    font.os2_typodescent = newfont_typoDescent
    font.os2_typodescent_add = 0
    font.os2_typolinegap = newfont_typoLinegap
    font.hhea_ascent = newfont_hheaAscent
    font.hhea_ascent_add = 0
    font.hhea_descent = newfont_hheaDescent
    font.hhea_descent_add = 0
    font.hhea_linegap = newfont_hheaLinegap

    font.upos = 45


charASCII = rng(0x0021, 0x007E)
charZHKana = list(u"ぁあぃいぅうぇえぉおかがきぎくぐけげこごさざしじすずせぜそぞただちぢっつづてでとどなにぬねのはばぱひびぴふぶぷへべぺほぼぽまみむめもゃやゅゆょよらりるれろゎわゐゑをん"),
charZKKana = list(u"ァアィイゥウェエォオカガキギクグケゲコゴサザシジスズセゼソゾタダチヂッツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポマミムメモャヤュユョヨラリルレロヮワヰヱヲンヴヵヶ"),
charHKKana = list(u"､｡･ｰﾞﾟ｢｣ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜｦﾝｧｨｩｪｫｬｭｮｯ")
charZEisu = list(u"０１２３４５６７８９ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ")

########################################
# modified ReplaceParts
########################################

print()
print("Open " + srcfontMyricaReplaceParts)
fRp = fontforge.open(srcfontMyricaReplaceParts)

# modify em
fRp.em = newfont_em
fRp.ascent = newfont_ascent
fRp.descent = newfont_descent

# post-process
fRp.selection.all()
fRp.round()

########################################
# modified Inconsolata
########################################

print()
print("Open " + srcfontIncosolata)
fIn = fontforge.open(srcfontIncosolata)

# modify
print("modify")

# D -> D of Eth (D with cross-bar)
copyAndPaste(fIn, 0x0110, fIn, 0x0044)

# 0 with slash -> 0 with dot (Inconsolata's unused glyph)
copyAndPaste(fIn, "zero.zero", fIn, 0x0030)

# modify em
# if change inconsolata's EM, TrueType hints break.
fIn.em = newfont_em
fIn.ascent = newfont_ascent
fIn.descent = newfont_descent

# 文字の置換え
print("merge ReplaceParts")
for glyph in fRp.glyphs():
    if glyph.unicode in (0x002a,): # ASTERISK
        select(fRp, glyph.glyphname)
        fRp.copy()
        select(fIn, glyph.glyphname)
        fIn.paste()

# 必要文字(半角英数字記号)だけを残して削除
select(fIn, rng(0x0021, 0x007E))
selectMore(fIn, 0x00B7) # MIDDLE DOT
selectMore(fIn, 0x0307) # CONBINING DOT ABOVE (for i and j)
fIn.selection.invert()
fIn.clear()

fIn.selection.all()
fIn.round()

fIn.generate("../Work/modIncosolata.ttf", '', generate_flags)
fIn.close()

########################################
# modified GenShin
########################################

print()
print("Open " + srcfontGenShin)
fGs = fontforge.open(srcfontGenShin)

# modify
print("modify")

# modify em
fGs.em = newfont_em
fGs.ascent = newfont_ascent
fGs.descent = newfont_descent

# 文字の置換え
print("merge ReplaceParts")
for glyph in fRp.glyphs():
    if glyph.unicode in (0x2013, 0x2014, 0x301c): # EN DASH, EM DASH, WAVE DASH
        select(fRp, glyph.glyphname)
        fRp.copy()
        select(fGs, glyph.glyphname)
        fGs.paste()

# 半角英数字記号を削除
select(fGs, rng(0x0021, 0x007E))
fGs.clear()

# scaling down
if scalingDownIfWidth_flag == True:
    print("While scaling, wait a little...")
    # 0.91はRictyに準じた。
    selectExistAll(fGs)
    selectLess(fGs, (charASCII, charHKKana, charZHKana, charZKKana, charZEisu))
    scalingDownIfWidth(fGs, 0.91, 0.91)
    # 平仮名/片仮名のサイズを調整
    select(fGs, (charZHKana, charZKKana))
    scalingDownIfWidth(fGs, 0.97, 0.97)
    # 全角英数の高さを調整 (半角英数の高さに合わせる)
    select(fGs, charZEisu)
    scalingDownIfWidth(fGs, 0.91, 0.86)

for l in fGs.gsub_lookups:
    fGs.removeLookup(l)
for l in fGs.gpos_lookups:
    fGs.removeLookup(l)

# autoHintAndInstr(fGs, (charZHKana, charZKKana, charHKKana, charZEisu))

fGs.generate("../Work/modGenShin.ttf", '', generate_flags)
os2_unicoderanges = fGs.os2_unicoderanges
os2_codepages = fGs.os2_codepages

fGs.close()
fRp.close()

########################################
# create Juglans
########################################
fMm = fontforge.open("../Work/modIncosolata.ttf")

print()
print("Build " + newfont_name[0])

# pre-process
setFontProp(fMm, newfont_name)

# merge GenShin
print("merge GenShin")
# マージ
fMm.mergeFonts("../Work/modGenShin.ttf")
fMm.os2_unicoderanges = os2_unicoderanges
fMm.os2_codepages = os2_codepages

# post-process
fMm.selection.all()
fMm.round()

# generate
print("Generate " + newfont_name[0])
fMm.generate(newfont_name[0], '', generate_flags)

fMm.close()