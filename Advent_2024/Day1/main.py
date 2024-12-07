# coding=utf-8

def main():
    left_list: list[int] = []
    right_list: list[int] = []
    with open('input.txt') as f:
        for line in f.readlines():
            left, right = line.strip().split("   ")
            left_list.append(int(left.strip()))
            right_list.append(int(right.strip()))

    total = sum(
        abs(a - b) for a, b in zip(sorted(left_list), sorted(right_list))
    )
    assert total == 936063
    second_total = 0
    for left_num in left_list:
        counter = 0
        for right_num in right_list:
            if left_num == right_num:
                counter += 1
        second_total += counter * left_num
    print(f"{total}, {second_total}")


if __name__ == '__main__':
    main()
