import json

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

logging.basicConfig(level=logging.DEBUG)

for fileName in sys.argv[1::]:
    fontName = fileName.split('.')[0]
    fontNameHuman = fontName.replace('-', ' ').replace('_', ' ')

    with open(fileName) as f:
        data = json.load(f)

    for glyph in data['glyphs']:
        glyph['name'] = Unicode[glyph['codePoint']]
    data['maxAdvance'] = max(map(lambda x: x['advance'], data['glyphs']))
    data['maxDim'] = max(data['maxAdvance'], data['ascent'])

    font = TTFont()

    font.glyphOrder = ['.notdef'] + list(map(lambda x: x['name'], data['glyphs']))

    post = table__p_o_s_t()
    post.formatType = 3.0
    post.italicAngle = 0.0
    post.underlinePosition = -1
    post.underlineThickness = 1
    post.isFixedPitch = 0
    post.minMemType42 = 0
    post.maxMemType42 = 0
    post.minMemType1 = 0
    post.maxMemType1 = 0
    post.glyphOrder = None
    font['post'] = post

    name = table__n_a_m_e()
    for platform in ((1, 0, 0), (3, 1, 0x409)):
        name.setName(fontNameHuman, 1, *platform)
        name.setName('Regular', 2, *platform)
        name.setName(fontNameHuman, 3, *platform)
        name.setName(fontNameHuman, 4, *platform)
        name.setName('0.1', 5, *platform)
        name.setName(fontName, 6, *platform)
        name.setName('Jagex Ltd.', 9, *platform)
        name.setName('http://oldschool.runescape.com', 12, *platform)
    font['name'] = name

    maxp = table__m_a_x_p()
    maxp.numGlyphs = len(data['glyphs']) + 1
    maxp.tableVersion = 0x10000
    maxp.maxPoints = 256
    maxp.maxContours = 64
    maxp.maxCompositePoints = 0
    maxp.maxCompositeContours = 0
    maxp.maxZones = 2
    maxp.maxTwilightPoints = 0
    maxp.maxStorage = 0
    maxp.maxFunctionDefs = 0
    maxp.maxInstructionDefs = 0
    maxp.maxStackElements = 0
    maxp.maxSizeOfInstructions = 0
    maxp.maxComponentElements = 0
    maxp.maxComponentDepth = 0
    font['maxp'] = maxp

    cmap = table__c_m_a_p()
    cmap.tableVersion = 0
    cmap4 = cmap_format_4(cmap_format_4_format)
    cmap4.platformID = 0
    cmap4.platEncID = 3
    cmap4.language = 0
    cmap4.cmap = {}
    for glyph in data['glyphs']:
        cmap4.cmap[glyph['codePoint']] = glyph['name']
    cmap.tables = [cmap4]
    font['cmap'] = cmap

    hmtx = table__h_m_t_x()
    hmtx.metrics = {}
    for glyph in data['glyphs']:
        hmtx.metrics[glyph['name']] = (glyph['advance'], glyph['leftBearing'])
    hmtx.metrics['.notdef'] = hmtx.metrics['QUESTION MARK']
    font['hmtx'] = hmtx

    head = table__h_e_a_d()
    head.macStyle = 0
    head.flags = 0
    head.created = timestampNow()
    head.modified = head.created
    head.magicNumber = 0x5F0F3CF5
    head.tableVersion = 1.0
    head.fontRevision = 1.0
    head.checkSumAdjustment = 0
    head.unitsPerEm = 2 ** (maxPowerOfTwo(data['maxDim']) + 1)
    head.xMin = 0
    head.yMin = data['maxDescent'] * -1
    head.xMax = data['maxAdvance']
    head.yMax = data['ascent']
    head.lowestRecPPEM = 12
    head.fontDirectionHint = 2
    head.indexToLocFormat = 0
    head.glyphDataFormat = 0
    font['head'] = head

    os2 = table_O_S_2f_2()
    os2.version = 2
    os2.xAvgCharWidth = sum(map(lambda x: x['width'], data['glyphs'])) // len(data['glyphs'])
    os2.usWeightClass = 400
    os2.usWidthClass = 5
    os2.fsType = 0
    os2.ySubscriptXSize = data['maxDim'] // 2
    os2.ySubscriptYSize = data['maxDim'] // 2
    os2.ySubscriptXOffset = 0
    os2.ySubscriptYOffset = 0
    os2.ySuperscriptXSize = data['maxDim'] // 2
    os2.ySuperscriptYSize = data['maxDim'] // 2
    os2.ySuperscriptXOffset = 0
    os2.ySuperscriptYOffset = 0
    os2.yStrikeoutSize = data['maxAdvance']
    os2.yStrikeoutPosition = data['ascent'] // 2
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
    os2.ulUnicodeRange1 = 1
    os2.ulUnicodeRange2 = 0
    os2.ulUnicodeRange3 = 0
    os2.ulUnicodeRange4 = 0
    os2.achVendID = ""
    os2.fsSelection = 0b1000000
    os2.usFirstCharIndex = 0
    os2.usLastCharIndex = 0
    os2.sTypoAscender = data['ascent']
    os2.sTypoDescender = data['maxDescent'] * -1
    os2.sTypoLineGap = 0
    os2.usWinAscent = data['ascent']
    os2.usWinDescent = data['maxDescent']
    os2.ulCodePageRange1 = 0b111111011
    os2.ulCodePageRange2 = 0
    os2.sxHeight = data['ascent'] // 2
    os2.sCapHeight = data['ascent']
    os2.usDefaultChar = 0
    os2.usBreakChar = 32
    os2.usMaxContext = 1
    font['OS/2'] = os2

    hhea = table__h_h_e_a()
    hhea.tableVersion = 0x00010000
    hhea.ascent = data['ascent']
    hhea.descent = data['maxDescent']
    hhea.lineGap = 0
    hhea.advanceWidthMax = data['maxAdvance']
    hhea.minLeftSideBearing = 0
    hhea.minRightSideBearing = 0
    hhea.xMaxExtent = data['maxAdvance']
    hhea.caretSlopeRise = 1
    hhea.caretSlopeRun = 0
    hhea.caretOffset = 0
    hhea.reserved0 = 0
    hhea.reserved1 = 0
    hhea.reserved2 = 0
    hhea.reserved3 = 0
    hhea.metricDataFormat = 0
    hhea.numberOfHMetrics = len(font.glyphOrder)
    font['hhea'] = hhea

    glyf = table__g_l_y_f()
    glyf.glyphs = {}
    for glyph in data['glyphs']:
        g = Glyph()
        g.program = None
        g.xMin = 0
        g.yMin = 0
        g.xMax = 0
        g.yMax = 0
        g.numberOfContours = 0
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
                flags = [True, True, True, True]
                coords.append((x, y))
                coords.append((x + 1, y))
                coords.append((x + 1, y + 1))
                coords.append((x, y + 1))
                g.xMin = min(g.xMin, x)
                g.yMin = min(g.yMin, y)
                g.xMax = max(g.xMax, x + 1)
                g.yMax = max(g.yMax, y + 1)
                if not hasattr(g, 'coordinates'):
                    g.coordinates = coords
                    g.flags = flags
                    g.endPtsOfContours = [len(coords) - 1]
                else:
                    g.coordinates.extend(coords)
                    g.flags.extend(flags)
                    g.endPtsOfContours.append(len(g.coordinates) - 1)
        glyf.glyphs[glyph['name']] = g
    glyf.glyphs['.notdef'] = glyf.glyphs['QUESTION MARK']
    font['glyf'] = glyf

    loca = table__l_o_c_a()
    font['loca'] = loca

    font.saveXML(fontName + '.ttx')

    font2 = TTFont(recalcBBoxes=True)
    font2.importXML(fontName + '.ttx')
    font2.save(fontName + '.ttf')

    # open ttf in fontforge
    # remove all overlaps
    # simplify
    # generate ttf font
