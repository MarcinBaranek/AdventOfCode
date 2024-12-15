# coding=utf-8
from copy import deepcopy
from base_board import BaseBoard


class Board(BaseBoard):
    def __init__(self, map_lines: list[list[str]], moves: str) -> None:
        super().__init__(map_lines, moves)
        self.robot = self.find_robot()

    def step(self, direction: str) -> None:
        i, j = self.map_direction(direction)
        map_char = self.map_lines[self.robot.row + i][self.robot.col + j]
        match map_char:
            case ".": self.robot.move(i, j)
            case "#": return
            case "O": self.robot.move(i, j) if self.push(i, j) else None
            case _: raise ValueError(f"Invalid map char: {map_char}")

    def push(self, i: int, j: int) -> bool:
        row_diff = i + (-1 if i < 0 else i > 0)
        col_diff = j + (-1 if j < 0 else j > 0)
        next_row = self.robot.row + i + (-1 if i < 0 else i > 0)
        next_col = self.robot.col + j + (-1 if j < 0 else j > 0)
        next_element = self.map_lines[next_row][next_col]
        if next_element == "#":
            return False
        if next_element == "O" and not self.push(row_diff, col_diff):
            return False
        self.map_lines[next_row][next_col] = "O"
        self.map_lines[self.robot.row + i][self.robot.col + j] = "."
        return True


class DoubledBoard(BaseBoard):
    def __init__(self, map_lines: list[list[str]], moves: str) -> None:
        super().__init__(map_lines, moves)
        self.double_map()
        self.robot = self.find_robot()

    def double_map(self) -> None:
        new_map_lines = []
        for line in self.map_lines:
            new_line = []
            for char in line:
                if char == "@":
                    new_line.append("@")
                    new_line.append(".")
                elif char == "#":
                    new_line.append("#")
                    new_line.append("#")
                elif char == "O":
                    new_line.append("[")
                    new_line.append("]")
                elif char == ".":
                    new_line.append(".")
                    new_line.append(".")
                else:
                    raise ValueError(f"Invalid char: {char}")
            new_map_lines.append(new_line)
        self.map_lines = new_map_lines

    def step(self, direction: str) -> None:
        i, j = self.map_direction(direction)
        map_char = self.map_lines[self.robot.row + i][self.robot.col + j]
        match map_char:
            case ".": self.robot.move(i, j)
            case "#": return
            case "[":
                if i == 0 and self.push_horizontally(j):
                    self.robot.move(i, j)
                if (j == 0
                        and self.is_box_pushable_vertically(i, self.robot.col)
                ):
                    self.push_vertically(i, self.robot.row + i, self.robot.col)
                    self.robot.move(i, j)
            case "]":
                if i == 0 and self.push_horizontally(j):
                    self.robot.move(i, j)
                if (j == 0
                        and self.is_box_pushable_vertically(
                            i, self.robot.col -1
                        )
                ):
                    self.push_vertically(
                        i, self.robot.row + i, self.robot.col - 1
                    )
                    self.robot.move(i, j)
            case _: raise ValueError(f"Invalid map char: {map_char}")

    def push_horizontally(self, j: int) -> bool:
        if j > 0:
            next_element = \
                self.map_lines[self.robot.row][self.robot.col + j + 2]
            if next_element == "#":
                return False
            if next_element == "[" and not self.push_horizontally(j + 2):
                return False
            self.map_lines[self.robot.row][self.robot.col + j + 1] = "["
            self.map_lines[self.robot.row][self.robot.col + j + 2] = "]"
            self.map_lines[self.robot.row][self.robot.col + j] = "."
            return True
        else:
            next_element =\
                self.map_lines[self.robot.row][self.robot.col + j - 2]
            if next_element == "#":
                return False
            if next_element == "]" and not self.push_horizontally(j - 2):
                return False
            self.map_lines[self.robot.row][self.robot.col + j - 2] = "["
            self.map_lines[self.robot.row][self.robot.col + j - 1] = "]"
            self.map_lines[self.robot.row][self.robot.col + j] = "."
            return True

    def is_box_pushable_vertically(self, i: int, col: int) -> bool:
        box_cols = col, col + 1
        shift = 1 if i > 0 else -1
        flags = []
        first_next_element =\
            self.map_lines[self.robot.row + i + shift][box_cols[0]]
        second_next_element = \
            self.map_lines[self.robot.row + i + shift][box_cols[1]]
        if first_next_element == "#" or second_next_element == "#":
            return False
        if first_next_element == "[":
            return self.is_box_pushable_vertically(i + shift, box_cols[0])
        if first_next_element == "]":
            flags.append(
                self.is_box_pushable_vertically(i + shift, box_cols[0] - 1)
            )
        else:
            flags.append(True)
        if second_next_element == "[":
            flags.append(
                self.is_box_pushable_vertically(i + shift, box_cols[1])
            )
        else:
            flags.append(True)
        return all(flags)

    def push_vertically(self, shift: int, row: int, col: int) -> None:
        box_cols = col, col + 1
        first_next_element = self.map_lines[row + shift][box_cols[0]]
        second_next_element = self.map_lines[row + shift][box_cols[1]]
        if first_next_element == "[":
            self.push_vertically(shift, row + shift, box_cols[0])
        if first_next_element == "]":
            self.push_vertically(shift, row + shift, box_cols[0] - 1)
        if second_next_element == "[":
            self.push_vertically(shift, row + shift, box_cols[1])
        self.map_lines[row + shift][col] = "["
        self.map_lines[row][col] = "."
        self.map_lines[row + shift][col + 1] = "]"
        self.map_lines[row][col + 1] = "."


def main():
    with open('input.txt') as f:
        map_lines = []
        moves = ""
        for line in f.readlines():
            if line.startswith("#"):
                map_lines.append(list(line.strip()))
            elif line == "\n":
                continue
            else:
                moves += line.strip()

    doubled_board = DoubledBoard(deepcopy(map_lines), moves)
    board = Board(map_lines, moves)
    board.go()
    result = board.sum_gps_coordinates()
    doubled_board.go()
    result2 = doubled_board.sum_gps_coordinates()
    assert result == 1559280
    assert result2 == 1576353
    print(f"{result=}, {result2=}")


if __name__ == '__main__':
    main()
