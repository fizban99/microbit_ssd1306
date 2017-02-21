from ssd1306 import initialize,create_stamp,show_bitmap,draw_stamp,clear_oled
from gc import mem_free
from microbit import accelerometer,sleep,Image

print("Started")
initialize()
print(mem_free())
show_bitmap("microbit_logo")
sleep(2000)
clear_oled()
stamp = create_stamp(Image.HEART)
(x, y) = (32, 16)
(x0, y0) = (x, y)
while True:
    reading = accelerometer.get_x()
    if reading > 20:
        if x < 58:
            x += 1
    elif reading < -20:
        if x > 0:
            x -= 1

    reading = accelerometer.get_y()
    if reading > 20 and y < 23:
        y += 1

    elif reading < -20 and y > 0:
        y -= 1

    if x0 != x or y0 != y:
        draw_stamp(x0, y0, stamp, 0, 0)
        draw_stamp(x, y, stamp, 1, 1)
        (x0, y0) = (x, y)
print("Done")
