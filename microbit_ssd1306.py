# I2C LCD library for micro:bit board
# Ported from Adafruit_Python_SSD1306 library by Dmitrii (dmitryelj@gmail.com)
# Ported from lopyi2c.py library by Mr. Moreno
# v0.1 beta
# Only supports display type I2C128x64

from microbit import i2c, Image
from os import listdir
from gc import mem_free, collect

# LCD Control constants
SSD1306_I2C_ADDRESS = 0x3C
screen = bytearray(b'\x00' * 1025)  # send byte plus pixels
screen[0]=0x40

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
    command1(0xaf)  # SSD1306_DISPLAYON


def show_bitmap(filename):
    global screen
    if filename not in listdir():
        print("File not found")
    else:
        reset_pos()
        command2(0xd6, 0)  # zoom off
        command1(0xa7)  # inverted display
        screen = bytearray(b'\x40')
        collect()
        with open(filename, 'rb') as my_file:
            for i in range(0, 16):
                # extend little by little to preserve memory
                screen.extend(my_file.read(64))
        i2c.write(0x3c, screen)


def reset_pos():
    command1(0xb0)
    command1(0x00)
    command1(0x10)


def fill_oled(c):
    reset_pos()
    for i in range(1, 1025):
        screen[i] = c
    i2c.write(SSD1306_I2C_ADDRESS, screen)


def text(x,  y,  str):
    global screen
    for i in range(0,  min(len(str), 12 - x)):
        for c in range(0, 5):
            col = 0
            for r in range(1, 6):
                col |= (Image(str[i]).get_pixel(c, r - 1) != 0) << r
            screen[x*5+y*128+i*5+c+ 1] = col

def drawScreen():
    global screen
    reset_pos()
    i2c.write(SSD1306_I2C_ADDRESS, screen)



if __name__ == "__main__":

    print("Started")

    initialize()
    fill_oled(0x00)
    command2(0xd5, 0xF0)
    command1(0xaf)
    text(0, 0,  "micro:bit")
    text(0, 1,   "font test")
    text(0, 2,  "AaBbCcDdEeFf")
    text(0, 3,  "012345678901")
    drawScreen()
    show_bitmap("bitmap")
    collect()
    print(mem_free())
print("Done")
