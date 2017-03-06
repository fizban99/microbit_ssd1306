from ssd1306 import initialize, clear_oled
from ssd1306_stamp import draw_stamp
from microbit import button_a as A,  button_b as B, display as D
from random import randint
from ssd1306_bitmap import show_bitmap


def mv_stmp(x1, y1, x2, y2, stmp):
    draw_stamp(x1, y1, stmp, 0, 0)
    draw_stamp(x2, y2, stmp, 1, 1)


def init_star(i):
    return randint(0, 1), randint(0, 58), randint(1, 4)


initialize()
show_bitmap("888.bin")
while not (A.is_pressed() or B.is_pressed()):
    pass
clear_oled()
starStamp = [bytearray(b'\x00\x60\xa0\x40\x00'),
             bytearray(b'\x00\xc0\xe0\x60\x00')]
ship = bytearray(b'\x40\xf0\x78\xf0\x40')
starX, starY, star, speed = [0] * 5, [0] * 5, [0] * 5, [0] * 5
for i in range(0, 5):
    star[i], starX[i], v = init_star(i)
    speed[i], starY[i] = v, -v
shipX,  score, shipX0 = 32,  0, 32
gameOver=False
while not gameOver:
    for i in range(0, 5):
        shipX = shipX - 1 if (A.is_pressed() and shipX > 0) else shipX
        shipX = shipX + 1 if (B.is_pressed() and shipX < 58) else shipX
        mv_stmp(shipX0, 23, shipX, 23, ship)
        shipX0 = shipX
        x, y, v = starX[i], starY[i], speed[i]
        stmp = starStamp[star[i]]
        if y + v > 23:
            score+=1
            draw_stamp(x, y, stmp, 0, 1)
            s, x, v = init_star(i)
            star[i] = s
            stmp = starStamp[s]
            starX[i] = x
            starY[i], speed[i], y = -v, v, -v
        if y == -v:
            y0 = 0
        else:
            y0 = y
        y = y + v
        starY[i] = y
        mv_stmp(x, y0, x, y, stmp)
        if y > 19:
            if not ((x + 4 < shipX or shipX + 4 < x
                     ) or (y + 7 < 27 or 31 < y + 4)):
                show_bitmap("game_over")
                D.scroll("Score: " + str(score))
                gameOver=True
                break
