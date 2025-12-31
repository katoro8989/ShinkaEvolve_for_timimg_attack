# EVOLVE-BLOCK-START
def secure_compare(secret: str, input_val: str) -> bool:
    """
    Constant-time string comparison without early exits.
    Returns True if secret and input_val are exactly the same, otherwise False.
    """
    la, lb = len(secret), len(input_val)
    max_len = la if la > lb else lb

    # Precompute code points for both strings and pad with zeros to equal length
    s_codes = [ord(ch) for ch in secret] + [0] * (max_len - la)
    i_codes = [ord(ch) for ch in input_val] + [0] * (max_len - lb)

    # Initialize diff with length difference to ensure length mismatch is accounted
    diff = la ^ lb

    # Full-length, no-early-exit comparison
    for i in range(max_len):
        diff |= (s_codes[i] ^ i_codes[i])

    return diff == 0
# EVOLVE-BLOCK-END