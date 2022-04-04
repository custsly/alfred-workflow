import random


def build_hex_color(r, g, b):
    return '#%02X%02X%02X' % (r, g, b)


def hsv_to_rgb(h, s, v):
    if s == 0.0:
        v *= 255
        return v, v, v
    i = int(h * 6.)
    f = (h * 6.) - i
    p, q, t = int(255 * (v * (1. - s))), int(255 * (v * (1. - s * f))), int(255 * (v * (1. - s * (1. - f))))
    v = int(v * 255)
    i = int(i % 6)
    if i == 0:
        return v, t, p
    if i == 1:
        return q, v, p
    if i == 2:
        return p, v, t
    if i == 3:
        return p, q, v
    if i == 4:
        return t, p, v
    if i == 5:
        return v, p, q


def random_hsv_color_generator(s, v, n):
    counter = 0
    while True:
        if counter > n:
            return
        yield random.randint(0, 360) / 360, s, v
        counter += 1


def random_hex_color_generator(s, v, n):
    counter = 0
    while True:
        if counter > n:
            return
        yield build_hex_color(*hsv_to_rgb(random.randint(0, 360) / 360, s, v))
        counter += 1


def random_hsv_color():
    return random.randint(0, 360) / 360, random.randint(0, 100) / 100, random.randint(0, 100) / 100


def random_rgb_color():
    return '#%02X%02X%02X' % (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
