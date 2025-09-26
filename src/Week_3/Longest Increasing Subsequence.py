def longest_increasing_contiguous(nums: list) -> int:
    max_len = 1
    curr_len = 1

    for i in range(1, len(nums)):
        if nums[i] >= nums[i - 1]:
            curr_len += 1
            if curr_len > max_len:
                max_len = curr_len
        else:
            curr_len = 1

    return max_len

if __name__ == '__main__':
    print(longest_increasing_contiguous([10, 9, 2, 5, 3, 7, 101, 18]))