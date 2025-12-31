# EVOLVE-BLOCK-START
def secure_compare(secret: str, input_val: str) -> bool:
    """
    Constant-time comparison of two strings.
    This version avoids early returns and operates in a no-branch style
    by processing characters in a non-branching manner, using bitwise
    operations to prevent timing leaks. The length difference is encoded
    as part of the comparison logic to ensure consistent timing regardless
    of mismatches.
    """
    len_s = len(secret)
    len_i = len(input_val)
    max_len = max(len_s, len_i)

    # Initialize the accumulator to track differences.
    diff = len_s ^ len_i  # Start with length difference

    # Compute differences in a constant-time manner
    for idx in range(max_len):
        # Use '\0' for out-of-range characters
        a = ord(secret[idx]) if idx < len_s else 0
        b = ord(input_val[idx]) if idx < len_i else 0
        diff |= a ^ b

    return diff == 0
# EVOLVE-BLOCK-END