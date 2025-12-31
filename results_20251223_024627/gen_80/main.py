# EVOLVE-BLOCK-START
def secure_compare(secret: str, input_val: str) -> bool:
    """
    Constant-time comparison of two strings to prevent timing attacks.
    Returns True if secret and input_val are exactly equal, otherwise False.
    This implementation inspects all characters, including padding with zeros
    for shorter strings to ensure uniform timing characteristics.
    """
    len_s = len(secret)
    len_i = len(input_val)
    max_len = max(len_s, len_i)

    # Start with a difference indicator that captures length differences
    diff = len_s ^ len_i

    # Compare characters and accumulate differences using XOR
    for i in range(max_len):
        # Get character code or 0 if out of bounds
        char_s = ord(secret[i]) if i < len_s else 0
        char_i = ord(input_val[i]) if i < len_i else 0
        diff |= char_s ^ char_i

    # Return True if diff is 0, indicating all characters matched
    return diff == 0
# EVOLVE-BLOCK-END