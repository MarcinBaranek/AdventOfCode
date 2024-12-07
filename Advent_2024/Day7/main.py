# coding=utf-8


def check_pair(result: int, numbers: list[int]) -> bool:
    if len(numbers) == 1:
        return result == numbers[0]
    number = numbers[-1]
    if result % number == 0 and check_pair(result // number, numbers[:-1]):
        return True
    return check_pair(result - number, numbers[:-1])


def concat(left, right) -> int:
    return int(f"{left}{right}")


def check_pairs_with_concat(result: int, numbers: list[int]) -> bool:
    if len(numbers) == 1:
        return result == numbers[0]
    if len(numbers) == 2:
        return (
            result == concat(*numbers)
            or result == sum(numbers)
            or result == numbers[0] * numbers[1]
        )
    number = numbers[-1]
    if (
        result % number == 0
        and check_pairs_with_concat(result // number, numbers[:-1])
    ):
        return True
    if str(result).endswith(str(number)):
        new_result = str(result)[:-len(str(number))]
        if not new_result:
            new_result = 1
        if check_pairs_with_concat(int(new_result), numbers[:-1]):
            return True
    return check_pairs_with_concat(result - number, numbers[:-1])


def process(results: list[int], numbers: list[list[int]]) -> tuple[int, int]:
    total = 0
    total_with_concat = 0
    for result, nums in zip(results, numbers):
        if check_pair(result, nums):
            total += result
        elif check_pairs_with_concat(result, nums):
            total_with_concat += result
            print(result, nums)
    return total, total_with_concat + total


def main():
    results = []
    numbers = []
    with open('input.txt') as f:
        for line in f.readlines():
            result, items = line.strip().split(":")
            results.append(int(result))
            numbers.append(list(map(int, items.strip().split(" "))))

    result = process(results, numbers)
    assert result[0] == 5540634308362
    assert result[1] == 472290821152397
    print(f"{result}")


if __name__ == '__main__':
    main()
