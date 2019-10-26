import fontforge
import os

os.makedirs('otf', exist_ok=True)

for fileName in os.listdir('ttf'):
    fontNameBase = fileName.split('.')[0]
    print(fontNameBase)

    fontNameTtf = os.path.join('ttf', fontNameBase + '.ttf')
    font = fontforge.open(fontNameTtf)
    font.selection.all()
    font.canonicalContours()
    font.removeOverlap()
    font.simplify()
    font.canonicalContours()
    font.canonicalStart()
    font.generate(fontNameTtf, flags='short-post')

    fontNameOtf = os.path.join('otf', fontNameBase + '.otf')
    font.private['BlueValues'] = []
    font.private['BlueScale'] = 0.0
    font.private['BlueFuzz'] = 0.0
    font.generate(fontNameOtf)