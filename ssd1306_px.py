# I2C LCD library for the micro:bit
# Thanks to adafruit_Python_SSD1306 library by Dmitrii (dmitryelj@gmail.com)
# Thanks to lopyi2c.py
# Author: fizban99
# v0.1 beta
# Only supports display type I2C128x64

from ssd1306 import *


def set_px(x, y, color, draw=1):
    global screen
    page, shiftPage = divmod(y, 8)
    ind = x * 2 + page * 128 + 1
    b = screen[ind] | (1 << shiftPage) if color else screen[
        ind] & ~ (1 << shiftPage)
    pack_into(">BB", screen, ind, b, b)
    if draw:
        set_zoom(1)
        set_pos(x, page)
        i2c.write(0x3c, bytearray([0x40, b, b]))


def get_px(x, y):
    global screen
    page, shiftPage = divmod(y, 8)
    ind = x * 2 + page * 128 + 1
    b = (screen[ind] & (1 << shiftPage)) >> shiftPage
    return b