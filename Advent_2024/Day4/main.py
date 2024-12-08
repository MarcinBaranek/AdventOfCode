# coding=utf-8
from fontTools.misc.textTools import tostr


def count_xmas(line: str) -> int:
    return line.count("XMAS") + line.count("SAMX")


def get_right_diagonal_str(lines: list[str], idx: int = 0) -> str:
    """
    >>> lines = [
    ...     "XMAS",
    ...     "WWAW",
    ...     "WMWW",
    ...     "XWWW",
    ... ]
    >>> get_right_diagonal_str(lines)
    'XWWW'
    >>> get_right_diagonal_str(lines, 2)
    'AW'
    """
    result = ""
    k = 0
    for i in range(len(lines[0])):
        if i >= len(lines) or idx + k >= len(lines[i]):
            break
        result += lines[i][idx + k]
        k += 1
    return result


def get_left_diagonal_str(lines: list[str], idx: int = 0) -> str:
    """
    >>> lines = [
    ...     "XMAS",
    ...     "WWAW",
    ...     "WMWW",
    ...     "XWWW",
    ... ]
    >>> get_left_diagonal_str(lines)
    'XMAS'
    >>> get_left_diagonal_str(lines, 2)
    'WM'
    """
    result = ""
    k = 0
    i = len(lines) - 1 - idx
    while True:
        if i < 0 or k >= len(lines[i]):
            break
        result += lines[i][k]
        i -= 1
        k += 1
    return result


def search_xmas(lines: list[str]):
    """
    >>> lines = [
    ...     "XMAS",
    ...     "WWAW",
    ...     "WMWW",
    ...     "XWWW",
    ... ]
    >>> search_xmas(lines)
    2
    >>> lines = [
    ...     "XMAS",
    ...     "WMAW",
    ...     "WMAW",
    ...     "XWWS",
    ... ]
    >>> search_xmas(lines)
    3
    >>> lines = [
    ...     "XMAS",
    ...     "MMAW",
    ...     "AMAW",
    ...     "SWWS",
    ... ]
    >>> search_xmas(lines)
    3
    >>> lines = [
    ...     "XWWWW",
    ...     "MMAWW",
    ...     "AMAWW",
    ...     "SWWSW",
    ... ]
    >>> search_xmas(lines)
    2
    >>> lines = [
    ...     "....XXMAS.",
    ...     ".SAMXMS...",
    ...     "...S..A...",
    ...     "..A.A.MS.X",
    ...     "XMASAMX.MM",
    ... ]
    >>> search_xmas(lines)
    6
    >>> lines = [
    ...     "MMMSXXMASM",
    ...     "MSAMXMSMSA",
    ...     "AMXSXMAAMM",
    ...     "MSAMASMSMX",
    ...     "XMASAMXAMM",
    ...     "XXAMMXXAMA",
    ...     "SMSMSASXSS",
    ...     "SAXAMASAAA",
    ...     "MAMMMXMMMM",
    ...     "MXMXAXMASX",
    ... ]
    >>> search_xmas(lines)
    18
    """
    total = sum(count_xmas(line) for line in lines)
    vertical_lines = [l for l in lines[0]]
    for i in range(1, len(lines)):
        for j, l in enumerate(lines[i]):
            vertical_lines[j] += l
    total += sum(count_xmas(line) for line in vertical_lines)

    right_diagonal_lines = []
    for i in range(len(lines[0])):
        right_diagonal_lines.append(get_right_diagonal_str(lines, i))
    for i in range(1, len(lines)):
        right_diagonal_lines.append(get_right_diagonal_str(lines[i:]))
    total += sum(count_xmas(line) for line in right_diagonal_lines)

    left_diagonal_lines = []
    for i in range(len(lines)):
        left_diagonal_lines.append(get_left_diagonal_str(lines, i))
    for i in range(1, len(lines[-1])):
        left_diagonal_lines.append(get_left_diagonal_str([l[i:] for l in lines]))
    total += sum(count_xmas(line) for line in left_diagonal_lines)
    return total


def count_x_mas(lines: list[str]) -> int:
    """
    >>> lines = [
    ...     "M.S",
    ...     ".A.",
    ...     "M.S",
    ... ]
    >>> count_x_mas(lines)
    1
    >>> lines = [
    ...     "MMMSXXMASM",
    ...     "MSAMXMSMSA",
    ...     "AMXSXMAAMM",
    ...     "MSAMASMSMX",
    ...     "XMASAMXAMM",
    ...     "XXAMMXXAMA",
    ...     "SMSMSASXSS",
    ...     "SAXAMASAAA",
    ...     "MAMMMXMMMM",
    ...     "MXMXAXMASX",
    ... ]
    >>> count_x_mas(lines)
    9
    """
    total = 0
    for line_idx in range(len(lines) - 2):
        for letter in range(len(lines[0]) - 2):
            word = ""
            for k in range(3):
                if letter + k >= len(lines[line_idx + k]):
                    continue
                word += lines[line_idx + k][letter + k]
            if word != "MAS" and word != "SAM":
                continue
            word = ""
            for k in range(3):
                word += lines[line_idx + 2 - k][letter + k]
            if word != "MAS" and word != "SAM":
                continue
            total += 1
    return total


def main():
    with open('input.txt') as f:
        lines: list[str] = [line for line in f.readlines()]
    result = search_xmas(lines)
    result_for_part_2 = count_x_mas(lines)
    assert result == 2483
    assert result_for_part_2 == 1925
    print(f"{result}, {result_for_part_2}")


if __name__ == '__main__':
    main()
