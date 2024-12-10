# coding=utf-8
from dataclasses import dataclass, field


@dataclass
class FrequencyBoard:
    char: str
    rows: int
    cols: int
    positions: set[tuple[int, int]] = field(default_factory=set)

    def add(self, position: tuple[int, int]) -> None:
        self.positions.add(position)

    @staticmethod
    def calc_anti_nodes(
            first: tuple[int, int],
            second: tuple[int, int]
    ) -> set[tuple[int, int]]:
        result = set()
        result.add(
            (
                    first[0] + (first[0] - second[0]),
                    first[1] + (first[1] - second[1])
            )
        )
        result.add(
            (
                second[0] + (second[0] - first[0]),
                second[1] + (second[1] - first[1])
            )
        )
        return result

    def calc_t_anti_nodes(
            self,
            first: tuple[int, int],
            second: tuple[int, int]
    ) -> set[tuple[int, int]]:
        result = set()
        left_diffs = (first[0] - second[0], first[1] - second[1])
        right_diffs = (second[0] - first[0], second[1] - first[1])
        flags = [True, True]
        for i in range(1, max(self.rows, self.cols)):

            node = (first[0] + i * left_diffs[0], first[1] + i * left_diffs[1])
            if 0 <= node[0] < self.rows and 0 <= node[1] < self.cols:
                result.add(node)
                continue
            else:
                flags[0] = False
            node = (
                second[0] + i * right_diffs[0],
                second[1] + i * right_diffs[1]
            )
            if 0 <= node[0] < self.rows and 0 <= node[1] < self.cols:
                result.add(node)
                continue
            else:
                flags[1] = False
            if not flags[0] and not flags[1]:
                break

        return result

    def find_anti_nodes(self) -> set[tuple[int, int]]:
        result = set()
        for antenna in self.positions:
            for other in self.positions:
                if antenna == other:
                    continue
                for anti_node in self.calc_anti_nodes(antenna, other):
                    result.add(anti_node)
        return result

    def find_t_anti_nodes(self) -> set[tuple[int, int]]:
        result = set()
        for antenna in self.positions:
            result.add(antenna)
            for other in self.positions:
                if antenna == other:
                    continue
                for anti_node in self.calc_t_anti_nodes(antenna, other):
                    result.add(anti_node)
        return result

class Board:
    def __init__(self, lines: list[str]):
        self.rows = len(lines)
        self.cols = len(lines[0])
        self.antennas: dict[str, FrequencyBoard] = {}
        for i, line in enumerate(lines):
            for j, char in enumerate(line):
                if char == ".":
                    continue
                if char not in self.antennas:
                    self.antennas[char] =\
                        FrequencyBoard(char, self.rows, self.cols)
                self.antennas[char].add((i, j))

    def calc_anit_nodes(self) -> int:
        result = set()
        for frequency in self.antennas.values():
            for node in frequency.find_anti_nodes():
                if 0 <= node[0] < self.rows and 0 <= node[1] < self.cols:
                    result.add(node)

        return len(result)


    def calc_t_anti_nodes(self) -> int:
        result = set()
        for frequency in self.antennas.values():
            for node in frequency.find_t_anti_nodes():
                if 0 <= node[0] < self.rows and 0 <= node[1] < self.cols:
                    result.add(node)

        return len(result)


def main():
    with open('input.txt') as f:
        solver = Board(
            [line.strip() for line in f.readlines()]
        )
    result = solver.calc_anit_nodes()
    result_t = solver.calc_t_anti_nodes()
    assert result == 271
    assert result_t == 994
    print(f"{result=}, {result_t=}")


if __name__ == '__main__':
    main()
