# I2C LCD library for the micro:bit
# Thanks to adafruit_Python_SSD1306 library by Dmitrii (dmitryelj@gmail.com)
# Thanks to lopyi2c.py
# Author: fizban99
# v0.1 beta
# Only supports display type I2C128x64

from microbit import i2c
from microbit import *

# LCD Control constants
ADDR = 0x3D
# For Adafruit OLED = 0x3D (0x7A)
# For chinesse OLED = 0x3C (0x78)
screen = bytearray(513)  # send byte plus pixels
screen[0] = 0x40
zoom = 1


def command(c):
    i2c.write(ADDR, b'\x00' + bytearray(c))


def initialize(i2cAddress = None, pinReset = None):
    cmd = [
        [0xAE],                     # SSD1306_DISPLAYOFF
        [0xA4],                     # SSD1306_DISPLAYALLON_RESUME
        [0xD5, 0xF0],               # SSD1306_SETDISPLAYCLOCKDIV
        [0xA8, 0x3F],               # SSD1306_SETMULTIPLEX
        [0xD3, 0x00],               # SSD1306_SETDISPLAYOFFSET
        [0 | 0x0],                  # line #SSD1306_SETSTARTLINE
        [0x8D, 0x14],               # SSD1306_CHARGEPUMP
        # 0x20 0x00 horizontal addressing
        [0x20, 0x00],               # SSD1306_MEMORYMODE
        [0x21, 0, 127],             # SSD1306_COLUMNADDR
        [0x22, 0, 63],              # SSD1306_PAGEADDR
        [0xa0 | 0x1],               # SSD1306_SEGREMAP
        [0xc8],                     # SSD1306_COMSCANDEC
        [0xDA, 0x12],               # SSD1306_SETCOMPINS
        [0x81, 0xCF],               # SSD1306_SETCONTRAST
        [0xd9, 0xF1],               # SSD1306_SETPRECHARGE
        [0xDB, 0x40],               # SSD1306_SETVCOMDETECT
        [0xA6],                     # SSD1306_NORMALDISPLAY
        [0xd6, 1],                  # zoom on
        [0xaf]                      # SSD1306_DISPLAYON
    ]
    if i2cAddress:
        ADDR = i2cAddress
    if pinReset:
        pinReset.write_digital(1)
        sleep(1)
        pinReset.write_digital(0)
        sleep(10)
        pinReset.write_digital(1)
        sleep(10)
    for c in cmd:
        command(c)


def set_pos(col=0, page=0):
    command([0xb0 | page])  # page number
    # take upper and lower value of col * 2
    c1, c2 = col * 2 & 0x0F, col >> 3
    command([0x00 | c1])  # lower start column address
    command([0x10 | c2])  # upper start column address


def clear_oled(c=0):
    global screen
    set_pos()
    for i in range(1, 513):
        screen[i] = 0
    draw_screen()


def set_zoom(v):
    global zoom
    if zoom != v:
        command([0xd6, v])  # zoom on/off
        command([0xa7 - v])  # inverted display
        zoom = v


def draw_screen():
    set_zoom(1)
    set_pos()
    i2c.write(ADDR, screen)
