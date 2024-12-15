# coding=utf-8
from dataclasses import dataclass
from abc import ABCMeta, abstractmethod


@dataclass
class Robot:
    row: int
    col: int

    def move(self, diff_row: int, diff_col: int) -> None:
        self.row += diff_row
        self.col += diff_col


class BaseBoard(metaclass=ABCMeta):
    def __init__(self, map_lines, moves):
        self.map_lines = map_lines
        self.moves = moves
        self.robot = None

    def find_robot(self) -> Robot:
        for i, line in enumerate(self.map_lines):
            for j, char in enumerate(line):
                if char == "@":
                    self.map_lines[i][j] = "."
                    return Robot(i, j)

    @staticmethod
    def map_direction(direction: str) -> tuple[int, int]:
        match direction:
            case "^": return -1, 0
            case ">": return 0, 1
            case "<": return 0, -1
            case "v": return 1, 0
            case _: raise ValueError(f"Invalid direction: {direction}")

    @abstractmethod
    def step(self, direction: str):
        pass

    def go(self) -> None:
        for direction in self.moves:
            self.step(direction)

    def show(self) -> None:
        for i, line in enumerate(self.map_lines):
            if self.robot.row != i:
                print("".join(line))
            else:
                result = ""
                for j, char in enumerate(line):
                    if j == self.robot.col:
                        result += "@"
                        continue
                    result += char
                print(result)

    def sum_gps_coordinates(self) -> int:
        count = 0
        for i, line in enumerate(self.map_lines):
            for j, char in enumerate(line):
                if char == "O" or char == "[":
                    count += 100 * i + j
        return count