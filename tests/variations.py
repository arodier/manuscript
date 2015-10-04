#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Testing character rendering variations

from freetype import *
import numpy as np
from PIL import Image
import random
import math

def render(filename = "./fonts/HaloHandletter.otf", hinting = (False,False), gamma = 1.5, lcd=True):
    text = "A Quick Brown Fox Jumps Over The Lazy Dog"
    text += ", and Innuendo is my favourite English word."
    size = 24
    size_variation = 4
    textDirection = 0;

    dpi = 90
    nbLines = 10
    W,H,D = dpi * 0.3 * len(text), dpi * nbLines, 1
    Z = np.zeros((H,W), dtype=np.ubyte )
    face = Face(filename)
    pen = Vector(50 * dpi, 50 * dpi)
    flags = FT_LOAD_RENDER

    if hinting[1]:
        flags |= FT_LOAD_FORCE_AUTOHINT
    else:
        flags |= FT_LOAD_NO_HINTING

    if hinting[0]:
        hres, hscale = dpi,    1.0
    else:
        hres, hscale = dpi*20, 0.1

    if lcd:
        flags |= FT_LOAD_TARGET_LCD
        Z = np.zeros((H+100,W+100,3), dtype=np.ubyte)
        set_lcd_filter(FT_LCD_FILTER_DEFAULT)

    for line in range(0,nbLines):
        previous = 0
        charpos = 0
        for current in text:
            charSize = random.randint(size-size_variation/2, size+size_variation/2)
            if current.isupper():
                chv = 0.01 * random.randint(75,105)   # Char height var
                cwv = 0.01 * random.randint(60,95)    # Char width variation
                civ = 0.01 * random.randint(0,25)     # Char italic variation
                crv = 0.001 * random.randint(-15,15)  # Char rotation variation
                csv = random.randint(-100,0)          # Char spacing variation
            else:
                chv = 0.01 * random.randint(85,115)   # Char height var
                cwv = 0.01 * random.randint(75,125)   # Char width variation
                civ = 0.01 * random.randint(0,15)     # Char italic variation
                crv = 0.001 * random.randint(-10,10)  # Char rotation variation
                csv = random.randint(-100,100)        # Char spacing variation


            face.set_char_size(charSize*dpi, 0, hres, 2*dpi)

            matrix  = Matrix()
            matrix.xx = int(cwv * hscale * 0x10000)
            matrix.yy = int(chv          * 0x10000)
            matrix.xy = int(civ          * 0x10000)
            matrix.yx = int(crv          * 0x10000)
            face.set_transform(matrix, pen)

            face.load_char(current, flags)

            kerning = face.get_kerning(previous, current, FT_KERNING_UNSCALED)
            pen.x += kerning.x + random.randint(-dpi,dpi)
            glyph = face.glyph
            bitmap = glyph.bitmap
            x, y = glyph.bitmap_left, glyph.bitmap_top
            y += int(textDirection * charpos)
            w, h, p = bitmap.width, bitmap.rows, bitmap.pitch
            buff = np.array(bitmap.buffer, dtype=np.ubyte).reshape((h,p))

            if lcd:
                Z[H-y:H-y+h, x:x+w/3].flat |= buff[:,:+w].flatten()
            else:
                Z[H-y:H-y+h, x:x+w].flat |= buff[:,:w].flatten()

            if current == ' ':
                pen.x += 1000
            else:
                pen.x += glyph.advance.x + csv

            previous = current
            charpos += 1
        # New line
        pen.x = 50 * dpi
        pen.y += int(2.4 * size * dpi)

    # Gamma correction
    Z = (Z/255.0)**(gamma)
    Z = ((1-Z)*255).astype(np.ubyte)
    if lcd:
        I = Image.fromarray(Z, mode='RGB')
    else:
        I = Image.fromarray(Z, mode='L')

    filename = 'tests/test.png'
    I.save(filename)



if __name__ == '__main__':
  render('./fonts/Notehand.ttf', (0,0), 1.25, False)
