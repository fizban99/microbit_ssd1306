from ssd1306 import initialize, create_stamp
from ssd1306 import draw_stamp, clear_oled, add_text
from microbit import accelerometer, sleep, Image
from random import randint


def move_stamp(x1, y1, x2, y2, stmp):
    draw_stamp(x1, y1, stmp, 0, 0)
    draw_stamp(x2, y2, stmp, 1, 1)


initialize()
# show_bitmap("microbit_logo")
sleep(2000)
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
    if ax < x + 5 and ax > x and ay > y + 1 and ay < y + 7:
        add_text(2, 2, "GAME OVER")
        add_text(2, 3, "Score: " + str(score))
        sleep(4000)
        clear_oled()
        ay = 0
