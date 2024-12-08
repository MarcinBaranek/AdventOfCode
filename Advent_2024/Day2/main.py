# coding=utf-8


def is_safe_report(report: list[int], accept_failure: bool = False) -> bool:
    """
    >>> data = [1, 2, 3, 1]
    >>> is_safe_report(data, accept_failure=True)
    True
    >>> data = [13, 2, 3, 4]
    >>> is_safe_report(data, accept_failure=True)
    True
    >>> data = [13, 2, 3, 1]
    >>> is_safe_report(data, accept_failure=True)
    False
    >>> data = [1, 2, 1, 3]
    >>> is_safe_report(data, accept_failure=True)
    True
    >>> data = [8, 6, 4, 4, 1]
    >>> is_safe_report(data, accept_failure=True)
    True
    >>> data = [9, 7, 6, 2, 1]
    >>> is_safe_report(data, accept_failure=True)
    False
    >>> data = [8, 7, 9, 10, 11]
    >>> is_safe_report(data, accept_failure=True)
    True
    >>> data = [8, 7, 8, 10, 11]
    >>> is_safe_report(data, accept_failure=True)
    True
    """
    if len(report) < 1:
        return True
    if report[0] >= report[1]:
        # make list potentially increasing
        report = [-level for level in report]
    for i in range(len(report) - 1):
        if (
            1 <= abs(report[i] - report[i + 1]) <= 3
            and report[i] < report[i + 1]
        ):
            continue
        if accept_failure:
            first_try = is_safe_report(report[:i + 1] + report[i + 2:])
            second_try = is_safe_report(report[:i - 1] + report[i:])\
                if i > 0 else is_safe_report(report[1:])
            return is_safe_report(report[:i] + report[i + 1:]) \
                or first_try or second_try
        return False
    return True



def main():
    with open('input.txt') as f:
        reports: list[list[int]] = [
            list(map(int, line.strip().split(' ')))
            for line in f.readlines()
        ]
    number_of_safe_reports = sum(map(is_safe_report, reports))
    safe_reports = sum(map(lambda x: is_safe_report(x, True), reports))
    assert number_of_safe_reports == 246
    assert safe_reports == 318
    print(f"{number_of_safe_reports}, {safe_reports}")


if __name__ == '__main__':
    main()
