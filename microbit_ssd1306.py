# I2C LCD library for micro:bit board
# Ported from Adafruit_Python_SSD1306 library by Dmitrii (dmitryelj@gmail.com)
# Ported from lopyi2c.py library by Mr. Moreno
# v0.1 beta
# Only supports display type I2C128x64

from microbit import i2c, Image, sleep
from os import listdir
from gc import mem_free, collect

# LCD Control constants
SSD1306_I2C_ADDRESS = 0x3C
screen = bytearray()
zoom = 1


def command1(c):
    i2c.write(SSD1306_I2C_ADDRESS, bytearray([0,  c]))


def command2(c1,  c2):
    i2c.write(SSD1306_I2C_ADDRESS, bytearray([0,  c1,  c2]))


def command3(c1,  c2,  c3):
    i2c.write(SSD1306_I2C_ADDRESS, bytearray([0,  c1,  c2,  c3]))


def initialize():
    command1(0xAE)                    # SSD1306_DISPLAYOFF
    command1(0xA4)           # SSD1306_DISPLAYALLON_RESUME
    command2(0xD5, 0xF0)            # SSD1306_SETDISPLAYCLOCKDIV
    command2(0xA8,  0x3F)                  # SSD1306_SETMULTIPLEX
    command2(0xD3,  0x0)              # SSD1306_SETDISPLAYOFFSET
    command1(0 | 0x0)            # line #SSD1306_SETSTARTLINE
    command2(0x8D,  0x14)                    # SSD1306_CHARGEPUMP
    # 0x20 0x00 horizontal addressing
    command2(0x20,  0x00)  # SSD1306_MEMORYMODE
    command3(0x21,  0, 127)  # SSD1306_COLUMNADDR
    command3(0x22,  0, 63)   # SSD1306_PAGEADDR
    command1(0xa0 | 0x1)  # SSD1306_SEGREMAP
    command1(0xc8)   # SSD1306_COMSCANDEC
    command2(0xDA,  0x12)                    # SSD1306_SETCOMPINS
    command2(0x81,  0xCF)                   # SSD1306_SETCONTRAST
    command2(0xd9,  0xF1)                  # SSD1306_SETPRECHARGE
    command2(0xDB,  0x40)                 # SSD1306_SETVCOMDETECT
    command1(0xA6)                 # SSD1306_NORMALDISPLAY
    command2(0xd6, 1)  # zoom on
    command1(0xaf)  # SSD1306_DISPLAYON
    init_buffer()


def show_bitmap(filename):
    global screen
    if filename not in listdir():
        print("File not found")
    else:
        set_pos()
        set_zoom(0)
        command1(0xa7)  # inverted display
        screen = bytearray(b'\x40')
        collect()
        with open(filename, 'rb') as my_file:
            for i in range(0, 16):
                # extend little by little to preserve memory
                screen.extend(my_file.read(64))
        i2c.write(0x3c, screen)
        init_buffer()  # free up some memory


def init_buffer():
    global screen
    screen = bytearray(b'\x00' * 513)  # send byte plus pixels
    screen[0] = 0x40


def set_pos(col=0, page=0):
    command1(0xb0 + page)  # page number
    c1 = col*2  & 0x0F  # take lower value of col
    c2 = col*2  >> 4  # take lower value of col
    command1(0x00 | c1)   # lower start column address
    command1(0x10 | c2)   # upper start column address


def fill_oled(c):
    set_pos()
    for i in range(1, 513):
        screen[i] = c
    for i in range(0, 2):
        i2c.write(SSD1306_I2C_ADDRESS, screen)


def set_zoom(v):
    global zoom
    if zoom != v:
        command2(0xd6, v)  # zoom on/off
        zoom = v


def set_pixel(x, y, color, draw=1):
    shiftPage = y % 8
    page = y // 8
    if color:
        b = screen[x * 2 + page * 128 + 1] | (1 << shiftPage)
    else:
        b = screen[x * 2 + page * 128 + 1] & ~ (1 << shiftPage)
    screen[x * 2 + page * 128 + 1] = b
    screen[x * 2 + page * 128 + 2] = b
    if draw:
        set_pos(x, page)
        i2c.write(0x3c, bytearray([0x40, b, b]))


def text(x,  y,  str, draw=1):
    global screen
    for i in range(0,  min(len(str), 12 - x)):
        for c in range(0, 5):
            col = 0
            for r in range(1, 6):
                col |= (Image(str[i]).get_pixel(c, r - 1) != 0) << r
            screen[x * 10 + y * 128 + i * 10 + c * 2 + 1] = col
            screen[x * 10 + y * 128 + i * 10 + c * 2 + 2] = col
    if draw == 1:
        draw_screen()


def draw_screen():
    global screen
    set_zoom(1)
    set_pos()
    i2c.write(SSD1306_I2C_ADDRESS, screen)


if __name__ == "__main__":

    print("Started")

    initialize()
    fill_oled(0x00)
    command2(0xd5, 0xF0)
    # text(0, 0,  "micro:bit",0)
    # text(0, 1,   "font test",0)
    # text(0, 2,  "AaBbCcDdEeFf",0)
    # text(0, 3,  "012345678901",0)
    # drawScreen()
    for i in range(1, 32):
        set_pixel(i - 1, i - 1, 0)
        set_pixel(i, i, 1)
        # sleep(100)
    draw_screen()
    collect()
    print(mem_free())
    print("Done")
