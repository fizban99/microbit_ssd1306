# I2C LCD library for the micro:bit
# Thanks to adafruit_Python_SSD1306 library by Dmitrii (dmitryelj@gmail.com)
# Thanks to lopyi2c.py
# Author: fizban99
# v0.1 beta
# Only supports display type I2C128x64

from ssd1306 import *
from microbit import Image

def add_text(x,  y, text, draw=1):
    global screen
    for i in range(0,  min(len(text), 12 - x)):
        for c in range(0, 5):
            col = 0
            for r in range(1, 6):
                col = col | (1 << r) if (Image(text[i]).get_pixel(c, r - 1) != 0) else col
            ind = x * 10 + y * 128 + i * 10 + c * 2 + 1
            screen[ind], screen[ind + 1] = col, col
    if draw == 1:
        set_zoom(1)
        set_pos(x * 10, y)
        ind0 = x * 10 + y * 128 + 1
        i2c.write(ADDR, b'\x40' + screen[ind0:ind+1])

