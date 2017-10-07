from microbit import Image, i2c

from ssd1306 import screen, set_zoom, set_pos, ADDR


def add_text(x, y, text, draw=1):
    for i in range(0, min(len(text), 12 - x)):
        for c in range(0, 5):
            col = 0
            for r in range(1, 6):
                p = Image(text[i]).get_pixel(c, r - 1)
                col = col | (1 << r) if (p != 0) else col
            ind = x * 10 + y * 128 + i * 10 + c * 2 + 1
            screen[ind], screen[ind + 1] = col, col
    if draw == 1:
        set_zoom(1)
        set_pos(x * 5, y)
        ind0 = x * 10 + y * 128 + 1
        i2c.write(ADDR, b'\x40' + screen[ind0:ind + 1])

def add_sentence(words):
    ''' print each word on its own line centered on the screen
        if the number of characters in the word exceed the number
        of columns on the screen, then indicate so with an asterisk
        
        caller of this method is responsible for clearing the screen
    '''
    row_count = 0
    for word in words.split():
        if len(word) <= 12:
            add_text(int((12-len(word))/2), row_count % 4, word)
        else:
            add_text(0, row_count % 4, word[:11] + "*")
        row_count = row_count + 
