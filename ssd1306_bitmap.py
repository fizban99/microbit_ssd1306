from microbit import i2c

from ssd1306 import command, set_zoom, set_pos, ADDR


def show_bitmap(filename):
    set_pos()
    command([0xae])
    with open(filename, 'rb') as my_file:
        for i in range(0, 16):
            i2c.write(ADDR, b'\x40' + my_file.read(64))
    set_zoom(0)
    command([0xaf])
