# EVOLVE-BLOCK-START
def secure_compare(secret: str, input_val: str) -> bool:
    """
    Constant-time comparison of two strings by converting to UTF-8 bytes,
    padding to equal length without branching, then performing a single
    XOR across all bytes using big-integer arithmetic.

    Returns True iff secret == input_val.
    """
    a = secret.encode('utf-8')
    b = input_val.encode('utf-8')

    la = len(a)
    lb = len(b)
    max_len = la if la >= lb else lb

    # Pad to equal length without branches
    a_p = a + b'\x00' * (max_len - la)
    b_p = b + b'\x00' * (max_len - lb)

    # Single big-integer XOR over the entire padded byte sequences
    diff = int.from_bytes(a_p, 'little') ^ int.from_bytes(b_p, 'little')

    return diff == 0
# EVOLVE-BLOCK-END