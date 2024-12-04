#!/usr/bin/env python3

import cs50

height = cs50.get_int("What's the pyramid height? ")
while (height <= 0 or height > 8):
    height = cs50.get_int("Please enter a height between 1 and 8..: ")

for ii in range(1, height + 1, 1):
    str = ""
    for jj in range(0, height - ii, 1):
        str += " "
    for jj in range(0, ii, 1):
        str += "#"
    str += "  "
    for jj in range(0, ii, 1):
        str += "#"
    print(str)
