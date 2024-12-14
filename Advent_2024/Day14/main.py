# coding=utf-8
from dataclasses import dataclass
import matplotlib.pyplot as plt

MAX_ROWS = 101
MAX_COLS = 103

@dataclass
class Robot:
    row: int
    col: int
    velocity_row: int
    velocity_col: int

    def position_after(self, second: int) -> tuple[int, int]:
        x_value = self.col + second * self.velocity_col
        y_value = self.row + second * self.velocity_row
        x = x_value % MAX_COLS
        y = y_value % MAX_ROWS
        return x, y

    def move(self) -> None:
        self.col, self.row = self.position_after(1)


@dataclass
class Board:
    robots: list[Robot]
    start_position: str = None
    counter: int = 0
    arrays = []

    def __post_init__(self):
        self.start_position = self.get_position()

    def safety_factor(self, seconds: int = 100) -> int:
        safety_row = (MAX_ROWS - 1) / 2
        safety_col = (MAX_COLS - 1) / 2
        quarters = {"0": 0, "1": 0, "2": 0, "3": 0}
        for robot in self.robots:
            x, y = robot.position_after(seconds)
            total = 0
            if x == safety_col or y == safety_row:
                total += 1
                continue
            match (x < safety_col, y < safety_row):
                case (0, 0): quarters["0"] += 1
                case (1, 0): quarters["1"] += 1
                case (1, 1): quarters["2"] += 1
                case (0, 1): quarters["3"] += 1
        score = 1
        for value in quarters.values():
            score *= value
        return score

    def get_position(self) -> str:
        array = [[0 for _ in range(MAX_COLS)] for _ in range(MAX_ROWS)]
        for robot in self.robots:
            array[robot.row][robot.col] = 1
        max_ = 0
        for line in array:
            max_ = max(sum(line), max_)
        result = "\n".join(
            "".join(map(lambda x: str(x) if x else ".", row)) for row in array
        )
        if max_ > 32:
            plt.imshow(array)
            plt.title(f"{self.counter=}")
            plt.savefig("Christmas_tree.png")
            plt.show()
            print(f"{self.counter=}")
        return result

    def move(self, seconds: int = 1) -> None:
        for _ in range(seconds):
            for robot in self.robots:
                robot.move()

    def find_easter_egg(self) -> None:
        while True:
            self.move()
            self.counter += 1
            if self.start_position == self.get_position():
                break


def main():
    with open('input.txt') as f:
        robots = []
        for line in f.readlines():
            position, velocity = line.strip().split(" ")
            position_x = int(position[2:].split(",")[0])
            position_y = int(position[2:].split(",")[1])
            velocity_x = int(velocity[2:].split(",")[0])
            velocity_y = int(velocity[2:].split(",")[1])
            robots.append(Robot(
                int(position_x), int(position_y), velocity_x, velocity_y
            ))

    board = Board(robots)
    result = board.safety_factor()
    print(f"{result=}")
    board.find_easter_egg()


if __name__ == '__main__':
    main()
