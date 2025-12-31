# EVOLVE-BLOCK-START
def secure_compare(secret: str, input_val: str) -> bool:
    """
    Constant-time string comparison without early returns.
    Compares both strings up to the maximum length, padding with 0 for the shorter string,
    and includes length mismatch in the diff. Returns True only if both strings are equal.
    """
    len_s = len(secret)
    len_i = len(input_val)
    max_len = max(len_s, len_i)

    # Initialize diff with length information to prevent length-based leaks
    diff = len_s ^ len_i

    # Process in 8-byte blocks
    for i in range(max_len):
        a = ord(secret[i]) if i < len_s else 0
        b = ord(input_val[i]) if i < len_i else 0
        diff |= a ^ b

    return diff == 0
# EVOLVE-BLOCK-END