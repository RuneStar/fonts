import sys
import fontforge

ttf = sys.argv[1]
otf = sys.argv[2]

font = fontforge.open(ttf)
font.selection.all()
font.canonicalContours()
font.removeOverlap()
font.simplify()
font.canonicalContours()
font.canonicalStart()
font.generate(ttf, flags='short-post')

font.private['BlueValues'] = []
font.private['BlueScale'] = 0.0
font.private['BlueFuzz'] = 0.0
font.generate(otf)
