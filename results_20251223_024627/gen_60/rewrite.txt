# EVOLVE-BLOCK-START
def secure_compare(secret: str, input_val: str) -> bool:
    """
    Constant-time comparison of two strings.
    This version processes characters in a non-branching manner,
    ensuring consistent timing regardless of mismatches.
    """
    len_s = len(secret)
    len_i = len(input_val)
    max_len = max(len_s, len_i)

    # Initialize the accumulator to track differences.
    diff = 0

    # Compute differences in a constant-time manner
    for i in range(max_len):
        # Use '\0' for out-of-range characters
        a = ord(secret[i]) if i < len_s else 0
        b = ord(input_val[i]) if i < len_i else 0
        diff |= a ^ b

    # Include length difference to prevent timing leaks
    diff |= len_s ^ len_i

    return diff == 0
# EVOLVE-BLOCK-END