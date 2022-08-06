#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Author: Tomokuni SEKIYA
# Modified by: pakutoma
#
# This script is for generating ``juglans'' font


# version
newfont_version = "2.004.20220807"
newfont_sfntRevision = 0x00010000

# set font name
newfont_name = (f"../Work/Juglans-{sys.argv[2]}-for-{sys.argv[1]}.ttf", "Juglans-Regular", "Juglans", "Juglans Regular")
newfont_name_bold = (f"../Work/Juglans-{sys.argv[2]}-for-{sys.argv[1]}.ttf", "Juglans-Bold", "Juglans", "Juglans Bold")
# source file
srcfont_incosolata = "../SourceTTF/Inconsolata-Regular.ttf"
srcfont_incosolata_bold = "../SourceTTF/Inconsolata-Bold.ttf"
srcfont_GenShin = "../SourceTTF/GenShinGothic-Monospace-Normal.ttf"
srcfont_GenShin_bold = "../SourceTTF/GenShinGothic-Monospace-Bold.ttf"
srcfont_dejavu = "../SourceTTF/DejaVuLGCSansMono.ttf"
srcfont_dejavu_bold = "../SourceTTF/DejaVuLGCSansMono-Bold.ttf"
srcfont_anonpro = "../SourceTTF/AnonymousProMinus.ttf"
srcfont_anonpro_bold = "../SourceTTF/AnonymousProMinusB.ttf"
srcfont_nerdfonts = "../SourceTTF/NerdFonts-without-pomicon-Regular.ttf"
srcfont_powerline = "../SourceTTF/Powerline-Mod.ttf"


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

# weight
newfont_weight = "Regular"
newfont_weight_bold = "Bold"

# define
generate_flags = ('opentype', 'PfEd-lookups', 'TeX-table')
panose_base = (2, 11, 6, 9, 2, 2, 3, 2, 2, 7)
panose_base_bold = (2, 11, 8, 9, 2, 2, 3, 2, 2, 7)

########################################
# setting
########################################

import os
import sys

import fontforge
import psMat
import unicodedata

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

if sys.argv[1] == "WindowsTerminal":
    powerline_y = -210
    powerline_h = 1.09
elif sys.argv[1] == "iTerm2":
    powerline_y = -175
    powerline_h = 1.065
else:
    powerline_y = -200
    powerline_y = 1.0

print(f"Generate Juglans {sys.argv[2]} for {sys.argv[1]}")
if sys.argv[2] == "Bold":
    newfont_name = newfont_name_bold
    newfont_weight = newfont_weight_bold
    srcfont_incosolata = srcfont_incosolata_bold
    srcfont_GenShin = srcfont_GenShin_bold
    srcfont_anonpro = srcfont_anonpro_bold
    panose_base = panose_base_bold

if os.path.exists(srcfont_incosolata) == False:
    print("Error: " + srcfont_incosolata + " not found")
    sys.exit(1)
if os.path.exists(srcfont_GenShin) == False:
    print("Error: " + srcfont_GenShin + " not found")
    sys.exit(1)

########################################
# define function
########################################


class Matrix:
    def __init__(self):
        self.ps_mat = None

    def move(self, x, y):
        mat = psMat.translate(x, y)
        self._compose(mat)
        return self
    
    def scale(self, x, y=None):
        if y is None:
            y = x
        mat = psMat.scale(x, y)
        self._compose(mat)
        return self
    
    def to_ff(self):
        return self.ps_mat
    
    def _compose(self, mat):
        if self.ps_mat is None:
            self.ps_mat = mat
            return
        self.ps_mat = psMat.compose(self.ps_mat, mat)
    
    

def composeChain(mat):
    return psMat.compose(self, chain)


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
    font.weight = newfont_weight
    font.copyright = "Copyright (c) 2021 pakutoma (Juglans)\n"
    font.copyright += "Copyright (c) 2006 The Inconsolata Project Authors (Inconsolata)\n"
    font.copyright += "Copyright (c) 2014 MM (GenShinGothic)\n"
    font.copyright += "Copyright (c) 2014 Adobe Systems Incorporated. (NotoSansJP)\n"
    font.copyright += "Copyright (c) Bitstream. DejaVu changes are in public domain. Glyphs imported from Arev fonts are (c) Tavmjong Bah. (DejaVu LGC)\n"
    font.copyright += "Copyright (c) 2009, Mark Simonson (http://www.ms-studio.com, mark@marksimonson.com) (Anonymous Pro Minus)\n"
    font.copyright += "Licenses:\n"
    font.copyright += "SIL Open Font License Version 1.1 "
    font.copyright += "(http://scripts.sil.org/ofl)\n"
    font.version = newfont_version
    font.sfntRevision = newfont_sfntRevision
    font.sfnt_names = (('English (US)', 'UniqueID', fontInfo[2]),)

    font.hasvmetrics = True
    font.head_optimized_for_cleartype = True

    font.os2_panose = panose_base
    font.os2_vendor = "    "
    font.os2_version = 4

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
# modified Inconsolata
########################################

print("Open " + srcfont_incosolata)
fIn = fontforge.open(srcfont_incosolata)

# modify
print("modify")

# 0 with slash -> 0 with dot (Inconsolata's unused glyph)
copyAndPaste(fIn, "zero.zero", fIn, 0x0030)

print("remove Glyphs")
fIn.selection.none()
# アスタリスクとチルダのグリフを削除
for glyph in fIn.glyphs():
    if glyph.unicode in (0x002a, 0x007e):
        fIn.selection.select(("more",), glyph.glyphname)
fIn.clear()

# modify em
# if change inconsolata's EM, TrueType hints break.
fIn.em = newfont_em
fIn.ascent = newfont_ascent
fIn.descent = newfont_descent

fIn.selection.all()
fIn.round()

fIn.generate("../Work/modIncosolata.ttf", '', generate_flags)
fIn.close()

########################################
# modify Anonymous Pro Minus
########################################

print("Open " + srcfont_anonpro)
anon_font = fontforge.open(srcfont_anonpro)

# modify
print("modify")

print("remove Glyphs")
anon_font.selection.none()
# アスタリスクとチルダ以外のグリフを削除
for glyph in anon_font.glyphs():
    if glyph.unicode not in (0x002a, 0x007e):
        anon_font.selection.select(("more",), glyph.glyphname)
anon_font.clear()

# modify em
anon_font.em = newfont_em
anon_font.ascent = newfont_ascent
anon_font.descent = newfont_descent

# scale down and move
for glyph in anon_font.glyphs():
    glyph.transform(psMat.translate(26, 90))
    glyph.width = 500

anon_font.selection.all()
anon_font.round()

anon_font.generate("../Work/modAnon.ttf", '', generate_flags)
anon_font.close()

########################################
# modify Powerline
########################################

print("Open " + srcfont_powerline)
powerline = fontforge.open(srcfont_powerline)

# modify
print("modify")

# modify em
powerline.em = newfont_em
powerline.ascent = newfont_ascent
powerline.descent = newfont_descent

# move
for glyph in powerline.glyphs():
    mat = (Matrix()
        .move(0, 200)
        .scale(1.0, powerline_h)
        .move(0, powerline_y)
        .to_ff())
    glyph.transform(mat)

powerline.selection.all()
powerline.round()

powerline.generate("../Work/modPower.ttf", '', generate_flags)
powerline.close()

########################################
# modify Nerd Fonts
########################################

print("Open " + srcfont_nerdfonts)
nerd_font = fontforge.open(srcfont_nerdfonts)

# modify
print("modify")

# modify em
nerd_font.em = newfont_em
nerd_font.ascent = newfont_ascent
nerd_font.descent = newfont_descent

# move
for glyph in nerd_font.glyphs():
    glyph.transform(psMat.translate(0, 60))

nerd_font.selection.all()
nerd_font.round()

nerd_font.generate("../Work/modNerd.ttf", '', generate_flags)
nerd_font.close()

########################################
# modify DejaVu LGC
########################################

print("Open " + srcfont_dejavu)
de_font = fontforge.open(srcfont_dejavu)

# modify
print("modify")

print("remove Glyphs")
de_font.selection.none()
# EastAsianWidthで全角（WまたはF）のグリフを削除
for glyph in de_font.glyphs():
    if glyph.unicode > 0 and unicodedata.east_asian_width(chr(glyph.unicode)) in ("W", "F"):
        de_font.selection.select(("more",), glyph.glyphname)
de_font.clear()

# modify em
de_font.em = newfont_em
de_font.ascent = newfont_ascent
de_font.descent = newfont_descent

# scale down
for glyph in de_font.glyphs():
    glyph.transform(psMat.scale(0.83))
    glyph.width = 500

de_font.selection.all()
de_font.round()

de_font.generate("../Work/modDejaVu.ttf", '', generate_flags)
de_font.close()

########################################
# modified GenShin
########################################

print("Open " + srcfont_GenShin)
fGs = fontforge.open(srcfont_GenShin)

# modify
print("modify")

# modify em
fGs.em = newfont_em
fGs.ascent = newfont_ascent
fGs.descent = newfont_descent

# scale down
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

########################################
# create Juglans
########################################
ju_font = fontforge.open("../Work/modIncosolata.ttf")

print("Build " + newfont_name[0])

# pre-process
setFontProp(ju_font, newfont_name)

# merge Anonymous Pro
print("merge Anonymous Pro")
ju_font.mergeFonts("../Work/modAnon.ttf")

# merge Powerline
print("merge Powerline")
ju_font.mergeFonts("../Work/modPower.ttf")

# merge Nerd Fonts
print("merge Nerd Fonts")
ju_font.mergeFonts("../Work/modNerd.ttf")

# merge DejaVu
print("merge DejaVu")
ju_font.mergeFonts("../Work/modDejaVu.ttf")

# merge GenShin
print("merge GenShin")
# マージ
ju_font.mergeFonts("../Work/modGenShin.ttf")

ju_font.os2_unicoderanges = os2_unicoderanges
ju_font.os2_codepages = os2_codepages

# post-process
ju_font.selection.all()
ju_font.round()

# generate
print("Generate " + newfont_name[0])
ju_font.generate(newfont_name[0], '', generate_flags)

ju_font.close()
