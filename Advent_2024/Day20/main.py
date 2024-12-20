# coding=utf-8
from __future__ import annotations
from collections import deque, defaultdict
from dataclasses import dataclass
from typing import Deque
from functools import lru_cache


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
class Point:
    row: int
    col: int

    def __sub__(self, other: Point | Shift) -> Shift | Point:
        if isinstance(other, Point):
            return Shift(self.row - other.row, self.col - other.col)
        if isinstance(other, Shift):
            return Point(
                self.row - other.row_shift,
                self.col - other.col_shift
            )

    def __add__(self, other: Shift) -> Point:
        return Point(
            self.row + other.row_shift,
            self.col + other.col_shift,
        )


class MazeExplorer:
    def __init__(self, map_lines: list[str]) -> None:
        self.map_lines = map_lines
        self.scores = defaultdict(lambda: 2**50)

    def reset(self) -> None:
        self.scores = defaultdict(lambda: 2**50)


    def get_neighbors(self, node: Point) -> set[Point]:
        result: set[Point] = set()
        for shift in get_shifts():
            new = node + shift
            if not (
                    0 <= new.row < len(self.map_lines)
                    and 0 <= new.col < len(self.map_lines[0])
            ):
                continue
            if self.map_lines[new.row][new.col] == "#":
                continue
            result.add(new)
        return result

    def bfs_scorer(self, start: Point):
        queue: Deque[Point] = deque()
        queue.append(start)
        self.scores[start] = 0
        while queue:
            node = queue.popleft()
            for neighbor in self.get_neighbors(node):
                distance = self.scores[node] + 1
                if distance < self.scores[neighbor]:
                    self.scores[neighbor] = distance
                    queue.append(neighbor)


    def show(self) -> None:
        for row, line in enumerate(self.map_lines):
            for col, char in enumerate(line):
                if char == "#":
                    print(char, end="\t")
                    continue
                point = Point(row, col)
                if point in self.scores:
                    print(self.scores[point], end="\t")
                else:
                    print(".", end="\t")
            print("")


    @lru_cache(maxsize=None)
    def cheated_neighbors(self, node: Point, chunks: 2) -> set[Point]:
        result: set[Point] = set()
        if chunks == 0:
            return result
        for shifts in get_shifts():
            new = node + shifts
            result.add(new)
            for other in self.cheated_neighbors(new, chunks - 1):
                result.add(other)
        return result

    def bfs_cheated_scorer(
            self, start: Point,
            threshold: int,
            end: Point,
            cheat_chunks_number: int = 2
    ) -> int:
        counter = 0
        queue: Deque[Point] = deque()
        queue.append(start)
        visited = set()
        while queue:
            node = queue.popleft()
            visited.add(node)
            if self.scores[node] - self.scores[end] < threshold:
                continue
            for neighbor in self.get_neighbors(node):
                if neighbor not in visited:
                    queue.append(neighbor)
            for neighbor in self.cheated_neighbors(
                    node, chunks=cheat_chunks_number
            ):
                diff = (self.scores[node]
                        - self.scores[neighbor]
                        - abs(node.row - neighbor.row)
                        - abs(node.col - neighbor.col))
                if diff >= threshold:
                    counter += 1
        return counter


def main():
    with open('input.txt') as f:
        solver = MazeExplorer([line.strip() for line in f.readlines()])

    start = Point(0, 0)
    end = Point(0, 0)
    for row, line in enumerate(solver.map_lines):
        for col, char in enumerate(line):
            if char == "S":
                start = Point(row, col)
            if char == "E":
                end = Point(row, col)

    solver.bfs_scorer(start=end)
    result = solver.bfs_cheated_scorer(
        start=start, threshold=100, end=end
    )
    result2 = solver.bfs_cheated_scorer(
        start=start, threshold=100, end=end, cheat_chunks_number=20
    )
    print(f"{solver.scores[start]=}")
    print(f"{result=}, {result2=}")


if __name__ == '__main__':
    main()
