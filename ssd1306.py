# I2C LCD library for the micro:bit
# Thanks to adafruit_Python_SSD1306 library by Dmitrii (dmitryelj@gmail.com)
# Thanks to lopyi2c.py
# Author: fizban99
# v0.1 beta
# Only supports display type I2C128x64

from microbit import i2c, Image

# LCD Control constants
ADDR = 0x3C
screen = bytearray(513)  # send byte plus pixels
screen[0] = 0x40
zoom = 1


def command(c):
    i2c.write(ADDR, b'\x00' + bytearray(c))


def initialize():
    cmd = [
        [0xAE],                    # SSD1306_DISPLAYOFF
        [0xA4],           # SSD1306_DISPLAYALLON_RESUME
        [0xD5, 0xF0],            # SSD1306_SETDISPLAYCLOCKDIV
        [0xA8, 0x3F],                  # SSD1306_SETMULTIPLEX
        [0xD3, 0x00],              # SSD1306_SETDISPLAYOFFSET
        [0 | 0x0],                   # line #SSD1306_SETSTARTLINE
        [0x8D,  0x14],                    # SSD1306_CHARGEPUMP
        # 0x20 0x00 horizontal addressing
        [0x20,  0x00],  # SSD1306_MEMORYMODE
        [0x21,  0, 127],  # SSD1306_COLUMNADDR
        [0x22,  0, 63],   # SSD1306_PAGEADDR
        [0xa0 | 0x1],  # SSD1306_SEGREMAP
        [0xc8],   # SSD1306_COMSCANDEC
        [0xDA,  0x12],                    # SSD1306_SETCOMPINS
        [0x81,  0xCF],                   # SSD1306_SETCONTRAST
        [0xd9,  0xF1],                  # SSD1306_SETPRECHARGE
        [0xDB,  0x40],                 # SSD1306_SETVCOMDETECT
        [0xA6],                 # SSD1306_NORMALDISPLAY
        [0xd6, 1],  # zoom on
        [0xaf]  # SSD1306_DISPLAYON
    ]
    for c in cmd:
        command(c)


def create_stamp(img):
    stamp = bytearray(5)
    for c in range(0, 5):
        col = 0
        for r in range(1, 6):
            col |= (img.get_pixel(c, r - 1) != 0) << r
        stamp[c] = col
    return stamp


def show_bitmap(filename):
    set_pos()
    set_zoom(0)
    with open(filename, 'rb') as my_file:
        for i in range(0, 16):
            i2c.write(ADDR, b'\x40' + my_file.read(64))


def set_pos(col=0, page=0):
    command([0xb0 | page])  # page number
    # take upper and lower value of col
    (c1, c2) = (col * 2 & 0x0F, col * 2 >> 4)
    command([0x00 | c1])   # lower start column address
    command([0x10 | c2])   # upper start column address


def clear_oled(c=0):
    set_pos()
    for i in range(1, 513):
        screen[i] = c
    draw_screen()


def set_zoom(v):
    global zoom
    if zoom != v:
        command([0xd6, v])  # zoom on/off
        command([0xa7 - v])  # inverted display
        zoom = v


def set_pixel(x, y, color, draw=1):
    global screen
    (shiftPage, page) = (y % 8, y // 8)
    ind = x * 2 + page * 128 + 1
    b = screen[ind] | (1 << shiftPage) if color else screen[
        ind] & ~ (1 << shiftPage)
    (screen[ind], screen[ind + 1]) = (b, b)
    if draw:
        set_zoom(1)
        set_pos(x, page)
        i2c.write(0x3c, bytearray([0x40, b, b]))


def add_text(x,  y, draw=1):
    global screen
    for i in range(0,  min(len(str), 12 - x)):
        for c in range(0, 5):
            col = 0
            for r in range(1, 6):
                col |= (Image(str[i]).get_pixel(c, r - 1) != 0) << r
            ind = x * 10 + y * 128 + i * 10 + c * 2 + 1
            (screen[ind], screen[ind + 1]) = (col, col)
    if draw == 1:
        draw_screen()


def draw_stamp(x, y, stamp, color, draw=1):
    global screen
    (shiftPage, page) = (y % 8, y >>3 )
    ind = (x << 1) + (page <<7) + 1
    for col in range(0, 5):
        index = ind + (col << 1)
        b = (screen[index] | (stamp[col] << shiftPage)
             ) if color else (screen[index
                                     ] & ~ (stamp[col] << shiftPage))
        (screen[index], screen[index + 1]) = (b, b)
    ind += 128
    for col in range(0, 5):
        index = ind + col * 2
        b = (screen[index] | (stamp[col] >> (8 - shiftPage))
             ) if color else screen[index
                                    ] & ~ (stamp[col] >> (8 - shiftPage))
        (screen[index], screen[index + 1]) = (b, b)
    if draw:
        set_zoom(1)
        offset = 2 if x != 0 else 0
        set_pos(x - (offset >>1 ), page)
        i2c.write(ADDR, b'\x40' + screen[ind - 128 - offset:ind - 116])
        set_pos(x - (offset >> 1), page + 1)
        i2c.write(ADDR, b'\x40' + screen[ind - offset:ind + 14])


def draw_screen():
    global screen
    set_zoom(1)
    set_pos()
    i2c.write(ADDR, screen)
