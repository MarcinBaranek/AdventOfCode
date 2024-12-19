# coding=utf-8
from typing import Deque
from collections import deque
from dataclasses import dataclass, field
from functools import lru_cache

@dataclass(frozen=True, slots=True)
class Counter:
    towels: tuple[str, ...]

    @lru_cache(maxsize=None)
    def count(self, word: str) -> int:
        if word == "":
            return 1
        total = 0
        for towel in self.towels:
            if word.startswith(towel):
                total += self.count(word[len(towel):])
        return total

def main():
    towels = []
    words = []
    with open('input.txt') as f:
        for line in f.readlines():
            if not towels:
                towels.extend(line.strip().split(", "))
                continue
            if line.strip() == "":
                continue
            words.append(line.strip())
    counter = Counter(tuple(towels))
    total = 0
    total_ways = 0
    for word in words:
        count = counter.count(word)
        total += bool(count)
        total_ways += count

    print(f"{total=}")
    print(f"{total_ways=}")


if __name__ == '__main__':
    main()
