def remove_duplicates(nums: list) -> int:
    pointer = 1
    for item in range(1, len(nums)):
        if nums[item] != nums[item - 1]:
            nums[pointer] = nums[item]
            pointer += 1
    return pointer

if __name__ == '__main__':
    nums = [1, 1, 2, 2, 3, 4, 4, 5]
    assert remove_duplicates(nums) == 5