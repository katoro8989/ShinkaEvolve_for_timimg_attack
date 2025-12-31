# EVOLVE-BLOCK-START
def secure_compare(secret: str, input_val: str) -> bool:
    """
    Constant-time comparison between two strings.
    - Encodes to UTF-8 bytes
    - Processes in fixed 16-byte blocks using memoryview to avoid copies
    - Pads conceptually via length comparison; diff accumulates any mismatch
    - No early exits; final result is True iff all bytes match
    """
    # UTF-8 encode both inputs
    b1 = secret.encode('utf-8')
    b2 = input_val.encode('utf-8')

    len1 = len(b1)
    len2 = len(b2)
    max_len = len1 if len1 >= len2 else len2

    # Initialize diff with length information
    diff = len1 ^ len2

    # Prepare memoryviews for block-wise access without copies
    mv1 = memoryview(b1)
    mv2 = memoryview(b2)

    BLOCK = 16
    i = 0

    # Process in fixed-size blocks to minimize Python overhead
    while i + BLOCK <= max_len:
        v1 = int.from_bytes(mv1[i:i+BLOCK], 'little')
        v2 = int.from_bytes(mv2[i:i+BLOCK], 'little')
        diff |= v1 ^ v2
        i += BLOCK

    # Process any remaining tail bytes in a tight loop (no branching based on data)
    while i < max_len:
        a = mv1[i] if i < len1 else 0
        b = mv2[i] if i < len2 else 0
        diff |= a ^ b
        i += 1

    return diff == 0
# EVOLVE-BLOCK-END