def two_sum(arr: list, target: int) -> list | None:
    res = dict()
    for index, number in enumerate(arr):
        diff = target - number
        if diff in res:
            return [res[diff], index]
        res[number] = index


if __name__ == '__main__':
    nums = [2, 7, 11, 15]
    target = 9
    assert two_sum(nums, target) == [0, 1]
