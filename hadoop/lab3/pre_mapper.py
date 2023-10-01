#!/usr/bin/python3.10

import json
import sys


def process(line: str, separator: str = "\t") -> str:
    _line = line.strip()
    pages = _line.split(separator)

    if len(pages) == 0:
        return ""

    _node = {
        "adjacent": pages[1:],
        "pr": 1
    }
    yield f"{pages[0]}{separator}node{separator}{json.dumps(_node)}"

    pagerank = 1 / (len(pages[1:]) if len(pages[1:]) != 0 else 1)
    for i in range(1, len(pages)):
        yield f"{pages[i]}{separator}pagerank{separator}{pagerank}"


if __name__ == "__main__":
    for line in sys.stdin:
        for node in process(line):
            print(node)
