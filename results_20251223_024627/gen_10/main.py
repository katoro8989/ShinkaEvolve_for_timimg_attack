# EVOLVE-BLOCK-START
def secure_compare(secret: str, input_val: str) -> bool:
    """
    2つの文字列が一致するか判定する関数。
    タイミング攻撃に耐性を持つよう、全長を走査して比較を行う。
    """
    max_len = max(len(secret), len(input_val))
    diff = 0
    len_s = len(secret)
    len_i = len(input_val)

    i = 0
    # Process 4 characters per iteration to reduce Python loop overhead
    while i <= max_len - 4:
        idx = i
        c1 = secret[idx] if idx < len_s else '\0'
        c2 = input_val[idx] if idx < len_i else '\0'
        diff |= ord(c1) ^ ord(c2)

        idx = i + 1
        c1 = secret[idx] if idx < len_s else '\0'
        c2 = input_val[idx] if idx < len_i else '\0'
        diff |= ord(c1) ^ ord(c2)

        idx = i + 2
        c1 = secret[idx] if idx < len_s else '\0'
        c2 = input_val[idx] if idx < len_i else '\0'
        diff |= ord(c1) ^ ord(c2)

        idx = i + 3
        c1 = secret[idx] if idx < len_s else '\0'
        c2 = input_val[idx] if idx < len_i else '\0'
        diff |= ord(c1) ^ ord(c2)

        i += 4

    while i < max_len:
        c1 = secret[i] if i < len_s else '\0'
        c2 = input_val[i] if i < len_i else '\0'
        diff |= ord(c1) ^ ord(c2)
        i += 1

    return diff == 0
# EVOLVE-BLOCK-END