def length_encoding(some_str: str) -> str:
    encoded = ""
    count = 1
    for i in range(1, len(some_str)):
        if some_str[i] == some_str[i - 1]:
            count += 1
        else:
            encoded += f"{some_str[i-1]}{count}"
            count = 1
    encoded += f"{some_str[-1]}{count}"
    return encoded


if __name__ == '__main__':
    s = "AAABBCCDDD"
    assert length_encoding(s) == "A3B2C2D3"
