from microbit import i2c
from ustruct import pack_into

from ssd1306 import screen, set_pos


def set_px(x, y, color, draw=1):
    page, shift_page = divmod(y, 8)
    ind = x * 2 + page * 128 + 1
    b = screen[ind] | (1 << shift_page) if color else screen[ind] & ~ (1 << shift_page)
    pack_into(">BB", screen, ind, b, b)
    if draw:
        set_pos(x, page)
        i2c.write(0x3c, bytearray([0x40, b, b]))


def get_px(x, y):
    page, shift_page = divmod(y, 8)
    ind = x * 2 + page * 128 + 1
    b = (screen[ind] & (1 << shift_page)) >> shift_page
    return b
