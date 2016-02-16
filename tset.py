#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Macpotty
# @Date:   2016-02-14 10:34:46
# @Last Modified by:   Macpotty
# @Last Modified time: 2016-02-14 17:14:45
# Just a dynamic test program for learning.
import threading
import time


def wait():
    print("wait")
    time.sleep(1)
    return

if __name__ == '__main__':
    for i in range(10):
        t = threading.Thread(target=wait)
        t.start()

    print("current has %d threads" % (threading.activeCount()-1))

    for item in threading.enumerate():
        print(item)
