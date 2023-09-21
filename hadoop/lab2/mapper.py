#!/usr/bin/python3.10

import sys

line_number = 1
print("(")
for line in sys.stdin:
    line = line.strip()
    words = line.split()
    for word in words:
        print(f"({word} ({line_number}))", end=",\n")
    line_number += 1
print(")")
