import fontforge
import os

for fileName in os.listdir('ttf'):
    fontNameBase = fileName.split('.')[0]
    print(fontNameBase)

    fontNameTtf = os.path.join('ttf', fontNameBase + '.ttf')

    if not os.path.isdir('otf'):
        os.makedirs('otf')
    fontNameOtf = os.path.join('otf', fontNameBase + '.otf')

    font = fontforge.open(fontNameTtf)
    font.selection.all()
    font.canonicalContours()
    font.removeOverlap()
    font.simplify()
    font.canonicalContours()
    font.canonicalStart()

    font.generate(fontNameTtf, flags='short-post')
    font.private['BlueValues'] = []
    font.private['BlueScale'] = 0.0
    font.private['BlueFuzz'] = 0.0
    font.generate(fontNameOtf)