# coding=utf-8
from __future__ import annotations
from collections import deque, defaultdict
from dataclasses import dataclass
from typing import Optional, Deque

MAX_COLS=71
MAX_ROWS=71


@dataclass(frozen=True)
class Shift:
    row_shift: int
    col_shift: int


def get_shifts() -> tuple[Shift, ...]:
    return (
        Shift(row_shift=1, col_shift=0),
        Shift(row_shift=-1, col_shift=0),
        Shift(row_shift=0, col_shift=1),
        Shift(row_shift=0, col_shift=-1),
    )


@dataclass(frozen=True)
class Node:
    row: int
    col: int

    def __sub__(self, other: Node | Shift) -> Shift | Node:
        if isinstance(other, Node):
            return Shift(self.row - other.row, self.col - other.col)
        if isinstance(other, Shift):
            return Node(self.row - other.row_shift, self.col - other.col_shift)

    def __add__(self, other: Shift) -> Node:
        return Node(
            self.row + other.row_shift,
            self.col + other.col_shift,
        )


class TurningCounter:
    def __init__(self, map_lines: list[list[str]]) -> None:
        self.map_lines = map_lines
        self.visited = [[False] * MAX_COLS for _ in range(MAX_ROWS)]
        self.scores = defaultdict(lambda: 2**50)
        self.parents: dict[Node, Optional[Node]] = {}

    def reset(self) -> None:
        self.parents = {}
        self.scores = defaultdict(lambda: 2**50)
        self.visited = [[False] * MAX_COLS for _ in range(MAX_ROWS)]

    def get_neighbors(self, node: Node) -> set[Node]:
        result: set[Node] = set()
        for shift in get_shifts():
            new = node + shift
            if not (0 <= new.row < MAX_ROWS and 0 <= new.col < MAX_COLS):
                continue
            if self.map_lines[new.row][new.col] == "#":
                continue
            result.add(new)
        return result

    def calc_distance(self, parent: Node, child: Node) -> int:
        return self.scores[parent] + 1

    def bfs_scorer(self, start: Node):
        queue: Deque[Node] = deque()
        queue.append(start)
        self.scores[start] = 0
        self.parents[start] = None
        while queue:
            node = queue.popleft()
            self.visited[node.row][node.col] = True
            for neighbor in self.get_neighbors(node):
                dist = self.calc_distance(node, neighbor)
                if dist < self.scores[neighbor]:
                    self.scores[neighbor] = dist
                    self.parents[neighbor] = node
                    queue.append(neighbor)


    def minimum_score(self) -> int:
        start_node = Node(0, 0)
        end_node = Node(MAX_ROWS - 1, MAX_COLS - 1)
        self.bfs_scorer(start_node)
        score = self.scores[end_node]
        return score


def main():
    board = TurningCounter([["."] * MAX_COLS for _ in range(MAX_ROWS)])
    with open('input.txt') as f:
        line_iterator = iter(f.readlines())
        counter = 0
        while True:
            if counter >= 1024:
                break
            counter += 1
            line = next(line_iterator)
            x, y = line.strip().split(",")
            if not (0 <= int(y) < MAX_COLS or 0 <= int(x) < MAX_ROWS):
                continue
            board.map_lines[int(x)][int(y)] = "#"

        result_2 = result = board.minimum_score()
        assert result == 326

        while result_2 < 2**50:
            board.reset()
            line = next(line_iterator)
            x, y = line.strip().split(",")
            if not (0 <= int(y) < MAX_COLS or 0 <= int(x) < MAX_ROWS):
                continue
            board.map_lines[int(x)][int(y)] = "#"
            result_2 = board.minimum_score()
    result_2 = f"{x},{y}"
    assert result_2 == "18,62"
    print(f"{result=}, {result_2=}")

if __name__ == '__main__':
    main()
