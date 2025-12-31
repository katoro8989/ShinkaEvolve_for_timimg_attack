# EVOLVE-BLOCK-START
def constant_time_compare(secret: str, input_val: str) -> bool:
    """
    Constant-time comparison of two strings.
    This function processes characters in a non-branching manner,
    ensuring consistent timing regardless of mismatches.
    """
    len_s = len(secret)
    len_i = len(input_val)
    max_len = max(len_s, len_i)

    # Initialize the difference accumulator with the length difference
    diff = len_s ^ len_i

    # Compare characters in a constant-time manner
    for i in range(max_len):
        a = ord(secret[i]) if i < len_s else 0
        b = ord(input_val[i]) if i < len_i else 0
        diff |= (a ^ b)

    # Return True if no differences were found
    return diff == 0
# EVOLVE-BLOCK-END