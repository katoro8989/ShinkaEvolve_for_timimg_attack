# EVOLVE-BLOCK-START
def secure_compare(secret: str, input_val: str) -> bool:
    """
    2つの文字列が一致するか判定する関数。
    タイミング攻撃に耐性を持つよう、全長を走査して比較を行う。
    """
    len_s = len(secret)
    len_i = len(input_val)
    max_len = max(len_s, len_i)
    
    diff = 0
    for i in range(max_len):
        c1 = ord(secret[i]) if i < len_s else 0
        c2 = ord(input_val[i]) if i < len_i else 0
        diff |= c1 ^ c2

    return diff == 0
# EVOLVE-BLOCK-END