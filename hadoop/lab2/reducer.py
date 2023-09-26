#!/usr/bin/python3.10

import re
import sys

current_word = None
current_locations = []
word = None
print("(")
for line in sys.stdin:
    regex = re.compile(r"\(\S+\s\(\d+(?:\s+\d+)*\)\)")
    matches = regex.findall(line)
    matches.sort()
    for word_with_info in matches:
        word_with_info = word_with_info.strip("(),")
        word, appearances = word_with_info.split(" ")
        word = word.lower()
        locations = appearances.strip("()\n,")
        locations = locations.split(" ")
        if current_word == word:
            current_locations.append(*locations)
            current_locations = list(set(current_locations))
        else:
            if current_word:
                print(
                    f'({current_word} ({" ".join(current_locations)}))',
                    end=",\n"
                )
            current_locations = locations
            current_word = word
if current_word == word:
    print(f'({current_word} ({" ".join(current_locations)}))')
print(")", end="")
