import fontforge
import sys

for fileName in sys.argv[1::]:
    fontNameBase = fileName.split('.')[0]
    fontNameTtf = fontNameBase + '.ttf'
    fontNameOtf = fontNameBase + '.otf'
    print(fontNameBase)
    font = fontforge.open(fontNameTtf)
    for glyph in font.glyphs():
        glyph.removeOverlap()
        glyph.simplify()
    font.generate(fontNameOtf, flags='short-post')
    font.generate(fontNameTtf, flags='short-post')