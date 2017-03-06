from ssd1306 import initialize, clear_oled
from ssd1306_stamp import draw_stamp
from ssd1306_img import create_stamp
from ssd1306_text import add_text
from microbit import accelerometer, sleep, Image
from random import randint


def move_stamp(x1, y1, x2, y2, stmp):
    draw_stamp(x1, y1, stmp, 0, 0)
    draw_stamp(x2, y2, stmp, 1, 1)


initialize()
clear_oled()
stamp = create_stamp(Image.HEART)
arrow = create_stamp(Image.ARROW_S)
(x, y, ax, ay, score) = (0, 16, 32, 0, 0)
(x0, y0, ax0, ay0) = (x, y, ax, ay)
while True:
    reading = accelerometer.get_x()
    x = x + 1 if (reading > 20 and x < 58) else x
    x = x - 1 if (reading < -20 and x > 0) else x
    reading = accelerometer.get_y()
    y = y + 1 if (reading > 20 and y < 23) else y
    y = y - 1 if (reading < -20 and y > 0) else y
    if x0 != x or y0 != y:
        move_stamp(x0, y0, x, y, stamp)
        (x0, y0) = (x, y)
    (ay, ax) = (ay + 1, ax) if ay < 31 else (0, randint(0, 58))
    move_stamp(ax0, ay0, ax, ay, arrow)
    (ax0, ay0) = (ax, ay)
    if x == 58:
        x = 0
        score = score + 1
        add_text(2, 3, "Score: " + str(score))
        sleep(1000)
        clear_oled()
    if not ((ax + 5 < x or x + 5 < ax) or (ay + 7 < y + 1 or y + 7 < ay+1)):
        add_text(2, 1, "GAME OVER")
        add_text(2, 3, "Score: " + str(score))
        sleep(4000)
        clear_oled()
        (score, ay, x)=(0, 0, 0)
