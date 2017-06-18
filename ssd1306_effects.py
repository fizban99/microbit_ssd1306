from microbit import sleep

from ssd1306 import command


def blink(time=1000):
    for c in ([0xae], [0xaf]):
        command(c)
        sleep(time / 2)


def pulse(time=500):
    per_step = time / 25
    r = [[250, 0, -10], [0, 250, 10]]
    for (x, y, z) in r:
        for i in range(x, y, z):
            command([0x81, i])
            sleep(per_step)
    command([0x81, 0xcf])
