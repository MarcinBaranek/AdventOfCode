# coding=utf-8
from functools import lru_cache


class StoneStore:
    def __init__(self, stones: list[str]):
        self.stones = stones

    @lru_cache(maxsize=1024)
    def count_after_blinks(self, stone: str, blinks: int) -> int:
        if blinks <= 0:
            return 1
        if int(stone) == 0:
            return self.count_after_blinks("1", blinks - 1)
        elif len(stone) % 2 == 0:
            new_stone = str(int(stone[len(stone)//2:]))
            return self.count_after_blinks(stone[:len(stone)//2], blinks - 1)\
                + self.count_after_blinks(new_stone, blinks - 1)
        else:
            return self.count_after_blinks(str(2024 * int(stone)), blinks - 1)

    def count_all_stones(self, blinks: int) -> int:
        return sum(
            self.count_after_blinks(stone, blinks) for stone in self.stones
        )


def main():
    with open('input.txt') as f:
        for line in f.readlines():
            stone_stores = StoneStore(line.strip().split(" "))

    result = stone_stores.count_all_stones(25)
    result2 = stone_stores.count_all_stones(75)
    assert result == 194557
    assert result2 == 231532558973909
    print(f"{result=}, {result2=}")


if __name__ == '__main__':
    main()
