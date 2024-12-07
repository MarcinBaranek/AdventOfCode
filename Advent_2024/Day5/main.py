# coding=utf-8
from dataclasses import dataclass


@dataclass
class Rule:
    first: int
    second: int
    first_appeared: bool = False
    second_appeared: bool = False

    def notify(self, number: int) -> None:
        error = ValueError(f"Broken rule: {self.first}|{self.second}")
        if number == self.first:
            self.first_appeared = True
            if self.second_appeared:
                raise error
        if number == self.second:
            self.second_appeared = True

    def reset(self) -> None:
        self.first_appeared = False
        self.second_appeared = False

    def fix(self, line: list[int]):
        l_idx = line.index(self.second)
        r_idx = line.index(self.first)
        line[l_idx], line[r_idx] = line[r_idx], line[l_idx]


def fix_line(line: list[int], rules: list[Rule]) -> list[int]:
    line_is_incorrect = False
    while not line_is_incorrect:
        line_is_incorrect = True
        for rule in rules:
            rule.reset()
        for page in line:
            for rule in rules:
                try:
                    rule.notify(page)
                except ValueError:
                    rule.fix(line)
                    line_is_incorrect = False
    return line


def process(rules: list[Rule], sections: list[list[int]]) -> tuple[int, int]:
    result_correct_lines = 0
    result_incorrect_lines = 0
    for line in sections:
        line_was_correct = True
        for rule in rules:
            rule.reset()
        for page in line:
            for rule in rules:
                try:
                    rule.notify(page)
                except ValueError:
                    line_was_correct = False
                    break
        if line_was_correct:
            result_correct_lines += line[len(line) // 2]
        else:
            line = fix_line(line, rules)
            result_incorrect_lines += line[len(line) // 2]

    return result_correct_lines, result_incorrect_lines


def main():
    rules: list[Rule] = []
    sections: list[list[int]] = []
    with open('input.txt') as f:
        for line in f.readlines():
            if "|" in line:
                rules.append(Rule(*map(int, line.strip().split("|"))))
            if "," in line:
                sections.append(list(map(int, line.strip().split(","))))

    result = process(rules, sections)
    # assert result[0] == 6498
    # assert result[1] == 5017
    print(f"{result}")


if __name__ == '__main__':
    main()
