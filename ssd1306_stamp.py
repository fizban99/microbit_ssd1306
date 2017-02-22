# I2C LCD library for the micro:bit
# Thanks to adafruit_Python_SSD1306 library by Dmitrii (dmitryelj@gmail.com)
# Thanks to lopyi2c.py
# Author: fizban99
# v0.1 beta
# Only supports display type I2C128x64

from ssd1306 import *

def create_stamp(img):
    stamp = bytearray(5)
    for c in range(0, 5):
        col = 0
        for r in range(1, 6):
            col |= (img.get_pixel(c, r - 1) != 0) << r
        stamp[c] = col
    return stamp

def draw_stamp(x, y, stamp, color, draw=1):
    global screen
    (page, shiftPage) = divmod(y, 8)
    ind = (x << 1) + (page << 7) + 1
    for col in range(0, 5):
        index = ind + (col << 1)
        b = (screen[index] | (stamp[col] << shiftPage)
             ) if color else (screen[index
                                     ] & ~ (stamp[col] << shiftPage))
        pack_into(">BB", screen, index, b, b)
    ind += 128
    if ind < 513:
        for col in range(0, 5):
            index = ind + col * 2
            b = (screen[index] | (stamp[col] >> (8 - shiftPage))
                 ) if color else screen[index
                                        ] & ~ (stamp[col] >> (8 - shiftPage))
            pack_into(">BB", screen, index, b, b)
    if draw:
        set_zoom(1)
        offset = 2 if x != 0 else 0
        set_pos(x - (offset >> 1), page)
        i2c.write(ADDR, b'\x40' + screen[ind - 128 - offset:ind - 116])
        if page < 3:
            set_pos(x - (offset >> 1), page + 1)
            i2c.write(ADDR, b'\x40' + screen[ind - offset:ind + 14])
