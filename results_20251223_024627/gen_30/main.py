# EVOLVE-BLOCK-START
def secure_compare(secret: str, input_val: str) -> bool:
    """
    Constant-time comparison of two strings by operating on UTF-8 bytes.
    - Encode both strings to UTF-8 bytes to obtain a uniform byte representation.
    - Pad the shorter input with zero bytes to equal length (no branching).
    - Compare in 8-byte blocks using memoryview and accumulate with XOR.
    - Include length information in the initial diff to reduce length-based leaks.
    - No early return; final check is whether diff == 0.
    """
    a = secret.encode('utf-8')
    b = input_val.encode('utf-8')

    len_a = len(a)
    len_b = len(b)
    max_len = len_a if len_a >= len_b else len_b

    if max_len == 0:
        return True

    # Pad to equal length
    a_p = a + b'\x00' * (max_len - len_a)
    b_p = b + b'\x00' * (max_len - len_b)

    diff = len_a ^ len_b

    BLOCK = 8
    mv_a = memoryview(a_p)
    mv_b = memoryview(b_p)

    for i in range(0, max_len, BLOCK):
        diff |= int.from_bytes(mv_a[i:i+BLOCK], 'little') ^ int.from_bytes(mv_b[i:i+BLOCK], 'little')

    return diff == 0
# EVOLVE-BLOCK-END