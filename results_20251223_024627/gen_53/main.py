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
    max_len = len_s if len_s > len_i else len_i

    diff = 0
    diff |= len_s ^ len_i  # Incorporate length difference

    for i in range(max_len):
        c1 = ord(secret[i]) if i < len_s else 0
        c2 = ord(input_val[i]) if i < len_i else 0
        diff |= c1 ^ c2

    return diff == 0
# EVOLVE-BLOCK-END