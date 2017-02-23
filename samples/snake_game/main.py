from ssd1306 import initialize, clear_oled
from ssd1306_px import get_px, set_px
from microbit import accelerometer, button_b, button_a, sleep, display
from random import randint
from ssd1306_text import add_text
initialize()
clear_oled()
pixels = []
# returns -2 to 2 from -1024 to +1024, empirically calculated


def tilt_scale(a):
    a = a + 1024  # range 0 to 2048
    # < 512 = 0, 512-853(512+341) = 1, 853-1194 = 2,
    # 1194-1536 = 3,  1536-2048 = 4
    for i in [[512, -2], [853, -1], [1194, 0], [1536, 1]]:
        if a < i[0]:
            return i[1]
    return 2


def get_tilt():
    x, y, z = accelerometer.get_values()
    return tilt_scale(x), tilt_scale(y), tilt_scale(z)


def pick_speed(speed):
    while not button_b.is_pressed():
        add_text(4, 1, str(speed))
        if button_a.is_pressed():
            speed = speed - 1 if speed > 1 else 9
            sleep(200)
    return speed


speed = 9  # set default speed
# play game forever
while True:
    # blank screen
    clear_oled()
    end, won, tailJustMissed, score = False, False, False, 0
    xpos, ypos = 2, 2  # start in centre
    xv, yv = 1, 0  # start going right
    foodX, foodY = 0, 0
    # snake is a list of tuples which are coordinates
    snake = [(xpos, ypos), (xpos+1, ypos)]
    oldBrightness = 0  # start on dark pixel
    foodEaten, foodTimeout = True, 0
    # pick a speed, A reduces speed, B sets speed
    speed = pick_speed(speed)
    clear_oled()
    while not end:  # run until the game is over
            # loop until randomly found blank square
        while foodEaten or foodTimeout == 0:
            if foodTimeout == 0 and not foodEaten:
                set_px(foodX, foodY, 0)
            foodX, foodY = randint(0, 63), randint(0, 31)
            if get_px(foodX, foodY) == 0:
                foodEaten, foodTimeout = False, 70
        # clear_oled()  # blank screen
        set_px(foodX, foodY, 1)  # draw food

        xt, yt, zt = get_tilt()
        # if tilting x more than y, and currently moving in y direction (to
        # avoid going back on yourself), change x
        if abs(xt) > abs(yt) and xv == 0:
            # change x
            xv, yv = 1 if xt > 0 else -1, 0
        # if tilting y more than x, and currently moving in x direction (to
        # avoid going back on yourself), change y
        elif abs(yt) > abs(xt) and yv == 0:
            # change y
            yv, xv = 1 if yt > 0 else -1, 0

        headx, heady = snake[-1]  # old head is last item in snake list
        # new head, mod 64 or 32 to wrap around
        newheadx, newheady = (headx + xv) % 64, (heady + yv) % 32

        for coord in snake[1:]:  # draw snake, without new head
            xpos, ypos = coord
            # make current position
            set_px(xpos, ypos, 1)

        newpixel = get_px(newheadx, newheady)
        # if newpixel is 0, 1, or tail of snake
        tailJustMissed = (newheadx, newheady) == snake[
            0]  # if tail of snake, delete tail
        if tailJustMissed:
            newpixel = 0
        if (((newheadx, newheady) == (foodX, foodY)
             ) and newpixel == 1) or newpixel == 0:
            # didn't hit ourself
            snake.append((newheadx, newheady))
            set_px(newheadx, newheady, 1)
        else:  # did hit ourself
            end = True
        if newpixel == 0:  # blank pixel to move to
            if not tailJustMissed:
                set_px(snake[0][0], snake[0][1], 0)
            del snake[0]
        elif (newheadx, newheady) == (foodX, foodY):  # eaten the food
            foodEaten = True
            score += (10 - speed)  # more points for faster game
        # higher the speed, slower the game
        foodTimeout -= 1
        sleep(speed * 10)
    display.scroll("Score " + str(score))
