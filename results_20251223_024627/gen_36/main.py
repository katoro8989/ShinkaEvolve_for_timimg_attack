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

    # Unrolled, no-branch loop to reduce Python overhead while preserving timing.
    # Process 8 characters per iteration when possible.
    idx = 0
    s = secret
    t = input_val

    while idx + 3 < n:
        a0 = ord(s[idx]) if idx < len_s else 0
        b0 = ord(t[idx]) if idx < len_i else 0

        a1 = ord(s[idx + 1]) if (idx + 1) < len_s else 0
        b1 = ord(t[idx + 1]) if (idx + 1) < len_i else 0

        a2 = ord(s[idx + 2]) if (idx + 2) < len_s else 0
        b2 = ord(t[idx + 2]) if (idx + 2) < len_i else 0

        a3 = ord(s[idx + 3]) if (idx + 3) < len_s else 0
        b3 = ord(t[idx + 3]) if (idx + 3) < len_i else 0

        diff |= a0 ^ b0
        diff |= a1 ^ b1
        diff |= a2 ^ b2
        diff |= a3 ^ b3

        idx += 4

    # Tail processing for remaining characters
    while idx < n:
        a = ord(s[idx]) if idx < len_s else 0
        b = ord(t[idx]) if idx < len_i else 0
        diff |= a ^ b
        idx += 1

    return diff == 0
# EVOLVE-BLOCK-END