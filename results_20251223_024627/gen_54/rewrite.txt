# EVOLVE-BLOCK-START
def secure_compare(secret: str, input_val: str) -> bool:
    """
    Constant-time comparison between two strings.
    Returns True if 'secret' and 'input_val' are equal; otherwise False.
    The implementation avoids early returns and ensures uniform timing characteristics.
    """
    len_s = len(secret)
    len_i = len(input_val)

    # Initialize the diff to capture length differences that provide a constant-time check
    diff = len_s ^ len_i
    max_len = max(len_s, len_i)

    for i in range(max_len):
        a = ord(secret[i]) if i < len_s else 0  # Use 0 as padding if out of bounds
        b = ord(input_val[i]) if i < len_i else 0
        diff |= a ^ b  # Accumulate differences

    return diff == 0  # Return True only if diff is 0
# EVOLVE-BLOCK-END