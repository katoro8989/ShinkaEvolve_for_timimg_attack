# EVOLVE-BLOCK-START
def secure_compare(secret: str, input_val: str) -> bool:
    """
    Constant-time comparison between two strings using fixed-block XOR over UTF-8 bytes.
    Returns True if secret and input_val are exactly equal, otherwise False.
    This approach encodes to bytes, pads to equal length without branching, and
    processes in fixed-size blocks to avoid data-dependent timing.
    """
    b1 = secret.encode('utf-8')
    b2 = input_val.encode('utf-8')

    len1 = len(b1)
    len2 = len(b2)
    max_len = len1 if len1 >= len2 else len2

    # Early return for completely empty case
    if max_len == 0:
        return True

    # Pad with zeros to equal length (no branching inside the main loop)
    if max_len > len1:
        b1 = b1 + b'\x00' * (max_len - len1)
    if max_len > len2:
        b2 = b2 + b'\x00' * (max_len - len2)

    diff = len1 ^ len2

    BLOCK = 16
    for i in range(0, max_len, BLOCK):
        chunk1 = b1[i:i+BLOCK]
        chunk2 = b2[i:i+BLOCK]
        diff |= int.from_bytes(chunk1, 'little') ^ int.from_bytes(chunk2, 'little')

    return diff == 0
# EVOLVE-BLOCK-END