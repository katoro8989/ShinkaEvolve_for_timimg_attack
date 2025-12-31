# EVOLVE-BLOCK-START
def secure_compare(secret: str, input_val: str) -> bool:
    """
    2つの文字列が一致するか判定する関数。
    constant-time style with length-aware initialization and 16-byte block processing.
    - Encode as UTF-8 bytes
    - Pad to equal length with zeros (no branching)
    - Initialize diff with length information (len1 ^ len2)
    - Process in fixed-size blocks (16 bytes) and accumulate diff via XOR
    - No early returns; final result is diff == 0
    """
    b1 = secret.encode('utf-8')
    b2 = input_val.encode('utf-8')

    len1 = len(b1)
    len2 = len(b2)
    max_len = len1 if len1 >= len2 else len2

    # Pad to equal length (no branching)
    b1_p = b1 + b'\x00' * (max_len - len1)
    b2_p = b2 + b'\x00' * (max_len - len2)

    # Initialize diff with length information to prevent length-based leaks
    diff = len1 ^ len2

    BLOCK = 16
    mv1 = memoryview(b1_p)
    mv2 = memoryview(b2_p)

    for i in range(0, max_len, BLOCK):
        diff |= int.from_bytes(mv1[i:i+BLOCK], 'little') ^ int.from_bytes(mv2[i:i+BLOCK], 'little')

    return diff == 0
# EVOLVE-BLOCK-END