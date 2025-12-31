# EVOLVE-BLOCK-START
def secure_compare(secret: str, input_val: str) -> bool:
    """
    Constant-time comparison of two strings.
    This version avoids early returns and operates in a no-branch style
    by padding the shorter string with zeros and comparing code points
    in fixed-length blocks.
    """
    # Convert to lists of code points (integers) for both strings
    len_s = len(secret)
    len_i = len(input_val)
    max_len = len_s if len_s > len_i else len_i

    s_codes = [ord(ch) for ch in secret]
    i_codes = [ord(ch) for ch in input_val]

    # Pad to the same length to avoid branching in the loop
    s_codes.extend([0] * (max_len - len_s))
    i_codes.extend([0] * (max_len - len_i))

    diff = 0
    for a, b in zip(s_codes, i_codes):
        diff |= a ^ b
    return diff == 0
# EVOLVE-BLOCK-END