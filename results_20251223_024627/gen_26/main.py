# EVOLVE-BLOCK-START
def secure_compare(secret: str, input_val: str) -> bool:
    """
    Constant-time comparison between two strings.
    No early return; compares all characters up to the longer length,
    padding shorter input with zeros to avoid data-dependent timing.
    """
    len_s = len(secret)
    len_i = len(input_val)
    max_len = len_s if len_s > len_i else len_i

    # Start with a diff that also encodes length differences
    diff = len_s ^ len_i

    s = secret
    t = input_val

    # Process in 4-character chunks to reduce Python loop overhead
    idx = 0
    while idx + 3 < max_len:
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
    while idx < max_len:
        a = ord(s[idx]) if idx < len_s else 0
        b = ord(t[idx]) if idx < len_i else 0
        diff |= a ^ b
        idx += 1

    return diff == 0
# EVOLVE-BLOCK-END