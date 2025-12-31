# EVOLVE-BLOCK-START
def secure_compare(secret: str, input_val: str) -> bool:
    """
    Constant-time string comparison without early exits.
    This version uses a single loop to compare UTF-8 encoded bytes
    of both strings, ensuring that all characters are inspected,
    including padding with zeros for shorter strings.
    Returns True iff secret and input_val are exactly the same.
    """
    # Encode strings to UTF-8 bytes
    s_bytes = secret.encode('utf-8')
    t_bytes = input_val.encode('utf-8')

    # Get lengths
    la = len(s_bytes)
    lb = len(t_bytes)
    max_len = max(la, lb)

    # Initialize diff with length difference to prevent timing leaks
    diff = la ^ lb

    # Create a memory view for both byte arrays
    mv_s = memoryview(s_bytes)
    mv_t = memoryview(t_bytes)

    for i in range(max_len):
        # Get byte value or 0 if out of bounds
        byte_s = mv_s[i] if i < la else 0
        byte_t = mv_t[i] if i < lb else 0
        diff |= byte_s ^ byte_t

    return diff == 0
# EVOLVE-BLOCK-END