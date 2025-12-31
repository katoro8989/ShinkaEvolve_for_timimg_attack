# EVOLVE-BLOCK-START
def constant_time_compare(secret: str, input_val: str) -> bool:
    """
    2つの文字列が一致するか判定する関数。
    タイミング脆弱性を排除するために、定数時間で比較を行う。
    """
    len_s = len(secret)
    len_i = len(input_val)

    # Initialize the result with the length difference
    result = len_s ^ len_i

    # Compare each character in a constant-time manner
    for i in range(max(len_s, len_i)):
        # Use ord() to get character codes, but XOR with padding for out-of-bounds
        char_s = ord(secret[i]) if i < len_s else 0
        char_i = ord(input_val[i]) if i < len_i else 0
        result |= (char_s ^ char_i)

    return result == 0
# EVOLVE-BLOCK-END