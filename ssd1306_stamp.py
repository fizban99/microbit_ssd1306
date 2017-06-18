from microbit import i2c
from ustruct import pack_into

from ssd1306 import screen, set_pos, ADDR


def draw_stamp(x, y, stamp, color, draw=1):
    page, shift_page = divmod(y, 8)
    ind = (x << 1) + (page << 7) + 1
    if ind > 0:
        for col in range(0, 5):
            index = ind + (col << 1)
            b = (screen[index] | (stamp[col] << shift_page)
                 ) if color else (screen[index] & ~ (stamp[col] << shift_page))
            pack_into(">BB", screen, index, b, b)
    ind += 128
    if ind < 513:
        for col in range(0, 5):
            index = ind + col * 2
            b = (screen[index] | (stamp[col] >> (8 - shift_page))
                 ) if color else screen[index] & ~ (stamp[col] >> (8 - shift_page))
            pack_into(">BB", screen, index, b, b)
    if draw:
        offset = 2 if x != 0 else 0
        set_pos(x - (offset >> 1), page)
        i2c.write(ADDR, b'\x40' + screen[ind - 128 - offset:ind - 116])
        if page < 3:
            set_pos(x - (offset >> 1), page + 1)
            i2c.write(ADDR, b'\x40' + screen[ind - offset:ind + 14])
