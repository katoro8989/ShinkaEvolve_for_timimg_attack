# EVOLVE-BLOCK-START
def secure_compare(secret: str, input_val: str) -> bool:
    """
    Constant-time comparison of two strings.
    - No early exit: always processes up to max(len(secret), len(input_val)).
    - Out-of-range positions are treated as 0 (sentinel).
    - Length difference is incorporated into the diff accumulator.
    - Returns True only if strings are exactly equal (same length and content).
    """
    len_s = len(secret)
    len_i = len(input_val)
    max_len = len_s if len_s > len_i else len_i

    diff = len_s ^ len_i  # incorporate length difference into the accumulator

    for idx in range(max_len):
        a = ord(secret[idx]) if idx < len_s else 0
        b = ord(input_val[idx]) if idx < len_i else 0
        diff |= (a ^ b)

    return diff == 0
# EVOLVE-BLOCK-END