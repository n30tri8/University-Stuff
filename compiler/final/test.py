import math


def f(x):
    t1 = 1 + math.sin(x*math.pi/4)
    t2 = 2 + math.cos(x * math.pi / 4)
    return x*t1/t2


for x in range(-16, 16):
    print(str(x) + '  :  ' + str(f(x)))