# coding=utf-8
from dataclasses import dataclass


@dataclass
class Button:
    x: int
    y: int


@dataclass
class ClownMachine:
    a: Button
    b: Button
    prize_x: int
    prize_y: int

    def calc_determinant(self) -> int:
        return (self.a.x * self.b.y) - (self.b.x * self.a.y)

    def calc_w_x(self):
        return (self.prize_x * self.b.y) - (self.b.x * self.prize_y)

    def calc_w_y(self):
        return (self.a.x * self.prize_y) - (self.prize_x * self.a.y)

    def calc_minimum_required_tokens(self) -> int:
        determinant = self.calc_determinant()
        if determinant == 0:
            raise RuntimeError(f"determinant is equal to zero")
        w_x = self.calc_w_x()
        w_y = self.calc_w_y()
        if (
                w_x / determinant != w_x // determinant
                or w_y / determinant != w_y // determinant
        ):
            return 0
        a_buttons = w_x // determinant
        b_buttons = w_y // determinant
        if a_buttons < 0 or b_buttons < 0:
            return 0
        return 3 * a_buttons + b_buttons




class Casino:
    def __init__(self, lines):
        self.machines = []
        while lines:
            line = lines.pop(0).strip()
            if not line:
                continue
            _, _, x, y = line.split(" ")
            a_button = Button(int(x[2:-1]), int(y[2:]))
            line = lines.pop(0).strip()
            _, _, x, y = line.split(" ")
            b_button = Button(int(x[2:-1]), int(y[2:]))
            line = lines.pop(0).strip()
            _, x, y = line.split(" ")
            self.machines.append(
                ClownMachine(a_button, b_button, int(x[2:-1]), int(y[2:]))
            )

    def tokens_to_win_all(self) -> int:
        tokens = 0
        n_errors = 0
        for machine in self.machines:
            try:
                tokens += machine.calc_minimum_required_tokens()
            except ValueError:
                n_errors += 1
                continue
        return tokens

    def tokens_after_corrections(self) -> int:
        tokens = 0
        n_errors = 0
        for machine in self.machines:
            machine.prize_y += 10000000000000
            machine.prize_x += 10000000000000
            try:
                tokens += machine.calc_minimum_required_tokens()
            except ValueError:
                n_errors += 1
                continue
        return tokens


def main():
    with open('input.txt') as f:
        casino = Casino([line for line in f.readlines()])

    result = casino.tokens_to_win_all()
    result2 = casino.tokens_after_corrections()
    assert result == 27157
    assert result2 == 104015411578548
    print(f"{result=}, {result2=}")


if __name__ == '__main__':
    main()
