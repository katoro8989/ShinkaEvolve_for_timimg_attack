# EVOLVE-BLOCK-START
def secure_compare(secret: str, input_val: str) -> bool:
    """
    Constant-time comparison of two strings.
    This version avoids early returns and operates in a no-branch style
    by processing characters in a non-branching manner, ensuring consistent
    timing regardless of mismatches.
    """
    len_s = len(secret)
    len_i = len(input_val)
    max_len = max(len_s, len_i)

    result = len_s ^ len_i  # Start with length difference

    for i in range(max_len):
        a = ord(secret[i]) if i < len_s else 0
        b = ord(input_val[i]) if i < len_i else 0
        result |= (a ^ b)

    return result == 0

    return True
# EVOLVE-BLOCK-END