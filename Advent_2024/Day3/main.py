# coding=utf-8
import re

def fix_mul_operation(instruction: str) -> int:
    """
    >>> data = "xmul(2,4)%&mul[37]!^t_mul(5,5)+mul(2,4]tn(mul(11,8)mul(8,5))"
    >>> fix_mul_operation(data)
    161
    """
    re.purge()
    mul_instructions = re.findall("mul\([0-9]+,[0-9]+\)", instruction)
    total = 0
    for mul in mul_instructions:
        a, b = mul[4:-1].split(",")
        total += int(a) * int(b)
    return total


enabled = True

def fix_switched_mul_operation(instruction: str) -> int:
    """
    >>> in_ = "mul(2,4)&m!^don't()_mul(5,5)+mul(32,4](mul(11,8)udo()?mul(8,5))"
    >>> fix_switched_mul_operation(in_)
    48
    >>> in_ = "mul(2,4)don't()mul(5,5)do()mul(2,4)do()mul(1,8)don't()mul(8,5)"
    >>> fix_switched_mul_operation(in_)
    24
    >>> in_ = "don't()mul(5,5)do()mul(2,4)do()mul(1,8)don't()mul(8,5)"
    >>> fix_switched_mul_operation(in_)
    16
    >>> in_ = "don't()mul(5,5)don't()mul(2,4)do()mul(1,8)don't()mul(8,5)"
    >>> fix_switched_mul_operation(in_)
    8
    """
    global enabled
    mul_pattern = r"mul\((\d+),(\d+)\)"
    do_pattern = r"do\(\)"
    dont_pattern = r"don't\(\)"
    combined_pattern = f"{mul_pattern}|{do_pattern}|{dont_pattern}"

    total_sum = 0
    matches = re.finditer(combined_pattern, instruction)
    for match in matches:
        if "do()" in str(match):  # Matches do()
            enabled = True
        elif "don't()" in str(match):  # Matches don't()
            enabled = False
        elif match.group(1) and match.group(2):  # Matches mul(X, Y)
            if enabled:
                x, y = int(match.group(1)), int(match.group(2))
                total_sum += x * y

    return total_sum


def main():
    with open('input.txt') as f:
        instructions: list[str] = [line for line in f.readlines()]
    result = sum(map(fix_mul_operation, instructions))
    part_2_result = sum(map(fix_switched_mul_operation, instructions))
    assert result == 155955228
    assert part_2_result == 100189366
    print(f"{result}, {part_2_result}")


if __name__ == '__main__':
    main()
