def create_stamp(img):
    stamp = bytearray(5)
    for c in range(0, 5):
        col = 0
        for r in range(1, 6):
            col |= (img.get_pixel(c, r - 1) != 0) << r
        stamp[c] = col
    return stamp
