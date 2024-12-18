# coding=utf-8
from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass
from itertools import product
from runpy import run_path

from tqdm import tqdm


@dataclass
class Registry:
    a: int = 729
    b: int = 0
    c: int = 0


def parse_combo_operand(operand: int, registry: Registry) -> int:
    if 0 <= operand <= 3:
        return operand
    elif operand == 4:
        return registry.a
    elif operand == 5:
        return registry.b
    elif operand == 6:
        return registry.c
    else:
        raise RuntimeError(f'Invalid operand {operand}')


def adv(operand: int, registry: Registry, **kwargs):
    registry.a = int(
        registry.a / (2 ** parse_combo_operand(operand, registry))
    )


def bxl(operand: int, registry: Registry, **kwargs):
    registry.b ^= operand


def bst(operand: int, registry: Registry, **kwargs):
    registry.b = parse_combo_operand(operand, registry) % 8


def jnz(operand: int, registry: Registry, **kwargs):
    if registry.a == 0:
        return
    return operand


def bxc(operand: int, registry: Registry, **kwargs):
    registry.b ^= registry.c


def bdv(operand: int, registry: Registry, **kwargs):
    registry.b = int(
        registry.a / (2 ** parse_combo_operand(operand, registry))
    )


def out(operand: int, registry: Registry, collector: list[int] = None):
    res = parse_combo_operand(operand, registry) % 8
    if collector is not None:
        collector.append(res)
    else:
        print(res, end=",")


def cdv(operand: int, registry: Registry, **kwargs):
    registry.c = int(
        registry.a / (2 ** parse_combo_operand(operand, registry))
    )

methods = {
    0: adv,
    1: bxl,
    2: bst,
    3: jnz,
    4: bxc,
    5: out,
    6: bdv,
    7: cdv
}


def run(program: list[int], registry: Registry, collector = None) -> None:
    idx = 0
    while idx < len(program):
        func = methods[program[idx]]
        operand = program[idx + 1]
        result = func(operand, registry, collector=collector)
        if result is not None:
            idx = result
        else:
            idx += 2


def find_mini_a_value(program: list[int]) -> int:
    init_val = 35184428000000
    while True:
        if init_val % 1_000_000 == 0:
            print(f"{init_val=}")
        collector = []
        registry = Registry(a=init_val)
        run(program, registry, collector)
        if len(collector) > len(program):
            break
        if collector == program:
            print(f"{collector=}")
            break
        init_val += 1
    return init_val


def process(r: int, a) -> int:
    b = a % 8
    b ^= 1
    c = a // (2 ** b)
    b ^= 5
    b ^= c
    return b % 8

def build_a(rests: dict[int, list[int]]):
    keys = list(sorted(rests.keys()))
    for key in keys:
        for r in rests[key]:
            a = r

def get_a(rests: list[int]) -> int:
    a = 0
    for r_ in rests:
        a += r_
        a *= 8
    return a

def get_out(a, index, exp, increment, programs):
    def do(tmp, idx):
        col = []
        run(programs, Registry(int(tmp)), col)
        return col[idx]
    last = a
    tmp = a
    inc = increment
    while True:
        current_result = do(tmp, index)
        if do(last, index) == exp and current_result != exp:
            return tmp
        if current_result != exp:
            print("too far")
            tmp = last
            inc = inc // 10
            inc = max(inc, 1 if inc > 0 else -1)
            continue
        last = tmp
        tmp += inc

import numpy as np
def get_mesh(a, b, programs, idx):
    x = np.linspace(a, b, 1000)
    result = []
    for e in x:
        collector = []
        run(programs, Registry(int(e)), collector=collector)
        result.append(collector[idx])
    return x, np.array(result)

import matplotlib.pyplot as plt
def main():
    programs = [2, 4, 1, 1, 7, 5, 0, 3, 1, 4, 4, 5, 5, 5, 3, 0]
    # programs = [2, 4, 1, 1, 7, 5, 1, 5, 0, 3, 4, 4, 5, 5, 3, 0]
    idx = -1
    exp = 0
    a, b = 8**15, 8**16 - 1
    min_set = set()
    max_set = set()


    xx, result = get_mesh(a, b, programs, -1)
    plt.plot(result)
    plt.show()
    for (x, r) in zip(xx, result):
        if r == 0:
            max_ = get_out(int(x), idx, exp, round((b-a) / 1000), programs)
            min_ = get_out(int(x), idx, exp, - round((b- a) / 1000), programs)
            min_set.add(min_)
            max_set.add(max_)
    print(f"{min_set=}")
    print(f"{max_set=}")

    # import numpy as np
    #
    # x = np.linspace(8**15, 8**16 - 1, 1000)
    # result = []
    # for e in x:
    #     collector = []
    #     run(programs, Registry(int(e)), collector=collector)
    #     result.append(collector[-1])
    # plt.plot(x, result)
    # plt.show()


    # stuck = [(0,)]
    # l = 0
    # while stuck:
    #     rest = stuck.pop()
    #     print(f"{rest=}, {len(rest)=}")
    #     l = max(l, len(rest))
    #     neighbors = []
    #     for r in range(7):
    #         a = get_a(rest)
    #         a += r
    #         # res = process(r, a)
    #         collectors = []
    #         run(programs, Registry(a), collector=collectors)
    #         # print(f"{rest=} => {collectors=}")
    #         if collectors == programs[-len(collectors):]:
    #         # out_ = programs[-len(rest)]
    #         # if res == out_:
    #             neighbors.append(r)
    #     for r in neighbors:
    #         stuck.append(rest + (r,))
    # print(f"{l=}")


    # for r in range(7):
    #     a = r
    #     res = process(r, a)
    #     if res == 0:
    #         print(r)
    # result = find_mini_a_value(programs)
    # print(result)
    #
    # collector = []
    # run(programs, Registry(result), collector=collector)
    # print(len(collector))
    # print(collector)
    # 35_169_804_035_309 too low
    # print(f"{result=}, {result2=}")


if __name__ == '__main__':
    main()
