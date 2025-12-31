# EVOLVE-BLOCK-START
def secure_compare(secret: str, input_val: str) -> bool:
    """
    2つの文字列が一致するか判定する関数。
    現在は典型的な「タイミング脆弱性」を含んでいる。
    1文字でも違うと即座に False を返すため、
    先頭で間違える場合と末尾で間違える場合で実行時間が異なる。
    """
    if len(secret) != len(input_val):
        return False

    diff = 0
    for i in range(len(secret)):
        diff |= ord(secret[i]) ^ ord(input_val[i])

    return diff == 0
# EVOLVE-BLOCK-END