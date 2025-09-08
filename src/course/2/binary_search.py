def binary_search(arr: list, target: int) -> bool:
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return True
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return False


if __name__ == "__main__":
    array = [1, 2, 3, 45, 356, 569, 600, 705, 923]
    assert binary_search(array, 45) is True
    assert binary_search(array, 4) is False
