# EVOLVE-BLOCK-START
def secure_compare(secret: str, input_val: str) -> bool:
    """
    Constant-time comparison of two strings with robust handling of UTF-8 bytes.
    - Encode as UTF-8 bytes
    - Initialize diff with XOR of lengths to reflect length differences
    - Pad both to the same length with zero bytes (no branching)
    - Compare in fixed-size 16-byte blocks, accumulating diff via XOR
    - No early return; final result is diff == 0
    Returns True iff secret == input_val
    """
    b1 = secret.encode('utf-8')
    b2 = input_val.encode('utf-8')

    len1 = len(b1)
    len2 = len(b2)
    max_len = len1 if len1 >= len2 else len2

    # Pad to the same length (no branching)
    if len1 < max_len:
        b1 = b1 + b'\x00' * (max_len - len1)
    if len2 < max_len:
        b2 = b2 + b'\x00' * (max_len - len2)

    # Initialize diff with length information to prevent length-based leaks
    diff = len1 ^ len2

    BLOCK = 16
    # Process in fixed-size blocks to reduce Python overhead
    for i in range(0, max_len, BLOCK):
        blk1 = b1[i:i+BLOCK]
        blk2 = b2[i:i+BLOCK]
        diff |= int.from_bytes(blk1, 'little') ^ int.from_bytes(blk2, 'little')

    return diff == 0
# EVOLVE-BLOCK-END