# coding=utf-8
from dataclasses import dataclass
from copy import deepcopy

@dataclass
class Guard:
    row: int
    col: int
    direction: str = "^"

    def move(self) -> None:
        match self.direction:
            case "^":
                self.row -= 1
            case ">":
                self.col += 1
            case "v":
                self.row += 1
            case "<":
                self.col -= 1
            case _:
                raise ValueError("Unknown direction")

    def change_direction(self) -> None:
        match self.direction:
            case "^":
                self.direction = ">"
            case ">":
                self.direction = "v"
            case "v":
                self.direction = "<"
            case "<":
                self.direction = "^"
            case _:
                raise ValueError("Unknown direction")

    def next_place(self) -> tuple[int, int]:
        match self.direction:
            case "^":
                return self.row - 1, self.col
            case ">":
                return self.row, self.col + 1
            case "v":
                return self.row + 1, self.col
            case "<":
                return self.row, self.col - 1
            case _:
                raise ValueError(f"Unknown direction: {self.direction}")


class Board:
    def __init__(self, map_lines: list[str], guard: Guard) -> None:
        self.map_lines = map_lines
        self.columns = len(map_lines[0])
        self.rows = len(map_lines)
        self.guard = guard

    def guard_in_board(self) -> bool:
        return 0 <= self.guard.row < self.rows \
            and 0 <= self.guard.col < self.columns

    def move_guard(self) -> tuple[int, int]:
        while not self.is_free_place(*self.guard.next_place()):
            self.guard.change_direction()
        self.guard.move()
        return self.guard.row, self.guard.col

    def is_free_place(self, row: int, col: int) -> bool:
        if row < 0 or col < 0 or row >= self.rows or col >= self.columns:
            return True
        try:
            return self.map_lines[row][col] != "#"
        except IndexError:
            return True


def search_guard(map_lines: list[str]) -> tuple[int, int]:
    for line_number, line in enumerate(map_lines):
        for i, char in enumerate(line):
            if char in ("^", ">", "v", "<"):
                return line_number, i


def visited_position(map_lines: list[str]) -> set[tuple[int, int]]:
    visited_positions: set[tuple[int, int]] = set()
    guard_position = search_guard(map_lines)
    guard = Guard(guard_position[0], guard_position[1])
    guard.direction = map_lines[guard.row][guard.col]
    board = Board(map_lines, guard)
    while board.guard_in_board():
        visited_positions.add((guard.row, guard.col))
        board.move_guard()
    return visited_positions


class VisitedPositionsTracker:
    def __init__(self):
        self.visited_positions: set[tuple[int, int, str]] = set()

    def add(self, guard: Guard) -> None:
        self.visited_positions.add((guard.row, guard.col, guard.direction))

    def reset(self) -> None:
        self.visited_positions = set()

    def was_visited(self, guard: Guard) -> bool:
        return (guard.row, guard.col, guard.direction) \
            in self.visited_positions


def count_new_obstructions(map_lines: list[str]) -> int:
    initial_position = search_guard(map_lines)
    initial_direction = map_lines[initial_position[0]][initial_position[1]]
    result = set()
    tracker = VisitedPositionsTracker()
    for i, j in visited_position(map_lines):
        if (i, j) == initial_position:
            continue
        tmp_map = deepcopy(map_lines)
        if j == 0:
            tmp_map[i] = "#" + tmp_map[i][1:]
        elif j == len(tmp_map[i]) - 1:
            tmp_map[i] = tmp_map[i][:-1] + "#"
        else:
            tmp_map[i] = tmp_map[i][:j] + "#" + tmp_map[i][j + 1:]
        board = Board(
            tmp_map, Guard(*initial_position, direction=initial_direction)
        )
        tracker.reset()
        while board.guard_in_board():
            if tracker.was_visited(board.guard):
                result.add((i, j))
                break
            tracker.add(board.guard)
            board.move_guard()
    return len(result)


def main():
    with open('input.txt') as f:
        lines: list[str] = [line.strip() for line in f.readlines()]
    result = len(visited_position(lines))
    result_for_part_2 = count_new_obstructions(lines)
    assert result == 4778
    assert result_for_part_2 == 1618
    print(f"{result}, {result_for_part_2}")


if __name__ == '__main__':
    main()
