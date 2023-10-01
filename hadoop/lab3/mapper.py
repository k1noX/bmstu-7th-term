#!/usr/bin/python3.10

import json
import sys


def process(line: str, separator: str = "\t") -> str:
    _line = line.strip()
    node_id, info = _line.split(separator)
    _node = json.loads(info)

    yield f"{node_id}{separator}node{separator}{json.dumps(_node)}"

    adjacent = _node["adjacent"]
    pagerank = _node["pr"] / (len(adjacent) if len(adjacent) != 0 else 1)

    for i in range(len(adjacent)):
        yield f"{adjacent[i]}{separator}pagerank{separator}{pagerank}"


if __name__ == "__main__":
    for line in sys.stdin:
        for node in process(line):
            print(node)
