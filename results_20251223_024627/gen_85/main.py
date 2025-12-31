# EVOLVE-BLOCK-START
def constant_time_compare(secret: str, input_val: str) -> bool:
    """
    Constant-time comparison of two strings.
    This implementation processes both strings character by character without
    early exits to prevent timing attacks. It accommodates different lengths
    by padding with sentinel values and incorporates length differences into
    the comparison.
    """
    len_s = len(secret)
    len_i = len(input_val)
    max_len = max(len_s, len_i)

    diff = 0
    for idx in range(max_len):
        a = secret[idx] if idx < len_s else '\0'
        b = input_val[idx] if idx < len_i else '\0'
        diff |= ord(a) ^ ord(b)

    # Include length difference to avoid timing variations
    diff |= (len_s ^ len_i)

    return diff == 0
# EVOLVE-BLOCK-END