#!/usr/bin/env python3

import cs50
import re

# regex to identify digits
regex = '^[0-9]+$'


def isdigit(str):
    return re.search(regex, str)


def is_checksum_valid(ccnum):
    length = len(ccnum)

    sum1 = 0
    start = length-2
    while (start >= 0):
        tmp = int(ccnum[start:start+1]) * 2
        if tmp < 10:
            sum1 = sum1 + tmp
        else:
            sum1 = sum1 + int(tmp/10) + int(tmp % 10)
        start = start - 2
        print("..sum1 %d" % sum1)

    sum2 = sum1
    start = length-1
    while (start >= 0):
        sum2 = sum2 + int(ccnum[start:start+1])
        start = start - 2
        print("..sum2 %d" % sum2)

    print("sum1 %d sum2 %d ccnum [%s]" % (sum1, sum2, ccnum))

    return (int(sum2 % 10) == 0)


def get_cc_type(ccnum):
    type = "INVALID"
    ccnum_len = len(ccnum)
    first_one = int(ccnum[0:1])
    first_two = int(ccnum[0:2])

    if ((first_two == 34 or first_two == 37) and ccnum_len == 15):
        type = "AMEX"
    elif (first_two >= 51 and first_two <= 55 and ccnum_len == 16):
        type = "MASTERCARD"
    elif (first_one == 4 and (ccnum_len == 13 or ccnum_len == 16)):
        type = "VISA"

    if type != "INVALID" and not is_checksum_valid(ccnum):
        type = "INVALID"

    return type


ccnum = cs50.get_string("Enter a CC number: ")
while (not isdigit(ccnum)):
    ccnum = cs50.get_string("Number: ")

print("%s" % get_cc_type(ccnum))
