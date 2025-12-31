# EVOLVE-BLOCK-START
def secure_compare(secret: str, input_val: str) -> bool:
    """
    Constant-time comparison between two strings.
    Returns True if 'secret' and 'input_val' are equal; otherwise False.
    The implementation avoids early returns and ensures uniform timing characteristics.
    """
    # Encode to UTF-8 to get a deterministic byte representation
    b1 = secret.encode('utf-8')
    b2 = input_val.encode('utf-8')

    len1 = len(b1)
    len2 = len(b2)
    max_len = len1 if len1 >= len2 else len2

    # Pad the shorter byte sequence to equal length (no branching in loop)
    if max_len > len1:
        b1 = b1 + b'\x00' * (max_len - len1)
    if max_len > len2:
        b2 = b2 + b'\x00' * (max_len - len2)

    # Start with a diff that captures length difference
    diff = len1 ^ len2

    BLOCK = 8
    i = 0
    # Process in fixed 8-byte blocks
    while i + BLOCK <= max_len:
        v1 = int.from_bytes(b1[i:i+BLOCK], 'little')
        v2 = int.from_bytes(b2[i:i+BLOCK], 'little')
        diff |= (v1 ^ v2)
        i += BLOCK

    # Tail processing for remaining bytes
    while i < max_len:
        diff |= (b1[i] ^ b2[i])
        i += 1

    return diff == 0
# EVOLVE-BLOCK-END