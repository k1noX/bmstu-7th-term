#!/usr/bin/python3.10

import json
import sys


def process(line: str, separator: str = "\t") -> str:
    _line = line.strip()
    node_id, info = _line.split(separator)
    _node = json.loads(info)

    yield f"{_node['pr']}{separator}{node_id}"


if __name__ == "__main__":
    for line in sys.stdin:
        for node in process(line):
            print(node)
