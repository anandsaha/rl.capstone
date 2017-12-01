"""
Various utility functions

(c) Anand Saha <anandsaha@gmail.com> 2017
"""
import numpy as np
import decimal
import datetime

LOG_FILE = 'qtables/log.txt'


def distance(pos1, pos2):
    x2 = np.square(pos1[0] - pos2[0])
    y2 = np.square(pos1[1] - pos2[1])
    z2 = np.square(pos1[2] - pos2[2])

    return np.sqrt(x2 + y2 + z2)


def log_and_display(msg):
    stat_file = open(LOG_FILE, 'a')
    content = "[{0}] {1}\n".format(datetime.datetime.now(), msg)
    stat_file.write(content)
    stat_file.close()
    print(content, end="")


def rnd(val, to='0.01'):
    return decimal.Decimal(val).quantize(decimal.Decimal(to), decimal.ROUND_HALF_DOWN)
