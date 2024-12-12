# coding=utf-8
from itertools import product


class Board:
    def __init__(self, lines: list[str]) -> None:
        self.map = list(list(map(int, line)) for line in lines)

    def get_neighbors(self, point: tuple[int, int]) -> set[tuple[int, int]]:
        result: set[tuple[int, int]] = set()
        value = self.map[point[0]][point[1]]
        if point[0] > 0 and value + 1 == self.map[point[0] - 1][point[1]]:
            result.add((point[0] - 1, point[1]))
        if point[0] < len(self.map) - 1\
                and value + 1 == self.map[point[0] + 1][point[1]]:
            result.add((point[0] + 1, point[1]))
        if point[1] > 0 and value + 1 == self.map[point[0]][point[1] - 1]:
            result.add((point[0], point[1] - 1))
        if point[1] < len(self.map[0]) - 1\
                and value + 1 == self.map[point[0]][point[1] + 1]:
            result.add((point[0], point[1] + 1))
        return result

    def walk(self, start_point: tuple[int, int]) -> set[tuple[int, int]]:
        result = set()
        if self.map[start_point[0]][start_point[1]] == 9:
            result.add(start_point)
            return result
        for point in self.get_neighbors(start_point):
            for res in self.walk(point):
                result.add(res)
        return result

    def count_scores(self) -> int:
        total = 0
        for i, j in product(range(len(self.map)), range(len(self.map[0]))):
            if self.map[i][j] == 0:
                total += len(self.walk((i, j)))
        return total

    def walk_for_ratings(self, start_point: tuple[int, int]) -> int:
        result = 0
        if self.map[start_point[0]][start_point[1]] == 9:
            return 1
        for point in self.get_neighbors(start_point):
            result += self.walk_for_ratings(point)
        return result

    def count_ratings(self) -> int:
        total = 0
        for i, j in product(range(len(self.map)), range(len(self.map[0]))):
            if self.map[i][j] == 0:
                total += self.walk_for_ratings((i, j))
        return total


def main():
    with open('input.txt') as f:
        board = Board([line.strip() for line in f.readlines()])


    result = board.count_scores()
    result2 = board.count_ratings()
    assert result == 644
    assert result2 == 1366
    print(f"{result=}, {result2=}")


if __name__ == '__main__':
    main()
