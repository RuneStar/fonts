import json
import subprocess

from fontTools.ttLib import *
from fontTools.ttLib.tables._c_m_a_p import *
from fontTools.ttLib.tables._m_a_x_p import *
from fontTools.ttLib.tables._h_m_t_x import *
from fontTools.ttLib.tables._p_o_s_t import *
from fontTools.ttLib.tables._n_a_m_e import *
from fontTools.ttLib.tables._h_e_a_d import *
from fontTools.ttLib.tables.O_S_2f_2 import *
from fontTools.ttLib.tables._h_h_e_a import *
from fontTools.ttLib.tables._g_l_y_f import *
from fontTools.ttLib.tables._l_o_c_a import *
from fontTools.ttLib.tables._g_a_s_p import *

logging.basicConfig(level=logging.DEBUG)

revision = 0.1

for fileName in os.listdir('data'):
    fontName = fileName.split('.')[0]
    fontNameHuman = fontName.replace('-', ' ')

    with open(os.path.join('data', fileName)) as f:
        data = json.load(f)

    for glyph in data['glyphs']:
        glyph['name'] = Unicode[glyph['codePoint']]
    data['maxAdvance'] = max((g['advance'] for g in data['glyphs']))
    data['maxDim'] = max(data['maxAdvance'], data['ascent'])

    font = TTFont()

    font.glyphOrder = ['.notdef'] + [g['name'] for g in data['glyphs']]
    if 'NO-BREAK SPACE' not in font.glyphOrder:
        font.glyphOrder.append('NO-BREAK SPACE')

    font['post'] = post = table__p_o_s_t()
    post.formatType = 3.0
    post.italicAngle = 0.0
    post.underlinePosition = -1
    post.underlineThickness = 1
    post.isFixedPitch = 0
    post.minMemType42 = post.maxMemType42 = post.minMemType1 = post.maxMemType1 = 0
    post.glyphOrder = None

    font['name'] = name = table__n_a_m_e()
    for platform in ((1, 0, 0), (3, 1, 0x409)):  # (Mac, Roman, English), (Windows, Unicode BMP, English US)
        name.setName('Copyright 1999-2018 Jagex Ltd.', 0, *platform)  # copyright notice
        name.setName(fontNameHuman, 1, *platform)
        name.setName('Regular', 2, *platform)
        name.setName(fontNameHuman, 3, *platform)
        name.setName(fontNameHuman, 4, *platform)
        name.setName(str(revision), 5, *platform)
        name.setName(fontName, 6, *platform)
        name.setName('RuneScape is a registered trademark of Jagex Ltd.', 7, *platform)  # trademark notice
        name.setName('Jagex Ltd.', 8, *platform)  # manufacturer
        name.setName('Jagex Ltd.', 9, *platform)  # designer
        name.setName('From Old School RuneScape, a fantasy MMORPG', 10, *platform)  # description
        name.setName('http://runestar.org', 11, *platform)  # vendor url
        name.setName('http://oldschool.runescape.com', 12, *platform)  # designer url
        name.setName('http://jagex.com', 14, *platform)  # license url

    font['maxp'] = maxp = table__m_a_x_p()
    maxp.tableVersion = 0x10000
    maxp.numGlyphs = 0  # calculated later
    maxp.maxPoints = maxp.maxContours = 0  # calculated later
    maxp.maxCompositePoints = 0
    maxp.maxCompositeContours = 0
    maxp.maxZones = 1
    maxp.maxTwilightPoints = 0
    maxp.maxStorage = 0
    maxp.maxFunctionDefs = 0
    maxp.maxInstructionDefs = 0
    maxp.maxStackElements = 0
    maxp.maxSizeOfInstructions = 0
    maxp.maxComponentElements = 0
    maxp.maxComponentDepth = 0

    font['cmap'] = cmap = table__c_m_a_p()
    cmap.tableVersion = 0
    cmapWin = cmap_format_4(4)
    cmapWin.platformID = 3  # Windows
    cmapWin.platEncID = 1  # Unicode BMP
    cmapWin.language = 0
    cmapWin.cmap = {g['codePoint']: g['name'] for g in data['glyphs']}
    cmapWin.cmap[160] = 'NO-BREAK SPACE'
    cmap.tables = [cmapWin]

    font['hmtx'] = hmtx = table__h_m_t_x()
    hmtx.metrics = {g['name']: (g['advance'], g['leftBearing']) for g in data['glyphs']}
    if 'NO-BREAK SPACE' not in hmtx.metrics:
        hmtx.metrics['NO-BREAK SPACE'] = hmtx.metrics['SPACE']
    if 'QUESTION MARK' in hmtx.metrics:
        hmtx.metrics['.notdef'] = hmtx.metrics['QUESTION MARK']
    else:
        hmtx.metrics['.notdef'] = hmtx.metrics['SPACE']

    font['head'] = head = table__h_e_a_d()
    head.macStyle = 0
    head.flags = 0
    head.created = timestampNow()
    head.modified = head.created
    head.magicNumber = 0x5F0F3CF5
    head.tableVersion = 1.0
    head.fontRevision = revision
    head.checkSumAdjustment = 0
    head.unitsPerEm = max(16, 2 ** (maxPowerOfTwo(data['maxDim']) + 1))
    head.xMin = head.yMin = head.xMax = head.yMax = 0  # calculated later
    head.lowestRecPPEM = 12
    head.fontDirectionHint = 2
    head.indexToLocFormat = 0
    head.glyphDataFormat = 0

    font['OS/2'] = os2 = table_O_S_2f_2()
    os2.version = 4
    os2.xAvgCharWidth = 0  # calculated later
    os2.usWeightClass = 400  # normal
    os2.usWidthClass = 5  # normal
    os2.fsType = 0
    os2.ySubscriptXSize = os2.ySubscriptYSize = os2.ySuperscriptXSize = os2.ySuperscriptYSize = head.unitsPerEm // 2
    os2.ySubscriptXOffset = 0
    os2.ySubscriptYOffset = 0
    os2.ySuperscriptXOffset = 0
    os2.ySuperscriptYOffset = 0
    os2.yStrikeoutSize = 1
    os2.yStrikeoutPosition = int(data['ascent'] * 0.70)
    os2.sFamilyClass = 0
    os2.panose = Panose()
    os2.panose.bFamilyType = 0
    os2.panose.bSerifStyle = 0
    os2.panose.bWeight = 0
    os2.panose.bProportion = 0
    os2.panose.bContrast = 0
    os2.panose.bStrokeVariation = 0
    os2.panose.bArmStyle = 0
    os2.panose.bLetterForm = 0
    os2.panose.bMidline = 0
    os2.panose.bXHeight = 0
    os2.ulUnicodeRange1 = os2.ulUnicodeRange2 = os2.ulUnicodeRange3 = os2.ulUnicodeRange4 = 0  # calculated later
    os2.achVendID = ""
    os2.fsSelection = 0b1000000  # regular
    os2.usFirstCharIndex = os2.usLastCharIndex = 0  # calculated later
    os2.sTypoAscender = data['ascent']
    os2.sTypoDescender = data['maxDescent'] * -1
    os2.sTypoLineGap = 0
    os2.usWinAscent = data['ascent']
    os2.usWinDescent = data['maxDescent']
    os2.ulCodePageRange1 = 1  # cp-1252
    os2.ulCodePageRange2 = 0
    os2.sxHeight = 0  # calculated later
    os2.sCapHeight = 0  # calculated later
    os2.usDefaultChar = 0
    os2.usBreakChar = 32  # space
    os2.usMaxContext = 1

    font['hhea'] = hhea = table__h_h_e_a()
    hhea.tableVersion = 0x00010000
    hhea.ascent = data['ascent']
    hhea.descent = data['maxDescent'] * -1
    hhea.lineGap = 0
    hhea.advanceWidthMax = 0  # calculated later
    hhea.minLeftSideBearing = 0
    hhea.minRightSideBearing = 0
    hhea.xMaxExtent = 0  # calculated later
    hhea.caretSlopeRise = 1
    hhea.caretSlopeRun = 0
    hhea.caretOffset = 0
    hhea.reserved0 = hhea.reserved1 = hhea.reserved2 = hhea.reserved3 = 0
    hhea.metricDataFormat = 0
    hhea.numberOfHMetrics = 0  # calculated later

    font['glyf'] = glyf = table__g_l_y_f()
    glyf.glyphs = {}
    for glyph in data['glyphs']:
        g = Glyph()
        g.program = None
        g.xMin = g.yMin = g.xMax = g.yMax = 0  # calculated later
        g.numberOfContours = 0
        g.coordinates = []
        g.flags = []
        g.endPtsOfContours = []
        x = glyph['leftBearing']
        y = data['ascent'] - glyph['topBearing']
        width = glyph['width']
        for i, p in enumerate(glyph['pixels']):
            x += 1
            if i % width is 0:
                x = 0
                y -= 1
            if p == 1:
                g.numberOfContours += 1
                coords = GlyphCoordinates()
                coords.extend([(x, y), (x + 1, y), (x + 1, y + 1), (x, y + 1)])
                g.coordinates.extend(coords)
                g.flags.extend([True, True, True, True])
                g.endPtsOfContours.append(len(g.coordinates) - 1)
        glyf.glyphs[glyph['name']] = g
    if 'NO-BREAK SPACE' not in glyf.glyphs:
        glyf.glyphs['NO-BREAK SPACE'] = glyf.glyphs['SPACE']
    if 'QUESTION MARK' in glyf.glyphs:
        glyf.glyphs['.notdef'] = glyf.glyphs['QUESTION MARK']
    else:
        glyf.glyphs['.notdef'] = glyf.glyphs['SPACE']

    font['loca'] = table__l_o_c_a()

    font['gasp'] = gasp = table__g_a_s_p()
    gasp.gaspRange = {0xFFFF: 0}

    os2.recalcUnicodeRanges(font)

    os.makedirs('ttf', exist_ok=True)
    ttfFile = os.path.join('ttf', fontName + '.ttf')
    ttxFile = fontName + '.ttx'

    font.saveXML(ttxFile)

    font2 = TTFont(recalcTimestamp=False)
    font2.importXML(ttxFile)
    font2.save(ttfFile)
    os.remove(ttxFile)

subprocess.run([r'C:\Program Files (x86)\FontForgeBuilds\bin\fontforge.exe', '-lang=py', '-script', 'FontForgeScript.py'])
