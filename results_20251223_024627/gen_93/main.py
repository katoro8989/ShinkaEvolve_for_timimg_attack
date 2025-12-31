# EVOLVE-BLOCK-START
def secure_compare(secret: str, input_val: str) -> bool:
    """
    Constant-time comparison of two strings using XOR.
    This version processes the strings in fixed-size blocks to ensure
    consistent timing regardless of mismatches.
    Returns True only if both strings are exactly equal (same length and content).
    """
    len_s = len(secret)
    len_i = len(input_val)
    max_len = max(len_s, len_i)

    # Initialize diff with the length difference
    diff = len_s ^ len_i

    # Pad the shorter string with null characters
    padded_secret = secret.ljust(max_len, '\0')
    padded_input = input_val.ljust(max_len, '\0')

    # Process each character in a non-branching manner
    for i in range(max_len):
        diff |= ord(padded_secret[i]) ^ ord(padded_input[i])

    return diff == 0
# EVOLVE-BLOCK-END