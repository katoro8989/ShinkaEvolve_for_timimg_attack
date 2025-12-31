# EVOLVE-BLOCK-START
def secure_compare(secret: str, input_val: str) -> bool:
    """
    Constant-time comparison using UTF-32 LE encoding.
    - Encodes strings into 32-bit code units.
    - Pads to equal length with zeros, then compares in fixed-size blocks.
    - Aggregates differences into a single diff variable with no early exits.
    - Returns True iff strings are exactly equal (same length and content).
    """
    # Encode to fixed-width 32-bit units
    a = secret.encode('utf-32-le')
    b = input_val.encode('utf-32-le')

    la = len(a)
    lb = len(b)
    max_len = la if la >= lb else lb

    # Include length difference in the diff to prevent leaks based on length
    diff = la ^ lb

    # Pad to equal length with zeros (no branching)
    pad_a = max_len - la
    pad_b = max_len - lb
    a_p = a + (b'\x00' * pad_a)
    b_p = b + (b'\x00' * pad_b)

    BLOCK = 16  # Process in 16-byte chunks (4 code units per chunk)
    for i in range(0, max_len, BLOCK):
        block_a = a_p[i:i + BLOCK]
        block_b = b_p[i:i + BLOCK]
        diff |= int.from_bytes(block_a, 'little') ^ int.from_bytes(block_b, 'little')

    return diff == 0
# EVOLVE-BLOCK-END