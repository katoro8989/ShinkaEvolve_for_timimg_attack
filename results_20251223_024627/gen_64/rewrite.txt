# EVOLVE-BLOCK-START
def secure_compare(secret: str, input_val: str) -> bool:
    """
    Constant-time comparison between two strings.
    Returns True if secret and input_val are exactly equal, otherwise False.
    The implementation avoids early returns and inspects all characters (padding
    shorter string with zeros) to ensure uniform timing characteristics.
    """
    # Convert strings to byte arrays
    b1 = secret.encode('utf-8')
    b2 = input_val.encode('utf-8')

    len1 = len(b1)
    len2 = len(b2)
    max_len = max(len1, len2)

    # Initialize diff with length difference
    diff = len1 ^ len2

    # Pad both byte arrays to the same length and compare
    for i in range(max_len):
        byte1 = b1[i] if i < len1 else 0
        byte2 = b2[i] if i < len2 else 0
        diff |= byte1 ^ byte2  # Accumulate differences

    return diff == 0  # Return True only if all bytes matched
# EVOLVE-BLOCK-END