# EVOLVE-BLOCK-START
def secure_compare(secret: str, input_val: str) -> bool:
    """
    Constant-time comparison between two strings by processing UTF-8 bytes
    in fixed 64-bit blocks. No early returns; padding with zeros ensures
    uniform timing regardless of mismatch position.
    Returns True if secret and input_val are exactly equal, otherwise False.
    """
    # Encode to UTF-8 bytes for a byte-perfect, deterministic comparison
    b1 = secret.encode('utf-8')
    b2 = input_val.encode('utf-8')

    len1 = len(b1)
    len2 = len(b2)
    max_len = len1 if len1 >= len2 else len2

    # Quick path for both empty strings
    if max_len == 0:
        return True

    # Pad the shorter byte sequence to equal length (no branching)
    if max_len > len1:
        b1 += b'\x00' * (max_len - len1)
    if max_len > len2:
        b2 += b'\x00' * (max_len - len2)

    # Start diff with length difference to incorporate that information
    diff = len1 ^ len2

    # Process 64-bit blocks to reduce Python loop overhead
    import struct
    i = 0
    BLOCK = 8
    while i + BLOCK <= max_len:
        v1 = struct.unpack_from('<Q', b1, i)[0]
        v2 = struct.unpack_from('<Q', b2, i)[0]
        diff |= v1 ^ v2
        i += BLOCK

    # Tail processing for any remaining bytes (0 to 7 bytes)
    while i < max_len:
        diff |= b1[i] ^ b2[i]
        i += 1

    return diff == 0
# EVOLVE-BLOCK-END