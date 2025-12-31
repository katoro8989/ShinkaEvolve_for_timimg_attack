# EVOLVE-BLOCK-START
def secure_compare(secret: str, input_val: str) -> bool:
    """
    2つの文字列が一致するか判定する関数。
    タイミング攻撃に耐性を持つよう、全長を走査して比較を行う。
    """
    max_len = max(len(secret), len(input_val))
    diff = 0
    for i in range(max_len):
        c1 = secret[i] if i < len(secret) else '\0'
        c2 = input_val[i] if i < len(input_val) else '\0'
        diff |= ord(c1) ^ ord(c2)

    return diff == 0
# EVOLVE-BLOCK-END