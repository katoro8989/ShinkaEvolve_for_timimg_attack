# EVOLVE-BLOCK-START
def secure_compare(secret: str, input_val: str) -> bool:
    """
    2つの文字列が一致するか判定する関数。
    現在は典型的な「タイミング脆弱性」を含んでいる。
    1文字でも違うと即座に False を返すため、
    先頭で間違える場合と末尾で間違える場合で実行時間が異なる。
    """
    len_s = len(secret)
    len_i = len(input_val)
    max_len = max(len_s, len_i)

    result = len_s ^ len_i  # Start with length difference

    for i in range(max_len):
        a = ord(secret[i]) if i < len_s else 0
        b = ord(input_val[i]) if i < len_i else 0
        result |= (a ^ b)

    return result == 0

    return True
# EVOLVE-BLOCK-END