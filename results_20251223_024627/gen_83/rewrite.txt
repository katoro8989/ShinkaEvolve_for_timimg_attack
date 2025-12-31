# EVOLVE-BLOCK-START
def secure_compare(secret: str, input_val: str) -> bool:
    """
    Constant-time comparison of two strings.
    This version processes characters in a non-branching manner,
    ensuring consistent timing regardless of mismatches.
    It incorporates length differences and uses a single accumulator
    to track differences.
    """
    len_s = len(secret)
    len_i = len(input_val)
    max_len = max(len_s, len_i)

    # Initialize the accumulator to track differences, including length difference
    diff = len_s ^ len_i

    # Compute differences in a constant-time manner
    for i in range(max_len):
        a = ord(secret[i]) if i < len_s else 0
        b = ord(input_val[i]) if i < len_i else 0
        diff |= a ^ b

    return diff == 0
# EVOLVE-BLOCK-END