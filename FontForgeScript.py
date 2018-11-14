import fontforge
import os

for fileName in os.listdir('ttf'):
    fontNameBase = fileName.split('.')[0]
    fontNameTtf = os.path.join('ttf', fontNameBase + '.ttf')
    if not os.path.isdir('otf'):
        os.makedirs('otf')
    fontNameOtf = os.path.join('otf', fontNameBase + '.otf')
    if not os.path.isdir('otf-1k'):
        os.makedirs('otf-1k')
    fontNameOtf1k = os.path.join('otf-1k', fontNameBase + '.otf')
    print(fontNameBase)

    font = fontforge.open(fontNameTtf)
    for glyph in font.glyphs():
        glyph.removeOverlap()
        glyph.simplify()

    font.generate(fontNameTtf, flags='short-post')

    font.private['BlueValues'] = []
    font.private['BlueScale'] = 0.0
    font.private['BlueFuzz'] = 0.0
    font.generate(fontNameOtf, flags='short-post')

    font.em = 1000
    font.generate(fontNameOtf1k, flags='short-post')