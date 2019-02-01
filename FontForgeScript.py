import fontforge
import os

for fileName in os.listdir('ttf'):
    fontNameBase = fileName.split('.')[0]
    print(fontNameBase)

    fontNameTtf = os.path.join('ttf', fontNameBase + '.ttf')

    if not os.path.isdir('otf'):
        os.makedirs('otf')
    fontNameOtf = os.path.join('otf', fontNameBase + '.otf')

    if not os.path.isdir('otf-1k'):
        os.makedirs('otf-1k')
    fontNameOtf1k = os.path.join('otf-1k', fontNameBase + '.otf')

    if not os.path.isdir('svg'):
        os.makedirs('svg')
    fontNameSvg = os.path.join('svg', fontNameBase + '.svg')

    if not os.path.isdir('fon'):
        os.makedirs('fon')
    fontNameFon = os.path.join('fon', fontNameBase + '.fon')

    if not os.path.isdir('dfont'):
        os.makedirs('dfont')
    fontNameDfont = os.path.join('dfont', fontNameBase + '.dfont')

    if not os.path.isdir('bdf'):
        os.makedirs('bdf')
    fontNameBdf = os.path.join('bdf', fontNameBase + '.bdf')

    font = fontforge.open(fontNameTtf)
    for glyph in font.glyphs():
        glyph.removeOverlap()
        glyph.simplify()

    font.selection.all()
    font.bitmapSizes = ((font.em,),)
    font.regenBitmaps(font.bitmapSizes)
    font.encoding = 'MS-ANSI'
    font.generate(fontNameFon, bitmap_type='fon', bitmap_resolution=font.em)
    font.encoding = 'UnicodeBmp'
    font.generate(fontNameBdf, bitmap_type='bdf', bitmap_resolution=font.em)
    font.generate(fontNameDfont, bitmap_type='dfont', bitmap_resolution=font.em, flags='short-post')
    font.bitmapSizes = (())

    font.generate(fontNameTtf, flags='short-post')
    font.generate(fontNameSvg)

    font.private['BlueValues'] = []
    font.private['BlueScale'] = 0.0
    font.private['BlueFuzz'] = 0.0
    font.generate(fontNameOtf, flags='short-post')

    font.em = 1000
    font.generate(fontNameOtf1k, flags='short-post')