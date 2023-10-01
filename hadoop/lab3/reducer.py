#!/usr/bin/python3.10

import json
import sys


class Reducer:

    def __init__(self, graph_length: int):
        self._current_node = {}
        self._current_node_id = None
        self._current_sum = 0
        self._graph_length = graph_length

    def _reduce_line(self, line: str, separator: str = "\t"):
        node_id, label, info = line.split(separator)

        if node_id == self._current_node_id:
            if label == "pagerank":
                self._current_sum += float(info)
            elif label == "node":
                self._current_node = json.loads(info)
        else:
            if self._current_node_id is not None and (
                    self._current_node is not None):
                self._current_node["pr"] = (0.15 / float(self._graph_length) +
                                            0.85 * self._current_sum)
                result = json.dumps(self._current_node)
                print(f"{self._current_node_id}{separator}{result}")
                self._current_sum = 0
                self._current_node = None
            if label == "node":
                self._current_sum = 0
                self._current_node = json.loads(info)
                self._current_node_id = node_id
            elif label == "pagerank":
                self._current_sum += float(info)

    def reduce(self, stream):
        for line in stream:
            self._reduce_line(line, "\t")


if __name__ == "__main__":
    reducer = Reducer(graph_length=316)
    reducer.reduce(sys.stdin)
