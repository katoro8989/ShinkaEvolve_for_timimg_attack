# EVOLVE-BLOCK-START
def secure_compare(secret: str, input_val: str) -> bool:
    """
    Constant-time comparison between two strings.
    Returns True if secret and input_val are exactly equal, otherwise False.
    The implementation avoids early returns and inspects all characters (padding
    shorter string with zeros) to ensure uniform timing characteristics.
    """
    len_s = len(secret)
    len_i = len(input_val)

    # Start with a difference indicator that also captures length differences
    diff = len_s ^ len_i

    # Compare up to the maximum length of the two strings
    n = max(len_s, len_i)
    for idx in range(n):
        # Fetch character code points if within bounds; otherwise use 0 as padding
        a = ord(secret[idx]) if idx < len_s else 0
        b = ord(input_val[idx]) if idx < len_i else 0
        diff |= a ^ b  # accumulate any difference in a way that does not short-circuit

    return diff == 0
# EVOLVE-BLOCK-END