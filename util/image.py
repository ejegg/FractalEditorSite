from PIL import Image
import sys


def resize(img, baseheight, newname):
    hpercent = (baseheight / float(img.size[1]))
    wsize = int((float(img.size[0]) * float(hpercent)))
    img = img.resize((wsize, baseheight), Image.ANTIALIAS)
    img.save(newname)

def makethumbnails(fname):
    img = Image.open(fname)
    x1 = fname.replace('.png', 'x1.png')
    resize(img, 200, x1)

    x15 = fname.replace('.png', 'x1.5.png')
    resize(img, 300, x15)

    x2 = fname.replace('.png', 'x2.png')
    resize(img, 400, x2)
