# EVOLVE-BLOCK-START
def secure_compare(secret: str, input_val: str) -> bool:
    """
    2つの文字列が一致するか判定する関数。
    タイミング攻撃に耐性を持つよう、全長を走査して比較を行う。
    """
    # Work entirely on UTF-8 bytes to ensure uniform representation and constant-time behavior.
    b1 = secret.encode('utf-8')
    b2 = input_val.encode('utf-8')

    len1 = len(b1)
    len2 = len(b2)
    max_len = len1 if len1 >= len2 else len2

    # Pad to equal length with zeros (no branching)
    b1_p = b1 + b'\x00' * (max_len - len1)
    b2_p = b2 + b'\x00' * (max_len - len2)

    # Initialize diff with length information to prevent length-based leaks
    diff = len1 ^ len2

    BLOCK = 16
    mv1 = memoryview(b1_p)
    mv2 = memoryview(b2_p)

    step = BLOCK * 4
    for i in range(0, max_len, step):
        diff |= int.from_bytes(mv1[i:i+BLOCK], 'little') ^ int.from_bytes(mv2[i:i+BLOCK], 'little')
        diff |= int.from_bytes(mv1[i+BLOCK:i+BLOCK*2], 'little') ^ int.from_bytes(mv2[i+BLOCK:i+BLOCK*2], 'little')
        diff |= int.from_bytes(mv1[i+BLOCK*2:i+BLOCK*3], 'little') ^ int.from_bytes(mv2[i+BLOCK*2:i+BLOCK*3], 'little')
        diff |= int.from_bytes(mv1[i+BLOCK*3:i+BLOCK*4], 'little') ^ int.from_bytes(mv2[i+BLOCK*3:i+BLOCK*4], 'little')

    return diff == 0
# EVOLVE-BLOCK-END