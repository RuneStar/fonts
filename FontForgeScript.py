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

    if not os.path.isdir('ttf-64'):
        os.makedirs('ttf-64')
    fontNameTtf64 = os.path.join('ttf-64', fontNameBase + '.ttf')

    if not os.path.isdir('svg'):
        os.makedirs('svg')
    fontNameSvg = os.path.join('svg', fontNameBase + '.svg')

    if not os.path.isdir('fon'):
        os.makedirs('fon')
    fontNameFon = os.path.join('fon', fontNameBase + '.fon')

    if not os.path.isdir('bdf'):
        os.makedirs('bdf')
    fontNameBdf = os.path.join('bdf', fontNameBase + '.bdf')

    font = fontforge.open(fontNameTtf)
    font.selection.all()
    font.removeOverlap()
    font.simplify()
    font.canonicalContours()
    font.canonicalStart()

    font.bitmapSizes = ((font.em,),)
    font.regenBitmaps(font.bitmapSizes)
    font.encoding = 'MS-ANSI'
    font.generate(fontNameFon, bitmap_type='fon', bitmap_resolution=font.em)
    font.encoding = 'UnicodeBmp'
    font.generate(fontNameBdf, bitmap_type='bdf', bitmap_resolution=font.em)
    font.bitmapSizes = (())

    font.generate(fontNameSvg)
    font.generate(fontNameTtf, flags='short-post')
    font.private['BlueValues'] = []
    font.private['BlueScale'] = 0.0
    font.private['BlueFuzz'] = 0.0
    font.generate(fontNameOtf)

    font.em = 64
    font.generate(fontNameTtf64)

    font.em = 1000
    font.generate(fontNameOtf1k)