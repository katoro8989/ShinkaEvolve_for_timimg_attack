# EVOLVE-BLOCK-START
def secure_compare(secret: str, input_val: str) -> bool:
    """
    Constant-time string comparison without early returns.
    Compares up to the maximum length of the two strings, padding with 0
    for the shorter string, and then encodes any length mismatch into the diff.
    Returns True only if both strings are exactly equal (same length and content).
    """
    len_s = len(secret)
    len_i = len(input_val)
    max_len = len_s if len_s > len_i else len_i

    diff = 0
    for i in range(max_len):
        a = ord(secret[i]) if i < len_s else 0
        b = ord(input_val[i]) if i < len_i else 0
        diff |= a ^ b

    # Include length difference in the accumulated diff to prevent
    # leaking information via timing if one string is longer.
    diff |= (len_s ^ len_i)

    return diff == 0
# EVOLVE-BLOCK-END