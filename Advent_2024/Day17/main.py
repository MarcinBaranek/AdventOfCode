# coding=utf-8
from dataclasses import dataclass


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


def main():
    programs = [2,4,1,1,7,5,1,5,0,3,4,4,5,5,3,0]
    collector = []
    run(programs, Registry(23999685), collector=collector)
    result = ",".join(map(str, collector))
    assert result == "5,0,3,5,7,6,1,5,4"
    print(f"{result=}")
    result2 = 164516454365621   # calculated manually
    collector = []
    run(programs, Registry(result2), collector=collector)
    print(collector)
    print(collector == programs)


if __name__ == '__main__':
    main()
