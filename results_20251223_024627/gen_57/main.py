# EVOLVE-BLOCK-START
def secure_compare(secret: str, input_val: str) -> bool:
    """
    Constant-time string comparison without early exits.
    Compares two strings of potentially different lengths by padding on-the-fly
    and aggregating per-character differences into a single diff value.
    Returns True if secret and input_val are exactly the same, otherwise False.
    """
    # Convert to a uniform byte representation
    s_bytes = secret.encode('utf-8')
    t_bytes = input_val.encode('utf-8')

    la = len(s_bytes)
    lb = len(t_bytes)
    max_len = la if la > lb else lb

    # Initialize diff with length difference
    diff = la ^ lb

    # Pad both buffers to equal length
    padded_length = ((max_len + 7) // 8) * 8
    s_pad = s_bytes + b'\x00' * (padded_length - la)
    t_pad = t_bytes + b'\x00' * (padded_length - lb)

    # Compare in 64-bit blocks
    w_s = memoryview(s_pad).cast('Q')
    w_t = memoryview(t_pad).cast('Q')
    blocks = padded_length // 8

    for i in range(blocks):
        diff |= (w_s[i] ^ w_t[i])

    return diff == 0
# EVOLVE-BLOCK-END