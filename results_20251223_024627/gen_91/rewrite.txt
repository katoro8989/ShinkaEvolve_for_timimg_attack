# EVOLVE-BLOCK-START
def secure_compare(secret: str, input_val: str) -> bool:
    """
    Constant-time comparison of two strings by converting to UTF-8 bytes,
    padding to equal length without branching, then performing a single
    XOR across all bytes using fixed-size blocks.

    Returns True iff secret == input_val.
    """
    a = secret.encode('utf-8')
    b = input_val.encode('utf-8')

    max_len = max(len(a), len(b))

    # Pad to the same length with zeros (no branching)
    a_p = a + b'\x00' * (max_len - len(a))
    b_p = b + b'\x00' * (max_len - len(b))

    diff = 0
    BLOCK = 32  # Process in 32-byte blocks for efficiency

    for i in range(0, max_len, BLOCK):
        # Use memoryview for efficient slicing
        block_a = memoryview(a_p)[i:i + BLOCK]
        block_b = memoryview(b_p)[i:i + BLOCK]
        diff |= int.from_bytes(block_a, 'little') ^ int.from_bytes(block_b, 'little')

    return diff == 0
# EVOLVE-BLOCK-END