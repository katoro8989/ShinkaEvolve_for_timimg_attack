# EVOLVE-BLOCK-START
def secure_compare(secret: str, input_val: str) -> bool:
    """
    Constant-time comparison of two strings by operating on UTF-8 bytes.
    - Encode both strings to UTF-8 bytes to obtain a uniform byte representation.
    - Pad the shorter input with zero bytes to equal length (no branching).
    - Compare in fixed-size blocks (16 bytes) using memoryview and accumulate a diff with XOR.
    - No early return; final check is whether diff == 0.
    """
    a = secret.encode('utf-8')
    b = input_val.encode('utf-8')

    max_len = max(len(a), len(b))

    # Pad to the same length with zeros (no branching)
    a_p = a + b'\x00' * (max_len - len(a))
    b_p = b + b'\x00' * (max_len - len(b))

    diff = 0
    BLOCK = 16
    mv_a = memoryview(a_p)
    mv_b = memoryview(b_p)

    for i in range(0, max_len, BLOCK):
        diff |= int.from_bytes(mv_a[i:i + BLOCK], 'little') ^ int.from_bytes(mv_b[i:i + BLOCK], 'little')

    return diff == 0
# EVOLVE-BLOCK-END