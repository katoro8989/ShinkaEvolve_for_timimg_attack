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

    # Initialize the result to the length difference, will ensure padding for unequal lengths
    result = len(secret) ^ len(input_val)
    for i in range(len(secret)):
        # Compare characters using XOR, constant time for each character
        result |= (ord(secret[i]) ^ ord(input_val[i]))
    # All characters match if result is 0

    return result == 0  # Result is 0 only if all characters matched
# EVOLVE-BLOCK-END