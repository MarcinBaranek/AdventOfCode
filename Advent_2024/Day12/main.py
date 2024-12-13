# coding=utf-8
from itertools import product
from dataclasses import dataclass


@dataclass(frozen=True)
class PerimeterPoint:
    row: int
    col: int
    linked_point: tuple[int, int]
    horizontal_connection: bool


@dataclass
class EdgeCounter:
    region_points: set[tuple[int, int]]
    perimeter_points: list[PerimeterPoint]

    @staticmethod
    def get_potential_perimeter_points(
            perimeter_point: PerimeterPoint
    ) -> set[PerimeterPoint]:
        diff = (
            int(not perimeter_point.horizontal_connection),
            int(perimeter_point.horizontal_connection)
        )
        return {
            PerimeterPoint(
                row=perimeter_point.row + sign * diff[0],
                col=perimeter_point.col + sign *diff[1],
                linked_point=(
                    perimeter_point.linked_point[0] + sign *diff[0],
                    perimeter_point.linked_point[1] + sign * diff[1]
                ),
                horizontal_connection=perimeter_point.horizontal_connection
            )
            for sign in (-1, 1)
        }

    def build_edge(
            self, perimeter_point: PerimeterPoint,
            edge_items: set[PerimeterPoint]
    ) -> None:
        edge_items.add(perimeter_point)
        for potential_perimeter_point\
                in self.get_potential_perimeter_points(perimeter_point):
            if (
                    potential_perimeter_point in edge_items
                    or potential_perimeter_point not in self.perimeter_points
            ):
                continue
            self.perimeter_points.pop(
                self.perimeter_points.index(potential_perimeter_point)
            )
            self.build_edge(potential_perimeter_point, edge_items)

    def count(self) -> int:
        total = 0
        while self.perimeter_points:
            perimeter_point = self.perimeter_points.pop()
            self.build_edge(perimeter_point, set())
            total += 1
        return total


class Collector:
    def __init__(self, char):
        self.char = char
        self.regions: list[set[tuple[int, int]]] = []

    def belongs_to_region(self, row: int, col: int, region_idx: int) -> bool:
        for i, j in self.regions[region_idx]:
            diff = abs(row - i) + abs(col - j)
            if diff == 1:
                return True
        return False

    def add_to_region(self, row: int, col: int, region_idx: int) -> None:
        self.regions[region_idx].add((row, col))
        to_merge = []
        for other_idx in range(len(self.regions)):
            if other_idx == region_idx:
                continue
            if self.belongs_to_region(row, col, other_idx):
                to_merge.append(other_idx)
        if not to_merge:
            return
        for other_idx in to_merge:
            for element in self.regions[other_idx]:
                self.regions[region_idx].add(element)
        for other_idx in reversed(sorted(to_merge)):
            self.regions.pop(other_idx)

    def add(self, row, col):
        region_id = None
        for region_id in range(len(self.regions)):
            if not self.belongs_to_region(row, col, region_id):
                continue
            break
        else:
            self.regions.append({(row, col)})
            return
        if region_id is None:
            self.regions.append({(row, col)})
        else:
            self.add_to_region(row, col, region_id)

    def add_perimeter_items(
            self, region_idx: int, result: list[PerimeterPoint]
    ) -> None:
        for row, col in self.regions[region_idx]:
            for i, j in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                item = (row + i, col + j)
                if item in self.regions[region_idx]:
                    continue
                result.append(PerimeterPoint(
                    *item, linked_point=(row, col),
                    horizontal_connection=abs(i) == 1
                ))

    def calculate_price(self):
        price = 0
        for region_idx in range(len(self.regions)):
            perimeter_set = []
            self.add_perimeter_items(region_idx, perimeter_set)
            price += len(self.regions[region_idx]) * len(perimeter_set)
        return price

    def calculate_discounted_price(self):
        price = 0
        for region_idx in range(len(self.regions)):
            perimeter_set = []
            self.add_perimeter_items(region_idx, perimeter_set)
            edge_counter = EdgeCounter(self.regions[region_idx], perimeter_set)
            price += len(self.regions[region_idx]) * edge_counter.count()
        return price


class Board:
    def __init__(self, lines: list[str]):
        self.map = lines
        self.collectors: dict[str, Collector] = {}
        self.setup_collectors()

    def setup_collectors(self):
        for row, col in product(range(len(self.map)), range(len(self.map[0]))):
            if self.map[row][col] not in self.collectors:
                self.collectors[self.map[row][col]] = Collector(
                    self.map[row][col]
                )
            self.collectors[self.map[row][col]].add(row, col)

    def calc_total_price(self) -> int:
        return sum(
            collector.calculate_price()
            for collector in self.collectors.values()
    )

    def calc_discount_price(self) -> int:
        return sum(
            collector.calculate_discounted_price()
            for collector in self.collectors.values()
        )


def main():
    with open('input.txt') as f:
        board = Board([line.strip() for line in f.readlines()])
    result = board.calc_total_price()
    result2 = board.calc_discount_price()
    assert result == 1421958
    assert result2 == 885394
    print(f"{result=}, {result2=}")


if __name__ == '__main__':
    main()
