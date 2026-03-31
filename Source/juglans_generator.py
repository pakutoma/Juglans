#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# Author: Tomokuni SEKIYA
# Modified by: pakutoma
#
# This script is for generating "Juglans" font
# Rewritten to use fonttools instead of FontForge

import copy
import os
import sys
import unicodedata

from fontTools.ttLib import TTFont
from fontTools.misc.transform import Transform
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib.tables._c_m_a_p import cmap_format_4, cmap_format_12

########################################
# configuration
########################################

newfont_version = "2.004.20220807"
newfont_sfntRevision = 1.0

# source files
srcfont_inconsolata = "../SourceTTF/Inconsolata-Regular.ttf"
srcfont_inconsolata_bold = "../SourceTTF/Inconsolata-Bold.ttf"
srcfont_genshin = "../SourceTTF/GenShinGothic-Monospace-Normal.ttf"
srcfont_genshin_bold = "../SourceTTF/GenShinGothic-Monospace-Bold.ttf"
srcfont_dejavu = "../SourceTTF/DejaVuLGCSansMono.ttf"
srcfont_dejavu_bold = "../SourceTTF/DejaVuLGCSansMono-Bold.ttf"
srcfont_anonpro = "../SourceTTF/AnonymousProMinus.ttf"
srcfont_anonpro_bold = "../SourceTTF/AnonymousProMinusB.ttf"
srcfont_nerdfonts = "../SourceTTF/InconsolataNerdFont-Regular.ttf"
srcfont_nerdfonts_bold = "../SourceTTF/InconsolataNerdFont-Bold.ttf"
srcfont_powerline = "../SourceTTF/Powerline-Mod.ttf"

# metrics
newfont_em = 1000
newfont_ascent = 800
newfont_descent = 200

newfont_winAscent = 1004
newfont_winDescent = 454
newfont_typoAscent = 859
newfont_typoDescent = -190
newfont_typoLinegap = 0
newfont_hheaAscent = newfont_typoAscent
newfont_hheaDescent = -newfont_typoDescent
newfont_hheaLinegap = 0

# panose
panose_regular = (2, 11, 6, 9, 2, 2, 3, 2, 2, 7)
panose_bold = (2, 11, 8, 9, 2, 2, 3, 2, 2, 7)

# character sets for GenShin scaling
charASCII = list(range(0x0021, 0x007F))
charZHKana = [ord(c) for c in "ぁあぃいぅうぇえぉおかがきぎくぐけげこごさざしじすずせぜそぞただちぢっつづてでとどなにぬねのはばぱひびぴふぶぷへべぺほぼぽまみむめもゃやゅゆょよらりるれろゎわゐゑをん"]
charZKKana = [ord(c) for c in "ァアィイゥウェエォオカガキギクグケゲコゴサザシジスズセゼソゾタダチヂッツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポマミムメモャヤュユョヨラリルレロヮワヰヱヲンヴヵヶ"]
charHKKana = [ord(c) for c in "､｡･ｰﾞﾟ｢｣ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜｦﾝｧｨｩｪｫｬｭｮｯ"]
charZEisu = [ord(c) for c in "０１２３４５６７８９ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ"]

########################################
# utility functions
########################################


def scale_font_em(font, new_em):
    """Change font EM and scale all glyph coordinates proportionally."""
    old_em = font["head"].unitsPerEm
    if old_em == new_em:
        return
    scale = new_em / old_em
    glyf = font["glyf"]
    hmtx = font["hmtx"].metrics

    for glyph_name in font.getGlyphOrder():
        if glyph_name not in glyf:
            continue
        g = glyf[glyph_name]

        if g.numberOfContours is None or g.numberOfContours == 0:
            # empty glyph
            pass
        elif g.isComposite():
            for comp in g.components:
                comp.x = round(comp.x * scale)
                comp.y = round(comp.y * scale)
            g.recalcBounds(glyf)
        else:
            coords = g.coordinates
            new_coords = [(round(x * scale), round(y * scale)) for x, y in coords]
            from fontTools.ttLib.tables._g_l_y_f import GlyphCoordinates
            g.coordinates = GlyphCoordinates(new_coords)
            g.recalcBounds(glyf)

        if glyph_name in hmtx:
            width, lsb = hmtx[glyph_name]
            hmtx[glyph_name] = (round(width * scale), round(lsb * scale))

    font["head"].unitsPerEm = new_em

    # scale cvt table if present
    if "cvt " in font:
        cvt = font["cvt "]
        cvt.values = [round(v * scale) for v in cvt.values]


def scaling_down_if_width(glyf, hmtx_metrics, glyph_name, scale_x, scale_y):
    """Scale glyph around center of its advance width, preserving width."""
    if glyph_name not in glyf or glyph_name not in hmtx_metrics:
        return
    g = glyf[glyph_name]
    width = hmtx_metrics[glyph_name][0]
    ox = width / 2

    if g.numberOfContours is None or g.numberOfContours == 0:
        return
    elif g.isComposite():
        for comp in g.components:
            comp.x = round(scale_x * (comp.x - ox) + ox)
            comp.y = round(scale_y * comp.y)
        g.recalcBounds(glyf)
    else:
        from fontTools.ttLib.tables._g_l_y_f import GlyphCoordinates
        new_coords = [
            (round(scale_x * (x - ox) + ox), round(scale_y * y))
            for x, y in g.coordinates
        ]
        g.coordinates = GlyphCoordinates(new_coords)
        g.recalcBounds(glyf)

    hmtx_metrics[glyph_name] = (width, g.xMin if hasattr(g, 'xMin') and g.xMin is not None else 0)


def transform_glyph_translate(glyf, hmtx_metrics, glyph_name, dx, dy):
    """Apply translation to a glyph via direct coordinate manipulation."""
    if glyph_name not in glyf:
        return
    g = glyf[glyph_name]

    if g.numberOfContours is None or g.numberOfContours == 0:
        return
    elif g.isComposite():
        for comp in g.components:
            comp.x = round(comp.x + dx)
            comp.y = round(comp.y + dy)
        g.recalcBounds(glyf)
    else:
        from fontTools.ttLib.tables._g_l_y_f import GlyphCoordinates
        new_coords = [(round(x + dx), round(y + dy)) for x, y in g.coordinates]
        g.coordinates = GlyphCoordinates(new_coords)
        g.recalcBounds(glyf)

    if glyph_name in hmtx_metrics:
        width, lsb = hmtx_metrics[glyph_name]
        hmtx_metrics[glyph_name] = (width, round(lsb + dx))


def transform_glyph_with_pen(src_font, src_glyph_name, transform):
    """Transform a glyph using the pen pipeline. Returns (glyph, width)."""
    glyph_set = src_font.getGlyphSet()
    rec = DecomposingRecordingPen(glyph_set)
    glyph_set[src_glyph_name].draw(rec)

    pen = TTGlyphPen(None)
    t_pen = TransformPen(pen, transform)
    rec.replay(t_pen)

    try:
        new_glyph = pen.glyph()
    except Exception:
        # empty glyph
        new_glyph = pen.glyph(dropImpliedOnCurvePoints=False)

    return new_glyph


def copy_glyph_decomposed(src_font, src_glyph_name, dst_glyf, dst_hmtx, dst_glyph_name):
    """Copy a glyph from src to dst, decomposing composites."""
    src_glyf = src_font["glyf"]
    src_hmtx = src_font["hmtx"].metrics
    src_g = src_glyf[src_glyph_name]

    if src_g.numberOfContours is None or src_g.numberOfContours == 0:
        # empty glyph - create a minimal empty glyph
        from fontTools.ttLib.tables._g_l_y_f import Glyph
        dst_glyf[dst_glyph_name] = Glyph()
    elif src_g.isComposite():
        new_glyph = transform_glyph_with_pen(src_font, src_glyph_name, Transform())
        dst_glyf[dst_glyph_name] = new_glyph
    else:
        dst_glyf[dst_glyph_name] = copy.deepcopy(src_g)

    dst_hmtx[dst_glyph_name] = src_hmtx[src_glyph_name]


def rebuild_cmap(font, codepoint_map):
    """Rebuild cmap table with format 4 (BMP) + format 12 (full Unicode)."""
    cmap_table = font["cmap"]
    cmap_table.tables = []

    bmp_map = {cp: name for cp, name in codepoint_map.items() if cp <= 0xFFFF}

    # Platform 0 (Unicode), Encoding 3, Format 4 (BMP)
    sub4_0 = cmap_format_4(4)
    sub4_0.platformID = 0
    sub4_0.platEncID = 3
    sub4_0.language = 0
    sub4_0.cmap = dict(bmp_map)
    cmap_table.tables.append(sub4_0)

    # Platform 3 (Windows), Encoding 1, Format 4 (BMP)
    sub4_3 = cmap_format_4(4)
    sub4_3.platformID = 3
    sub4_3.platEncID = 1
    sub4_3.language = 0
    sub4_3.cmap = dict(bmp_map)
    cmap_table.tables.append(sub4_3)

    # Platform 0 (Unicode), Encoding 4, Format 12 (full)
    sub12_0 = cmap_format_12(12)
    sub12_0.platformID = 0
    sub12_0.platEncID = 4
    sub12_0.language = 0
    sub12_0.cmap = dict(codepoint_map)
    cmap_table.tables.append(sub12_0)

    # Platform 3 (Windows), Encoding 10, Format 12 (full)
    sub12_3 = cmap_format_12(12)
    sub12_3.platformID = 3
    sub12_3.platEncID = 10
    sub12_3.language = 0
    sub12_3.cmap = dict(codepoint_map)
    cmap_table.tables.append(sub12_3)


def round_all_coordinates(font):
    """Round all glyph coordinates to integers."""
    glyf = font["glyf"]
    from fontTools.ttLib.tables._g_l_y_f import GlyphCoordinates
    for glyph_name in font.getGlyphOrder():
        if glyph_name not in glyf:
            continue
        g = glyf[glyph_name]
        if g.numberOfContours is None or g.numberOfContours == 0:
            continue
        if g.isComposite():
            for comp in g.components:
                comp.x = round(comp.x)
                comp.y = round(comp.y)
        else:
            new_coords = [(round(x), round(y)) for x, y in g.coordinates]
            g.coordinates = GlyphCoordinates(new_coords)
        g.recalcBounds(glyf)


########################################
# font processing functions
########################################


def process_inconsolata(path):
    """Process Inconsolata: replace zero, remove asterisk/tilde."""
    print(f"Open {path}")
    font = TTFont(path)
    glyf = font["glyf"]
    hmtx = font["hmtx"].metrics

    # Replace 0 with dot variant
    print("Replace zero with zero.zero")
    if "zero.zero" in glyf:
        glyf["zero"] = copy.deepcopy(glyf["zero.zero"])
        hmtx["zero"] = hmtx["zero.zero"]

    # Remove asterisk and tilde glyph data (clear outlines, keep names)
    print("Remove asterisk and tilde glyphs")
    from fontTools.ttLib.tables._g_l_y_f import Glyph
    for name in ("asterisk", "asciitilde"):
        if name in glyf:
            glyf[name] = Glyph()
            hmtx[name] = (0, 0)

    # Remove from cmap
    for subtable in font["cmap"].tables:
        for cp in (0x002A, 0x007E):
            if cp in subtable.cmap:
                del subtable.cmap[cp]

    # EM is already 1000
    return font


def process_anonymous_pro(path):
    """Process Anonymous Pro: extract asterisk and tilde only."""
    print(f"Open {path}")
    font = TTFont(path)
    em_scale = newfont_em / font["head"].unitsPerEm

    cmap = font.getBestCmap()
    asterisk_name = cmap.get(0x002A)
    tilde_name = cmap.get(0x007E)

    result_glyphs = {}
    for cp, glyph_name in [(0x002A, asterisk_name), (0x007E, tilde_name)]:
        if glyph_name is None:
            continue
        # EM scale + translate(26, 90)
        t = Transform().translate(26, 90).scale(em_scale, em_scale)
        new_glyph = transform_glyph_with_pen(font, glyph_name, t)
        result_glyphs[cp] = (glyph_name, new_glyph, 500)

    font.close()
    return result_glyphs


def process_powerline(path, terminal):
    """Process Powerline: apply terminal-specific transform."""
    print(f"Open {path}")
    font = TTFont(path)

    if terminal == "WindowsTerminal":
        powerline_y = -210
        powerline_h = 1.09
    elif terminal == "iTerm2":
        powerline_y = -175
        powerline_h = 1.065
    else:
        powerline_y = -200
        powerline_h = 1.0

    glyf = font["glyf"]
    hmtx = font["hmtx"].metrics
    # EM is already 1000

    # Transform: move(0,200) -> scale(1.0, h) -> move(0, y)
    for glyph_name in font.getGlyphOrder():
        if glyph_name not in glyf:
            continue
        g = glyf[glyph_name]
        if g.numberOfContours is None or g.numberOfContours == 0:
            continue

        t = Transform().translate(0, powerline_y).scale(1.0, powerline_h).translate(0, 200)
        new_glyph = transform_glyph_with_pen(font, glyph_name, t)
        glyf[glyph_name] = new_glyph

    round_all_coordinates(font)
    return font


def process_nerd_fonts(path):
    """Process Nerd Fonts: translate all glyphs by (0, 60)."""
    print(f"Open {path}")
    font = TTFont(path)
    glyf = font["glyf"]
    hmtx = font["hmtx"].metrics
    # EM is already 1000

    print("Translate glyphs by (0, 60)")
    for glyph_name in font.getGlyphOrder():
        transform_glyph_translate(glyf, hmtx, glyph_name, 0, 60)

    round_all_coordinates(font)
    return font


def process_dejavu(path):
    """Process DejaVu: remove wide chars, scale down."""
    print(f"Open {path}")
    font = TTFont(path)

    # Mark wide characters to exclude
    cmap = font.getBestCmap()
    wide_codepoints = set()
    for cp in cmap:
        if cp > 0:
            try:
                if unicodedata.east_asian_width(chr(cp)) in ("W", "F"):
                    wide_codepoints.add(cp)
            except (ValueError, OverflowError):
                pass

    # Remove wide chars from cmap
    for subtable in font["cmap"].tables:
        for cp in wide_codepoints:
            if cp in subtable.cmap:
                del subtable.cmap[cp]

    # EM scale (2048 -> 1000) + additional 0.83 scale
    em_scale = newfont_em / font["head"].unitsPerEm
    combined_scale = em_scale * 0.83
    scale_font_em(font, newfont_em)

    # Apply 0.83 scale and set width to 500
    glyf = font["glyf"]
    hmtx = font["hmtx"].metrics
    from fontTools.ttLib.tables._g_l_y_f import GlyphCoordinates

    for glyph_name in font.getGlyphOrder():
        if glyph_name not in glyf:
            continue
        g = glyf[glyph_name]

        if g.numberOfContours is None or g.numberOfContours == 0:
            pass
        elif g.isComposite():
            for comp in g.components:
                comp.x = round(comp.x * 0.83)
                comp.y = round(comp.y * 0.83)
            g.recalcBounds(glyf)
        else:
            new_coords = [(round(x * 0.83), round(y * 0.83)) for x, y in g.coordinates]
            g.coordinates = GlyphCoordinates(new_coords)
            g.recalcBounds(glyf)

        if glyph_name in hmtx:
            hmtx[glyph_name] = (500, g.xMin if hasattr(g, 'xMin') and g.xMin is not None else 0)

    round_all_coordinates(font)
    return font, wide_codepoints


def process_genshin(path):
    """Process GenShin Gothic: EM scale, conditional scaling, remove lookups."""
    print(f"Open {path}")
    font = TTFont(path)

    # EM scale (1024 -> 1000)
    print("Scale EM 1024 -> 1000")
    scale_font_em(font, newfont_em)

    glyf = font["glyf"]
    hmtx = font["hmtx"].metrics
    cmap = font.getBestCmap()

    # Build codepoint sets
    kana_cps = set(charZHKana + charZKKana)
    zeisu_cps = set(charZEisu)

    # Classify glyphs by codepoint
    print("Conditional scaling...")
    for cp, glyph_name in cmap.items():
        # Due to selectLess bug, ALL glyphs get 0.91 first
        scaling_down_if_width(glyf, hmtx, glyph_name, 0.91, 0.91)

    # Then hiragana/katakana get additional 0.97
    for cp, glyph_name in cmap.items():
        if cp in kana_cps:
            scaling_down_if_width(glyf, hmtx, glyph_name, 0.97, 0.97)

    # Then fullwidth alphanumeric get additional 0.91/0.86
    for cp, glyph_name in cmap.items():
        if cp in zeisu_cps:
            scaling_down_if_width(glyf, hmtx, glyph_name, 0.91, 0.86)

    # Remove GSUB and GPOS
    print("Remove GSUB/GPOS lookups")
    for table_tag in ("GSUB", "GPOS"):
        if table_tag in font:
            del font[table_tag]

    # Save unicode ranges and code pages
    os2 = font["OS/2"]
    unicode_ranges = (os2.ulUnicodeRange1, os2.ulUnicodeRange2,
                      os2.ulUnicodeRange3, os2.ulUnicodeRange4)
    code_pages = (os2.ulCodePageRange1, os2.ulCodePageRange2)

    round_all_coordinates(font)
    return font, unicode_ranges, code_pages


########################################
# merge and output
########################################


def merge_fonts(base, sources):
    """
    Merge glyphs from source fonts into base, first-wins by codepoint.
    sources: list of (TTFont, source_id, excluded_codepoints_set)
    """
    # Collect existing codepoints from base
    target_cmap = {}
    for subtable in base["cmap"].tables:
        target_cmap.update(subtable.cmap)
    existing_cps = set(target_cmap.keys())

    target_glyf = base["glyf"]
    target_hmtx = base["hmtx"].metrics
    glyph_order = list(base.getGlyphOrder())
    existing_names = set(glyph_order)

    for source_font, src_id, excluded_cps in sources:
        src_cmap = source_font.getBestCmap()
        if src_cmap is None:
            continue

        count = 0
        for cp, src_glyph_name in sorted(src_cmap.items()):
            if cp in existing_cps:
                continue
            if cp in excluded_cps:
                continue

            # Determine target glyph name
            tgt_name = src_glyph_name
            if tgt_name in existing_names:
                tgt_name = f"{src_glyph_name}.{src_id}"
                suffix = 2
                while tgt_name in existing_names:
                    tgt_name = f"{src_glyph_name}.{src_id}{suffix}"
                    suffix += 1

            copy_glyph_decomposed(source_font, src_glyph_name, target_glyf, target_hmtx, tgt_name)

            target_cmap[cp] = tgt_name
            glyph_order.append(tgt_name)
            existing_names.add(tgt_name)
            existing_cps.add(cp)
            count += 1

        print(f"  Merged {count} glyphs from {src_id}")

    # Rebuild cmap
    rebuild_cmap(base, target_cmap)

    # Update glyph order
    base.setGlyphOrder(glyph_order)

    return base


def merge_anonymous_pro_glyphs(base, anon_glyphs):
    """Merge the 2 Anonymous Pro glyphs directly into base."""
    glyf = base["glyf"]
    hmtx = base["hmtx"].metrics

    for cp, (glyph_name, glyph_obj, width) in anon_glyphs.items():
        if glyph_name in glyf:
            glyf[glyph_name] = glyph_obj
            hmtx[glyph_name] = (width, glyph_obj.xMin if hasattr(glyph_obj, 'xMin') and glyph_obj.xMin is not None else 0)

    # Re-add cmap entries
    for subtable in base["cmap"].tables:
        for cp, (glyph_name, _, _) in anon_glyphs.items():
            subtable.cmap[cp] = glyph_name


def set_font_properties(font, font_info, weight, panose, unicode_ranges, code_pages):
    """Set all font metadata properties."""
    is_bold = weight == "Bold"

    # Copyright
    copyright_text = "Copyright (c) 2021 pakutoma (Juglans)\n"
    copyright_text += "Copyright (c) 2006 The Inconsolata Project Authors (Inconsolata)\n"
    copyright_text += "Copyright (c) 2014 MM (GenShinGothic)\n"
    copyright_text += "Copyright (c) 2014 Adobe Systems Incorporated. (NotoSansJP)\n"
    copyright_text += "Copyright (c) Bitstream. DejaVu changes are in public domain. Glyphs imported from Arev fonts are (c) Tavmjong Bah. (DejaVu LGC)\n"
    copyright_text += "Copyright (c) 2009, Mark Simonson (http://www.ms-studio.com, mark@marksimonson.com) (Anonymous Pro Minus)\n"
    copyright_text += "Licenses:\n"
    copyright_text += "SIL Open Font License Version 1.1 "
    copyright_text += "(http://scripts.sil.org/ofl)\n"

    # Name table
    name_table = font["name"]
    name_table.names = []  # clear existing

    names = {
        0: copyright_text,
        1: font_info["family"],
        2: weight,
        3: font_info["family"],
        4: font_info["fullname"],
        5: f"Version {newfont_version}",
        6: font_info["postscript"],
        16: font_info["family"],
    }

    for name_id, value in names.items():
        name_table.setName(value, name_id, 3, 1, 0x0409)
        name_table.setName(value, name_id, 1, 0, 0)

    # head table
    font["head"].flags |= (1 << 13)  # Optimized for ClearType
    font["head"].unitsPerEm = newfont_em
    font["head"].fontRevision = newfont_sfntRevision

    # OS/2 table
    os2 = font["OS/2"]
    os2.usWinAscent = newfont_winAscent
    os2.usWinDescent = newfont_winDescent
    os2.sTypoAscender = newfont_typoAscent
    os2.sTypoDescender = newfont_typoDescent
    os2.sTypoLineGap = newfont_typoLinegap
    os2.xAvgCharWidth = 505
    os2.usWeightClass = 700 if is_bold else 400
    os2.achVendID = "    "
    os2.version = 4
    from fontTools.ttLib.tables.O_S_2f_2 import Panose
    panose_obj = Panose()
    panose_obj.bFamilyType = panose[0]
    panose_obj.bSerifStyle = panose[1]
    panose_obj.bWeight = panose[2]
    panose_obj.bProportion = panose[3]
    panose_obj.bContrast = panose[4]
    panose_obj.bStrokeVariation = panose[5]
    panose_obj.bArmStyle = panose[6]
    panose_obj.bLetterForm = panose[7]
    panose_obj.bMidline = panose[8]
    panose_obj.bXHeight = panose[9]
    os2.panose = panose_obj

    # Unicode ranges and code pages from GenShin
    os2.ulUnicodeRange1 = unicode_ranges[0]
    os2.ulUnicodeRange2 = unicode_ranges[1]
    os2.ulUnicodeRange3 = unicode_ranges[2]
    os2.ulUnicodeRange4 = unicode_ranges[3]
    os2.ulCodePageRange1 = code_pages[0]
    os2.ulCodePageRange2 = code_pages[1]

    # hhea table
    font["hhea"].ascent = newfont_hheaAscent
    font["hhea"].descent = newfont_hheaDescent
    font["hhea"].lineGap = newfont_hheaLinegap

    # post table
    font["post"].underlinePosition = 45


########################################
# main
########################################

def main():
    if len(sys.argv) < 3:
        print("Usage: juglans_generator.py <terminal> <weight>")
        print("  terminal: WindowsTerminal, iTerm2")
        print("  weight: Regular, Bold")
        sys.exit(1)

    terminal = sys.argv[1]
    weight = sys.argv[2]
    is_bold = weight == "Bold"

    print(f"Juglans generator {newfont_version}")
    print(f"Generate Juglans {weight} for {terminal}")

    # Select source files based on weight
    src_inconsolata = srcfont_inconsolata_bold if is_bold else srcfont_inconsolata
    src_genshin = srcfont_genshin_bold if is_bold else srcfont_genshin
    src_anonpro = srcfont_anonpro_bold if is_bold else srcfont_anonpro
    src_nerdfonts = srcfont_nerdfonts_bold if is_bold else srcfont_nerdfonts
    src_dejavu = srcfont_dejavu_bold if is_bold else srcfont_dejavu
    panose = panose_bold if is_bold else panose_regular

    # Font info
    if is_bold:
        font_info = {
            "postscript": "Juglans-Bold",
            "family": "Juglans",
            "fullname": "Juglans Bold",
        }
    else:
        font_info = {
            "postscript": "Juglans-Regular",
            "family": "Juglans",
            "fullname": "Juglans Regular",
        }

    output_path = f"../Work/Juglans-{weight}-for-{terminal}.ttf"

    # Process each source font
    print("\n=== Processing Inconsolata ===")
    base_font = process_inconsolata(src_inconsolata)

    print("\n=== Processing Anonymous Pro ===")
    anon_glyphs = process_anonymous_pro(src_anonpro)

    print("\n=== Processing Powerline ===")
    powerline_font = process_powerline(srcfont_powerline, terminal)

    print("\n=== Processing Nerd Fonts ===")
    nerd_font = process_nerd_fonts(src_nerdfonts)

    print("\n=== Processing DejaVu LGC ===")
    dejavu_font, dejavu_wide_cps = process_dejavu(src_dejavu)

    print("\n=== Processing GenShin Gothic ===")
    genshin_font, unicode_ranges, code_pages = process_genshin(src_genshin)

    # Merge Anonymous Pro glyphs directly (replace cleared asterisk/tilde)
    print("\n=== Merging ===")
    print("Merge Anonymous Pro")
    merge_anonymous_pro_glyphs(base_font, anon_glyphs)

    # Merge remaining fonts (first-wins by codepoint)
    print("Merge Powerline, Nerd Fonts, DejaVu, GenShin")
    merge_fonts(base_font, [
        (powerline_font, "pw", set()),
        (nerd_font, "nf", set()),
        (dejavu_font, "dv", dejavu_wide_cps),
        (genshin_font, "gs", set()),
    ])

    # Set font properties
    print("\n=== Setting font properties ===")
    set_font_properties(base_font, font_info, weight, panose, unicode_ranges, code_pages)

    # Round all coordinates
    round_all_coordinates(base_font)

    # Save
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    print(f"\nGenerate {output_path}")
    base_font.save(output_path)
    base_font.close()

    # Close source fonts
    powerline_font.close()
    nerd_font.close()
    dejavu_font.close()
    genshin_font.close()

    print("Done!")


if __name__ == "__main__":
    main()
