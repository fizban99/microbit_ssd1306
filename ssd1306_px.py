from microbit import i2c
from ustruct import pack_into

from ssd1306 import screen, set_pos


def set_px(x, y, color, draw=1):
    global screen
    page, shiftPage = divmod(y, 8)
    ind = x * 2 + page * 128 + 1
    b = screen[ind] | (1 << shiftPage) if color else screen[ind] & ~ (1 << shiftPage)
    pack_into(">BB", screen, ind, b, b)
    if draw:
        set_pos(x, page)
        i2c.write(0x3c, bytearray([0x40, b, b]))


def get_px(x, y):
    global screen
    page, shiftPage = divmod(y, 8)
    ind = x * 2 + page * 128 + 1
    b = (screen[ind] & (1 << shiftPage)) >> shiftPage
    return b
